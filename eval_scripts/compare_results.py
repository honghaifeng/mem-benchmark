"""
对比分析工具：对比 baseline 和 cognitive 的评测结果
"""
import json
import os
import sys
from collections import defaultdict


CAT_NAMES = {
    0: "single-hop",
    1: "multi-hop",
    2: "temporal",
    3: "numerical",
    4: "comparison",
    5: "cat_5",
}


def load_results(path: str) -> dict:
    with open(path) as f:
        return json.load(f)


def compare(baseline_path: str, cognitive_path: str):
    bl = load_results(baseline_path)
    co = load_results(cognitive_path)
    
    print("=" * 70)
    print("LoCoMo 记忆系统对比分析")
    print("=" * 70)
    
    print(f"\n{'指标':<20} {'Baseline':>12} {'Cognitive':>12} {'提升':>12}")
    print("-" * 60)
    
    bl_acc = bl["accuracy"]
    co_acc = co["accuracy"]
    diff = co_acc - bl_acc
    sign = "+" if diff >= 0 else ""
    print(f"{'总体准确率':<20} {bl_acc:>11.1f}% {co_acc:>11.1f}% {sign}{diff:>10.1f}%")
    
    print(f"{'总题数':<20} {bl['total_questions']:>12} {co['total_questions']:>12} {'':>12}")
    print(f"{'正确数':<20} {bl['correct']:>12} {co['correct']:>12} {co['correct']-bl['correct']:>+12}")
    
    print(f"\n各类别对比：")
    print(f"{'类别':<18} {'Baseline':>10} {'Cognitive':>10} {'提升':>10} {'题数':>8}")
    print("-" * 56)
    
    all_cats = sorted(set(list(bl["category_stats"].keys()) + list(co["category_stats"].keys())))
    for cat in all_cats:
        bl_stat = bl["category_stats"].get(cat, {"total": 0, "correct": 0})
        co_stat = co["category_stats"].get(cat, {"total": 0, "correct": 0})
        
        bl_acc = bl_stat["correct"] / bl_stat["total"] * 100 if bl_stat["total"] > 0 else 0
        co_acc = co_stat["correct"] / co_stat["total"] * 100 if co_stat["total"] > 0 else 0
        diff = co_acc - bl_acc
        sign = "+" if diff >= 0 else ""
        cat_name = CAT_NAMES.get(int(cat), f"cat_{cat}")
        total = max(bl_stat["total"], co_stat["total"])
        print(f"{cat_name:<18} {bl_acc:>9.1f}% {co_acc:>9.1f}% {sign}{diff:>8.1f}% {total:>8}")
    
    print()
    
    # 错误分析
    bl_details = {d["qa_idx"]: d for d in bl["details"]}
    co_details = {d["qa_idx"]: d for d in co["details"]}
    
    both_wrong = 0
    bl_right_co_wrong = 0
    bl_wrong_co_right = 0
    both_right = 0
    
    for idx in set(bl_details.keys()) & set(co_details.keys()):
        bl_correct = bl_details[idx]["judgment"] == "CORRECT"
        co_correct = co_details[idx]["judgment"] == "CORRECT"
        if bl_correct and co_correct:
            both_right += 1
        elif bl_correct and not co_correct:
            bl_right_co_wrong += 1
        elif not bl_correct and co_correct:
            bl_wrong_co_right += 1
        else:
            both_wrong += 1
    
    print(f"错误模式分析：")
    print(f"  两个都对: {both_right}")
    print(f"  两个都错: {both_wrong}")
    print(f"  基线对/认知错: {bl_right_co_wrong}")
    print(f"  基线错/认知对: {bl_wrong_co_right} (认知额外答对的)")
    print()
    
    # 展示认知额外答对的题
    if bl_wrong_co_right > 0:
        print("认知记忆额外答对的题目（示例，最多5题）：")
        count = 0
        for idx in sorted(set(bl_details.keys()) & set(co_details.keys())):
            bl_correct = bl_details[idx]["judgment"] == "CORRECT"
            co_correct = co_details[idx]["judgment"] == "CORRECT"
            if not bl_correct and co_correct:
                q = co_details[idx]
                cat = CAT_NAMES.get(q.get("category", 0), f"cat_{q.get('category')}")
                print(f"  [{cat}] Q: {q['question'][:80]}")
                print(f"       Gold: {q['gold_answer']}")
                print(f"       Gen:  {q['generated_answer'][:100]}")
                count += 1
                if count >= 5:
                    break
        print()
    
    # 展示认知答错但基线答对的题
    if bl_right_co_wrong > 0:
        print("认知记忆答错但基线答对的题目（示例，最多5题）：")
        count = 0
        for idx in sorted(set(bl_details.keys()) & set(co_details.keys())):
            bl_correct = bl_details[idx]["judgment"] == "CORRECT"
            co_correct = co_details[idx]["judgment"] == "CORRECT"
            if bl_correct and not co_correct:
                q = co_details[idx]
                cat = CAT_NAMES.get(q.get("category", 0), f"cat_{q.get('category')}")
                print(f"  [{cat}] Q: {q['question'][:80]}")
                print(f"       Gold: {q['gold_answer']}")
                print(f"       Gen:  {q['generated_answer'][:100]}")
                count += 1
                if count >= 5:
                    break
        print()


def main():
    if len(sys.argv) < 3:
        print("用法: python compare_results.py <baseline_results.json> <cognitive_results.json>")
        sys.exit(1)
    
    compare(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    main()
