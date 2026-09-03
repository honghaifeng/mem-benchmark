"""
CLongEval（港中文）中文长对话记忆评测框架
适配 CLongEval LCvMem 子任务数据格式

数据结构：
- JSONL 格式，每行一个测试条目
- context: 完整对话文本（含日期分隔符 "以下是YYYY年MM月DD日的对话记录："）
- query: 中文问题
- answer: 标准答案
- 同一对话的多个问题通过 context 前缀 hash 分组

流程：加载JSONL → 按对话分组 → 逐天写入记忆 → 回答QA → LLM裁判评分 → 统计结果

用法：
    python clong_eval.py --system baseline --size small --max-questions 5
    python clong_eval.py --system cognitive --size small
    python clong_eval.py --system cognitive --size small --conversations 0,1,2
"""
import argparse
import json
import os
import re
import sys
import time
import hashlib
from datetime import datetime, timezone
from collections import defaultdict

from llm_client import chat_completion_json, chat_completion, reset_token_stats, get_token_stats
from baseline_memory import BaselineMemory
from cognitive_memory import CognitiveMemory
from cognitive_vector_memory import CognitiveVectorMemory
from amem_memory import AMemMemory
from mem0_memory import Mem0Memory
from amem_official_memory import OfficialAMemMemory
from oom_memory import OOMMemory
from oom_memory_paperA import OOMemoryPaperA


# =============================================================================
# CLongEval 数据解析
# =============================================================================
def load_clong_data(data_path: str) -> list[dict]:
    """加载 JSONL 格式的 CLongEval 数据"""
    entries = []
    with open(data_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return entries


def parse_date_cn(date_str: str) -> datetime | None:
    """解析中文日期格式：'2023年04月27日'"""
    for fmt in ("%Y年%m月%d日", "%Y年%m月%d日"):
        try:
            return datetime.strptime(date_str, fmt)
        except (ValueError, TypeError):
            continue
    return None


def cn_date_to_epoch(date_str: str) -> int:
    """中文日期转 epoch"""
    parsed = parse_date_cn(date_str)
    if parsed:
        return int(parsed.replace(tzinfo=timezone.utc).timestamp())
    return int(time.time())


def extract_daily_segments(context: str) -> list[tuple[str, str]]:
    """
    从 CLongEval context 中提取每日对话段
    返回 [(date_str, conversation_text), ...]
    """
    # 移除末尾的 "请记住以上全部对话记录，回答问题。\n问题："
    clean_ctx = context
    if "请记住以上全部对话记录" in clean_ctx:
        clean_ctx = clean_ctx[:clean_ctx.index("请记住以上全部对话记录")]

    # 按日期分隔符分割
    date_pattern = r"以下是(\d{4}年\d{2}月\d{2}日)的对话记录："
    segments = re.split(date_pattern, clean_ctx)

    results = []
    # segments[0] 是日期前的空串，之后交替出现 (date_str, content)
    for i in range(1, len(segments), 2):
        date_str = segments[i]
        content = segments[i + 1] if i + 1 < len(segments) else ""
        if content.strip():
            results.append((date_str, content.strip()))

    return results


def group_by_conversation(entries: list[dict]) -> list[tuple[str, list[dict]]]:
    """
    将多条目按对话分组（同一对话的不同问题归到一起）
    用 context 前 500 字符的 hash 作为对话标识
    """
    groups = defaultdict(list)
    for i, entry in enumerate(entries):
        ctx = entry.get("context", "")
        conv_text = ctx.split("请记住以上全部对话记录")[0] if "请记住以上全部对话记录" in ctx else ctx
        conv_hash = hashlib.md5(conv_text[:500].encode()).hexdigest()[:8]
        entry["_original_idx"] = i
        groups[conv_hash].append(entry)

    # 按原始顺序返回
    result = []
    for h, items in groups.items():
        items.sort(key=lambda x: x["_original_idx"])
        result.append((h, items))
    return result


def clean_dialog_text(text: str) -> str:
    """清理对话文本，去除引号包裹等"""
    text = text.strip()
    # 去除外层引号
    if text.startswith("\u201c") and text.endswith("\u201d"):
        text = text[1:-1]
    elif text.startswith('"') and text.endswith('"'):
        text = text[1:-1]
    return text.strip()


# =============================================================================
# 中文答案生成 Prompt
# =============================================================================
ANSWER_PROMPT_CN = """你是一个精确的问答助手。根据以下记忆内容回答问题。

## 记忆内容
{memories}

## 问题
{question}

## 参考日期
最后一次对话发生在 {reference_date}。请据此进行时间推理。

## 要求
1. 仔细阅读所有记忆，逐条检查，找到最相关的信息
2. 如果问题提到某个日期（如"4月27日"），优先查找与该日期相关的记忆
3. 如果需要多步推理，请连接不同记忆中的事实
4. 如果需要时间计算，基于参考日期进行推理
5. 记忆中可能包含答案，也可能需要从多条记忆中推断
6. 直接给出答案，不要说"无法确定"——尝试从记忆中推断最可能的答案
7. 用中文回答

答案：
"""


# =============================================================================
# 中文 LLM 裁判 Prompt
# =============================================================================
JUDGE_SYSTEM_CN = "你是一个严格的答案评判员。判断生成的答案是否正确。只返回有效的 JSON。"

JUDGE_PROMPT_CN = """判断以下问题的答案是否正确。

问题: {question}
标准答案: {gold_answer}
生成答案: {generated_answer}

评判规则:
1. **部分正确也算对**: 生成的答案包含标准答案中的至少一个正确内容，即算正确
2. **同义词算对**: 同一概念的不同表达方式算正确（如"巧克力蛋糕"="巧克力味的蛋糕"）
3. **额外细节不扣分**: 比标准答案更详细不算错，只要核心事实正确
4. **日期容错**: 日期相差14天以内算正确。时间跨度相差50%以内算正确
5. **语义优先**: 判断语义一致性，而非字面匹配

只有当生成的答案完全没有正确内容或完全偏题时才判错。

只返回 JSON:
{{
  "label": "CORRECT" 或 "WRONG",
  "reasoning": "简要说明判断理由"
}}
"""


# =============================================================================
# 核心评测流程
# =============================================================================
def run_clong_evaluation(
    data_path: str,
    system_name: str,
    size: str,
    conv_indices: list[int] | None = None,
    max_questions: int | None = None,
    top_k: int = 30,
    output_dir: str = "results",
):
    """运行 CLongEval 评测"""
    # 加载数据
    entries = load_clong_data(data_path)
    conversations = group_by_conversation(entries)

    print(f"\n{'='*60}")
    print(f"CLongEval 评测 - 系统: {system_name}")
    print(f"数据集: {size} ({len(entries)} 题, {len(conversations)} 个对话)")
    print(f"Top-K: {top_k}")
    print(f"{'='*60}\n")

    # 选择对话
    if conv_indices is not None:
        conversations = [(h, items) for i, (h, items) in enumerate(conversations) if i in conv_indices]
        print(f"已选择 {len(conversations)} 个对话\n")

    # 初始化记忆系统
    os.makedirs(output_dir, exist_ok=True)
    if system_name == "baseline":
        mem = BaselineMemory(db_path=os.path.join(output_dir, f"clong_{system_name}_{int(time.time())}.db"))
    elif system_name == "cognitive":
        mem = CognitiveMemory(db_path=os.path.join(output_dir, f"clong_{system_name}_{int(time.time())}.db"))
    elif system_name == "cognitive_vector":
        mem = CognitiveVectorMemory(db_path=os.path.join(output_dir, f"clong_{system_name}_{int(time.time())}.db"))
    elif system_name == "amem":
        mem = AMemMemory(db_path=os.path.join(output_dir, f"clong_{system_name}_{int(time.time())}.db"))
    elif system_name == "mem0":
        mem = Mem0Memory(db_path=os.path.join(output_dir, f"clong_{system_name}_{int(time.time())}.db"))
    elif system_name == "amem_official":
        mem = OfficialAMemMemory(db_path=os.path.join(output_dir, f"clong_{system_name}_{int(time.time())}.db"))
    elif system_name == "oom":
        mem = OOMMemory(db_path=os.path.join(output_dir, f"clong_oom_{int(time.time())}.db"))
    elif system_name == "oom_paperA":
        mem = OOMemoryPaperA(db_path=os.path.join(output_dir, f"clong_oom_paperA_{int(time.time())}.db"))
    elif system_name == "oom_paperA_no_inherit":
        mem = OOMemoryPaperA(db_path=os.path.join(output_dir, f"clong_oom_paperA_noinh_{int(time.time())}.db"),
                            use_inheritance=False)
    elif system_name == "oom_paperA_no_poly":
        mem = OOMemoryPaperA(db_path=os.path.join(output_dir, f"clong_oom_paperA_nopoly_{int(time.time())}.db"),
                            use_polymorphism=False)
    elif system_name == "oom_paperA_no_encap":
        mem = OOMemoryPaperA(db_path=os.path.join(output_dir, f"clong_oom_paperA_noenc_{int(time.time())}.db"),
                            use_encapsulation=False, use_inheritance=False, use_polymorphism=False)
    else:
        raise ValueError(f"Unknown system: {system_name}")

    all_results = []
    total_questions = 0
    total_correct = 0

    # 成本统计
    cost_stats = {
        "write_time_seconds": 0,
        "answer_time_seconds": 0,
        "total_time_seconds": 0,
        "write_tokens": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0, "call_count": 0},
        "answer_tokens": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0, "call_count": 0},
        "db_size_bytes": 0,
        "memory_entries": 0,
        "avg_answer_time_ms": 0,
    }
    answer_times = []
    eval_start_time = time.time()

    for conv_idx, (conv_hash, conv_entries) in enumerate(conversations):
        # 从第一条获取 context
        context = conv_entries[0]["context"]
        daily_segments = extract_daily_segments(context)

        # 参考日期（最后一天）
        ref_date = daily_segments[-1][0] if daily_segments else "2023年05月"

        # 提取用户名（如果有）
        user_name = "用户"
        m = re.search(r"用户: 你好，我叫(\S+?)[，,。]", context)
        if m:
            user_name = m.group(1)
        # 也尝试其他模式
        if user_name == "用户":
            m = re.search(r"我叫(\S+?)[，,。]", context[:200])
            if m:
                user_name = m.group(1)

        user_id = f"clong_{system_name}_{conv_hash}"

        # 准备 QA 列表
        qa_list = conv_entries
        if max_questions:
            qa_list = qa_list[:max_questions]

        print(f"\n[对话 {conv_idx}] {user_name} ({len(daily_segments)}天, {len(qa_list)}题)")

        # --- 写入记忆 ---
        print("  写入记忆中...")
        reset_token_stats()
        write_start = time.time()

        for seg_idx, (date_str, seg_text) in enumerate(daily_segments):
            seg_epoch = cn_date_to_epoch(date_str)
            date_header = f"[对话日期: {date_str}]\n"
            clean_text = clean_dialog_text(seg_text)

            # 分批写入（每 10 轮一批）
            lines = clean_text.split("\n")
            batch_size = 10
            for i in range(0, len(lines), batch_size):
                batch = "\n".join(lines[i:i+batch_size])
                if batch.strip():
                    try:
                        full_text = date_header + batch
                        mem.add(full_text, user_id=user_id, timestamp=seg_epoch)
                    except Exception as e:
                        print(f"    [警告] 写入失败 {date_str} batch {i}: {e}")

            if (seg_idx + 1) % 5 == 0:
                print(f"    已处理 {seg_idx + 1}/{len(daily_segments)} 天")

        write_elapsed = time.time() - write_start
        write_tokens = get_token_stats()
        cost_stats["write_time_seconds"] += write_elapsed
        for k in write_tokens:
            cost_stats["write_tokens"][k] += write_tokens[k]
        print(f"  写入完成: {write_elapsed:.1f}s, tokens: {write_tokens['total_tokens']}, LLM调用: {write_tokens['call_count']}次")

        # --- 回答问题 ---
        print("  回答问题中...")
        conv_correct = 0
        conv_total = 0
        reset_token_stats()
        answer_start = time.time()

        for entry in qa_list:
            question = entry["query"]
            gold_answer = str(entry["answer"])

            q_start = time.time()

            # 检索
            search_results = mem.search(question, user_id=user_id, top_k=top_k)
            memories_text = "\n".join([
                f"{i+1}. {r['memory']}" for i, r in enumerate(search_results)
            ])

            # 生成答案（中文）
            try:
                generated = chat_completion(
                    system="你是一个精确的问答助手。直接、简洁地用中文回答。",
                    user=ANSWER_PROMPT_CN.format(
                        memories=memories_text,
                        question=question,
                        reference_date=ref_date,
                    ),
                    temperature=0.1,
                )
            except Exception as e:
                generated = f"[ERROR] {e}"

            # LLM 裁判（中文）
            try:
                judge_result = chat_completion_json(
                    system=JUDGE_SYSTEM_CN,
                    user=JUDGE_PROMPT_CN.format(
                        question=question,
                        gold_answer=gold_answer,
                        generated_answer=generated,
                    ),
                    temperature=0.1,
                )
                label = judge_result.get("label", "WRONG").upper()
                reasoning = judge_result.get("reasoning", "")
            except Exception as e:
                label = "WRONG"
                reasoning = f"Judge error: {e}"

            is_correct = (label == "CORRECT")

            q_elapsed = time.time() - q_start
            answer_times.append(q_elapsed)

            conv_total += 1
            total_questions += 1
            if is_correct:
                conv_correct += 1
                total_correct += 1

            all_results.append({
                "conversation_idx": conv_idx,
                "conversation_hash": conv_hash,
                "user_name": user_name,
                "question": question,
                "gold_answer": gold_answer,
                "generated_answer": generated.strip(),
                "judgment": label,
                "judge_reason": reasoning,
                "top_memories": [r["memory"] for r in search_results[:5]],
            })

        acc = conv_correct / conv_total * 100 if conv_total > 0 else 0

        answer_elapsed = time.time() - answer_start
        answer_tokens = get_token_stats()
        cost_stats["answer_time_seconds"] += answer_elapsed
        for k in answer_tokens:
            cost_stats["answer_tokens"][k] += answer_tokens[k]

        print(f"  结果: {conv_correct}/{conv_total} ({acc:.1f}%)")
        print(f"  答题耗时: {answer_elapsed:.1f}s, tokens: {answer_tokens['total_tokens']}")

    # --- 汇总 ---
    overall_acc = total_correct / total_questions * 100 if total_questions > 0 else 0

    print(f"\n{'='*60}")
    print(f"CLongEval 评测完成 - {system_name}")
    print(f"{'='*60}")
    print(f"数据集: {size}")
    print(f"总题数: {total_questions}")
    print(f"正确数: {total_correct}")
    print(f"准确率: {overall_acc:.1f}%")

    # --- 成本统计 ---
    total_elapsed = time.time() - eval_start_time
    cost_stats["total_time_seconds"] = total_elapsed

    db_path = getattr(mem, "db_path", "")
    if db_path and os.path.exists(db_path):
        cost_stats["db_size_bytes"] = os.path.getsize(db_path)

    try:
        cost_stats["memory_entries"] = mem.count_memories() if hasattr(mem, "count_memories") else 0
    except:
        cost_stats["memory_entries"] = 0

    if answer_times:
        cost_stats["avg_answer_time_ms"] = sum(answer_times) / len(answer_times) * 1000

    print(f"\n{'='*60}")
    print(f"成本统计 - {system_name}")
    print(f"{'='*60}")
    print(f"总耗时: {total_elapsed/60:.1f} 分钟")
    print(f"  写入记忆: {cost_stats['write_time_seconds']/60:.1f} 分钟")
    print(f"  答题: {cost_stats['answer_time_seconds']/60:.1f} 分钟")
    print(f"\nToken 消耗:")
    wt = cost_stats["write_tokens"]
    at = cost_stats["answer_tokens"]
    print(f"  写入阶段: {wt['total_tokens']:,} tokens ({wt['call_count']} 次调用)")
    print(f"  答题阶段: {at['total_tokens']:,} tokens ({at['call_count']} 次调用)")
    print(f"  总计: {wt['total_tokens']+at['total_tokens']:,} tokens")
    print(f"\n存储占用:")
    print(f"  数据库大小: {cost_stats['db_size_bytes']/1024:.1f} KB")
    print(f"  记忆条目: {cost_stats['memory_entries']}")
    print(f"\n答题性能:")
    print(f"  平均每题耗时: {cost_stats['avg_answer_time_ms']:.0f} ms")

    # 保存结果
    result_data = {
        "system": system_name,
        "dataset": f"CLongEval_{size}",
        "total_questions": total_questions,
        "correct": total_correct,
        "accuracy": overall_acc,
        "num_conversations": len(conversations),
        "details": all_results,
        "top_k": top_k,
        "cost_stats": cost_stats,
    }

    result_path = os.path.join(output_dir, f"clong_{system_name}_results.json")
    with open(result_path, "w") as f:
        json.dump(result_data, f, indent=2, ensure_ascii=False)

    print(f"\n结果已保存到: {result_path}")

    mem.close()
    return result_data


# =============================================================================
# 命令行入口
# =============================================================================
def main():
    parser = argparse.ArgumentParser(description="CLongEval 中文长对话记忆系统评测")
    parser.add_argument("--data-dir", type=str, default="clong_data",
                        help="CLongEval 数据目录")
    parser.add_argument("--size", type=str, default="small",
                        choices=["small", "medium", "large"],
                        help="数据集大小: small(1K-16K), medium(16K-50K), large(50K-100K)")
    parser.add_argument("--system", type=str, required=True,
                        choices=["baseline", "cognitive", "cognitive_vector", "amem", "mem0", "amem_official", "oom",
                                 "oom_paperA", "oom_paperA_no_inherit", "oom_paperA_no_poly", "oom_paperA_no_encap"],
                        help="记忆系统类型")
    parser.add_argument("--conversations", type=str, default=None,
                        help="对话索引，如 '0' 或 '0,1,2' 或 'all'（默认全部）")
    parser.add_argument("--max-questions", type=int, default=None,
                        help="每个对话最多测试多少题")
    parser.add_argument("--top-k", type=int, default=30,
                        help="检索返回的记忆数量")
    parser.add_argument("--output-dir", type=str, default="results",
                        help="结果输出目录")

    args = parser.parse_args()

    data_path = os.path.join(args.data_dir, f"{args.size}.jsonl")
    if not os.path.exists(data_path):
        print(f"错误: 数据文件不存在: {data_path}")
        sys.exit(1)

    # 解析对话索引
    conv_indices = None
    if args.conversations and args.conversations != "all":
        conv_indices = [int(x.strip()) for x in args.conversations.split(",")]

    run_clong_evaluation(
        data_path=data_path,
        system_name=args.system,
        size=args.size,
        conv_indices=conv_indices,
        max_questions=args.max_questions,
        top_k=args.top_k,
        output_dir=args.output_dir,
    )


if __name__ == "__main__":
    main()
