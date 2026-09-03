"""
Mem0 官方版 CLongEval 中文测评脚本
使用 mem0ai 官方 SDK + DeepSeek LLM
用我们的 LLM 裁判评分（与 baseline/cognitive 一致，保证公平）
"""
import json
import os
import re
import sys
import time
import argparse
import hashlib
from datetime import datetime, timezone
from collections import defaultdict

from mem0 import Memory

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from llm_client import chat_completion_json, chat_completion


# =============================================================================
# CLongEval 数据解析（与 clong_eval.py 完全一致）
# =============================================================================
def load_clong_data(data_path: str) -> list[dict]:
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
    for fmt in ("%Y年%m月%d日", "%Y年%m月%d日"):
        try:
            return datetime.strptime(date_str, fmt)
        except (ValueError, TypeError):
            continue
    return None


def cn_date_to_epoch(date_str: str) -> int:
    parsed = parse_date_cn(date_str)
    if parsed:
        return int(parsed.replace(tzinfo=timezone.utc).timestamp())
    return int(time.time())


def extract_daily_segments(context: str) -> list[tuple[str, str]]:
    clean_ctx = context
    if "请记住以上全部对话记录" in clean_ctx:
        clean_ctx = clean_ctx[:clean_ctx.index("请记住以上全部对话记录")]

    date_pattern = r"以下是(\d{4}年\d{2}月\d{2}日)的对话记录："
    segments = re.split(date_pattern, clean_ctx)

    results = []
    for i in range(1, len(segments), 2):
        date_str = segments[i]
        content = segments[i + 1] if i + 1 < len(segments) else ""
        if content.strip():
            results.append((date_str, content.strip()))
    return results


def group_by_conversation(entries: list[dict]) -> list[tuple[str, list[dict]]]:
    groups = defaultdict(list)
    for i, entry in enumerate(entries):
        ctx = entry.get("context", "")
        conv_text = ctx.split("请记住以上全部对话记录")[0] if "请记住以上全部对话记录" in ctx else ctx
        conv_hash = hashlib.md5(conv_text[:500].encode()).hexdigest()[:8]
        entry["_original_idx"] = i
        groups[conv_hash].append(entry)

    result = []
    for h, items in groups.items():
        items.sort(key=lambda x: x["_original_idx"])
        result.append((h, items))
    return result


def clean_dialog_text(text: str) -> str:
    text = text.strip()
    if text.startswith("\u201c") and text.endswith("\u201d"):
        text = text[1:-1]
    elif text.startswith('"') and text.endswith('"'):
        text = text[1:-1]
    return text.strip()


# =============================================================================
# 中文答案生成 Prompt（与 clong_eval.py 一致）
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
# 中文 LLM 裁判 Prompt（与 clong_eval.py 一致）
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


def judge_answer_cn(question: str, gold_answer: str, generated_answer: str) -> tuple[str, str]:
    result = chat_completion_json(
        system=JUDGE_SYSTEM_CN,
        user=JUDGE_PROMPT_CN.format(
            question=question,
            gold_answer=gold_answer,
            generated_answer=generated_answer
        ),
        temperature=0.1,
    )
    label = result.get("label", "WRONG").upper()
    reasoning = result.get("reasoning", "")
    if label not in ("CORRECT", "WRONG"):
        label = "WRONG"
    return label, reasoning


# =============================================================================
# 主测评函数
# =============================================================================
def evaluate_mem0_clong(data_path: str, output_dir: str,
                        conv_idx: int, max_questions: int | None,
                        top_k: int = 30):
    """跑单个 CLongEval 对话的 Mem0 官方版测评"""
    os.makedirs(output_dir, exist_ok=True)

    # 初始化 Mem0（官方 SDK）
    config = {
        "llm": {
            "provider": "deepseek",
            "config": {
                "model": "deepseek-chat",
                "temperature": 0.1,
            }
        },
        "embedder": {
            "provider": "fastembed",
            "config": {
                "model": "BAAI/bge-small-zh-v1.5",
            }
        },
        "vector_store": {
            "provider": "qdrant",
            "config": {
                "collection_name": f"mem0_clong_conv{conv_idx}",
                "path": os.path.join(output_dir, "qdrant_data"),
                "embedding_model_dims": 512,
            }
        },
        "history_db_path": os.path.join(output_dir, f"mem0_history_conv{conv_idx}.db"),
        "version": "v1.1",
    }

    print(f"[Conv {conv_idx}] Initializing Mem0...")
    m = Memory.from_config(config)
    print(f"[Conv {conv_idx}] Mem0 initialized.")

    # 加载数据
    entries = load_clong_data(data_path)
    conversations = group_by_conversation(entries)

    if conv_idx >= len(conversations):
        print(f"[Conv {conv_idx}] 跳过（数据集只有 {len(conversations)} 个对话）")
        return None

    conv_hash, conv_entries = conversations[conv_idx]
    context = conv_entries[0]["context"]
    daily_segments = extract_daily_segments(context)
    ref_date = daily_segments[-1][0] if daily_segments else "2023年05月"

    # 提取用户名
    user_name = "用户"
    m_user = re.search(r"用户: 你好，我叫(\S+?)[，,。]", context)
    if m_user:
        user_name = m_user.group(1)
    if user_name == "用户":
        m_user = re.search(r"我叫(\S+?)[，,。]", context[:200])
        if m_user:
            user_name = m_user.group(1)

    user_id = f"clong_mem0_{conv_hash}"
    qa_list = conv_entries[:max_questions] if max_questions else conv_entries

    print(f"[Conv {conv_idx}] {user_name} ({len(daily_segments)}天, {len(qa_list)}题)")

    # --- 写入记忆 ---
    print(f"[Conv {conv_idx}] 写入记忆中...")
    mem_count = 0
    write_start = time.time()

    for seg_idx, (date_str, seg_text) in enumerate(daily_segments):
        seg_epoch = cn_date_to_epoch(date_str)
        date_header = f"[对话日期: {date_str}]\n"
        clean_text = clean_dialog_text(seg_text)

        lines = clean_text.split("\n")
        batch_size = 10
        for i in range(0, len(lines), batch_size):
            batch = "\n".join(lines[i:i+batch_size])
            if batch.strip():
                try:
                    full_text = date_header + batch
                    result = m.add(full_text, user_id=user_id)
                    added = result.get('results', []) if isinstance(result, dict) else []
                    mem_count += len(added)
                except Exception as e:
                    print(f"[Conv {conv_idx}] 写入失败 {date_str} batch {i}: {e}")

        if (seg_idx + 1) % 5 == 0:
            print(f"[Conv {conv_idx}]   已处理 {seg_idx + 1}/{len(daily_segments)} 天")

    write_elapsed = time.time() - write_start
    print(f"[Conv {conv_idx}] 写入完成: {mem_count}条记忆, {write_elapsed:.1f}s")

    # --- 回答问题 ---
    print(f"[Conv {conv_idx}] 回答问题中...")
    conv_correct = 0
    conv_total = 0
    all_results = []
    answer_start = time.time()

    for entry in qa_list:
        question = entry["query"]
        gold_answer = str(entry["answer"])

        # Mem0 检索
        try:
            search_result = m.search(question, filters={"user_id": user_id}, limit=top_k)
            results_list = search_result.get('results', []) if isinstance(search_result, dict) else []
            top_memories = [r.get("memory", "") for r in results_list[:top_k]]
        except Exception as e:
            print(f"[Conv {conv_idx}] 检索失败: {e}")
            top_memories = []

        memory_text = "\n".join([f"{i+1}. {mem}" for i, mem in enumerate(top_memories)])

        # 生成答案
        try:
            generated = chat_completion(
                system="你是一个精确的问答助手。直接、简洁地用中文回答。",
                user=ANSWER_PROMPT_CN.format(
                    memories=memory_text[:8000],
                    question=question,
                    reference_date=ref_date,
                ),
                temperature=0.1,
            )
            generated = generated.strip()
        except Exception as e:
            generated = f"[ERROR] {e}"

        # 裁判评分
        try:
            label, reasoning = judge_answer_cn(question, gold_answer, generated)
        except Exception as e:
            label = "WRONG"
            reasoning = f"Judge error: {e}"

        is_correct = (label == "CORRECT")
        conv_total += 1
        if is_correct:
            conv_correct += 1

        all_results.append({
            "conversation_idx": conv_idx,
            "conversation_hash": conv_hash,
            "user_name": user_name,
            "question": question,
            "gold_answer": gold_answer,
            "generated_answer": generated,
            "judgment": label,
            "judge_reason": reasoning,
            "top_memories": top_memories[:5],
        })

    answer_elapsed = time.time() - answer_start
    acc = conv_correct / conv_total * 100 if conv_total > 0 else 0
    print(f"[Conv {conv_idx}] 结果: {conv_correct}/{conv_total} = {acc:.1f}% ({answer_elapsed:.1f}s)")

    # 保存结果
    result_data = {
        "system": "mem0_official",
        "dataset": "CLongEval_small",
        "total_questions": conv_total,
        "correct": conv_correct,
        "accuracy": acc,
        "conversation_idx": conv_idx,
        "conversation_hash": conv_hash,
        "details": all_results,
        "top_k": top_k,
        "memory_count": mem_count,
        "write_time_seconds": write_elapsed,
        "answer_time_seconds": answer_elapsed,
    }

    result_path = os.path.join(output_dir, "mem0_results.json")
    with open(result_path, 'w') as f:
        json.dump(result_data, f, indent=2, ensure_ascii=False)

    print(f"[Conv {conv_idx}] 结果已保存到: {result_path}")
    return result_data


def main():
    parser = argparse.ArgumentParser(description="Mem0 官方版 CLongEval 中文测评")
    parser.add_argument("--data-path", type=str, required=True,
                        help="CLongEval JSONL 数据路径")
    parser.add_argument("--conv-idx", type=int, required=True,
                        help="对话索引")
    parser.add_argument("--max-questions", type=int, default=None,
                        help="每个对话最多测试多少题")
    parser.add_argument("--top-k", type=int, default=30,
                        help="检索返回的记忆数量")
    parser.add_argument("--output-dir", type=str, default="results/mem0_official_clong",
                        help="结果输出目录")
    args = parser.parse_args()

    # 读取 API key
    env_path = os.path.expanduser("~/.hermes/.env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.startswith("DEEPSEEK_API_KEY="):
                    os.environ["DEEPSEEK_API_KEY"] = line.strip().split("=", 1)[1]
                    break

    evaluate_mem0_clong(
        data_path=args.data_path,
        output_dir=args.output_dir,
        conv_idx=args.conv_idx,
        max_questions=args.max_questions,
        top_k=args.top_k,
    )


if __name__ == "__main__":
    main()
