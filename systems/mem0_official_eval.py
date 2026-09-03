"""
Mem0 官方版 LoCoMo 测评脚本
使用 mem0ai 官方 SDK + DeepSeek LLM
用我们的 LLM 裁判评分（与 baseline/cognitive 一致，保证公平）
"""
import json
import os
import re
import sys
import time
import argparse
from datetime import datetime, timezone
from collections import defaultdict

from mem0 import Memory

# 复用我们框架的 LLM 裁判和工具函数
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from llm_client import chat_completion_json, chat_completion


# =============================================================================
# 数据集加载与解析（从 locomo_eval.py 复制，保持一致）
# =============================================================================
def parse_locomo_date(date_str: str) -> datetime | None:
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

def turns_to_text(turns: list[dict], speaker_a: str, speaker_b: str) -> str:
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
# 答案生成 Prompt
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
# LLM 裁判 Prompt（与我们的框架完全一致，保证公平）
# =============================================================================
JUDGE_SYSTEM = "You are a strict judge evaluating the correctness of an answer."

JUDGE_PROMPT = """Evaluate if the generated answer is correct compared to the gold answer.

Question: {question}
Gold Answer: {gold_answer}
Generated Answer: {generated_answer}

Scoring Rules:
1. Exact match = CORRECT
2. Synonyms or paraphrasing with same meaning = CORRECT
3. Partial correctness (contains key info but missing some details) = CORRECT (partial credit counts)
4. Wrong answer, wrong date, wrong person = INCORRECT
5. If the generated answer says "I don't know" or similar = INCORRECT
6. Date tolerance: if the gold answer has a full date and generated has month+year only, it's still CORRECT if month and year match
7. Semantic similarity is more important than exact wording

Return ONLY valid JSON:
{{
  "judgment": "CORRECT" or "INCORRECT",
  "reason": "one sentence explaining why"
}}
"""


def judge_answer(question: str, gold_answer: str, generated_answer: str) -> tuple[str, str]:
    result = chat_completion_json(
        system=JUDGE_SYSTEM,
        user=JUDGE_PROMPT.format(
            question=question,
            gold_answer=gold_answer,
            generated_answer=generated_answer
        ),
        temperature=0.1,
    )
    judgment = result.get("judgment", "INCORRECT")
    reason = result.get("reason", "")
    if judgment not in ("CORRECT", "INCORRECT"):
        judgment = "INCORRECT"
    return judgment, reason


# =============================================================================
# 主测评函数
# =============================================================================
def evaluate_mem0(dataset_path: str, output_dir: str, 
                  conv_indices: list[int], max_questions: int | None,
                  top_k: int, deepseek_key: str, deepseek_base_url: str):
    os.makedirs(output_dir, exist_ok=True)
    
    # 初始化 Mem0（官方 SDK）
    # - LLM: DeepSeek（与其他系统一致，保证公平）
    # - Embedder: fastembed 本地嵌入（DeepSeek 不提供嵌入 API，用本地 BGE 模型，与 A-Mem 官方类似）
    # - Vector Store: Qdrant（Mem0 默认）
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
                "model": "BAAI/bge-small-en-v1.5",
            }
        },
        "vector_store": {
            "provider": "qdrant",
            "config": {
                "collection_name": "mem0_locomo_eval",
                "path": os.path.join(output_dir, "qdrant_data"),
                "embedding_model_dims": 384,
            }
        },
        "history_db_path": os.path.join(output_dir, "mem0_history.db"),
        "version": "v1.1",
    }
    
    print("Initializing Mem0...")
    m = Memory.from_config(config)
    print("Mem0 initialized successfully.")
    
    # 载入数据集
    with open(dataset_path, 'r') as f:
        dataset = json.load(f)
    
    if isinstance(dataset, dict):
        dataset = [dataset]
    
    all_results = []
    total_questions = 0
    total_correct = 0
    category_stats = defaultdict(lambda: {"total": 0, "correct": 0})
    
    print(f"\n{'='*60}")
    print(f"LoCoMo 评测 - 系统: Mem0 (官方版)")
    print(f"对话: {conv_indices}, Top-K: {top_k}")
    print(f"{'='*60}\n")
    
    for conv_idx in conv_indices:
        if conv_idx >= len(dataset):
            print(f"[对话 {conv_idx}] 跳过（数据集只有 {len(dataset)} 个对话）")
            continue
        
        conv = dataset[conv_idx]
        conv_data = conv.get("conversation", conv)
        qa_pairs = conv.get("qa", conv.get("qa_pairs", []))
        
        speaker_a = conv_data.get("speaker_a", "A")
        speaker_b = conv_data.get("speaker_b", "B")
        user_id = f"locomo_mem0_{conv_idx}"
        
        # 收集 session
        session_keys = sorted(
            [k for k in conv_data if re.match(r'^session_\d+$', k)],
            key=lambda x: int(re.search(r'\d+', x).group())
        )
        
        print(f"[对话 {conv_idx}] {speaker_a} & {speaker_b}")
        print(f"  Sessions: {len(session_keys)}, QA: {len(qa_pairs)}")
        
        # 写入记忆
        print(f"  写入记忆中...", end="", flush=True)
        mem_count = 0
        for skey in session_keys:
            date_key = f"{skey}_date_time"
            date_str = conv_data.get(date_key, "")
            turns = conv_data.get(skey, [])
            
            conv_text = turns_to_text(turns, speaker_a, speaker_b)
            if not conv_text.strip():
                continue
            
            # Mem0 官方 API: add 方法接收文本，自动提取事实存储
            # 返回: {'results': [{'id': ..., 'memory': ..., 'event': ...}]}
            # 关键：带上对话日期上下文，否则相对时间会被错误地按当前日期换算
            date_header = f"[Conversation Date: {date_str}]\n"
            try:
                result = m.add(date_header + conv_text, user_id=user_id)
                added = result.get('results', []) if isinstance(result, dict) else []
                mem_count += len(added)
            except Exception as e:
                print(f"\n  Warning: Mem0 add failed for {skey}: {e}")
        
        print(f" 完成（{mem_count} 条记忆）")
        
        # 答题
        print(f"  回答问题中...", end="", flush=True)
        conv_correct = 0
        conv_total = 0
        
        # 获取最后一个 session 的日期作为 reference date
        last_date = ""
        for skey in reversed(session_keys):
            date_key = f"{skey}_date_time"
            if conv_data.get(date_key):
                last_date = conv_data[date_key]
                break
        
        q_count = 0
        for qa_idx, qa in enumerate(qa_pairs):
            if max_questions is not None and q_count >= max_questions:
                break
            
            question = qa.get("question", "")
            gold_answer = qa.get("answer", qa.get("final_answer", ""))
            category = qa.get("category", 0)
            if isinstance(category, str):
                try:
                    category = int(category)
                except:
                    category = 0
            
            # Mem0 检索（官方 API：用 filters 传 user_id，返回 dict 含 results 列表）
            try:
                search_result = m.search(question, filters={"user_id": user_id}, limit=top_k)
                results_list = search_result.get('results', []) if isinstance(search_result, dict) else []
                top_memories = [r.get("memory", "") for r in results_list[:top_k]]
            except Exception as e:
                print(f"\n  Warning: search failed for Q{qa_idx}: {e}")
                top_memories = []
            
            memory_text = "\n".join([f"- {m}" for m in top_memories])
            
            # 生成答案
            try:
                generated = chat_completion(
                    system="You are a precise question-answering assistant.",
                    user=ANSWER_PROMPT.format(
                        memories=memory_text[:8000],
                        question=question,
                        reference_date=last_date
                    ),
                    temperature=0.1,
                )
                generated = generated.strip()
            except Exception as e:
                generated = ""
            
            # 裁判评分
            judgment, reason = judge_answer(question, gold_answer, generated)
            
            is_correct = judgment == "CORRECT"
            if is_correct:
                total_correct += 1
                conv_correct += 1
            
            total_questions += 1
            conv_total += 1
            category_stats[str(category)]["total"] += 1
            if is_correct:
                category_stats[str(category)]["correct"] += 1
            
            all_results.append({
                "conversation_idx": conv_idx,
                "qa_idx": qa_idx,
                "question": question,
                "gold_answer": gold_answer,
                "generated_answer": generated,
                "judgment": judgment,
                "judge_reason": reason,
                "category": category,
                "top_memories": top_memories[:5],
            })
            
            q_count += 1
        
        acc = conv_correct / conv_total * 100 if conv_total > 0 else 0
        print(f" 完成（{conv_correct}/{conv_total} = {acc:.1f}%）")
    
    # 汇总
    accuracy = total_correct / total_questions * 100 if total_questions > 0 else 0
    
    print(f"\n{'='*60}")
    print(f"评测完成 - Mem0 (官方版)")
    print(f"总题数: {total_questions}")
    print(f"正确数: {total_correct}")
    print(f"准确率: {accuracy:.2f}%")
    print(f"{'='*60}\n")
    
    # 保存结果
    result_data = {
        "system": "mem0_official",
        "total_questions": total_questions,
        "correct": total_correct,
        "accuracy": accuracy,
        "category_stats": dict(category_stats),
        "details": all_results,
        "top_k": top_k,
    }
    
    result_path = os.path.join(output_dir, "mem0_results.json")
    with open(result_path, 'w') as f:
        json.dump(result_data, f, indent=2, ensure_ascii=False)
    
    print(f"结果已保存到: {result_path}")
    return result_data


def main():
    parser = argparse.ArgumentParser(description="Mem0 官方版 LoCoMo 测评")
    parser.add_argument("--dataset", type=str, default="locomo10.json",
                        help="LoCoMo 数据集路径")
    parser.add_argument("--conversations", type=str, default="0",
                        help="对话索引，如 '0' 或 '0,1,2' 或 'all'")
    parser.add_argument("--max-questions", type=int, default=None,
                        help="每个对话最多测试多少题")
    parser.add_argument("--top-k", type=int, default=15,
                        help="检索返回的记忆数量")
    parser.add_argument("--output-dir", type=str, default="results/mem0_official",
                        help="结果输出目录")
    args = parser.parse_args()
    
    # 解析对话索引
    if args.conversations == "all":
        with open(args.dataset, 'r') as f:
            data = json.load(f)
        if isinstance(data, dict):
            data = [data]
        conv_indices = list(range(len(data)))
    else:
        conv_indices = [int(x.strip()) for x in args.conversations.split(",") if x.strip()]
    
    # 获取 DeepSeek 配置（从环境变量）
    deepseek_key = os.environ.get("DEEPSEEK_API_KEY", "")
    deepseek_base_url = os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
    
    if not deepseek_key:
        print("Error: DEEPSEEK_API_KEY environment variable not set")
        sys.exit(1)
    
    evaluate_mem0(
        dataset_path=args.dataset,
        output_dir=args.output_dir,
        conv_indices=conv_indices,
        max_questions=args.max_questions,
        top_k=args.top_k,
        deepseek_key=deepseek_key,
        deepseek_base_url=deepseek_base_url,
    )


if __name__ == "__main__":
    main()
