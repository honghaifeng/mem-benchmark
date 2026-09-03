"""
Mem0 官方版 LoCoMo 英文并行测评
10个对话并行跑
"""
import json
import os
import sys
import time
import subprocess
from concurrent.futures import ProcessPoolExecutor, as_completed

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET = os.path.join(BASE_DIR, "locomo10.json")
OUTPUT_DIR = os.path.join(BASE_DIR, "results", "mem0_official_locomo10")
SCRIPT = os.path.join(BASE_DIR, "mem0_official_eval.py")
NUM_CONV = 10
TOP_K = 15


def run_single_conv(conv_idx: int) -> dict:
    """跑单个对话"""
    env = os.environ.copy()
    for k in ["http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "all_proxy"]:
        env.pop(k, None)

    env_path = os.path.expanduser("~/.hermes/.env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.startswith("DEEPSEEK_API_KEY="):
                    env["DEEPSEEK_API_KEY"] = line.strip().split("=", 1)[1]
                    break

    conv_output = os.path.join(OUTPUT_DIR, f"conv{conv_idx}")
    os.makedirs(conv_output, exist_ok=True)

    cmd = [
        sys.executable, "-u",
        SCRIPT,
        "--dataset", DATASET,
        "--conversations", str(conv_idx),
        "--top-k", str(TOP_K),
        "--output-dir", conv_output,
    ]

    print(f"[Conv {conv_idx}] 启动...", flush=True)
    start = time.time()
    result = subprocess.run(
        cmd,
        cwd=BASE_DIR,
        env=env,
        capture_output=True,
        text=True,
        timeout=1800,
    )
    elapsed = time.time() - start

    if result.returncode != 0:
        print(f"[Conv {conv_idx}] 失败 ({elapsed:.0f}s)\n{result.stderr[-800:]}", flush=True)
        return {"conv_idx": conv_idx, "status": "failed", "error": result.stderr[-800:], "time": elapsed}

    result_file = os.path.join(conv_output, "mem0_results.json")
    if os.path.exists(result_file):
        with open(result_file) as f:
            data = json.load(f)
        correct = data.get("correct", 0)
        total = data.get("total_questions", 0)
        acc = data.get("accuracy", 0)
        print(f"[Conv {conv_idx}] 完成: {correct}/{total} = {acc:.1f}% ({elapsed:.0f}s)", flush=True)
        return {"conv_idx": conv_idx, "status": "ok", "data": data, "time": elapsed}
    else:
        print(f"[Conv {conv_idx}] 结果文件不存在 ({elapsed:.0f}s)", flush=True)
        return {"conv_idx": conv_idx, "status": "no_result", "time": elapsed}


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Mem0 官方版 LoCoMo 英文并行测评")
    print(f"对话数: {NUM_CONV}, Top-K: {TOP_K}")
    print(f"输出目录: {OUTPUT_DIR}")
    print(f"{'='*60}\n")

    start_all = time.time()
    results = [None] * NUM_CONV

    max_workers = 5
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(run_single_conv, i): i for i in range(NUM_CONV)}
        for future in as_completed(futures):
            conv_idx = futures[future]
            try:
                result = future.result()
                results[conv_idx] = result
            except Exception as e:
                print(f"[Conv {conv_idx}] 异常: {e}", flush=True)
                results[conv_idx] = {"conv_idx": conv_idx, "status": "exception", "error": str(e)}

    total_elapsed = time.time() - start_all
    print(f"\n{'='*60}")
    print(f"全部完成，总耗时: {total_elapsed/60:.1f} 分钟")

    # 合并结果
    all_details = []
    total_correct = 0
    total_questions = 0
    ok_count = 0
    for r in results:
        if r and r["status"] == "ok":
            ok_count += 1
            d = r["data"]
            total_correct += d.get("correct", 0)
            total_questions += d.get("total_questions", 0)
            all_details.extend(d.get("details", []))
        elif r:
            print(f"  Conv {r['conv_idx']}: {r['status']}")

    overall_acc = total_correct / total_questions * 100 if total_questions > 0 else 0
    print(f"\n成功: {ok_count}/{NUM_CONV} 个对话")
    print(f"总题数: {total_questions}")
    print(f"正确数: {total_correct}")
    print(f"准确率: {overall_acc:.2f}%")

    # 保存合并结果
    merged = {
        "system": "mem0_official",
        "dataset": "LoCoMo_10",
        "total_questions": total_questions,
        "correct": total_correct,
        "accuracy": overall_acc,
        "num_conversations": ok_count,
        "details": all_details,
        "top_k": TOP_K,
        "total_time_seconds": total_elapsed,
    }
    merged_path = os.path.join(OUTPUT_DIR, "mem0_official_locomo_merged.json")
    with open(merged_path, "w") as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)
    print(f"\n合并结果已保存: {merged_path}")


if __name__ == "__main__":
    main()
