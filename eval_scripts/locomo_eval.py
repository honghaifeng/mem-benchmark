"""
LoCoMo 测评框架
流程：载入数据集 → 逐 session 写入记忆 → 回答 QA 问题 → LLM 裁判评分 → 统计结果

用法：
    python locomo_eval.py --system baseline --conversations 0 --max-questions 5
    python locomo_eval.py --system cognitive --conversations 0,1
    python locomo_eval.py --system cognitive --conversations all
"""
import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from collections import defaultdict

from llm_client import chat_completion_json, chat_completion, reset_token_stats, get_token_stats
from baseline_memory import BaselineMemory
from cognitive_memory import CognitiveMemory
from cognitive_vector_memory import CognitiveVectorMemory
from amem_memory import AMemMemory
from mem0_memory import Mem0Memory
from amem_official_memory import OfficialAMemMemory
from oom_memory import OOMMemory


# =============================================================================
# 数据集加载与解析
# =============================================================================
def parse_locomo_date(date_str: str) -> datetime | None:
    """解析 LoCoMo 日期格式：'1:56 pm on 8 May, 2023'"""
    for fmt in ("%I:%M %p on %d %B, %Y", "%I:%M %p on %d %b, %Y"):
        try:
            return datetime.strptime(date_str, fmt)
        except (ValueError, TypeError):
            continue
    return None


def locomo_date_to_epoch(date_str: str) -> int | None:
    parsed = parse_locomo_date(date_str)
    if parsed:
        return int(parsed.replace(tzinfo=timezone.utc).timestamp())
    return None


def get_sorted_sessions(conversation: dict) -> list[tuple[str, str, list[dict]]]:
    """提取并按时序排序 session"""
    session_keys = [k for k in conversation if re.match(r'^session_\d+$', k)]
    paired = []
    for key in session_keys:
        date_key = f"{key}_date_time"
        date_str = conversation.get(date_key, "")
        turns = conversation[key]
        paired.append((key, date_str, turns))
    
    def sort_key(item):
        parsed = parse_locomo_date(item[1])
        if parsed:
            return (0, parsed)
        num = int(re.search(r'\d+', item[0]).group())
        return (1, datetime(2000, 1, num))
    
    paired.sort(key=sort_key)
    return paired


def turns_to_text(turns: list[dict], speaker_a: str, speaker_b: str) -> str:
    """将一轮对话转成文本"""
    lines = []
    for turn in turns:
        speaker = turn.get("speaker", "")
        text = turn.get("text", "")
        blip = turn.get("blip_caption", "")
        if blip:
            text = f"{text} [image: {blip}]" if text else f"[image: {blip}]"
        if text:
            lines.append(f"{speaker}: {text}")
    return "\n".join(lines)


# =============================================================================
# 答案生成 Prompt（英文，与数据集语言一致）
# =============================================================================
ANSWER_PROMPT = """You are a precise question-answering assistant. Answer the question based on the memory content below.

## Memory Content
{memories}

## Question
{question}

## Reference Date
The latest conversation happened on {reference_date}. Use this for time reasoning.

## Instructions
1. Read all memories carefully and find the most relevant information
2. If multi-hop reasoning is needed, connect facts from different memories
3. If time calculation is needed, reason based on the reference date
4. Give the answer directly, no extra explanation
5. If no exact answer, give the most likely answer based on available info
6. Answer in the same language as the question

Answer:
"""


# =============================================================================
# LLM 裁判 Prompt（基于 LoCoMo 的 J-score 方法）
# =============================================================================
JUDGE_SYSTEM = "You are a strict answer judge. Judge whether the generated answer is correct. Return ONLY valid JSON."

JUDGE_PROMPT = """Judge whether the answer to the following question is correct.

Question: {question}
Gold Answer: {gold_answer}
Generated Answer: {generated_answer}

Judging Rules:
1. **Partial correctness counts**: If the generated answer contains at least one correct option from the gold answer, it's correct.
2. **Synonyms count**: Same concept expressed differently is correct (e.g., "chocolate cake" = "chocolate-flavored cake").
3. **Extra details don't penalize**: More detail than gold answer is fine as long as core fact is correct.
4. **Date tolerance**: Dates within 14 days difference are correct. Durations within 50% difference are correct.
5. **Semantic priority**: Judge semantic consistency, not literal matching.

Only judge WRONG when the generated answer has completely no correct content or is entirely off-topic.

Return ONLY valid JSON:
{{
  "label": "CORRECT" or "WRONG",
  "reasoning": "brief reason for the judgment"
}}
"""


# =============================================================================
# 核心评测流程
# =============================================================================
def run_evaluation(
    dataset_path: str,
    system_name: str,
    conv_indices: list[int],
    max_questions: int | None = None,
    top_k: int = 20,
    output_dir: str = "results",
    categories: list[int] = None,
):
    """运行 LoCoMo 评测"""
    # 加载数据集
    with open(dataset_path) as f:
        dataset = json.load(f)
    
    # 初始化记忆系统
    os.makedirs(output_dir, exist_ok=True)
    if system_name == "baseline":
        mem = BaselineMemory(db_path=os.path.join(output_dir, f"baseline_{int(time.time())}.db"))
    elif system_name == "cognitive":
        mem = CognitiveMemory(db_path=os.path.join(output_dir, f"cognitive_{int(time.time())}.db"))
    elif system_name == "cognitive_vector":
        mem = CognitiveVectorMemory(db_path=os.path.join(output_dir, f"cognitive_vector_{int(time.time())}.db"))
    elif system_name == "amem":
        mem = AMemMemory(db_path=os.path.join(output_dir, f"amem_{int(time.time())}.db"))
    elif system_name == "mem0":
        mem = Mem0Memory(db_path=os.path.join(output_dir, f"mem0_{int(time.time())}.db"))
    elif system_name == "amem_official":
        mem = OfficialAMemMemory(db_path=os.path.join(output_dir, f"amem_off_{int(time.time())}.db"))
    elif system_name == "oom":
        mem = OOMMemory(db_path=os.path.join(output_dir, f"oom_{int(time.time())}.db"))
    else:
        raise ValueError(f"Unknown system: {system_name}")
    
    all_results = []
    total_questions = 0
    total_correct = 0
    category_stats = defaultdict(lambda: {"total": 0, "correct": 0})
    
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
    answer_times = []  # 每题答题耗时
    
    eval_start_time = time.time()
    
    print(f"\n{'='*60}")
    print(f"LoCoMo 评测 - 系统: {system_name}")
    print(f"对话: {conv_indices}, Top-K: {top_k}")
    print(f"{'='*60}\n")
    
    for conv_idx in conv_indices:
        if conv_idx >= len(dataset):
            continue
        
        entry = dataset[conv_idx]
        conversation = entry["conversation"]
        speaker_a = conversation["speaker_a"]
        speaker_b = conversation["speaker_b"]
        user_id = f"locomo_{system_name}_{conv_idx}"
        
        sorted_sessions = get_sorted_sessions(conversation)
        
        # QA 对（跳过没有 answer 的对抗性问题）
        all_qa = entry.get("qa", entry.get("qa_pairs", []))
        qa_list = []
        for i, qa in enumerate(all_qa):
            if "answer" not in qa or not qa["answer"]:
                continue
            if categories and qa.get("category") not in categories:
                continue
            qa_list.append((i, qa))
        
        if max_questions:
            qa_list = qa_list[:max_questions]
        
        print(f"\n[对话 {conv_idx}] {speaker_a} & {speaker_b}")
        print(f"  Sessions: {len(sorted_sessions)}, QA: {len(qa_list)}")
        
        # --- 写入记忆 ---
        print("  写入记忆中...")
        reset_token_stats()
        write_start = time.time()
        for sess_idx, (session_key, date_str, turns) in enumerate(sorted_sessions):
            session_epoch = locomo_date_to_epoch(date_str) or time.time()
            
            # 构造带日期上下文的对话
            date_header = f"[Conversation Date: {date_str}]\n"
            
            # 分批写入（每 5 轮一批，避免太长）
            batch_size = 5
            for i in range(0, len(turns), batch_size):
                batch = turns[i:i+batch_size]
                batch_text = turns_to_text(batch, speaker_a, speaker_b)
                if batch_text.strip():
                    try:
                        full_text = date_header + batch_text
                        mem.add(full_text, user_id=user_id, timestamp=session_epoch)
                    except Exception as e:
                        print(f"    [警告] 写入失败 session {session_key} batch {i}: {e}")
            
            if (sess_idx + 1) % 5 == 0:
                print(f"    已处理 {sess_idx + 1}/{len(sorted_sessions)} sessions")
        
        write_elapsed = time.time() - write_start
        write_tokens = get_token_stats()
        cost_stats["write_time_seconds"] += write_elapsed
        for k in write_tokens:
            cost_stats["write_tokens"][k] += write_tokens[k]
        print(f"  写入完成: {write_elapsed:.1f}s, tokens: {write_tokens['total_tokens']}, LLM调用: {write_tokens['call_count']}次")
        
        # 参考日期（最后一个 session 的日期）
        ref_date = sorted_sessions[-1][1] if sorted_sessions else "2023"
        
        # --- 回答问题 ---
        print("  回答问题中...")
        conv_correct = 0
        conv_total = 0
        reset_token_stats()
        answer_start = time.time()
        
        for qa_idx, qa in qa_list:
            question = qa["question"]
            gold_answer = str(qa["answer"])
            category = qa.get("category", 0)
            
            q_start = time.time()
            
            # 检索
            search_results = mem.search(question, user_id=user_id, top_k=top_k)
            memories_text = "\n".join([
                f"{i+1}. {r['memory']}" for i, r in enumerate(search_results)
            ])
            
            # 生成答案
            try:
                generated = chat_completion(
                    system="You are a precise QA assistant. Answer directly and concisely.",
                    user=ANSWER_PROMPT.format(
                        memories=memories_text,
                        question=question,
                        reference_date=ref_date,
                    ),
                    temperature=0.1,
                )
            except Exception as e:
                generated = f"[ERROR] {e}"
            
            # LLM 裁判
            try:
                judge_result = chat_completion_json(
                    system=JUDGE_SYSTEM,
                    user=JUDGE_PROMPT.format(
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
            
            category_stats[category]["total"] += 1
            if is_correct:
                category_stats[category]["correct"] += 1
            
            all_results.append({
                "conversation_idx": conv_idx,
                "qa_idx": qa_idx,
                "question": question,
                "gold_answer": gold_answer,
                "generated_answer": generated.strip(),
                "judgment": label,
                "judge_reason": reasoning,
                "category": category,
                "top_memories": [r['memory'] for r in search_results[:5]],
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
    print(f"评测完成 - {system_name}")
    print(f"{'='*60}")
    print(f"总题数: {total_questions}")
    print(f"正确数: {total_correct}")
    print(f"准确率: {overall_acc:.1f}%")
    
    print(f"\n各类别准确率:")
    cat_names = {
        0: "single-hop",
        1: "multi-hop",
        2: "temporal",
        3: "numerical",
        4: "comparison",
    }
    for cat, stats in sorted(category_stats.items()):
        cat_name = cat_names.get(cat, f"cat_{cat}")
        acc = stats['correct'] / stats['total'] * 100 if stats['total'] > 0 else 0
        print(f"  {cat_name:<15}: {stats['correct']:>3}/{stats['total']:<3} ({acc:>5.1f}%)")
    
    # --- 成本统计 ---
    total_elapsed = time.time() - eval_start_time
    cost_stats["total_time_seconds"] = total_elapsed
    
    # 数据库大小
    db_path = getattr(mem, 'db_path', '')
    if db_path and os.path.exists(db_path):
        cost_stats["db_size_bytes"] = os.path.getsize(db_path)
    
    # 记忆条目数（从 memory 系统获取）
    try:
        cost_stats["memory_entries"] = mem.count_memories() if hasattr(mem, 'count_memories') else 0
    except:
        cost_stats["memory_entries"] = 0
    
    # 平均答题耗时
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
    print(f"    输入: {wt['prompt_tokens']:,}, 输出: {wt['completion_tokens']:,}")
    print(f"  答题阶段: {at['total_tokens']:,} tokens ({at['call_count']} 次调用)")
    print(f"    输入: {at['prompt_tokens']:,}, 输出: {at['completion_tokens']:,}")
    print(f"  总计: {wt['total_tokens']+at['total_tokens']:,} tokens")
    print(f"\n存储占用:")
    print(f"  数据库大小: {cost_stats['db_size_bytes']/1024:.1f} KB")
    print(f"  记忆条目: {cost_stats['memory_entries']}")
    print(f"\n答题性能:")
    print(f"  平均每题耗时: {cost_stats['avg_answer_time_ms']:.0f} ms")
    
    # 保存结果
    result_data = {
        "system": system_name,
        "total_questions": total_questions,
        "correct": total_correct,
        "accuracy": overall_acc,
        "category_stats": {
            str(k): v for k, v in category_stats.items()
        },
        "details": all_results,
        "top_k": top_k,
        "cost_stats": cost_stats,
    }
    
    result_path = os.path.join(output_dir, f"{system_name}_results.json")
    with open(result_path, "w") as f:
        json.dump(result_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n结果已保存到: {result_path}")
    
    mem.close()
    return result_data


# =============================================================================
# 命令行入口
# =============================================================================
def main():
    parser = argparse.ArgumentParser(description="LoCoMo Memory System Evaluation")
    parser.add_argument("--dataset", type=str, 
                        default="data/LoCoMo_dataset.json",
                        help="LoCoMo 数据集路径")
    parser.add_argument("--system", type=str, required=True,
                        choices=["baseline", "cognitive", "cognitive_vector", "amem", "mem0", "amem_official", "oom"],
                        help="记忆系统类型")
    parser.add_argument("--conversations", type=str, default="0",
                        help="对话索引，如 '0' 或 '0,1,2' 或 'all'")
    parser.add_argument("--max-questions", type=int, default=None,
                        help="每个对话最多测试多少题")
    parser.add_argument("--top-k", type=int, default=20,
                        help="检索返回的记忆数量")
    parser.add_argument("--output-dir", type=str, default="results",
                        help="结果输出目录")
    parser.add_argument("--categories", type=str, default=None,
                        help="只测试指定类别，如 '0,1'")
    
    args = parser.parse_args()
    
    # 解析对话索引
    if args.conversations == "all":
        with open(args.dataset) as f:
            dataset = json.load(f)
        conv_indices = list(range(len(dataset)))
    else:
        conv_indices = [int(x.strip()) for x in args.conversations.split(",")]
    
    categories = None
    if args.categories:
        categories = [int(x.strip()) for x in args.categories.split(",")]
    
    run_evaluation(
        dataset_path=args.dataset,
        system_name=args.system,
        conv_indices=conv_indices,
        max_questions=args.max_questions,
        top_k=args.top_k,
        output_dir=args.output_dir,
        categories=categories,
    )


if __name__ == "__main__":
    main()
