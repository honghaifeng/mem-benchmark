"""
A-Mem 官方版 LoCoMo 并行测评脚本
每个对话一个进程，10个对话同时跑
"""
import"""
A-Mem 官方版 LoCoMo 并行测评脚本
每个对话一个进程，10个对话同时跑
"""
import json
import os
import sys
import time
import argparse
import subprocess
from pathlib import Path

def run_single_conv(conv_idx: int, dataset_path: str,"""
A-Mem 官方版 LoCoMo 并行测评脚本
每个对话一个进程，10个对话同时跑
"""
import json
import os
import sys
import time
import argparse
import subprocess
from pathlib import Path

def run_single_conv(conv_idx: int, dataset_path: str, output_dir: str, top_k: int):
    """单个对话的测评（子进程）"""
    # 加载数据集
    with open(dataset_path) as f:
        dataset = json.load"""
A-Mem 官方版 LoCoMo 并行测评脚本
每个对话一个进程，10个对话同时跑
"""
import json
import os
import sys
import time
import argparse
import subprocess
from pathlib import Path

def run_single_conv(conv_idx: int, dataset_path: str, output_dir: str, top_k: int):
    """单个对话的测评（子进程）"""
    # 加载数据集
    with open(dataset_path) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    
    entry = dataset[conv_idx]
    conversation = entry["conversation"]
    speaker_a = conversation["speaker_a"]
    speaker_b = conversation["speaker_b"""
A-Mem 官方版 LoCoMo 并行测评脚本
每个对话一个进程，10个对话同时跑
"""
import json
import os
import sys
import time
import argparse
import subprocess
from pathlib import Path

def run_single_conv(conv_idx: int, dataset_path: str, output_dir: str, top_k: int):
    """单个对话的测评（子进程）"""
    # 加载数据集
    with open(dataset_path) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    
    entry = dataset[conv_idx]
    conversation = entry["conversation"]
    speaker_a = conversation["speaker_a"]
    speaker_b = conversation["speaker_b"]
    
    # 获取 sessions
    from locomo_eval import get_sorted_sessions, locomo_date_to_epoch, turns_to_text
    from locomo_eval import ANSW"""
A-Mem 官方版 LoCoMo 并行测评脚本
每个对话一个进程，10个对话同时跑
"""
import json
import os
import sys
import time
import argparse
import subprocess
from pathlib import Path

def run_single_conv(conv_idx: int, dataset_path: str, output_dir: str, top_k: int):
    """单个对话的测评（子进程）"""
    # 加载数据集
    with open(dataset_path) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    
    entry = dataset[conv_idx]
    conversation = entry["conversation"]
    speaker_a = conversation["speaker_a"]
    speaker_b = conversation["speaker_b"]
    
    # 获取 sessions
    from locomo_eval import get_sorted_sessions, locomo_date_to_epoch, turns_to_text
    from locomo_eval import ANSWER_PROMPT, JUDGE_SYSTEM, JUDGE_PROMPT
    from llm_client import chat_completion, chat_completion_json, reset_token_stats, get_token_stats
    from amem_official_memory import OfficialAMemMemory"""
A-Mem 官方版 LoCoMo 并行测评脚本
每个对话一个进程，10个对话同时跑
"""
import json
import os
import sys
import time
import argparse
import subprocess
from pathlib import Path

def run_single_conv(conv_idx: int, dataset_path: str, output_dir: str, top_k: int):
    """单个对话的测评（子进程）"""
    # 加载数据集
    with open(dataset_path) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    
    entry = dataset[conv_idx]
    conversation = entry["conversation"]
    speaker_a = conversation["speaker_a"]
    speaker_b = conversation["speaker_b"]
    
    # 获取 sessions
    from locomo_eval import get_sorted_sessions, locomo_date_to_epoch, turns_to_text
    from locomo_eval import ANSWER_PROMPT, JUDGE_SYSTEM, JUDGE_PROMPT
    from llm_client import chat_completion, chat_completion_json, reset_token_stats, get_token_stats
    from amem_official_memory import OfficialAMemMemory
    
    sorted_sessions = get_sorted_sessions(conversation)
    
    qa_list = []
    all_qa = entry.get("qa", entry.get("qa_pairs", []))
    for i, qa in enumerate(all_qa):
        if """"
A-Mem 官方版 LoCoMo 并行测评脚本
每个对话一个进程，10个对话同时跑
"""
import json
import os
import sys
import time
import argparse
import subprocess
from pathlib import Path

def run_single_conv(conv_idx: int, dataset_path: str, output_dir: str, top_k: int):
    """单个对话的测评（子进程）"""
    # 加载数据集
    with open(dataset_path) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    
    entry = dataset[conv_idx]
    conversation = entry["conversation"]
    speaker_a = conversation["speaker_a"]
    speaker_b = conversation["speaker_b"]
    
    # 获取 sessions
    from locomo_eval import get_sorted_sessions, locomo_date_to_epoch, turns_to_text
    from locomo_eval import ANSWER_PROMPT, JUDGE_SYSTEM, JUDGE_PROMPT
    from llm_client import chat_completion, chat_completion_json, reset_token_stats, get_token_stats
    from amem_official_memory import OfficialAMemMemory
    
    sorted_sessions = get_sorted_sessions(conversation)
    
    qa_list = []
    all_qa = entry.get("qa", entry.get("qa_pairs", []))
    for i, qa in enumerate(all_qa):
        if "answer" not in qa or not qa["answer"]:
            continue
        qa_list.append((i, qa))
    
    user_id = f"locomo_amem_raw_{conv_idx}"
    
    # 每个对话独立的"""
A-Mem 官方版 LoCoMo 并行测评脚本
每个对话一个进程，10个对话同时跑
"""
import json
import os
import sys
import time
import argparse
import subprocess
from pathlib import Path

def run_single_conv(conv_idx: int, dataset_path: str, output_dir: str, top_k: int):
    """单个对话的测评（子进程）"""
    # 加载数据集
    with open(dataset_path) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    
    entry = dataset[conv_idx]
    conversation = entry["conversation"]
    speaker_a = conversation["speaker_a"]
    speaker_b = conversation["speaker_b"]
    
    # 获取 sessions
    from locomo_eval import get_sorted_sessions, locomo_date_to_epoch, turns_to_text
    from locomo_eval import ANSWER_PROMPT, JUDGE_SYSTEM, JUDGE_PROMPT
    from llm_client import chat_completion, chat_completion_json, reset_token_stats, get_token_stats
    from amem_official_memory import OfficialAMemMemory
    
    sorted_sessions = get_sorted_sessions(conversation)
    
    qa_list = []
    all_qa = entry.get("qa", entry.get("qa_pairs", []))
    for i, qa in enumerate(all_qa):
        if "answer" not in qa or not qa["answer"]:
            continue
        qa_list.append((i, qa))
    
    user_id = f"locomo_amem_raw_{conv_idx}"
    
    # 每个对话独立的 A-Mem 实例
    mem = OfficialAMemMemory(db_path=os.path.join(output_dir, f"amem_raw_conv{conv_idx}.db"))
    
    print(f"[Conv {conv_idx"""
A-Mem 官方版 LoCoMo 并行测评脚本
每个对话一个进程，10个对话同时跑
"""
import json
import os
import sys
import time
import argparse
import subprocess
from pathlib import Path

def run_single_conv(conv_idx: int, dataset_path: str, output_dir: str, top_k: int):
    """单个对话的测评（子进程）"""
    # 加载数据集
    with open(dataset_path) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    
    entry = dataset[conv_idx]
    conversation = entry["conversation"]
    speaker_a = conversation["speaker_a"]
    speaker_b = conversation["speaker_b"]
    
    # 获取 sessions
    from locomo_eval import get_sorted_sessions, locomo_date_to_epoch, turns_to_text
    from locomo_eval import ANSWER_PROMPT, JUDGE_SYSTEM, JUDGE_PROMPT
    from llm_client import chat_completion, chat_completion_json, reset_token_stats, get_token_stats
    from amem_official_memory import OfficialAMemMemory
    
    sorted_sessions = get_sorted_sessions(conversation)
    
    qa_list = []
    all_qa = entry.get("qa", entry.get("qa_pairs", []))
    for i, qa in enumerate(all_qa):
        if "answer" not in qa or not qa["answer"]:
            continue
        qa_list.append((i, qa))
    
    user_id = f"locomo_amem_raw_{conv_idx}"
    
    # 每个对话独立的 A-Mem 实例
    mem = OfficialAMemMemory(db_path=os.path.join(output_dir, f"amem_raw_conv{conv_idx}.db"))
    
    print(f"[Conv {conv_idx}] {speaker_a} & {speaker_b} | {len(sorted_sessions)} sessions, {len(qa_list)} QA")
    
    # 写入记忆
    write_start = time.time()"""
A-Mem 官方版 LoCoMo 并行测评脚本
每个对话一个进程，10个对话同时跑
"""
import json
import os
import sys
import time
import argparse
import subprocess
from pathlib import Path

def run_single_conv(conv_idx: int, dataset_path: str, output_dir: str, top_k: int):
    """单个对话的测评（子进程）"""
    # 加载数据集
    with open(dataset_path) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    
    entry = dataset[conv_idx]
    conversation = entry["conversation"]
    speaker_a = conversation["speaker_a"]
    speaker_b = conversation["speaker_b"]
    
    # 获取 sessions
    from locomo_eval import get_sorted_sessions, locomo_date_to_epoch, turns_to_text
    from locomo_eval import ANSWER_PROMPT, JUDGE_SYSTEM, JUDGE_PROMPT
    from llm_client import chat_completion, chat_completion_json, reset_token_stats, get_token_stats
    from amem_official_memory import OfficialAMemMemory
    
    sorted_sessions = get_sorted_sessions(conversation)
    
    qa_list = []
    all_qa = entry.get("qa", entry.get("qa_pairs", []))
    for i, qa in enumerate(all_qa):
        if "answer" not in qa or not qa["answer"]:
            continue
        qa_list.append((i, qa))
    
    user_id = f"locomo_amem_raw_{conv_idx}"
    
    # 每个对话独立的 A-Mem 实例
    mem = OfficialAMemMemory(db_path=os.path.join(output_dir, f"amem_raw_conv{conv_idx}.db"))
    
    print(f"[Conv {conv_idx}] {speaker_a} & {speaker_b} | {len(sorted_sessions)} sessions, {len(qa_list)} QA")
    
    # 写入记忆
    write_start = time.time()
    mem_count = 0
    for sess_idx, (session_key, date_str, turns) in enumerate(sorted_sessions):
        session_epoch = locomo_date_to_epoch(date_str) or time.time()
        date_header = f"""
A-Mem 官方版 LoCoMo 并行测评脚本
每个对话一个进程，10个对话同时跑
"""
import json
import os
import sys
import time
import argparse
import subprocess
from pathlib import Path

def run_single_conv(conv_idx: int, dataset_path: str, output_dir: str, top_k: int):
    """单个对话的测评（子进程）"""
    # 加载数据集
    with open(dataset_path) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    
    entry = dataset[conv_idx]
    conversation = entry["conversation"]
    speaker_a = conversation["speaker_a"]
    speaker_b = conversation["speaker_b"]
    
    # 获取 sessions
    from locomo_eval import get_sorted_sessions, locomo_date_to_epoch, turns_to_text
    from locomo_eval import ANSWER_PROMPT, JUDGE_SYSTEM, JUDGE_PROMPT
    from llm_client import chat_completion, chat_completion_json, reset_token_stats, get_token_stats
    from amem_official_memory import OfficialAMemMemory
    
    sorted_sessions = get_sorted_sessions(conversation)
    
    qa_list = []
    all_qa = entry.get("qa", entry.get("qa_pairs", []))
    for i, qa in enumerate(all_qa):
        if "answer" not in qa or not qa["answer"]:
            continue
        qa_list.append((i, qa))
    
    user_id = f"locomo_amem_raw_{conv_idx}"
    
    # 每个对话独立的 A-Mem 实例
    mem = OfficialAMemMemory(db_path=os.path.join(output_dir, f"amem_raw_conv{conv_idx}.db"))
    
    print(f"[Conv {conv_idx}] {speaker_a} & {speaker_b} | {len(sorted_sessions)} sessions, {len(qa_list)} QA")
    
    # 写入记忆
    write_start = time.time()
    mem_count = 0
    for sess_idx, (session_key, date_str, turns) in enumerate(sorted_sessions):
        session_epoch = locomo_date_to_epoch(date_str) or time.time()
        date_header = f"[Conversation Date: {date_str}]\n"
        batch_size = 5
        for i in range(0, len(turns), batch_size):
            batch = turns[i:i+batch_size]
            batch_text = turns_to_text"""
A-Mem 官方版 LoCoMo 并行测评脚本
每个对话一个进程，10个对话同时跑
"""
import json
import os
import sys
import time
import argparse
import subprocess
from pathlib import Path

def run_single_conv(conv_idx: int, dataset_path: str, output_dir: str, top_k: int):
    """单个对话的测评（子进程）"""
    # 加载数据集
    with open(dataset_path) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    
    entry = dataset[conv_idx]
    conversation = entry["conversation"]
    speaker_a = conversation["speaker_a"]
    speaker_b = conversation["speaker_b"]
    
    # 获取 sessions
    from locomo_eval import get_sorted_sessions, locomo_date_to_epoch, turns_to_text
    from locomo_eval import ANSWER_PROMPT, JUDGE_SYSTEM, JUDGE_PROMPT
    from llm_client import chat_completion, chat_completion_json, reset_token_stats, get_token_stats
    from amem_official_memory import OfficialAMemMemory
    
    sorted_sessions = get_sorted_sessions(conversation)
    
    qa_list = []
    all_qa = entry.get("qa", entry.get("qa_pairs", []))
    for i, qa in enumerate(all_qa):
        if "answer" not in qa or not qa["answer"]:
            continue
        qa_list.append((i, qa))
    
    user_id = f"locomo_amem_raw_{conv_idx}"
    
    # 每个对话独立的 A-Mem 实例
    mem = OfficialAMemMemory(db_path=os.path.join(output_dir, f"amem_raw_conv{conv_idx}.db"))
    
    print(f"[Conv {conv_idx}] {speaker_a} & {speaker_b} | {len(sorted_sessions)} sessions, {len(qa_list)} QA")
    
    # 写入记忆
    write_start = time.time()
    mem_count = 0
    for sess_idx, (session_key, date_str, turns) in enumerate(sorted_sessions):
        session_epoch = locomo_date_to_epoch(date_str) or time.time()
        date_header = f"[Conversation Date: {date_str}]\n"
        batch_size = 5
        for i in range(0, len(turns), batch_size):
            batch = turns[i:i+batch_size]
            batch_text = turns_to_text(batch, speaker_a, speaker_b)
            if batch_text.strip():
                try:
                    full_text = date_header + batch_text
                    mem.add(full_text, user_id=user_id, timestamp=session_epoch)
                    mem_count += 1"""
A-Mem 官方版 LoCoMo 并行测评脚本
每个对话一个进程，10个对话同时跑
"""
import json
import os
import sys
import time
import argparse
import subprocess
from pathlib import Path

def run_single_conv(conv_idx: int, dataset_path: str, output_dir: str, top_k: int):
    """单个对话的测评（子进程）"""
    # 加载数据集
    with open(dataset_path) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    
    entry = dataset[conv_idx]
    conversation = entry["conversation"]
    speaker_a = conversation["speaker_a"]
    speaker_b = conversation["speaker_b"]
    
    # 获取 sessions
    from locomo_eval import get_sorted_sessions, locomo_date_to_epoch, turns_to_text
    from locomo_eval import ANSWER_PROMPT, JUDGE_SYSTEM, JUDGE_PROMPT
    from llm_client import chat_completion, chat_completion_json, reset_token_stats, get_token_stats
    from amem_official_memory import OfficialAMemMemory
    
    sorted_sessions = get_sorted_sessions(conversation)
    
    qa_list = []
    all_qa = entry.get("qa", entry.get("qa_pairs", []))
    for i, qa in enumerate(all_qa):
        if "answer" not in qa or not qa["answer"]:
            continue
        qa_list.append((i, qa))
    
    user_id = f"locomo_amem_raw_{conv_idx}"
    
    # 每个对话独立的 A-Mem 实例
    mem = OfficialAMemMemory(db_path=os.path.join(output_dir, f"amem_raw_conv{conv_idx}.db"))
    
    print(f"[Conv {conv_idx}] {speaker_a} & {speaker_b} | {len(sorted_sessions)} sessions, {len(qa_list)} QA")
    
    # 写入记忆
    write_start = time.time()
    mem_count = 0
    for sess_idx, (session_key, date_str, turns) in enumerate(sorted_sessions):
        session_epoch = locomo_date_to_epoch(date_str) or time.time()
        date_header = f"[Conversation Date: {date_str}]\n"
        batch_size = 5
        for i in range(0, len(turns), batch_size):
            batch = turns[i:i+batch_size]
            batch_text = turns_to_text(batch, speaker_a, speaker_b)
            if batch_text.strip():
                try:
                    full_text = date_header + batch_text
                    mem.add(full_text, user_id=user_id, timestamp=session_epoch)
                    mem_count += 1
                except Exception as e:
                    print(f"  [Conv {conv_idx}] 写入失败: {e}")
    write_elapsed = time.time() - write_start
    print(f"[Conv {conv_idx}] 写入完成: {mem_count} batches, {write_elapsed:.1f}s")
    
    # 参考日期
    ref_date = sorted_sessions[-1][1] if sorted_sessions else "2023"
    
    #"""
A-Mem 官方版 LoCoMo 并行测评脚本
每个对话一个进程，10个对话同时跑
"""
import json
import os
import sys
import time
import argparse
import subprocess
from pathlib import Path

def run_single_conv(conv_idx: int, dataset_path: str, output_dir: str, top_k: int):
    """单个对话的测评（子进程）"""
    # 加载数据集
    with open(dataset_path) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    
    entry = dataset[conv_idx]
    conversation = entry["conversation"]
    speaker_a = conversation["speaker_a"]
    speaker_b = conversation["speaker_b"]
    
    # 获取 sessions
    from locomo_eval import get_sorted_sessions, locomo_date_to_epoch, turns_to_text
    from locomo_eval import ANSWER_PROMPT, JUDGE_SYSTEM, JUDGE_PROMPT
    from llm_client import chat_completion, chat_completion_json, reset_token_stats, get_token_stats
    from amem_official_memory import OfficialAMemMemory
    
    sorted_sessions = get_sorted_sessions(conversation)
    
    qa_list = []
    all_qa = entry.get("qa", entry.get("qa_pairs", []))
    for i, qa in enumerate(all_qa):
        if "answer" not in qa or not qa["answer"]:
            continue
        qa_list.append((i, qa))
    
    user_id = f"locomo_amem_raw_{conv_idx}"
    
    # 每个对话独立的 A-Mem 实例
    mem = OfficialAMemMemory(db_path=os.path.join(output_dir, f"amem_raw_conv{conv_idx}.db"))
    
    print(f"[Conv {conv_idx}] {speaker_a} & {speaker_b} | {len(sorted_sessions)} sessions, {len(qa_list)} QA")
    
    # 写入记忆
    write_start = time.time()
    mem_count = 0
    for sess_idx, (session_key, date_str, turns) in enumerate(sorted_sessions):
        session_epoch = locomo_date_to_epoch(date_str) or time.time()
        date_header = f"[Conversation Date: {date_str}]\n"
        batch_size = 5
        for i in range(0, len(turns), batch_size):
            batch = turns[i:i+batch_size]
            batch_text = turns_to_text(batch, speaker_a, speaker_b)
            if batch_text.strip():
                try:
                    full_text = date_header + batch_text
                    mem.add(full_text, user_id=user_id, timestamp=session_epoch)
                    mem_count += 1
                except Exception as e:
                    print(f"  [Conv {conv_idx}] 写入失败: {e}")
    write_elapsed = time.time() - write_start
    print(f"[Conv {conv_idx}] 写入完成: {mem_count} batches, {write_elapsed:.1f}s")
    
    # 参考日期
    ref_date = sorted_sessions[-1][1] if sorted_sessions else "2023"
    
    # 答题
    conv_results = []
    conv_correct = 0
    answer_start = time.time()
    for qa_idx, (orig_idx"""
A-Mem 官方版 LoCoMo 并行测评脚本
每个对话一个进程，10个对话同时跑
"""
import json
import os
import sys
import time
import argparse
import subprocess
from pathlib import Path

def run_single_conv(conv_idx: int, dataset_path: str, output_dir: str, top_k: int):
    """单个对话的测评（子进程）"""
    # 加载数据集
    with open(dataset_path) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    
    entry = dataset[conv_idx]
    conversation = entry["conversation"]
    speaker_a = conversation["speaker_a"]
    speaker_b = conversation["speaker_b"]
    
    # 获取 sessions
    from locomo_eval import get_sorted_sessions, locomo_date_to_epoch, turns_to_text
    from locomo_eval import ANSWER_PROMPT, JUDGE_SYSTEM, JUDGE_PROMPT
    from llm_client import chat_completion, chat_completion_json, reset_token_stats, get_token_stats
    from amem_official_memory import OfficialAMemMemory
    
    sorted_sessions = get_sorted_sessions(conversation)
    
    qa_list = []
    all_qa = entry.get("qa", entry.get("qa_pairs", []))
    for i, qa in enumerate(all_qa):
        if "answer" not in qa or not qa["answer"]:
            continue
        qa_list.append((i, qa))
    
    user_id = f"locomo_amem_raw_{conv_idx}"
    
    # 每个对话独立的 A-Mem 实例
    mem = OfficialAMemMemory(db_path=os.path.join(output_dir, f"amem_raw_conv{conv_idx}.db"))
    
    print(f"[Conv {conv_idx}] {speaker_a} & {speaker_b} | {len(sorted_sessions)} sessions, {len(qa_list)} QA")
    
    # 写入记忆
    write_start = time.time()
    mem_count = 0
    for sess_idx, (session_key, date_str, turns) in enumerate(sorted_sessions):
        session_epoch = locomo_date_to_epoch(date_str) or time.time()
        date_header = f"[Conversation Date: {date_str}]\n"
        batch_size = 5
        for i in range(0, len(turns), batch_size):
            batch = turns[i:i+batch_size]
            batch_text = turns_to_text(batch, speaker_a, speaker_b)
            if batch_text.strip():
                try:
                    full_text = date_header + batch_text
                    mem.add(full_text, user_id=user_id, timestamp=session_epoch)
                    mem_count += 1
                except Exception as e:
                    print(f"  [Conv {conv_idx}] 写入失败: {e}")
    write_elapsed = time.time() - write_start
    print(f"[Conv {conv_idx}] 写入完成: {mem_count} batches, {write_elapsed:.1f}s")
    
    # 参考日期
    ref_date = sorted_sessions[-1][1] if sorted_sessions else "2023"
    
    # 答题
    conv_results = []
    conv_correct = 0
    answer_start = time.time()
    for qa_idx, (orig_idx, qa) in enumerate(qa_list):
        question = qa["question"]
        gold_answer = qa["answer"]
        category = qa.get("category", 0)
        
        # 检索"""
A-Mem 官方版 LoCoMo 并行测评脚本
每个对话一个进程，10个对话同时跑
"""
import json
import os
import sys
import time
import argparse
import subprocess
from pathlib import Path

def run_single_conv(conv_idx: int, dataset_path: str, output_dir: str, top_k: int):
    """单个对话的测评（子进程）"""
    # 加载数据集
    with open(dataset_path) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    
    entry = dataset[conv_idx]
    conversation = entry["conversation"]
    speaker_a = conversation["speaker_a"]
    speaker_b = conversation["speaker_b"]
    
    # 获取 sessions
    from locomo_eval import get_sorted_sessions, locomo_date_to_epoch, turns_to_text
    from locomo_eval import ANSWER_PROMPT, JUDGE_SYSTEM, JUDGE_PROMPT
    from llm_client import chat_completion, chat_completion_json, reset_token_stats, get_token_stats
    from amem_official_memory import OfficialAMemMemory
    
    sorted_sessions = get_sorted_sessions(conversation)
    
    qa_list = []
    all_qa = entry.get("qa", entry.get("qa_pairs", []))
    for i, qa in enumerate(all_qa):
        if "answer" not in qa or not qa["answer"]:
            continue
        qa_list.append((i, qa))
    
    user_id = f"locomo_amem_raw_{conv_idx}"
    
    # 每个对话独立的 A-Mem 实例
    mem = OfficialAMemMemory(db_path=os.path.join(output_dir, f"amem_raw_conv{conv_idx}.db"))
    
    print(f"[Conv {conv_idx}] {speaker_a} & {speaker_b} | {len(sorted_sessions)} sessions, {len(qa_list)} QA")
    
    # 写入记忆
    write_start = time.time()
    mem_count = 0
    for sess_idx, (session_key, date_str, turns) in enumerate(sorted_sessions):
        session_epoch = locomo_date_to_epoch(date_str) or time.time()
        date_header = f"[Conversation Date: {date_str}]\n"
        batch_size = 5
        for i in range(0, len(turns), batch_size):
            batch = turns[i:i+batch_size]
            batch_text = turns_to_text(batch, speaker_a, speaker_b)
            if batch_text.strip():
                try:
                    full_text = date_header + batch_text
                    mem.add(full_text, user_id=user_id, timestamp=session_epoch)
                    mem_count += 1
                except Exception as e:
                    print(f"  [Conv {conv_idx}] 写入失败: {e}")
    write_elapsed = time.time() - write_start
    print(f"[Conv {conv_idx}] 写入完成: {mem_count} batches, {write_elapsed:.1f}s")
    
    # 参考日期
    ref_date = sorted_sessions[-1][1] if sorted_sessions else "2023"
    
    # 答题
    conv_results = []
    conv_correct = 0
    answer_start = time.time()
    for qa_idx, (orig_idx, qa) in enumerate(qa_list):
        question = qa["question"]
        gold_answer = qa["answer"]
        category = qa.get("category", 0)
        
        # 检索
        try:
            search_results = mem.search(question, user_id=user_id, top_k=top_k)
            top_memories = [r.get("memory", "") for r in search_results[:top_k]]
        except Exception as e"""
A-Mem 官方版 LoCoMo 并行测评脚本
每个对话一个进程，10个对话同时跑
"""
import json
import os
import sys
import time
import argparse
import subprocess
from pathlib import Path

def run_single_conv(conv_idx: int, dataset_path: str, output_dir: str, top_k: int):
    """单个对话的测评（子进程）"""
    # 加载数据集
    with open(dataset_path) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    
    entry = dataset[conv_idx]
    conversation = entry["conversation"]
    speaker_a = conversation["speaker_a"]
    speaker_b = conversation["speaker_b"]
    
    # 获取 sessions
    from locomo_eval import get_sorted_sessions, locomo_date_to_epoch, turns_to_text
    from locomo_eval import ANSWER_PROMPT, JUDGE_SYSTEM, JUDGE_PROMPT
    from llm_client import chat_completion, chat_completion_json, reset_token_stats, get_token_stats
    from amem_official_memory import OfficialAMemMemory
    
    sorted_sessions = get_sorted_sessions(conversation)
    
    qa_list = []
    all_qa = entry.get("qa", entry.get("qa_pairs", []))
    for i, qa in enumerate(all_qa):
        if "answer" not in qa or not qa["answer"]:
            continue
        qa_list.append((i, qa))
    
    user_id = f"locomo_amem_raw_{conv_idx}"
    
    # 每个对话独立的 A-Mem 实例
    mem = OfficialAMemMemory(db_path=os.path.join(output_dir, f"amem_raw_conv{conv_idx}.db"))
    
    print(f"[Conv {conv_idx}] {speaker_a} & {speaker_b} | {len(sorted_sessions)} sessions, {len(qa_list)} QA")
    
    # 写入记忆
    write_start = time.time()
    mem_count = 0
    for sess_idx, (session_key, date_str, turns) in enumerate(sorted_sessions):
        session_epoch = locomo_date_to_epoch(date_str) or time.time()
        date_header = f"[Conversation Date: {date_str}]\n"
        batch_size = 5
        for i in range(0, len(turns), batch_size):
            batch = turns[i:i+batch_size]
            batch_text = turns_to_text(batch, speaker_a, speaker_b)
            if batch_text.strip():
                try:
                    full_text = date_header + batch_text
                    mem.add(full_text, user_id=user_id, timestamp=session_epoch)
                    mem_count += 1
                except Exception as e:
                    print(f"  [Conv {conv_idx}] 写入失败: {e}")
    write_elapsed = time.time() - write_start
    print(f"[Conv {conv_idx}] 写入完成: {mem_count} batches, {write_elapsed:.1f}s")
    
    # 参考日期
    ref_date = sorted_sessions[-1][1] if sorted_sessions else "2023"
    
    # 答题
    conv_results = []
    conv_correct = 0
    answer_start = time.time()
    for qa_idx, (orig_idx, qa) in enumerate(qa_list):
        question = qa["question"]
        gold_answer = qa["answer"]
        category = qa.get("category", 0)
        
        # 检索
        try:
            search_results = mem.search(question, user_id=user_id, top_k=top_k)
            top_memories = [r.get("memory", "") for r in search_results[:top_k]]
        except Exception as e:
            print(f"  [Conv {conv_idx}] 检索失败 Q{qa_idx}: {e}")
            top_memories = []
        
        memory_text = "\n".join([f"- {m}""""
A-Mem 官方版 LoCoMo 并行测评脚本
每个对话一个进程，10个对话同时跑
"""
import json
import os
import sys
import time
import argparse
import subprocess
from pathlib import Path

def run_single_conv(conv_idx: int, dataset_path: str, output_dir: str, top_k: int):
    """单个对话的测评（子进程）"""
    # 加载数据集
    with open(dataset_path) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    
    entry = dataset[conv_idx]
    conversation = entry["conversation"]
    speaker_a = conversation["speaker_a"]
    speaker_b = conversation["speaker_b"]
    
    # 获取 sessions
    from locomo_eval import get_sorted_sessions, locomo_date_to_epoch, turns_to_text
    from locomo_eval import ANSWER_PROMPT, JUDGE_SYSTEM, JUDGE_PROMPT
    from llm_client import chat_completion, chat_completion_json, reset_token_stats, get_token_stats
    from amem_official_memory import OfficialAMemMemory
    
    sorted_sessions = get_sorted_sessions(conversation)
    
    qa_list = []
    all_qa = entry.get("qa", entry.get("qa_pairs", []))
    for i, qa in enumerate(all_qa):
        if "answer" not in qa or not qa["answer"]:
            continue
        qa_list.append((i, qa))
    
    user_id = f"locomo_amem_raw_{conv_idx}"
    
    # 每个对话独立的 A-Mem 实例
    mem = OfficialAMemMemory(db_path=os.path.join(output_dir, f"amem_raw_conv{conv_idx}.db"))
    
    print(f"[Conv {conv_idx}] {speaker_a} & {speaker_b} | {len(sorted_sessions)} sessions, {len(qa_list)} QA")
    
    # 写入记忆
    write_start = time.time()
    mem_count = 0
    for sess_idx, (session_key, date_str, turns) in enumerate(sorted_sessions):
        session_epoch = locomo_date_to_epoch(date_str) or time.time()
        date_header = f"[Conversation Date: {date_str}]\n"
        batch_size = 5
        for i in range(0, len(turns), batch_size):
            batch = turns[i:i+batch_size]
            batch_text = turns_to_text(batch, speaker_a, speaker_b)
            if batch_text.strip():
                try:
                    full_text = date_header + batch_text
                    mem.add(full_text, user_id=user_id, timestamp=session_epoch)
                    mem_count += 1
                except Exception as e:
                    print(f"  [Conv {conv_idx}] 写入失败: {e}")
    write_elapsed = time.time() - write_start
    print(f"[Conv {conv_idx}] 写入完成: {mem_count} batches, {write_elapsed:.1f}s")
    
    # 参考日期
    ref_date = sorted_sessions[-1][1] if sorted_sessions else "2023"
    
    # 答题
    conv_results = []
    conv_correct = 0
    answer_start = time.time()
    for qa_idx, (orig_idx, qa) in enumerate(qa_list):
        question = qa["question"]
        gold_answer = qa["answer"]
        category = qa.get("category", 0)
        
        # 检索
        try:
            search_results = mem.search(question, user_id=user_id, top_k=top_k)
            top_memories = [r.get("memory", "") for r in search_results[:top_k]]
        except Exception as e:
            print(f"  [Conv {conv_idx}] 检索失败 Q{qa_idx}: {e}")
            top_memories = []
        
        memory_text = "\n".join([f"- {m}" for m in top_memories])
        
        # 生成答案
        try:
            generated = chat_completion(
                system="You are a precise question-answering assistant.",
                user=ANSWER_PROMPT.format(
                    memories="""
A-Mem 官方版 LoCoMo 并行测评脚本
每个对话一个进程，10个对话同时跑
"""
import json
import os
import sys
import time
import argparse
import subprocess
from pathlib import Path

def run_single_conv(conv_idx: int, dataset_path: str, output_dir: str, top_k: int):
    """单个对话的测评（子进程）"""
    # 加载数据集
    with open(dataset_path) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    
    entry = dataset[conv_idx]
    conversation = entry["conversation"]
    speaker_a = conversation["speaker_a"]
    speaker_b = conversation["speaker_b"]
    
    # 获取 sessions
    from locomo_eval import get_sorted_sessions, locomo_date_to_epoch, turns_to_text
    from locomo_eval import ANSWER_PROMPT, JUDGE_SYSTEM, JUDGE_PROMPT
    from llm_client import chat_completion, chat_completion_json, reset_token_stats, get_token_stats
    from amem_official_memory import OfficialAMemMemory
    
    sorted_sessions = get_sorted_sessions(conversation)
    
    qa_list = []
    all_qa = entry.get("qa", entry.get("qa_pairs", []))
    for i, qa in enumerate(all_qa):
        if "answer" not in qa or not qa["answer"]:
            continue
        qa_list.append((i, qa))
    
    user_id = f"locomo_amem_raw_{conv_idx}"
    
    # 每个对话独立的 A-Mem 实例
    mem = OfficialAMemMemory(db_path=os.path.join(output_dir, f"amem_raw_conv{conv_idx}.db"))
    
    print(f"[Conv {conv_idx}] {speaker_a} & {speaker_b} | {len(sorted_sessions)} sessions, {len(qa_list)} QA")
    
    # 写入记忆
    write_start = time.time()
    mem_count = 0
    for sess_idx, (session_key, date_str, turns) in enumerate(sorted_sessions):
        session_epoch = locomo_date_to_epoch(date_str) or time.time()
        date_header = f"[Conversation Date: {date_str}]\n"
        batch_size = 5
        for i in range(0, len(turns), batch_size):
            batch = turns[i:i+batch_size]
            batch_text = turns_to_text(batch, speaker_a, speaker_b)
            if batch_text.strip():
                try:
                    full_text = date_header + batch_text
                    mem.add(full_text, user_id=user_id, timestamp=session_epoch)
                    mem_count += 1
                except Exception as e:
                    print(f"  [Conv {conv_idx}] 写入失败: {e}")
    write_elapsed = time.time() - write_start
    print(f"[Conv {conv_idx}] 写入完成: {mem_count} batches, {write_elapsed:.1f}s")
    
    # 参考日期
    ref_date = sorted_sessions[-1][1] if sorted_sessions else "2023"
    
    # 答题
    conv_results = []
    conv_correct = 0
    answer_start = time.time()
    for qa_idx, (orig_idx, qa) in enumerate(qa_list):
        question = qa["question"]
        gold_answer = qa["answer"]
        category = qa.get("category", 0)
        
        # 检索
        try:
            search_results = mem.search(question, user_id=user_id, top_k=top_k)
            top_memories = [r.get("memory", "") for r in search_results[:top_k]]
        except Exception as e:
            print(f"  [Conv {conv_idx}] 检索失败 Q{qa_idx}: {e}")
            top_memories = []
        
        memory_text = "\n".join([f"- {m}" for m in top_memories])
        
        # 生成答案
        try:
            generated = chat_completion(
                system="You are a precise question-answering assistant.",
                user=ANSWER_PROMPT.format(
                    memories=memory_text[:8000],
                    question=question,
                    reference_date=ref_date
                ),
                temperature=0.1,
            )
            generated = generated.strip()
        except Exception as e:
            generated = ""
        
        #"""
A-Mem 官方版 LoCoMo 并行测评脚本
每个对话一个进程，10个对话同时跑
"""
import json
import os
import sys
import time
import argparse
import subprocess
from pathlib import Path

def run_single_conv(conv_idx: int, dataset_path: str, output_dir: str, top_k: int):
    """单个对话的测评（子进程）"""
    # 加载数据集
    with open(dataset_path) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    
    entry = dataset[conv_idx]
    conversation = entry["conversation"]
    speaker_a = conversation["speaker_a"]
    speaker_b = conversation["speaker_b"]
    
    # 获取 sessions
    from locomo_eval import get_sorted_sessions, locomo_date_to_epoch, turns_to_text
    from locomo_eval import ANSWER_PROMPT, JUDGE_SYSTEM, JUDGE_PROMPT
    from llm_client import chat_completion, chat_completion_json, reset_token_stats, get_token_stats
    from amem_official_memory import OfficialAMemMemory
    
    sorted_sessions = get_sorted_sessions(conversation)
    
    qa_list = []
    all_qa = entry.get("qa", entry.get("qa_pairs", []))
    for i, qa in enumerate(all_qa):
        if "answer" not in qa or not qa["answer"]:
            continue
        qa_list.append((i, qa))
    
    user_id = f"locomo_amem_raw_{conv_idx}"
    
    # 每个对话独立的 A-Mem 实例
    mem = OfficialAMemMemory(db_path=os.path.join(output_dir, f"amem_raw_conv{conv_idx}.db"))
    
    print(f"[Conv {conv_idx}] {speaker_a} & {speaker_b} | {len(sorted_sessions)} sessions, {len(qa_list)} QA")
    
    # 写入记忆
    write_start = time.time()
    mem_count = 0
    for sess_idx, (session_key, date_str, turns) in enumerate(sorted_sessions):
        session_epoch = locomo_date_to_epoch(date_str) or time.time()
        date_header = f"[Conversation Date: {date_str}]\n"
        batch_size = 5
        for i in range(0, len(turns), batch_size):
            batch = turns[i:i+batch_size]
            batch_text = turns_to_text(batch, speaker_a, speaker_b)
            if batch_text.strip():
                try:
                    full_text = date_header + batch_text
                    mem.add(full_text, user_id=user_id, timestamp=session_epoch)
                    mem_count += 1
                except Exception as e:
                    print(f"  [Conv {conv_idx}] 写入失败: {e}")
    write_elapsed = time.time() - write_start
    print(f"[Conv {conv_idx}] 写入完成: {mem_count} batches, {write_elapsed:.1f}s")
    
    # 参考日期
    ref_date = sorted_sessions[-1][1] if sorted_sessions else "2023"
    
    # 答题
    conv_results = []
    conv_correct = 0
    answer_start = time.time()
    for qa_idx, (orig_idx, qa) in enumerate(qa_list):
        question = qa["question"]
        gold_answer = qa["answer"]
        category = qa.get("category", 0)
        
        # 检索
        try:
            search_results = mem.search(question, user_id=user_id, top_k=top_k)
            top_memories = [r.get("memory", "") for r in search_results[:top_k]]
        except Exception as e:
            print(f"  [Conv {conv_idx}] 检索失败 Q{qa_idx}: {e}")
            top_memories = []
        
        memory_text = "\n".join([f"- {m}" for m in top_memories])
        
        # 生成答案
        try:
            generated = chat_completion(
                system="You are a precise question-answering assistant.",
                user=ANSWER_PROMPT.format(
                    memories=memory_text[:8000],
                    question=question,
                    reference_date=ref_date
                ),
                temperature=0.1,
            )
            generated = generated.strip()
        except Exception as e:
            generated = ""
        
        # 裁判评分
        result = chat_completion_json(
            system=JUDGE_SYSTEM,
            user=JUDGE_PROMPT.format(
                question=question,
                gold_answer=gold_answer,
                generated_answer=generated"""
A-Mem 官方版 LoCoMo 并行测评脚本
每个对话一个进程，10个对话同时跑
"""
import json
import os
import sys
import time
import argparse
import subprocess
from pathlib import Path

def run_single_conv(conv_idx: int, dataset_path: str, output_dir: str, top_k: int):
    """单个对话的测评（子进程）"""
    # 加载数据集
    with open(dataset_path) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    
    entry = dataset[conv_idx]
    conversation = entry["conversation"]
    speaker_a = conversation["speaker_a"]
    speaker_b = conversation["speaker_b"]
    
    # 获取 sessions
    from locomo_eval import get_sorted_sessions, locomo_date_to_epoch, turns_to_text
    from locomo_eval import ANSWER_PROMPT, JUDGE_SYSTEM, JUDGE_PROMPT
    from llm_client import chat_completion, chat_completion_json, reset_token_stats, get_token_stats
    from amem_official_memory import OfficialAMemMemory
    
    sorted_sessions = get_sorted_sessions(conversation)
    
    qa_list = []
    all_qa = entry.get("qa", entry.get("qa_pairs", []))
    for i, qa in enumerate(all_qa):
        if "answer" not in qa or not qa["answer"]:
            continue
        qa_list.append((i, qa))
    
    user_id = f"locomo_amem_raw_{conv_idx}"
    
    # 每个对话独立的 A-Mem 实例
    mem = OfficialAMemMemory(db_path=os.path.join(output_dir, f"amem_raw_conv{conv_idx}.db"))
    
    print(f"[Conv {conv_idx}] {speaker_a} & {speaker_b} | {len(sorted_sessions)} sessions, {len(qa_list)} QA")
    
    # 写入记忆
    write_start = time.time()
    mem_count = 0
    for sess_idx, (session_key, date_str, turns) in enumerate(sorted_sessions):
        session_epoch = locomo_date_to_epoch(date_str) or time.time()
        date_header = f"[Conversation Date: {date_str}]\n"
        batch_size = 5
        for i in range(0, len(turns), batch_size):
            batch = turns[i:i+batch_size]
            batch_text = turns_to_text(batch, speaker_a, speaker_b)
            if batch_text.strip():
                try:
                    full_text = date_header + batch_text
                    mem.add(full_text, user_id=user_id, timestamp=session_epoch)
                    mem_count += 1
                except Exception as e:
                    print(f"  [Conv {conv_idx}] 写入失败: {e}")
    write_elapsed = time.time() - write_start
    print(f"[Conv {conv_idx}] 写入完成: {mem_count} batches, {write_elapsed:.1f}s")
    
    # 参考日期
    ref_date = sorted_sessions[-1][1] if sorted_sessions else "2023"
    
    # 答题
    conv_results = []
    conv_correct = 0
    answer_start = time.time()
    for qa_idx, (orig_idx, qa) in enumerate(qa_list):
        question = qa["question"]
        gold_answer = qa["answer"]
        category = qa.get("category", 0)
        
        # 检索
        try:
            search_results = mem.search(question, user_id=user_id, top_k=top_k)
            top_memories = [r.get("memory", "") for r in search_results[:top_k]]
        except Exception as e:
            print(f"  [Conv {conv_idx}] 检索失败 Q{qa_idx}: {e}")
            top_memories = []
        
        memory_text = "\n".join([f"- {m}" for m in top_memories])
        
        # 生成答案
        try:
            generated = chat_completion(
                system="You are a precise question-answering assistant.",
                user=ANSWER_PROMPT.format(
                    memories=memory_text[:8000],
                    question=question,
                    reference_date=ref_date
                ),
                temperature=0.1,
            )
            generated = generated.strip()
        except Exception as e:
            generated = ""
        
        # 裁判评分
        result = chat_completion_json(
            system=JUDGE_SYSTEM,
            user=JUDGE_PROMPT.format(
                question=question,
                gold_answer=gold_answer,
                generated_answer=generated
            ),
            temperature=0.1,
        )
        judgment = result.get("judgment", "INCORRECT")
        if judgment not in ("CORRECT", "INCORRECT"):
            judgment = "INCORRECT"
        
        is"""
A-Mem 官方版 LoCoMo 并行测评脚本
每个对话一个进程，10个对话同时跑
"""
import json
import os
import sys
import time
import argparse
import subprocess
from pathlib import Path

def run_single_conv(conv_idx: int, dataset_path: str, output_dir: str, top_k: int):
    """单个对话的测评（子进程）"""
    # 加载数据集
    with open(dataset_path) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    
    entry = dataset[conv_idx]
    conversation = entry["conversation"]
    speaker_a = conversation["speaker_a"]
    speaker_b = conversation["speaker_b"]
    
    # 获取 sessions
    from locomo_eval import get_sorted_sessions, locomo_date_to_epoch, turns_to_text
    from locomo_eval import ANSWER_PROMPT, JUDGE_SYSTEM, JUDGE_PROMPT
    from llm_client import chat_completion, chat_completion_json, reset_token_stats, get_token_stats
    from amem_official_memory import OfficialAMemMemory
    
    sorted_sessions = get_sorted_sessions(conversation)
    
    qa_list = []
    all_qa = entry.get("qa", entry.get("qa_pairs", []))
    for i, qa in enumerate(all_qa):
        if "answer" not in qa or not qa["answer"]:
            continue
        qa_list.append((i, qa))
    
    user_id = f"locomo_amem_raw_{conv_idx}"
    
    # 每个对话独立的 A-Mem 实例
    mem = OfficialAMemMemory(db_path=os.path.join(output_dir, f"amem_raw_conv{conv_idx}.db"))
    
    print(f"[Conv {conv_idx}] {speaker_a} & {speaker_b} | {len(sorted_sessions)} sessions, {len(qa_list)} QA")
    
    # 写入记忆
    write_start = time.time()
    mem_count = 0
    for sess_idx, (session_key, date_str, turns) in enumerate(sorted_sessions):
        session_epoch = locomo_date_to_epoch(date_str) or time.time()
        date_header = f"[Conversation Date: {date_str}]\n"
        batch_size = 5
        for i in range(0, len(turns), batch_size):
            batch = turns[i:i+batch_size]
            batch_text = turns_to_text(batch, speaker_a, speaker_b)
            if batch_text.strip():
                try:
                    full_text = date_header + batch_text
                    mem.add(full_text, user_id=user_id, timestamp=session_epoch)
                    mem_count += 1
                except Exception as e:
                    print(f"  [Conv {conv_idx}] 写入失败: {e}")
    write_elapsed = time.time() - write_start
    print(f"[Conv {conv_idx}] 写入完成: {mem_count} batches, {write_elapsed:.1f}s")
    
    # 参考日期
    ref_date = sorted_sessions[-1][1] if sorted_sessions else "2023"
    
    # 答题
    conv_results = []
    conv_correct = 0
    answer_start = time.time()
    for qa_idx, (orig_idx, qa) in enumerate(qa_list):
        question = qa["question"]
        gold_answer = qa["answer"]
        category = qa.get("category", 0)
        
        # 检索
        try:
            search_results = mem.search(question, user_id=user_id, top_k=top_k)
            top_memories = [r.get("memory", "") for r in search_results[:top_k]]
        except Exception as e:
            print(f"  [Conv {conv_idx}] 检索失败 Q{qa_idx}: {e}")
            top_memories = []
        
        memory_text = "\n".join([f"- {m}" for m in top_memories])
        
        # 生成答案
        try:
            generated = chat_completion(
                system="You are a precise question-answering assistant.",
                user=ANSWER_PROMPT.format(
                    memories=memory_text[:8000],
                    question=question,
                    reference_date=ref_date
                ),
                temperature=0.1,
            )
            generated = generated.strip()
        except Exception as e:
            generated = ""
        
        # 裁判评分
        result = chat_completion_json(
            system=JUDGE_SYSTEM,
            user=JUDGE_PROMPT.format(
                question=question,
                gold_answer=gold_answer,
                generated_answer=generated
            ),
            temperature=0.1,
        )
        judgment = result.get("judgment", "INCORRECT")
        if judgment not in ("CORRECT", "INCORRECT"):
            judgment = "INCORRECT"
        
        is_correct = judgment == "CORRECT"
        if is_correct:
            conv_correct += 1
        
        conv_results.append({
            "conversation_idx": conv_idx,
            "qa_idx": orig_idx,
            "question": question,"""
A-Mem 官方版 LoCoMo 并行测评脚本
每个对话一个进程，10个对话同时跑
"""
import json
import os
import sys
import time
import argparse
import subprocess
from pathlib import Path

def run_single_conv(conv_idx: int, dataset_path: str, output_dir: str, top_k: int):
    """单个对话的测评（子进程）"""
    # 加载数据集
    with open(dataset_path) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    
    entry = dataset[conv_idx]
    conversation = entry["conversation"]
    speaker_a = conversation["speaker_a"]
    speaker_b = conversation["speaker_b"]
    
    # 获取 sessions
    from locomo_eval import get_sorted_sessions, locomo_date_to_epoch, turns_to_text
    from locomo_eval import ANSWER_PROMPT, JUDGE_SYSTEM, JUDGE_PROMPT
    from llm_client import chat_completion, chat_completion_json, reset_token_stats, get_token_stats
    from amem_official_memory import OfficialAMemMemory
    
    sorted_sessions = get_sorted_sessions(conversation)
    
    qa_list = []
    all_qa = entry.get("qa", entry.get("qa_pairs", []))
    for i, qa in enumerate(all_qa):
        if "answer" not in qa or not qa["answer"]:
            continue
        qa_list.append((i, qa))
    
    user_id = f"locomo_amem_raw_{conv_idx}"
    
    # 每个对话独立的 A-Mem 实例
    mem = OfficialAMemMemory(db_path=os.path.join(output_dir, f"amem_raw_conv{conv_idx}.db"))
    
    print(f"[Conv {conv_idx}] {speaker_a} & {speaker_b} | {len(sorted_sessions)} sessions, {len(qa_list)} QA")
    
    # 写入记忆
    write_start = time.time()
    mem_count = 0
    for sess_idx, (session_key, date_str, turns) in enumerate(sorted_sessions):
        session_epoch = locomo_date_to_epoch(date_str) or time.time()
        date_header = f"[Conversation Date: {date_str}]\n"
        batch_size = 5
        for i in range(0, len(turns), batch_size):
            batch = turns[i:i+batch_size]
            batch_text = turns_to_text(batch, speaker_a, speaker_b)
            if batch_text.strip():
                try:
                    full_text = date_header + batch_text
                    mem.add(full_text, user_id=user_id, timestamp=session_epoch)
                    mem_count += 1
                except Exception as e:
                    print(f"  [Conv {conv_idx}] 写入失败: {e}")
    write_elapsed = time.time() - write_start
    print(f"[Conv {conv_idx}] 写入完成: {mem_count} batches, {write_elapsed:.1f}s")
    
    # 参考日期
    ref_date = sorted_sessions[-1][1] if sorted_sessions else "2023"
    
    # 答题
    conv_results = []
    conv_correct = 0
    answer_start = time.time()
    for qa_idx, (orig_idx, qa) in enumerate(qa_list):
        question = qa["question"]
        gold_answer = qa["answer"]
        category = qa.get("category", 0)
        
        # 检索
        try:
            search_results = mem.search(question, user_id=user_id, top_k=top_k)
            top_memories = [r.get("memory", "") for r in search_results[:top_k]]
        except Exception as e:
            print(f"  [Conv {conv_idx}] 检索失败 Q{qa_idx}: {e}")
            top_memories = []
        
        memory_text = "\n".join([f"- {m}" for m in top_memories])
        
        # 生成答案
        try:
            generated = chat_completion(
                system="You are a precise question-answering assistant.",
                user=ANSWER_PROMPT.format(
                    memories=memory_text[:8000],
                    question=question,
                    reference_date=ref_date
                ),
                temperature=0.1,
            )
            generated = generated.strip()
        except Exception as e:
            generated = ""
        
        # 裁判评分
        result = chat_completion_json(
            system=JUDGE_SYSTEM,
            user=JUDGE_PROMPT.format(
                question=question,
                gold_answer=gold_answer,
                generated_answer=generated
            ),
            temperature=0.1,
        )
        judgment = result.get("judgment", "INCORRECT")
        if judgment not in ("CORRECT", "INCORRECT"):
            judgment = "INCORRECT"
        
        is_correct = judgment == "CORRECT"
        if is_correct:
            conv_correct += 1
        
        conv_results.append({
            "conversation_idx": conv_idx,
            "qa_idx": orig_idx,
            "question": question,
            "gold_answer": gold_answer,
            "generated_answer": generated,
            "judgment": judgment,
            "judge_reason": result.get("reason", ""),
            "category": category,
            "top_memories": top_memories[:5"""
A-Mem 官方版 LoCoMo 并行测评脚本
每个对话一个进程，10个对话同时跑
"""
import json
import os
import sys
import time
import argparse
import subprocess
from pathlib import Path

def run_single_conv(conv_idx: int, dataset_path: str, output_dir: str, top_k: int):
    """单个对话的测评（子进程）"""
    # 加载数据集
    with open(dataset_path) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    
    entry = dataset[conv_idx]
    conversation = entry["conversation"]
    speaker_a = conversation["speaker_a"]
    speaker_b = conversation["speaker_b"]
    
    # 获取 sessions
    from locomo_eval import get_sorted_sessions, locomo_date_to_epoch, turns_to_text
    from locomo_eval import ANSWER_PROMPT, JUDGE_SYSTEM, JUDGE_PROMPT
    from llm_client import chat_completion, chat_completion_json, reset_token_stats, get_token_stats
    from amem_official_memory import OfficialAMemMemory
    
    sorted_sessions = get_sorted_sessions(conversation)
    
    qa_list = []
    all_qa = entry.get("qa", entry.get("qa_pairs", []))
    for i, qa in enumerate(all_qa):
        if "answer" not in qa or not qa["answer"]:
            continue
        qa_list.append((i, qa))
    
    user_id = f"locomo_amem_raw_{conv_idx}"
    
    # 每个对话独立的 A-Mem 实例
    mem = OfficialAMemMemory(db_path=os.path.join(output_dir, f"amem_raw_conv{conv_idx}.db"))
    
    print(f"[Conv {conv_idx}] {speaker_a} & {speaker_b} | {len(sorted_sessions)} sessions, {len(qa_list)} QA")
    
    # 写入记忆
    write_start = time.time()
    mem_count = 0
    for sess_idx, (session_key, date_str, turns) in enumerate(sorted_sessions):
        session_epoch = locomo_date_to_epoch(date_str) or time.time()
        date_header = f"[Conversation Date: {date_str}]\n"
        batch_size = 5
        for i in range(0, len(turns), batch_size):
            batch = turns[i:i+batch_size]
            batch_text = turns_to_text(batch, speaker_a, speaker_b)
            if batch_text.strip():
                try:
                    full_text = date_header + batch_text
                    mem.add(full_text, user_id=user_id, timestamp=session_epoch)
                    mem_count += 1
                except Exception as e:
                    print(f"  [Conv {conv_idx}] 写入失败: {e}")
    write_elapsed = time.time() - write_start
    print(f"[Conv {conv_idx}] 写入完成: {mem_count} batches, {write_elapsed:.1f}s")
    
    # 参考日期
    ref_date = sorted_sessions[-1][1] if sorted_sessions else "2023"
    
    # 答题
    conv_results = []
    conv_correct = 0
    answer_start = time.time()
    for qa_idx, (orig_idx, qa) in enumerate(qa_list):
        question = qa["question"]
        gold_answer = qa["answer"]
        category = qa.get("category", 0)
        
        # 检索
        try:
            search_results = mem.search(question, user_id=user_id, top_k=top_k)
            top_memories = [r.get("memory", "") for r in search_results[:top_k]]
        except Exception as e:
            print(f"  [Conv {conv_idx}] 检索失败 Q{qa_idx}: {e}")
            top_memories = []
        
        memory_text = "\n".join([f"- {m}" for m in top_memories])
        
        # 生成答案
        try:
            generated = chat_completion(
                system="You are a precise question-answering assistant.",
                user=ANSWER_PROMPT.format(
                    memories=memory_text[:8000],
                    question=question,
                    reference_date=ref_date
                ),
                temperature=0.1,
            )
            generated = generated.strip()
        except Exception as e:
            generated = ""
        
        # 裁判评分
        result = chat_completion_json(
            system=JUDGE_SYSTEM,
            user=JUDGE_PROMPT.format(
                question=question,
                gold_answer=gold_answer,
                generated_answer=generated
            ),
            temperature=0.1,
        )
        judgment = result.get("judgment", "INCORRECT")
        if judgment not in ("CORRECT", "INCORRECT"):
            judgment = "INCORRECT"
        
        is_correct = judgment == "CORRECT"
        if is_correct:
            conv_correct += 1
        
        conv_results.append({
            "conversation_idx": conv_idx,
            "qa_idx": orig_idx,
            "question": question,
            "gold_answer": gold_answer,
            "generated_answer": generated,
            "judgment": judgment,
            "judge_reason": result.get("reason", ""),
            "category": category,
            "top_memories": top_memories[:5],
        })
        
        if (qa_idx + 1) % 20 == 0:
            acc_so_far = conv_correct / (qa_idx + 1) * 100"""
A-Mem 官方版 LoCoMo 并行测评脚本
每个对话一个进程，10个对话同时跑
"""
import json
import os
import sys
import time
import argparse
import subprocess
from pathlib import Path

def run_single_conv(conv_idx: int, dataset_path: str, output_dir: str, top_k: int):
    """单个对话的测评（子进程）"""
    # 加载数据集
    with open(dataset_path) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    
    entry = dataset[conv_idx]
    conversation = entry["conversation"]
    speaker_a = conversation["speaker_a"]
    speaker_b = conversation["speaker_b"]
    
    # 获取 sessions
    from locomo_eval import get_sorted_sessions, locomo_date_to_epoch, turns_to_text
    from locomo_eval import ANSWER_PROMPT, JUDGE_SYSTEM, JUDGE_PROMPT
    from llm_client import chat_completion, chat_completion_json, reset_token_stats, get_token_stats
    from amem_official_memory import OfficialAMemMemory
    
    sorted_sessions = get_sorted_sessions(conversation)
    
    qa_list = []
    all_qa = entry.get("qa", entry.get("qa_pairs", []))
    for i, qa in enumerate(all_qa):
        if "answer" not in qa or not qa["answer"]:
            continue
        qa_list.append((i, qa))
    
    user_id = f"locomo_amem_raw_{conv_idx}"
    
    # 每个对话独立的 A-Mem 实例
    mem = OfficialAMemMemory(db_path=os.path.join(output_dir, f"amem_raw_conv{conv_idx}.db"))
    
    print(f"[Conv {conv_idx}] {speaker_a} & {speaker_b} | {len(sorted_sessions)} sessions, {len(qa_list)} QA")
    
    # 写入记忆
    write_start = time.time()
    mem_count = 0
    for sess_idx, (session_key, date_str, turns) in enumerate(sorted_sessions):
        session_epoch = locomo_date_to_epoch(date_str) or time.time()
        date_header = f"[Conversation Date: {date_str}]\n"
        batch_size = 5
        for i in range(0, len(turns), batch_size):
            batch = turns[i:i+batch_size]
            batch_text = turns_to_text(batch, speaker_a, speaker_b)
            if batch_text.strip():
                try:
                    full_text = date_header + batch_text
                    mem.add(full_text, user_id=user_id, timestamp=session_epoch)
                    mem_count += 1
                except Exception as e:
                    print(f"  [Conv {conv_idx}] 写入失败: {e}")
    write_elapsed = time.time() - write_start
    print(f"[Conv {conv_idx}] 写入完成: {mem_count} batches, {write_elapsed:.1f}s")
    
    # 参考日期
    ref_date = sorted_sessions[-1][1] if sorted_sessions else "2023"
    
    # 答题
    conv_results = []
    conv_correct = 0
    answer_start = time.time()
    for qa_idx, (orig_idx, qa) in enumerate(qa_list):
        question = qa["question"]
        gold_answer = qa["answer"]
        category = qa.get("category", 0)
        
        # 检索
        try:
            search_results = mem.search(question, user_id=user_id, top_k=top_k)
            top_memories = [r.get("memory", "") for r in search_results[:top_k]]
        except Exception as e:
            print(f"  [Conv {conv_idx}] 检索失败 Q{qa_idx}: {e}")
            top_memories = []
        
        memory_text = "\n".join([f"- {m}" for m in top_memories])
        
        # 生成答案
        try:
            generated = chat_completion(
                system="You are a precise question-answering assistant.",
                user=ANSWER_PROMPT.format(
                    memories=memory_text[:8000],
                    question=question,
                    reference_date=ref_date
                ),
                temperature=0.1,
            )
            generated = generated.strip()
        except Exception as e:
            generated = ""
        
        # 裁判评分
        result = chat_completion_json(
            system=JUDGE_SYSTEM,
            user=JUDGE_PROMPT.format(
                question=question,
                gold_answer=gold_answer,
                generated_answer=generated
            ),
            temperature=0.1,
        )
        judgment = result.get("judgment", "INCORRECT")
        if judgment not in ("CORRECT", "INCORRECT"):
            judgment = "INCORRECT"
        
        is_correct = judgment == "CORRECT"
        if is_correct:
            conv_correct += 1
        
        conv_results.append({
            "conversation_idx": conv_idx,
            "qa_idx": orig_idx,
            "question": question,
            "gold_answer": gold_answer,
            "generated_answer": generated,
            "judgment": judgment,
            "judge_reason": result.get("reason", ""),
            "category": category,
            "top_memories": top_memories[:5],
        })
        
        if (qa_idx + 1) % 20 == 0:
            acc_so_far = conv_correct / (qa_idx + 1) * 100
            print(f"  [Conv {conv_idx}] Q{qa_idx+1}/{len(qa_list)} | acc={acc_so_far:.1f}"""
A-Mem 官方版 LoCoMo 并行测评脚本
每个对话一个进程，10个对话同时跑
"""
import json
import os
import sys
import time
import argparse
import subprocess
from pathlib import Path

def run_single_conv(conv_idx: int, dataset_path: str, output_dir: str, top_k: int):
    """单个对话的测评（子进程）"""
    # 加载数据集
    with open(dataset_path) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    
    entry = dataset[conv_idx]
    conversation = entry["conversation"]
    speaker_a = conversation["speaker_a"]
    speaker_b = conversation["speaker_b"]
    
    # 获取 sessions
    from locomo_eval import get_sorted_sessions, locomo_date_to_epoch, turns_to_text
    from locomo_eval import ANSWER_PROMPT, JUDGE_SYSTEM, JUDGE_PROMPT
    from llm_client import chat_completion, chat_completion_json, reset_token_stats, get_token_stats
    from amem_official_memory import OfficialAMemMemory
    
    sorted_sessions = get_sorted_sessions(conversation)
    
    qa_list = []
    all_qa = entry.get("qa", entry.get("qa_pairs", []))
    for i, qa in enumerate(all_qa):
        if "answer" not in qa or not qa["answer"]:
            continue
        qa_list.append((i, qa))
    
    user_id = f"locomo_amem_raw_{conv_idx}"
    
    # 每个对话独立的 A-Mem 实例
    mem = OfficialAMemMemory(db_path=os.path.join(output_dir, f"amem_raw_conv{conv_idx}.db"))
    
    print(f"[Conv {conv_idx}] {speaker_a} & {speaker_b} | {len(sorted_sessions)} sessions, {len(qa_list)} QA")
    
    # 写入记忆
    write_start = time.time()
    mem_count = 0
    for sess_idx, (session_key, date_str, turns) in enumerate(sorted_sessions):
        session_epoch = locomo_date_to_epoch(date_str) or time.time()
        date_header = f"[Conversation Date: {date_str}]\n"
        batch_size = 5
        for i in range(0, len(turns), batch_size):
            batch = turns[i:i+batch_size]
            batch_text = turns_to_text(batch, speaker_a, speaker_b)
            if batch_text.strip():
                try:
                    full_text = date_header + batch_text
                    mem.add(full_text, user_id=user_id, timestamp=session_epoch)
                    mem_count += 1
                except Exception as e:
                    print(f"  [Conv {conv_idx}] 写入失败: {e}")
    write_elapsed = time.time() - write_start
    print(f"[Conv {conv_idx}] 写入完成: {mem_count} batches, {write_elapsed:.1f}s")
    
    # 参考日期
    ref_date = sorted_sessions[-1][1] if sorted_sessions else "2023"
    
    # 答题
    conv_results = []
    conv_correct = 0
    answer_start = time.time()
    for qa_idx, (orig_idx, qa) in enumerate(qa_list):
        question = qa["question"]
        gold_answer = qa["answer"]
        category = qa.get("category", 0)
        
        # 检索
        try:
            search_results = mem.search(question, user_id=user_id, top_k=top_k)
            top_memories = [r.get("memory", "") for r in search_results[:top_k]]
        except Exception as e:
            print(f"  [Conv {conv_idx}] 检索失败 Q{qa_idx}: {e}")
            top_memories = []
        
        memory_text = "\n".join([f"- {m}" for m in top_memories])
        
        # 生成答案
        try:
            generated = chat_completion(
                system="You are a precise question-answering assistant.",
                user=ANSWER_PROMPT.format(
                    memories=memory_text[:8000],
                    question=question,
                    reference_date=ref_date
                ),
                temperature=0.1,
            )
            generated = generated.strip()
        except Exception as e:
            generated = ""
        
        # 裁判评分
        result = chat_completion_json(
            system=JUDGE_SYSTEM,
            user=JUDGE_PROMPT.format(
                question=question,
                gold_answer=gold_answer,
                generated_answer=generated
            ),
            temperature=0.1,
        )
        judgment = result.get("judgment", "INCORRECT")
        if judgment not in ("CORRECT", "INCORRECT"):
            judgment = "INCORRECT"
        
        is_correct = judgment == "CORRECT"
        if is_correct:
            conv_correct += 1
        
        conv_results.append({
            "conversation_idx": conv_idx,
            "qa_idx": orig_idx,
            "question": question,
            "gold_answer": gold_answer,
            "generated_answer": generated,
            "judgment": judgment,
            "judge_reason": result.get("reason", ""),
            "category": category,
            "top_memories": top_memories[:5],
        })
        
        if (qa_idx + 1) % 20 == 0:
            acc_so_far = conv_correct / (qa_idx + 1) * 100
            print(f"  [Conv {conv_idx}] Q{qa_idx+1}/{len(qa_list)} | acc={acc_so_far:.1f}%", flush=True)
    
    answer_elapsed = time.time() - answer_start
    acc = conv_correct / len(qa_list) * 100 if qa_list else 0
    print(f"[Conv {conv_idx}] 完成"""
A-Mem 官方版 LoCoMo 并行测评脚本
每个对话一个进程，10个对话同时跑
"""
import json
import os
import sys
import time
import argparse
import subprocess
from pathlib import Path

def run_single_conv(conv_idx: int, dataset_path: str, output_dir: str, top_k: int):
    """单个对话的测评（子进程）"""
    # 加载数据集
    with open(dataset_path) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    
    entry = dataset[conv_idx]
    conversation = entry["conversation"]
    speaker_a = conversation["speaker_a"]
    speaker_b = conversation["speaker_b"]
    
    # 获取 sessions
    from locomo_eval import get_sorted_sessions, locomo_date_to_epoch, turns_to_text
    from locomo_eval import ANSWER_PROMPT, JUDGE_SYSTEM, JUDGE_PROMPT
    from llm_client import chat_completion, chat_completion_json, reset_token_stats, get_token_stats
    from amem_official_memory import OfficialAMemMemory
    
    sorted_sessions = get_sorted_sessions(conversation)
    
    qa_list = []
    all_qa = entry.get("qa", entry.get("qa_pairs", []))
    for i, qa in enumerate(all_qa):
        if "answer" not in qa or not qa["answer"]:
            continue
        qa_list.append((i, qa))
    
    user_id = f"locomo_amem_raw_{conv_idx}"
    
    # 每个对话独立的 A-Mem 实例
    mem = OfficialAMemMemory(db_path=os.path.join(output_dir, f"amem_raw_conv{conv_idx}.db"))
    
    print(f"[Conv {conv_idx}] {speaker_a} & {speaker_b} | {len(sorted_sessions)} sessions, {len(qa_list)} QA")
    
    # 写入记忆
    write_start = time.time()
    mem_count = 0
    for sess_idx, (session_key, date_str, turns) in enumerate(sorted_sessions):
        session_epoch = locomo_date_to_epoch(date_str) or time.time()
        date_header = f"[Conversation Date: {date_str}]\n"
        batch_size = 5
        for i in range(0, len(turns), batch_size):
            batch = turns[i:i+batch_size]
            batch_text = turns_to_text(batch, speaker_a, speaker_b)
            if batch_text.strip():
                try:
                    full_text = date_header + batch_text
                    mem.add(full_text, user_id=user_id, timestamp=session_epoch)
                    mem_count += 1
                except Exception as e:
                    print(f"  [Conv {conv_idx}] 写入失败: {e}")
    write_elapsed = time.time() - write_start
    print(f"[Conv {conv_idx}] 写入完成: {mem_count} batches, {write_elapsed:.1f}s")
    
    # 参考日期
    ref_date = sorted_sessions[-1][1] if sorted_sessions else "2023"
    
    # 答题
    conv_results = []
    conv_correct = 0
    answer_start = time.time()
    for qa_idx, (orig_idx, qa) in enumerate(qa_list):
        question = qa["question"]
        gold_answer = qa["answer"]
        category = qa.get("category", 0)
        
        # 检索
        try:
            search_results = mem.search(question, user_id=user_id, top_k=top_k)
            top_memories = [r.get("memory", "") for r in search_results[:top_k]]
        except Exception as e:
            print(f"  [Conv {conv_idx}] 检索失败 Q{qa_idx}: {e}")
            top_memories = []
        
        memory_text = "\n".join([f"- {m}" for m in top_memories])
        
        # 生成答案
        try:
            generated = chat_completion(
                system="You are a precise question-answering assistant.",
                user=ANSWER_PROMPT.format(
                    memories=memory_text[:8000],
                    question=question,
                    reference_date=ref_date
                ),
                temperature=0.1,
            )
            generated = generated.strip()
        except Exception as e:
            generated = ""
        
        # 裁判评分
        result = chat_completion_json(
            system=JUDGE_SYSTEM,
            user=JUDGE_PROMPT.format(
                question=question,
                gold_answer=gold_answer,
                generated_answer=generated
            ),
            temperature=0.1,
        )
        judgment = result.get("judgment", "INCORRECT")
        if judgment not in ("CORRECT", "INCORRECT"):
            judgment = "INCORRECT"
        
        is_correct = judgment == "CORRECT"
        if is_correct:
            conv_correct += 1
        
        conv_results.append({
            "conversation_idx": conv_idx,
            "qa_idx": orig_idx,
            "question": question,
            "gold_answer": gold_answer,
            "generated_answer": generated,
            "judgment": judgment,
            "judge_reason": result.get("reason", ""),
            "category": category,
            "top_memories": top_memories[:5],
        })
        
        if (qa_idx + 1) % 20 == 0:
            acc_so_far = conv_correct / (qa_idx + 1) * 100
            print(f"  [Conv {conv_idx}] Q{qa_idx+1}/{len(qa_list)} | acc={acc_so_far:.1f}%", flush=True)
    
    answer_elapsed = time.time() - answer_start
    acc = conv_correct / len(qa_list) * 100 if qa_list else 0
    print(f"[Conv {conv_idx}] 完成: {conv_correct}/{len(qa_list)} = {acc:.1f}% | write={write_elapsed:.0f}s answer={answer_elapsed:.0f}s")
    
    # 保存单"""
A-Mem 官方版 LoCoMo 并行测评脚本
每个对话一个进程，10个对话同时跑
"""
import json
import os
import sys
import time
import argparse
import subprocess
from pathlib import Path

def run_single_conv(conv_idx: int, dataset_path: str, output_dir: str, top_k: int):
    """单个对话的测评（子进程）"""
    # 加载数据集
    with open(dataset_path) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    
    entry = dataset[conv_idx]
    conversation = entry["conversation"]
    speaker_a = conversation["speaker_a"]
    speaker_b = conversation["speaker_b"]
    
    # 获取 sessions
    from locomo_eval import get_sorted_sessions, locomo_date_to_epoch, turns_to_text
    from locomo_eval import ANSWER_PROMPT, JUDGE_SYSTEM, JUDGE_PROMPT
    from llm_client import chat_completion, chat_completion_json, reset_token_stats, get_token_stats
    from amem_official_memory import OfficialAMemMemory
    
    sorted_sessions = get_sorted_sessions(conversation)
    
    qa_list = []
    all_qa = entry.get("qa", entry.get("qa_pairs", []))
    for i, qa in enumerate(all_qa):
        if "answer" not in qa or not qa["answer"]:
            continue
        qa_list.append((i, qa))
    
    user_id = f"locomo_amem_raw_{conv_idx}"
    
    # 每个对话独立的 A-Mem 实例
    mem = OfficialAMemMemory(db_path=os.path.join(output_dir, f"amem_raw_conv{conv_idx}.db"))
    
    print(f"[Conv {conv_idx}] {speaker_a} & {speaker_b} | {len(sorted_sessions)} sessions, {len(qa_list)} QA")
    
    # 写入记忆
    write_start = time.time()
    mem_count = 0
    for sess_idx, (session_key, date_str, turns) in enumerate(sorted_sessions):
        session_epoch = locomo_date_to_epoch(date_str) or time.time()
        date_header = f"[Conversation Date: {date_str}]\n"
        batch_size = 5
        for i in range(0, len(turns), batch_size):
            batch = turns[i:i+batch_size]
            batch_text = turns_to_text(batch, speaker_a, speaker_b)
            if batch_text.strip():
                try:
                    full_text = date_header + batch_text
                    mem.add(full_text, user_id=user_id, timestamp=session_epoch)
                    mem_count += 1
                except Exception as e:
                    print(f"  [Conv {conv_idx}] 写入失败: {e}")
    write_elapsed = time.time() - write_start
    print(f"[Conv {conv_idx}] 写入完成: {mem_count} batches, {write_elapsed:.1f}s")
    
    # 参考日期
    ref_date = sorted_sessions[-1][1] if sorted_sessions else "2023"
    
    # 答题
    conv_results = []
    conv_correct = 0
    answer_start = time.time()
    for qa_idx, (orig_idx, qa) in enumerate(qa_list):
        question = qa["question"]
        gold_answer = qa["answer"]
        category = qa.get("category", 0)
        
        # 检索
        try:
            search_results = mem.search(question, user_id=user_id, top_k=top_k)
            top_memories = [r.get("memory", "") for r in search_results[:top_k]]
        except Exception as e:
            print(f"  [Conv {conv_idx}] 检索失败 Q{qa_idx}: {e}")
            top_memories = []
        
        memory_text = "\n".join([f"- {m}" for m in top_memories])
        
        # 生成答案
        try:
            generated = chat_completion(
                system="You are a precise question-answering assistant.",
                user=ANSWER_PROMPT.format(
                    memories=memory_text[:8000],
                    question=question,
                    reference_date=ref_date
                ),
                temperature=0.1,
            )
            generated = generated.strip()
        except Exception as e:
            generated = ""
        
        # 裁判评分
        result = chat_completion_json(
            system=JUDGE_SYSTEM,
            user=JUDGE_PROMPT.format(
                question=question,
                gold_answer=gold_answer,
                generated_answer=generated
            ),
            temperature=0.1,
        )
        judgment = result.get("judgment", "INCORRECT")
        if judgment not in ("CORRECT", "INCORRECT"):
            judgment = "INCORRECT"
        
        is_correct = judgment == "CORRECT"
        if is_correct:
            conv_correct += 1
        
        conv_results.append({
            "conversation_idx": conv_idx,
            "qa_idx": orig_idx,
            "question": question,
            "gold_answer": gold_answer,
            "generated_answer": generated,
            "judgment": judgment,
            "judge_reason": result.get("reason", ""),
            "category": category,
            "top_memories": top_memories[:5],
        })
        
        if (qa_idx + 1) % 20 == 0:
            acc_so_far = conv_correct / (qa_idx + 1) * 100
            print(f"  [Conv {conv_idx}] Q{qa_idx+1}/{len(qa_list)} | acc={acc_so_far:.1f}%", flush=True)
    
    answer_elapsed = time.time() - answer_start
    acc = conv_correct / len(qa_list) * 100 if qa_list else 0
    print(f"[Conv {conv_idx}] 完成: {conv_correct}/{len(qa_list)} = {acc:.1f}% | write={write_elapsed:.0f}s answer={answer_elapsed:.0f}s")
    
    # 保存单对话结果
    result_data = {
        "conv_idx": conv_idx,
        "speaker_a": speaker_a,
        "speaker_b": speaker_b,
        "total": len(qa_list),
        "correct": conv"""
A-Mem 官方版 LoCoMo 并行测评脚本
每个对话一个进程，10个对话同时跑
"""
import json
import os
import sys
import time
import argparse
import subprocess
from pathlib import Path

def run_single_conv(conv_idx: int, dataset_path: str, output_dir: str, top_k: int):
    """单个对话的测评（子进程）"""
    # 加载数据集
    with open(dataset_path) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    
    entry = dataset[conv_idx]
    conversation = entry["conversation"]
    speaker_a = conversation["speaker_a"]
    speaker_b = conversation["speaker_b"]
    
    # 获取 sessions
    from locomo_eval import get_sorted_sessions, locomo_date_to_epoch, turns_to_text
    from locomo_eval import ANSWER_PROMPT, JUDGE_SYSTEM, JUDGE_PROMPT
    from llm_client import chat_completion, chat_completion_json, reset_token_stats, get_token_stats
    from amem_official_memory import OfficialAMemMemory
    
    sorted_sessions = get_sorted_sessions(conversation)
    
    qa_list = []
    all_qa = entry.get("qa", entry.get("qa_pairs", []))
    for i, qa in enumerate(all_qa):
        if "answer" not in qa or not qa["answer"]:
            continue
        qa_list.append((i, qa))
    
    user_id = f"locomo_amem_raw_{conv_idx}"
    
    # 每个对话独立的 A-Mem 实例
    mem = OfficialAMemMemory(db_path=os.path.join(output_dir, f"amem_raw_conv{conv_idx}.db"))
    
    print(f"[Conv {conv_idx}] {speaker_a} & {speaker_b} | {len(sorted_sessions)} sessions, {len(qa_list)} QA")
    
    # 写入记忆
    write_start = time.time()
    mem_count = 0
    for sess_idx, (session_key, date_str, turns) in enumerate(sorted_sessions):
        session_epoch = locomo_date_to_epoch(date_str) or time.time()
        date_header = f"[Conversation Date: {date_str}]\n"
        batch_size = 5
        for i in range(0, len(turns), batch_size):
            batch = turns[i:i+batch_size]
            batch_text = turns_to_text(batch, speaker_a, speaker_b)
            if batch_text.strip():
                try:
                    full_text = date_header + batch_text
                    mem.add(full_text, user_id=user_id, timestamp=session_epoch)
                    mem_count += 1
                except Exception as e:
                    print(f"  [Conv {conv_idx}] 写入失败: {e}")
    write_elapsed = time.time() - write_start
    print(f"[Conv {conv_idx}] 写入完成: {mem_count} batches, {write_elapsed:.1f}s")
    
    # 参考日期
    ref_date = sorted_sessions[-1][1] if sorted_sessions else "2023"
    
    # 答题
    conv_results = []
    conv_correct = 0
    answer_start = time.time()
    for qa_idx, (orig_idx, qa) in enumerate(qa_list):
        question = qa["question"]
        gold_answer = qa["answer"]
        category = qa.get("category", 0)
        
        # 检索
        try:
            search_results = mem.search(question, user_id=user_id, top_k=top_k)
            top_memories = [r.get("memory", "") for r in search_results[:top_k]]
        except Exception as e:
            print(f"  [Conv {conv_idx}] 检索失败 Q{qa_idx}: {e}")
            top_memories = []
        
        memory_text = "\n".join([f"- {m}" for m in top_memories])
        
        # 生成答案
        try:
            generated = chat_completion(
                system="You are a precise question-answering assistant.",
                user=ANSWER_PROMPT.format(
                    memories=memory_text[:8000],
                    question=question,
                    reference_date=ref_date
                ),
                temperature=0.1,
            )
            generated = generated.strip()
        except Exception as e:
            generated = ""
        
        # 裁判评分
        result = chat_completion_json(
            system=JUDGE_SYSTEM,
            user=JUDGE_PROMPT.format(
                question=question,
                gold_answer=gold_answer,
                generated_answer=generated
            ),
            temperature=0.1,
        )
        judgment = result.get("judgment", "INCORRECT")
        if judgment not in ("CORRECT", "INCORRECT"):
            judgment = "INCORRECT"
        
        is_correct = judgment == "CORRECT"
        if is_correct:
            conv_correct += 1
        
        conv_results.append({
            "conversation_idx": conv_idx,
            "qa_idx": orig_idx,
            "question": question,
            "gold_answer": gold_answer,
            "generated_answer": generated,
            "judgment": judgment,
            "judge_reason": result.get("reason", ""),
            "category": category,
            "top_memories": top_memories[:5],
        })
        
        if (qa_idx + 1) % 20 == 0:
            acc_so_far = conv_correct / (qa_idx + 1) * 100
            print(f"  [Conv {conv_idx}] Q{qa_idx+1}/{len(qa_list)} | acc={acc_so_far:.1f}%", flush=True)
    
    answer_elapsed = time.time() - answer_start
    acc = conv_correct / len(qa_list) * 100 if qa_list else 0
    print(f"[Conv {conv_idx}] 完成: {conv_correct}/{len(qa_list)} = {acc:.1f}% | write={write_elapsed:.0f}s answer={answer_elapsed:.0f}s")
    
    # 保存单对话结果
    result_data = {
        "conv_idx": conv_idx,
        "speaker_a": speaker_a,
        "speaker_b": speaker_b,
        "total": len(qa_list),
        "correct": conv_correct,
        "accuracy": acc,
        "write_time": write_elapsed,
        "answer_time": answer_elapsed,
        "mem_count": mem_count,
        "details": conv_results,
    }"""
A-Mem 官方版 LoCoMo 并行测评脚本
每个对话一个进程，10个对话同时跑
"""
import json
import os
import sys
import time
import argparse
import subprocess
from pathlib import Path

def run_single_conv(conv_idx: int, dataset_path: str, output_dir: str, top_k: int):
    """单个对话的测评（子进程）"""
    # 加载数据集
    with open(dataset_path) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    
    entry = dataset[conv_idx]
    conversation = entry["conversation"]
    speaker_a = conversation["speaker_a"]
    speaker_b = conversation["speaker_b"]
    
    # 获取 sessions
    from locomo_eval import get_sorted_sessions, locomo_date_to_epoch, turns_to_text
    from locomo_eval import ANSWER_PROMPT, JUDGE_SYSTEM, JUDGE_PROMPT
    from llm_client import chat_completion, chat_completion_json, reset_token_stats, get_token_stats
    from amem_official_memory import OfficialAMemMemory
    
    sorted_sessions = get_sorted_sessions(conversation)
    
    qa_list = []
    all_qa = entry.get("qa", entry.get("qa_pairs", []))
    for i, qa in enumerate(all_qa):
        if "answer" not in qa or not qa["answer"]:
            continue
        qa_list.append((i, qa))
    
    user_id = f"locomo_amem_raw_{conv_idx}"
    
    # 每个对话独立的 A-Mem 实例
    mem = OfficialAMemMemory(db_path=os.path.join(output_dir, f"amem_raw_conv{conv_idx}.db"))
    
    print(f"[Conv {conv_idx}] {speaker_a} & {speaker_b} | {len(sorted_sessions)} sessions, {len(qa_list)} QA")
    
    # 写入记忆
    write_start = time.time()
    mem_count = 0
    for sess_idx, (session_key, date_str, turns) in enumerate(sorted_sessions):
        session_epoch = locomo_date_to_epoch(date_str) or time.time()
        date_header = f"[Conversation Date: {date_str}]\n"
        batch_size = 5
        for i in range(0, len(turns), batch_size):
            batch = turns[i:i+batch_size]
            batch_text = turns_to_text(batch, speaker_a, speaker_b)
            if batch_text.strip():
                try:
                    full_text = date_header + batch_text
                    mem.add(full_text, user_id=user_id, timestamp=session_epoch)
                    mem_count += 1
                except Exception as e:
                    print(f"  [Conv {conv_idx}] 写入失败: {e}")
    write_elapsed = time.time() - write_start
    print(f"[Conv {conv_idx}] 写入完成: {mem_count} batches, {write_elapsed:.1f}s")
    
    # 参考日期
    ref_date = sorted_sessions[-1][1] if sorted_sessions else "2023"
    
    # 答题
    conv_results = []
    conv_correct = 0
    answer_start = time.time()
    for qa_idx, (orig_idx, qa) in enumerate(qa_list):
        question = qa["question"]
        gold_answer = qa["answer"]
        category = qa.get("category", 0)
        
        # 检索
        try:
            search_results = mem.search(question, user_id=user_id, top_k=top_k)
            top_memories = [r.get("memory", "") for r in search_results[:top_k]]
        except Exception as e:
            print(f"  [Conv {conv_idx}] 检索失败 Q{qa_idx}: {e}")
            top_memories = []
        
        memory_text = "\n".join([f"- {m}" for m in top_memories])
        
        # 生成答案
        try:
            generated = chat_completion(
                system="You are a precise question-answering assistant.",
                user=ANSWER_PROMPT.format(
                    memories=memory_text[:8000],
                    question=question,
                    reference_date=ref_date
                ),
                temperature=0.1,
            )
            generated = generated.strip()
        except Exception as e:
            generated = ""
        
        # 裁判评分
        result = chat_completion_json(
            system=JUDGE_SYSTEM,
            user=JUDGE_PROMPT.format(
                question=question,
                gold_answer=gold_answer,
                generated_answer=generated
            ),
            temperature=0.1,
        )
        judgment = result.get("judgment", "INCORRECT")
        if judgment not in ("CORRECT", "INCORRECT"):
            judgment = "INCORRECT"
        
        is_correct = judgment == "CORRECT"
        if is_correct:
            conv_correct += 1
        
        conv_results.append({
            "conversation_idx": conv_idx,
            "qa_idx": orig_idx,
            "question": question,
            "gold_answer": gold_answer,
            "generated_answer": generated,
            "judgment": judgment,
            "judge_reason": result.get("reason", ""),
            "category": category,
            "top_memories": top_memories[:5],
        })
        
        if (qa_idx + 1) % 20 == 0:
            acc_so_far = conv_correct / (qa_idx + 1) * 100
            print(f"  [Conv {conv_idx}] Q{qa_idx+1}/{len(qa_list)} | acc={acc_so_far:.1f}%", flush=True)
    
    answer_elapsed = time.time() - answer_start
    acc = conv_correct / len(qa_list) * 100 if qa_list else 0
    print(f"[Conv {conv_idx}] 完成: {conv_correct}/{len(qa_list)} = {acc:.1f}% | write={write_elapsed:.0f}s answer={answer_elapsed:.0f}s")
    
    # 保存单对话结果
    result_data = {
        "conv_idx": conv_idx,
        "speaker_a": speaker_a,
        "speaker_b": speaker_b,
        "total": len(qa_list),
        "correct": conv_correct,
        "accuracy": acc,
        "write_time": write_elapsed,
        "answer_time": answer_elapsed,
        "mem_count": mem_count,
        "details": conv_results,
    }
    
    result_path = os.path.join(output_dir, f"conv{conv_idx}_result.json")
    with open(result_path, 'w') as f:
        json.dump(result_data, f, indent=2"""
A-Mem 官方版 LoCoMo 并行测评脚本
每个对话一个进程，10个对话同时跑
"""
import json
import os
import sys
import time
import argparse
import subprocess
from pathlib import Path

def run_single_conv(conv_idx: int, dataset_path: str, output_dir: str, top_k: int):
    """单个对话的测评（子进程）"""
    # 加载数据集
    with open(dataset_path) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    
    entry = dataset[conv_idx]
    conversation = entry["conversation"]
    speaker_a = conversation["speaker_a"]
    speaker_b = conversation["speaker_b"]
    
    # 获取 sessions
    from locomo_eval import get_sorted_sessions, locomo_date_to_epoch, turns_to_text
    from locomo_eval import ANSWER_PROMPT, JUDGE_SYSTEM, JUDGE_PROMPT
    from llm_client import chat_completion, chat_completion_json, reset_token_stats, get_token_stats
    from amem_official_memory import OfficialAMemMemory
    
    sorted_sessions = get_sorted_sessions(conversation)
    
    qa_list = []
    all_qa = entry.get("qa", entry.get("qa_pairs", []))
    for i, qa in enumerate(all_qa):
        if "answer" not in qa or not qa["answer"]:
            continue
        qa_list.append((i, qa))
    
    user_id = f"locomo_amem_raw_{conv_idx}"
    
    # 每个对话独立的 A-Mem 实例
    mem = OfficialAMemMemory(db_path=os.path.join(output_dir, f"amem_raw_conv{conv_idx}.db"))
    
    print(f"[Conv {conv_idx}] {speaker_a} & {speaker_b} | {len(sorted_sessions)} sessions, {len(qa_list)} QA")
    
    # 写入记忆
    write_start = time.time()
    mem_count = 0
    for sess_idx, (session_key, date_str, turns) in enumerate(sorted_sessions):
        session_epoch = locomo_date_to_epoch(date_str) or time.time()
        date_header = f"[Conversation Date: {date_str}]\n"
        batch_size = 5
        for i in range(0, len(turns), batch_size):
            batch = turns[i:i+batch_size]
            batch_text = turns_to_text(batch, speaker_a, speaker_b)
            if batch_text.strip():
                try:
                    full_text = date_header + batch_text
                    mem.add(full_text, user_id=user_id, timestamp=session_epoch)
                    mem_count += 1
                except Exception as e:
                    print(f"  [Conv {conv_idx}] 写入失败: {e}")
    write_elapsed = time.time() - write_start
    print(f"[Conv {conv_idx}] 写入完成: {mem_count} batches, {write_elapsed:.1f}s")
    
    # 参考日期
    ref_date = sorted_sessions[-1][1] if sorted_sessions else "2023"
    
    # 答题
    conv_results = []
    conv_correct = 0
    answer_start = time.time()
    for qa_idx, (orig_idx, qa) in enumerate(qa_list):
        question = qa["question"]
        gold_answer = qa["answer"]
        category = qa.get("category", 0)
        
        # 检索
        try:
            search_results = mem.search(question, user_id=user_id, top_k=top_k)
            top_memories = [r.get("memory", "") for r in search_results[:top_k]]
        except Exception as e:
            print(f"  [Conv {conv_idx}] 检索失败 Q{qa_idx}: {e}")
            top_memories = []
        
        memory_text = "\n".join([f"- {m}" for m in top_memories])
        
        # 生成答案
        try:
            generated = chat_completion(
                system="You are a precise question-answering assistant.",
                user=ANSWER_PROMPT.format(
                    memories=memory_text[:8000],
                    question=question,
                    reference_date=ref_date
                ),
                temperature=0.1,
            )
            generated = generated.strip()
        except Exception as e:
            generated = ""
        
        # 裁判评分
        result = chat_completion_json(
            system=JUDGE_SYSTEM,
            user=JUDGE_PROMPT.format(
                question=question,
                gold_answer=gold_answer,
                generated_answer=generated
            ),
            temperature=0.1,
        )
        judgment = result.get("judgment", "INCORRECT")
        if judgment not in ("CORRECT", "INCORRECT"):
            judgment = "INCORRECT"
        
        is_correct = judgment == "CORRECT"
        if is_correct:
            conv_correct += 1
        
        conv_results.append({
            "conversation_idx": conv_idx,
            "qa_idx": orig_idx,
            "question": question,
            "gold_answer": gold_answer,
            "generated_answer": generated,
            "judgment": judgment,
            "judge_reason": result.get("reason", ""),
            "category": category,
            "top_memories": top_memories[:5],
        })
        
        if (qa_idx + 1) % 20 == 0:
            acc_so_far = conv_correct / (qa_idx + 1) * 100
            print(f"  [Conv {conv_idx}] Q{qa_idx+1}/{len(qa_list)} | acc={acc_so_far:.1f}%", flush=True)
    
    answer_elapsed = time.time() - answer_start
    acc = conv_correct / len(qa_list) * 100 if qa_list else 0
    print(f"[Conv {conv_idx}] 完成: {conv_correct}/{len(qa_list)} = {acc:.1f}% | write={write_elapsed:.0f}s answer={answer_elapsed:.0f}s")
    
    # 保存单对话结果
    result_data = {
        "conv_idx": conv_idx,
        "speaker_a": speaker_a,
        "speaker_b": speaker_b,
        "total": len(qa_list),
        "correct": conv_correct,
        "accuracy": acc,
        "write_time": write_elapsed,
        "answer_time": answer_elapsed,
        "mem_count": mem_count,
        "details": conv_results,
    }
    
    result_path = os.path.join(output_dir, f"conv{conv_idx}_result.json")
    with open(result_path, 'w') as f:
        json.dump(result_data, f, indent=2, ensure_ascii=False)
    
    mem.close()
    return result_data


def merge_results(output_dir: str, num_convs: int):
    """合并所有对话"""
A-Mem 官方版 LoCoMo 并行测评脚本
每个对话一个进程，10个对话同时跑
"""
import json
import os
import sys
import time
import argparse
import subprocess
from pathlib import Path

def run_single_conv(conv_idx: int, dataset_path: str, output_dir: str, top_k: int):
    """单个对话的测评（子进程）"""
    # 加载数据集
    with open(dataset_path) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    
    entry = dataset[conv_idx]
    conversation = entry["conversation"]
    speaker_a = conversation["speaker_a"]
    speaker_b = conversation["speaker_b"]
    
    # 获取 sessions
    from locomo_eval import get_sorted_sessions, locomo_date_to_epoch, turns_to_text
    from locomo_eval import ANSWER_PROMPT, JUDGE_SYSTEM, JUDGE_PROMPT
    from llm_client import chat_completion, chat_completion_json, reset_token_stats, get_token_stats
    from amem_official_memory import OfficialAMemMemory
    
    sorted_sessions = get_sorted_sessions(conversation)
    
    qa_list = []
    all_qa = entry.get("qa", entry.get("qa_pairs", []))
    for i, qa in enumerate(all_qa):
        if "answer" not in qa or not qa["answer"]:
            continue
        qa_list.append((i, qa))
    
    user_id = f"locomo_amem_raw_{conv_idx}"
    
    # 每个对话独立的 A-Mem 实例
    mem = OfficialAMemMemory(db_path=os.path.join(output_dir, f"amem_raw_conv{conv_idx}.db"))
    
    print(f"[Conv {conv_idx}] {speaker_a} & {speaker_b} | {len(sorted_sessions)} sessions, {len(qa_list)} QA")
    
    # 写入记忆
    write_start = time.time()
    mem_count = 0
    for sess_idx, (session_key, date_str, turns) in enumerate(sorted_sessions):
        session_epoch = locomo_date_to_epoch(date_str) or time.time()
        date_header = f"[Conversation Date: {date_str}]\n"
        batch_size = 5
        for i in range(0, len(turns), batch_size):
            batch = turns[i:i+batch_size]
            batch_text = turns_to_text(batch, speaker_a, speaker_b)
            if batch_text.strip():
                try:
                    full_text = date_header + batch_text
                    mem.add(full_text, user_id=user_id, timestamp=session_epoch)
                    mem_count += 1
                except Exception as e:
                    print(f"  [Conv {conv_idx}] 写入失败: {e}")
    write_elapsed = time.time() - write_start
    print(f"[Conv {conv_idx}] 写入完成: {mem_count} batches, {write_elapsed:.1f}s")
    
    # 参考日期
    ref_date = sorted_sessions[-1][1] if sorted_sessions else "2023"
    
    # 答题
    conv_results = []
    conv_correct = 0
    answer_start = time.time()
    for qa_idx, (orig_idx, qa) in enumerate(qa_list):
        question = qa["question"]
        gold_answer = qa["answer"]
        category = qa.get("category", 0)
        
        # 检索
        try:
            search_results = mem.search(question, user_id=user_id, top_k=top_k)
            top_memories = [r.get("memory", "") for r in search_results[:top_k]]
        except Exception as e:
            print(f"  [Conv {conv_idx}] 检索失败 Q{qa_idx}: {e}")
            top_memories = []
        
        memory_text = "\n".join([f"- {m}" for m in top_memories])
        
        # 生成答案
        try:
            generated = chat_completion(
                system="You are a precise question-answering assistant.",
                user=ANSWER_PROMPT.format(
                    memories=memory_text[:8000],
                    question=question,
                    reference_date=ref_date
                ),
                temperature=0.1,
            )
            generated = generated.strip()
        except Exception as e:
            generated = ""
        
        # 裁判评分
        result = chat_completion_json(
            system=JUDGE_SYSTEM,
            user=JUDGE_PROMPT.format(
                question=question,
                gold_answer=gold_answer,
                generated_answer=generated
            ),
            temperature=0.1,
        )
        judgment = result.get("judgment", "INCORRECT")
        if judgment not in ("CORRECT", "INCORRECT"):
            judgment = "INCORRECT"
        
        is_correct = judgment == "CORRECT"
        if is_correct:
            conv_correct += 1
        
        conv_results.append({
            "conversation_idx": conv_idx,
            "qa_idx": orig_idx,
            "question": question,
            "gold_answer": gold_answer,
            "generated_answer": generated,
            "judgment": judgment,
            "judge_reason": result.get("reason", ""),
            "category": category,
            "top_memories": top_memories[:5],
        })
        
        if (qa_idx + 1) % 20 == 0:
            acc_so_far = conv_correct / (qa_idx + 1) * 100
            print(f"  [Conv {conv_idx}] Q{qa_idx+1}/{len(qa_list)} | acc={acc_so_far:.1f}%", flush=True)
    
    answer_elapsed = time.time() - answer_start
    acc = conv_correct / len(qa_list) * 100 if qa_list else 0
    print(f"[Conv {conv_idx}] 完成: {conv_correct}/{len(qa_list)} = {acc:.1f}% | write={write_elapsed:.0f}s answer={answer_elapsed:.0f}s")
    
    # 保存单对话结果
    result_data = {
        "conv_idx": conv_idx,
        "speaker_a": speaker_a,
        "speaker_b": speaker_b,
        "total": len(qa_list),
        "correct": conv_correct,
        "accuracy": acc,
        "write_time": write_elapsed,
        "answer_time": answer_elapsed,
        "mem_count": mem_count,
        "details": conv_results,
    }
    
    result_path = os.path.join(output_dir, f"conv{conv_idx}_result.json")
    with open(result_path, 'w') as f:
        json.dump(result_data, f, indent=2, ensure_ascii=False)
    
    mem.close()
    return result_data


def merge_results(output_dir: str, num_convs: int):
    """合并所有对话结果"""
    all_details = []
    total_q = 0
    total_correct = 0
    from collections import defaultdict
    category_stats = defaultdict(lambda: {"total":"""
A-Mem 官方版 LoCoMo 并行测评脚本
每个对话一个进程，10个对话同时跑
"""
import json
import os
import sys
import time
import argparse
import subprocess
from pathlib import Path

def run_single_conv(conv_idx: int, dataset_path: str, output_dir: str, top_k: int):
    """单个对话的测评（子进程）"""
    # 加载数据集
    with open(dataset_path) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    
    entry = dataset[conv_idx]
    conversation = entry["conversation"]
    speaker_a = conversation["speaker_a"]
    speaker_b = conversation["speaker_b"]
    
    # 获取 sessions
    from locomo_eval import get_sorted_sessions, locomo_date_to_epoch, turns_to_text
    from locomo_eval import ANSWER_PROMPT, JUDGE_SYSTEM, JUDGE_PROMPT
    from llm_client import chat_completion, chat_completion_json, reset_token_stats, get_token_stats
    from amem_official_memory import OfficialAMemMemory
    
    sorted_sessions = get_sorted_sessions(conversation)
    
    qa_list = []
    all_qa = entry.get("qa", entry.get("qa_pairs", []))
    for i, qa in enumerate(all_qa):
        if "answer" not in qa or not qa["answer"]:
            continue
        qa_list.append((i, qa))
    
    user_id = f"locomo_amem_raw_{conv_idx}"
    
    # 每个对话独立的 A-Mem 实例
    mem = OfficialAMemMemory(db_path=os.path.join(output_dir, f"amem_raw_conv{conv_idx}.db"))
    
    print(f"[Conv {conv_idx}] {speaker_a} & {speaker_b} | {len(sorted_sessions)} sessions, {len(qa_list)} QA")
    
    # 写入记忆
    write_start = time.time()
    mem_count = 0
    for sess_idx, (session_key, date_str, turns) in enumerate(sorted_sessions):
        session_epoch = locomo_date_to_epoch(date_str) or time.time()
        date_header = f"[Conversation Date: {date_str}]\n"
        batch_size = 5
        for i in range(0, len(turns), batch_size):
            batch = turns[i:i+batch_size]
            batch_text = turns_to_text(batch, speaker_a, speaker_b)
            if batch_text.strip():
                try:
                    full_text = date_header + batch_text
                    mem.add(full_text, user_id=user_id, timestamp=session_epoch)
                    mem_count += 1
                except Exception as e:
                    print(f"  [Conv {conv_idx}] 写入失败: {e}")
    write_elapsed = time.time() - write_start
    print(f"[Conv {conv_idx}] 写入完成: {mem_count} batches, {write_elapsed:.1f}s")
    
    # 参考日期
    ref_date = sorted_sessions[-1][1] if sorted_sessions else "2023"
    
    # 答题
    conv_results = []
    conv_correct = 0
    answer_start = time.time()
    for qa_idx, (orig_idx, qa) in enumerate(qa_list):
        question = qa["question"]
        gold_answer = qa["answer"]
        category = qa.get("category", 0)
        
        # 检索
        try:
            search_results = mem.search(question, user_id=user_id, top_k=top_k)
            top_memories = [r.get("memory", "") for r in search_results[:top_k]]
        except Exception as e:
            print(f"  [Conv {conv_idx}] 检索失败 Q{qa_idx}: {e}")
            top_memories = []
        
        memory_text = "\n".join([f"- {m}" for m in top_memories])
        
        # 生成答案
        try:
            generated = chat_completion(
                system="You are a precise question-answering assistant.",
                user=ANSWER_PROMPT.format(
                    memories=memory_text[:8000],
                    question=question,
                    reference_date=ref_date
                ),
                temperature=0.1,
            )
            generated = generated.strip()
        except Exception as e:
            generated = ""
        
        # 裁判评分
        result = chat_completion_json(
            system=JUDGE_SYSTEM,
            user=JUDGE_PROMPT.format(
                question=question,
                gold_answer=gold_answer,
                generated_answer=generated
            ),
            temperature=0.1,
        )
        judgment = result.get("judgment", "INCORRECT")
        if judgment not in ("CORRECT", "INCORRECT"):
            judgment = "INCORRECT"
        
        is_correct = judgment == "CORRECT"
        if is_correct:
            conv_correct += 1
        
        conv_results.append({
            "conversation_idx": conv_idx,
            "qa_idx": orig_idx,
            "question": question,
            "gold_answer": gold_answer,
            "generated_answer": generated,
            "judgment": judgment,
            "judge_reason": result.get("reason", ""),
            "category": category,
            "top_memories": top_memories[:5],
        })
        
        if (qa_idx + 1) % 20 == 0:
            acc_so_far = conv_correct / (qa_idx + 1) * 100
            print(f"  [Conv {conv_idx}] Q{qa_idx+1}/{len(qa_list)} | acc={acc_so_far:.1f}%", flush=True)
    
    answer_elapsed = time.time() - answer_start
    acc = conv_correct / len(qa_list) * 100 if qa_list else 0
    print(f"[Conv {conv_idx}] 完成: {conv_correct}/{len(qa_list)} = {acc:.1f}% | write={write_elapsed:.0f}s answer={answer_elapsed:.0f}s")
    
    # 保存单对话结果
    result_data = {
        "conv_idx": conv_idx,
        "speaker_a": speaker_a,
        "speaker_b": speaker_b,
        "total": len(qa_list),
        "correct": conv_correct,
        "accuracy": acc,
        "write_time": write_elapsed,
        "answer_time": answer_elapsed,
        "mem_count": mem_count,
        "details": conv_results,
    }
    
    result_path = os.path.join(output_dir, f"conv{conv_idx}_result.json")
    with open(result_path, 'w') as f:
        json.dump(result_data, f, indent=2, ensure_ascii=False)
    
    mem.close()
    return result_data


def merge_results(output_dir: str, num_convs: int):
    """合并所有对话结果"""
    all_details = []
    total_q = 0
    total_correct = 0
    from collections import defaultdict
    category_stats = defaultdict(lambda: {"total": 0, "correct": 0})
    
    for i in range(num_convs):
        path = os.path.join(output_dir, f"conv{i}_result.json")
        if not os.path.exists(path):
            print"""
A-Mem 官方版 LoCoMo 并行测评脚本
每个对话一个进程，10个对话同时跑
"""
import json
import os
import sys
import time
import argparse
import subprocess
from pathlib import Path

def run_single_conv(conv_idx: int, dataset_path: str, output_dir: str, top_k: int):
    """单个对话的测评（子进程）"""
    # 加载数据集
    with open(dataset_path) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    
    entry = dataset[conv_idx]
    conversation = entry["conversation"]
    speaker_a = conversation["speaker_a"]
    speaker_b = conversation["speaker_b"]
    
    # 获取 sessions
    from locomo_eval import get_sorted_sessions, locomo_date_to_epoch, turns_to_text
    from locomo_eval import ANSWER_PROMPT, JUDGE_SYSTEM, JUDGE_PROMPT
    from llm_client import chat_completion, chat_completion_json, reset_token_stats, get_token_stats
    from amem_official_memory import OfficialAMemMemory
    
    sorted_sessions = get_sorted_sessions(conversation)
    
    qa_list = []
    all_qa = entry.get("qa", entry.get("qa_pairs", []))
    for i, qa in enumerate(all_qa):
        if "answer" not in qa or not qa["answer"]:
            continue
        qa_list.append((i, qa))
    
    user_id = f"locomo_amem_raw_{conv_idx}"
    
    # 每个对话独立的 A-Mem 实例
    mem = OfficialAMemMemory(db_path=os.path.join(output_dir, f"amem_raw_conv{conv_idx}.db"))
    
    print(f"[Conv {conv_idx}] {speaker_a} & {speaker_b} | {len(sorted_sessions)} sessions, {len(qa_list)} QA")
    
    # 写入记忆
    write_start = time.time()
    mem_count = 0
    for sess_idx, (session_key, date_str, turns) in enumerate(sorted_sessions):
        session_epoch = locomo_date_to_epoch(date_str) or time.time()
        date_header = f"[Conversation Date: {date_str}]\n"
        batch_size = 5
        for i in range(0, len(turns), batch_size):
            batch = turns[i:i+batch_size]
            batch_text = turns_to_text(batch, speaker_a, speaker_b)
            if batch_text.strip():
                try:
                    full_text = date_header + batch_text
                    mem.add(full_text, user_id=user_id, timestamp=session_epoch)
                    mem_count += 1
                except Exception as e:
                    print(f"  [Conv {conv_idx}] 写入失败: {e}")
    write_elapsed = time.time() - write_start
    print(f"[Conv {conv_idx}] 写入完成: {mem_count} batches, {write_elapsed:.1f}s")
    
    # 参考日期
    ref_date = sorted_sessions[-1][1] if sorted_sessions else "2023"
    
    # 答题
    conv_results = []
    conv_correct = 0
    answer_start = time.time()
    for qa_idx, (orig_idx, qa) in enumerate(qa_list):
        question = qa["question"]
        gold_answer = qa["answer"]
        category = qa.get("category", 0)
        
        # 检索
        try:
            search_results = mem.search(question, user_id=user_id, top_k=top_k)
            top_memories = [r.get("memory", "") for r in search_results[:top_k]]
        except Exception as e:
            print(f"  [Conv {conv_idx}] 检索失败 Q{qa_idx}: {e}")
            top_memories = []
        
        memory_text = "\n".join([f"- {m}" for m in top_memories])
        
        # 生成答案
        try:
            generated = chat_completion(
                system="You are a precise question-answering assistant.",
                user=ANSWER_PROMPT.format(
                    memories=memory_text[:8000],
                    question=question,
                    reference_date=ref_date
                ),
                temperature=0.1,
            )
            generated = generated.strip()
        except Exception as e:
            generated = ""
        
        # 裁判评分
        result = chat_completion_json(
            system=JUDGE_SYSTEM,
            user=JUDGE_PROMPT.format(
                question=question,
                gold_answer=gold_answer,
                generated_answer=generated
            ),
            temperature=0.1,
        )
        judgment = result.get("judgment", "INCORRECT")
        if judgment not in ("CORRECT", "INCORRECT"):
            judgment = "INCORRECT"
        
        is_correct = judgment == "CORRECT"
        if is_correct:
            conv_correct += 1
        
        conv_results.append({
            "conversation_idx": conv_idx,
            "qa_idx": orig_idx,
            "question": question,
            "gold_answer": gold_answer,
            "generated_answer": generated,
            "judgment": judgment,
            "judge_reason": result.get("reason", ""),
            "category": category,
            "top_memories": top_memories[:5],
        })
        
        if (qa_idx + 1) % 20 == 0:
            acc_so_far = conv_correct / (qa_idx + 1) * 100
            print(f"  [Conv {conv_idx}] Q{qa_idx+1}/{len(qa_list)} | acc={acc_so_far:.1f}%", flush=True)
    
    answer_elapsed = time.time() - answer_start
    acc = conv_correct / len(qa_list) * 100 if qa_list else 0
    print(f"[Conv {conv_idx}] 完成: {conv_correct}/{len(qa_list)} = {acc:.1f}% | write={write_elapsed:.0f}s answer={answer_elapsed:.0f}s")
    
    # 保存单对话结果
    result_data = {
        "conv_idx": conv_idx,
        "speaker_a": speaker_a,
        "speaker_b": speaker_b,
        "total": len(qa_list),
        "correct": conv_correct,
        "accuracy": acc,
        "write_time": write_elapsed,
        "answer_time": answer_elapsed,
        "mem_count": mem_count,
        "details": conv_results,
    }
    
    result_path = os.path.join(output_dir, f"conv{conv_idx}_result.json")
    with open(result_path, 'w') as f:
        json.dump(result_data, f, indent=2, ensure_ascii=False)
    
    mem.close()
    return result_data


def merge_results(output_dir: str, num_convs: int):
    """合并所有对话结果"""
    all_details = []
    total_q = 0
    total_correct = 0
    from collections import defaultdict
    category_stats = defaultdict(lambda: {"total": 0, "correct": 0})
    
    for i in range(num_convs):
        path = os.path.join(output_dir, f"conv{i}_result.json")
        if not os.path.exists(path):
            print(f"  对话 {i} 结果不存在，跳过")
            continue
        with open(path) as f:
            data = json.load(f)"""
A-Mem 官方版 LoCoMo 并行测评脚本
每个对话一个进程，10个对话同时跑
"""
import json
import os
import sys
import time
import argparse
import subprocess
from pathlib import Path

def run_single_conv(conv_idx: int, dataset_path: str, output_dir: str, top_k: int):
    """单个对话的测评（子进程）"""
    # 加载数据集
    with open(dataset_path) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    
    entry = dataset[conv_idx]
    conversation = entry["conversation"]
    speaker_a = conversation["speaker_a"]
    speaker_b = conversation["speaker_b"]
    
    # 获取 sessions
    from locomo_eval import get_sorted_sessions, locomo_date_to_epoch, turns_to_text
    from locomo_eval import ANSWER_PROMPT, JUDGE_SYSTEM, JUDGE_PROMPT
    from llm_client import chat_completion, chat_completion_json, reset_token_stats, get_token_stats
    from amem_official_memory import OfficialAMemMemory
    
    sorted_sessions = get_sorted_sessions(conversation)
    
    qa_list = []
    all_qa = entry.get("qa", entry.get("qa_pairs", []))
    for i, qa in enumerate(all_qa):
        if "answer" not in qa or not qa["answer"]:
            continue
        qa_list.append((i, qa))
    
    user_id = f"locomo_amem_raw_{conv_idx}"
    
    # 每个对话独立的 A-Mem 实例
    mem = OfficialAMemMemory(db_path=os.path.join(output_dir, f"amem_raw_conv{conv_idx}.db"))
    
    print(f"[Conv {conv_idx}] {speaker_a} & {speaker_b} | {len(sorted_sessions)} sessions, {len(qa_list)} QA")
    
    # 写入记忆
    write_start = time.time()
    mem_count = 0
    for sess_idx, (session_key, date_str, turns) in enumerate(sorted_sessions):
        session_epoch = locomo_date_to_epoch(date_str) or time.time()
        date_header = f"[Conversation Date: {date_str}]\n"
        batch_size = 5
        for i in range(0, len(turns), batch_size):
            batch = turns[i:i+batch_size]
            batch_text = turns_to_text(batch, speaker_a, speaker_b)
            if batch_text.strip():
                try:
                    full_text = date_header + batch_text
                    mem.add(full_text, user_id=user_id, timestamp=session_epoch)
                    mem_count += 1
                except Exception as e:
                    print(f"  [Conv {conv_idx}] 写入失败: {e}")
    write_elapsed = time.time() - write_start
    print(f"[Conv {conv_idx}] 写入完成: {mem_count} batches, {write_elapsed:.1f}s")
    
    # 参考日期
    ref_date = sorted_sessions[-1][1] if sorted_sessions else "2023"
    
    # 答题
    conv_results = []
    conv_correct = 0
    answer_start = time.time()
    for qa_idx, (orig_idx, qa) in enumerate(qa_list):
        question = qa["question"]
        gold_answer = qa["answer"]
        category = qa.get("category", 0)
        
        # 检索
        try:
            search_results = mem.search(question, user_id=user_id, top_k=top_k)
            top_memories = [r.get("memory", "") for r in search_results[:top_k]]
        except Exception as e:
            print(f"  [Conv {conv_idx}] 检索失败 Q{qa_idx}: {e}")
            top_memories = []
        
        memory_text = "\n".join([f"- {m}" for m in top_memories])
        
        # 生成答案
        try:
            generated = chat_completion(
                system="You are a precise question-answering assistant.",
                user=ANSWER_PROMPT.format(
                    memories=memory_text[:8000],
                    question=question,
                    reference_date=ref_date
                ),
                temperature=0.1,
            )
            generated = generated.strip()
        except Exception as e:
            generated = ""
        
        # 裁判评分
        result = chat_completion_json(
            system=JUDGE_SYSTEM,
            user=JUDGE_PROMPT.format(
                question=question,
                gold_answer=gold_answer,
                generated_answer=generated
            ),
            temperature=0.1,
        )
        judgment = result.get("judgment", "INCORRECT")
        if judgment not in ("CORRECT", "INCORRECT"):
            judgment = "INCORRECT"
        
        is_correct = judgment == "CORRECT"
        if is_correct:
            conv_correct += 1
        
        conv_results.append({
            "conversation_idx": conv_idx,
            "qa_idx": orig_idx,
            "question": question,
            "gold_answer": gold_answer,
            "generated_answer": generated,
            "judgment": judgment,
            "judge_reason": result.get("reason", ""),
            "category": category,
            "top_memories": top_memories[:5],
        })
        
        if (qa_idx + 1) % 20 == 0:
            acc_so_far = conv_correct / (qa_idx + 1) * 100
            print(f"  [Conv {conv_idx}] Q{qa_idx+1}/{len(qa_list)} | acc={acc_so_far:.1f}%", flush=True)
    
    answer_elapsed = time.time() - answer_start
    acc = conv_correct / len(qa_list) * 100 if qa_list else 0
    print(f"[Conv {conv_idx}] 完成: {conv_correct}/{len(qa_list)} = {acc:.1f}% | write={write_elapsed:.0f}s answer={answer_elapsed:.0f}s")
    
    # 保存单对话结果
    result_data = {
        "conv_idx": conv_idx,
        "speaker_a": speaker_a,
        "speaker_b": speaker_b,
        "total": len(qa_list),
        "correct": conv_correct,
        "accuracy": acc,
        "write_time": write_elapsed,
        "answer_time": answer_elapsed,
        "mem_count": mem_count,
        "details": conv_results,
    }
    
    result_path = os.path.join(output_dir, f"conv{conv_idx}_result.json")
    with open(result_path, 'w') as f:
        json.dump(result_data, f, indent=2, ensure_ascii=False)
    
    mem.close()
    return result_data


def merge_results(output_dir: str, num_convs: int):
    """合并所有对话结果"""
    all_details = []
    total_q = 0
    total_correct = 0
    from collections import defaultdict
    category_stats = defaultdict(lambda: {"total": 0, "correct": 0})
    
    for i in range(num_convs):
        path = os.path.join(output_dir, f"conv{i}_result.json")
        if not os.path.exists(path):
            print(f"  对话 {i} 结果不存在，跳过")
            continue
        with open(path) as f:
            data = json.load(f)
        
        all_details.extend(data["details"])
        total_q += data["total"]
        total_correct += data["correct"]
        
        for d in data["details"]:
            cat = str(d.get("category", 0"""
A-Mem 官方版 LoCoMo 并行测评脚本
每个对话一个进程，10个对话同时跑
"""
import json
import os
import sys
import time
import argparse
import subprocess
from pathlib import Path

def run_single_conv(conv_idx: int, dataset_path: str, output_dir: str, top_k: int):
    """单个对话的测评（子进程）"""
    # 加载数据集
    with open(dataset_path) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    
    entry = dataset[conv_idx]
    conversation = entry["conversation"]
    speaker_a = conversation["speaker_a"]
    speaker_b = conversation["speaker_b"]
    
    # 获取 sessions
    from locomo_eval import get_sorted_sessions, locomo_date_to_epoch, turns_to_text
    from locomo_eval import ANSWER_PROMPT, JUDGE_SYSTEM, JUDGE_PROMPT
    from llm_client import chat_completion, chat_completion_json, reset_token_stats, get_token_stats
    from amem_official_memory import OfficialAMemMemory
    
    sorted_sessions = get_sorted_sessions(conversation)
    
    qa_list = []
    all_qa = entry.get("qa", entry.get("qa_pairs", []))
    for i, qa in enumerate(all_qa):
        if "answer" not in qa or not qa["answer"]:
            continue
        qa_list.append((i, qa))
    
    user_id = f"locomo_amem_raw_{conv_idx}"
    
    # 每个对话独立的 A-Mem 实例
    mem = OfficialAMemMemory(db_path=os.path.join(output_dir, f"amem_raw_conv{conv_idx}.db"))
    
    print(f"[Conv {conv_idx}] {speaker_a} & {speaker_b} | {len(sorted_sessions)} sessions, {len(qa_list)} QA")
    
    # 写入记忆
    write_start = time.time()
    mem_count = 0
    for sess_idx, (session_key, date_str, turns) in enumerate(sorted_sessions):
        session_epoch = locomo_date_to_epoch(date_str) or time.time()
        date_header = f"[Conversation Date: {date_str}]\n"
        batch_size = 5
        for i in range(0, len(turns), batch_size):
            batch = turns[i:i+batch_size]
            batch_text = turns_to_text(batch, speaker_a, speaker_b)
            if batch_text.strip():
                try:
                    full_text = date_header + batch_text
                    mem.add(full_text, user_id=user_id, timestamp=session_epoch)
                    mem_count += 1
                except Exception as e:
                    print(f"  [Conv {conv_idx}] 写入失败: {e}")
    write_elapsed = time.time() - write_start
    print(f"[Conv {conv_idx}] 写入完成: {mem_count} batches, {write_elapsed:.1f}s")
    
    # 参考日期
    ref_date = sorted_sessions[-1][1] if sorted_sessions else "2023"
    
    # 答题
    conv_results = []
    conv_correct = 0
    answer_start = time.time()
    for qa_idx, (orig_idx, qa) in enumerate(qa_list):
        question = qa["question"]
        gold_answer = qa["answer"]
        category = qa.get("category", 0)
        
        # 检索
        try:
            search_results = mem.search(question, user_id=user_id, top_k=top_k)
            top_memories = [r.get("memory", "") for r in search_results[:top_k]]
        except Exception as e:
            print(f"  [Conv {conv_idx}] 检索失败 Q{qa_idx}: {e}")
            top_memories = []
        
        memory_text = "\n".join([f"- {m}" for m in top_memories])
        
        # 生成答案
        try:
            generated = chat_completion(
                system="You are a precise question-answering assistant.",
                user=ANSWER_PROMPT.format(
                    memories=memory_text[:8000],
                    question=question,
                    reference_date=ref_date
                ),
                temperature=0.1,
            )
            generated = generated.strip()
        except Exception as e:
            generated = ""
        
        # 裁判评分
        result = chat_completion_json(
            system=JUDGE_SYSTEM,
            user=JUDGE_PROMPT.format(
                question=question,
                gold_answer=gold_answer,
                generated_answer=generated
            ),
            temperature=0.1,
        )
        judgment = result.get("judgment", "INCORRECT")
        if judgment not in ("CORRECT", "INCORRECT"):
            judgment = "INCORRECT"
        
        is_correct = judgment == "CORRECT"
        if is_correct:
            conv_correct += 1
        
        conv_results.append({
            "conversation_idx": conv_idx,
            "qa_idx": orig_idx,
            "question": question,
            "gold_answer": gold_answer,
            "generated_answer": generated,
            "judgment": judgment,
            "judge_reason": result.get("reason", ""),
            "category": category,
            "top_memories": top_memories[:5],
        })
        
        if (qa_idx + 1) % 20 == 0:
            acc_so_far = conv_correct / (qa_idx + 1) * 100
            print(f"  [Conv {conv_idx}] Q{qa_idx+1}/{len(qa_list)} | acc={acc_so_far:.1f}%", flush=True)
    
    answer_elapsed = time.time() - answer_start
    acc = conv_correct / len(qa_list) * 100 if qa_list else 0
    print(f"[Conv {conv_idx}] 完成: {conv_correct}/{len(qa_list)} = {acc:.1f}% | write={write_elapsed:.0f}s answer={answer_elapsed:.0f}s")
    
    # 保存单对话结果
    result_data = {
        "conv_idx": conv_idx,
        "speaker_a": speaker_a,
        "speaker_b": speaker_b,
        "total": len(qa_list),
        "correct": conv_correct,
        "accuracy": acc,
        "write_time": write_elapsed,
        "answer_time": answer_elapsed,
        "mem_count": mem_count,
        "details": conv_results,
    }
    
    result_path = os.path.join(output_dir, f"conv{conv_idx}_result.json")
    with open(result_path, 'w') as f:
        json.dump(result_data, f, indent=2, ensure_ascii=False)
    
    mem.close()
    return result_data


def merge_results(output_dir: str, num_convs: int):
    """合并所有对话结果"""
    all_details = []
    total_q = 0
    total_correct = 0
    from collections import defaultdict
    category_stats = defaultdict(lambda: {"total": 0, "correct": 0})
    
    for i in range(num_convs):
        path = os.path.join(output_dir, f"conv{i}_result.json")
        if not os.path.exists(path):
            print(f"  对话 {i} 结果不存在，跳过")
            continue
        with open(path) as f:
            data = json.load(f)
        
        all_details.extend(data["details"])
        total_q += data["total"]
        total_correct += data["correct"]
        
        for d in data["details"]:
            cat = str(d.get("category", 0))
            category_stats[cat]["total"] += 1
            if d["judgment"] == "CORRECT":
                category_stats[cat]["correct"] += 1
        
        print(f"  Conv {i}: {data"""
A-Mem 官方版 LoCoMo 并行测评脚本
每个对话一个进程，10个对话同时跑
"""
import json
import os
import sys
import time
import argparse
import subprocess
from pathlib import Path

def run_single_conv(conv_idx: int, dataset_path: str, output_dir: str, top_k: int):
    """单个对话的测评（子进程）"""
    # 加载数据集
    with open(dataset_path) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    
    entry = dataset[conv_idx]
    conversation = entry["conversation"]
    speaker_a = conversation["speaker_a"]
    speaker_b = conversation["speaker_b"]
    
    # 获取 sessions
    from locomo_eval import get_sorted_sessions, locomo_date_to_epoch, turns_to_text
    from locomo_eval import ANSWER_PROMPT, JUDGE_SYSTEM, JUDGE_PROMPT
    from llm_client import chat_completion, chat_completion_json, reset_token_stats, get_token_stats
    from amem_official_memory import OfficialAMemMemory
    
    sorted_sessions = get_sorted_sessions(conversation)
    
    qa_list = []
    all_qa = entry.get("qa", entry.get("qa_pairs", []))
    for i, qa in enumerate(all_qa):
        if "answer" not in qa or not qa["answer"]:
            continue
        qa_list.append((i, qa))
    
    user_id = f"locomo_amem_raw_{conv_idx}"
    
    # 每个对话独立的 A-Mem 实例
    mem = OfficialAMemMemory(db_path=os.path.join(output_dir, f"amem_raw_conv{conv_idx}.db"))
    
    print(f"[Conv {conv_idx}] {speaker_a} & {speaker_b} | {len(sorted_sessions)} sessions, {len(qa_list)} QA")
    
    # 写入记忆
    write_start = time.time()
    mem_count = 0
    for sess_idx, (session_key, date_str, turns) in enumerate(sorted_sessions):
        session_epoch = locomo_date_to_epoch(date_str) or time.time()
        date_header = f"[Conversation Date: {date_str}]\n"
        batch_size = 5
        for i in range(0, len(turns), batch_size):
            batch = turns[i:i+batch_size]
            batch_text = turns_to_text(batch, speaker_a, speaker_b)
            if batch_text.strip():
                try:
                    full_text = date_header + batch_text
                    mem.add(full_text, user_id=user_id, timestamp=session_epoch)
                    mem_count += 1
                except Exception as e:
                    print(f"  [Conv {conv_idx}] 写入失败: {e}")
    write_elapsed = time.time() - write_start
    print(f"[Conv {conv_idx}] 写入完成: {mem_count} batches, {write_elapsed:.1f}s")
    
    # 参考日期
    ref_date = sorted_sessions[-1][1] if sorted_sessions else "2023"
    
    # 答题
    conv_results = []
    conv_correct = 0
    answer_start = time.time()
    for qa_idx, (orig_idx, qa) in enumerate(qa_list):
        question = qa["question"]
        gold_answer = qa["answer"]
        category = qa.get("category", 0)
        
        # 检索
        try:
            search_results = mem.search(question, user_id=user_id, top_k=top_k)
            top_memories = [r.get("memory", "") for r in search_results[:top_k]]
        except Exception as e:
            print(f"  [Conv {conv_idx}] 检索失败 Q{qa_idx}: {e}")
            top_memories = []
        
        memory_text = "\n".join([f"- {m}" for m in top_memories])
        
        # 生成答案
        try:
            generated = chat_completion(
                system="You are a precise question-answering assistant.",
                user=ANSWER_PROMPT.format(
                    memories=memory_text[:8000],
                    question=question,
                    reference_date=ref_date
                ),
                temperature=0.1,
            )
            generated = generated.strip()
        except Exception as e:
            generated = ""
        
        # 裁判评分
        result = chat_completion_json(
            system=JUDGE_SYSTEM,
            user=JUDGE_PROMPT.format(
                question=question,
                gold_answer=gold_answer,
                generated_answer=generated
            ),
            temperature=0.1,
        )
        judgment = result.get("judgment", "INCORRECT")
        if judgment not in ("CORRECT", "INCORRECT"):
            judgment = "INCORRECT"
        
        is_correct = judgment == "CORRECT"
        if is_correct:
            conv_correct += 1
        
        conv_results.append({
            "conversation_idx": conv_idx,
            "qa_idx": orig_idx,
            "question": question,
            "gold_answer": gold_answer,
            "generated_answer": generated,
            "judgment": judgment,
            "judge_reason": result.get("reason", ""),
            "category": category,
            "top_memories": top_memories[:5],
        })
        
        if (qa_idx + 1) % 20 == 0:
            acc_so_far = conv_correct / (qa_idx + 1) * 100
            print(f"  [Conv {conv_idx}] Q{qa_idx+1}/{len(qa_list)} | acc={acc_so_far:.1f}%", flush=True)
    
    answer_elapsed = time.time() - answer_start
    acc = conv_correct / len(qa_list) * 100 if qa_list else 0
    print(f"[Conv {conv_idx}] 完成: {conv_correct}/{len(qa_list)} = {acc:.1f}% | write={write_elapsed:.0f}s answer={answer_elapsed:.0f}s")
    
    # 保存单对话结果
    result_data = {
        "conv_idx": conv_idx,
        "speaker_a": speaker_a,
        "speaker_b": speaker_b,
        "total": len(qa_list),
        "correct": conv_correct,
        "accuracy": acc,
        "write_time": write_elapsed,
        "answer_time": answer_elapsed,
        "mem_count": mem_count,
        "details": conv_results,
    }
    
    result_path = os.path.join(output_dir, f"conv{conv_idx}_result.json")
    with open(result_path, 'w') as f:
        json.dump(result_data, f, indent=2, ensure_ascii=False)
    
    mem.close()
    return result_data


def merge_results(output_dir: str, num_convs: int):
    """合并所有对话结果"""
    all_details = []
    total_q = 0
    total_correct = 0
    from collections import defaultdict
    category_stats = defaultdict(lambda: {"total": 0, "correct": 0})
    
    for i in range(num_convs):
        path = os.path.join(output_dir, f"conv{i}_result.json")
        if not os.path.exists(path):
            print(f"  对话 {i} 结果不存在，跳过")
            continue
        with open(path) as f:
            data = json.load(f)
        
        all_details.extend(data["details"])
        total_q += data["total"]
        total_correct += data["correct"]
        
        for d in data["details"]:
            cat = str(d.get("category", 0))
            category_stats[cat]["total"] += 1
            if d["judgment"] == "CORRECT":
                category_stats[cat]["correct"] += 1
        
        print(f"  Conv {i}: {data['correct']}/{data['total']} = {data['accuracy']:.1f}%")
    
    accuracy = total_correct / total_q * 100 if total_q else 0
    
    merged = {
        "system": "am"""
A-Mem 官方版 LoCoMo 并行测评脚本
每个对话一个进程，10个对话同时跑
"""
import json
import os
import sys
import time
import argparse
import subprocess
from pathlib import Path

def run_single_conv(conv_idx: int, dataset_path: str, output_dir: str, top_k: int):
    """单个对话的测评（子进程）"""
    # 加载数据集
    with open(dataset_path) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    
    entry = dataset[conv_idx]
    conversation = entry["conversation"]
    speaker_a = conversation["speaker_a"]
    speaker_b = conversation["speaker_b"]
    
    # 获取 sessions
    from locomo_eval import get_sorted_sessions, locomo_date_to_epoch, turns_to_text
    from locomo_eval import ANSWER_PROMPT, JUDGE_SYSTEM, JUDGE_PROMPT
    from llm_client import chat_completion, chat_completion_json, reset_token_stats, get_token_stats
    from amem_official_memory import OfficialAMemMemory
    
    sorted_sessions = get_sorted_sessions(conversation)
    
    qa_list = []
    all_qa = entry.get("qa", entry.get("qa_pairs", []))
    for i, qa in enumerate(all_qa):
        if "answer" not in qa or not qa["answer"]:
            continue
        qa_list.append((i, qa))
    
    user_id = f"locomo_amem_raw_{conv_idx}"
    
    # 每个对话独立的 A-Mem 实例
    mem = OfficialAMemMemory(db_path=os.path.join(output_dir, f"amem_raw_conv{conv_idx}.db"))
    
    print(f"[Conv {conv_idx}] {speaker_a} & {speaker_b} | {len(sorted_sessions)} sessions, {len(qa_list)} QA")
    
    # 写入记忆
    write_start = time.time()
    mem_count = 0
    for sess_idx, (session_key, date_str, turns) in enumerate(sorted_sessions):
        session_epoch = locomo_date_to_epoch(date_str) or time.time()
        date_header = f"[Conversation Date: {date_str}]\n"
        batch_size = 5
        for i in range(0, len(turns), batch_size):
            batch = turns[i:i+batch_size]
            batch_text = turns_to_text(batch, speaker_a, speaker_b)
            if batch_text.strip():
                try:
                    full_text = date_header + batch_text
                    mem.add(full_text, user_id=user_id, timestamp=session_epoch)
                    mem_count += 1
                except Exception as e:
                    print(f"  [Conv {conv_idx}] 写入失败: {e}")
    write_elapsed = time.time() - write_start
    print(f"[Conv {conv_idx}] 写入完成: {mem_count} batches, {write_elapsed:.1f}s")
    
    # 参考日期
    ref_date = sorted_sessions[-1][1] if sorted_sessions else "2023"
    
    # 答题
    conv_results = []
    conv_correct = 0
    answer_start = time.time()
    for qa_idx, (orig_idx, qa) in enumerate(qa_list):
        question = qa["question"]
        gold_answer = qa["answer"]
        category = qa.get("category", 0)
        
        # 检索
        try:
            search_results = mem.search(question, user_id=user_id, top_k=top_k)
            top_memories = [r.get("memory", "") for r in search_results[:top_k]]
        except Exception as e:
            print(f"  [Conv {conv_idx}] 检索失败 Q{qa_idx}: {e}")
            top_memories = []
        
        memory_text = "\n".join([f"- {m}" for m in top_memories])
        
        # 生成答案
        try:
            generated = chat_completion(
                system="You are a precise question-answering assistant.",
                user=ANSWER_PROMPT.format(
                    memories=memory_text[:8000],
                    question=question,
                    reference_date=ref_date
                ),
                temperature=0.1,
            )
            generated = generated.strip()
        except Exception as e:
            generated = ""
        
        # 裁判评分
        result = chat_completion_json(
            system=JUDGE_SYSTEM,
            user=JUDGE_PROMPT.format(
                question=question,
                gold_answer=gold_answer,
                generated_answer=generated
            ),
            temperature=0.1,
        )
        judgment = result.get("judgment", "INCORRECT")
        if judgment not in ("CORRECT", "INCORRECT"):
            judgment = "INCORRECT"
        
        is_correct = judgment == "CORRECT"
        if is_correct:
            conv_correct += 1
        
        conv_results.append({
            "conversation_idx": conv_idx,
            "qa_idx": orig_idx,
            "question": question,
            "gold_answer": gold_answer,
            "generated_answer": generated,
            "judgment": judgment,
            "judge_reason": result.get("reason", ""),
            "category": category,
            "top_memories": top_memories[:5],
        })
        
        if (qa_idx + 1) % 20 == 0:
            acc_so_far = conv_correct / (qa_idx + 1) * 100
            print(f"  [Conv {conv_idx}] Q{qa_idx+1}/{len(qa_list)} | acc={acc_so_far:.1f}%", flush=True)
    
    answer_elapsed = time.time() - answer_start
    acc = conv_correct / len(qa_list) * 100 if qa_list else 0
    print(f"[Conv {conv_idx}] 完成: {conv_correct}/{len(qa_list)} = {acc:.1f}% | write={write_elapsed:.0f}s answer={answer_elapsed:.0f}s")
    
    # 保存单对话结果
    result_data = {
        "conv_idx": conv_idx,
        "speaker_a": speaker_a,
        "speaker_b": speaker_b,
        "total": len(qa_list),
        "correct": conv_correct,
        "accuracy": acc,
        "write_time": write_elapsed,
        "answer_time": answer_elapsed,
        "mem_count": mem_count,
        "details": conv_results,
    }
    
    result_path = os.path.join(output_dir, f"conv{conv_idx}_result.json")
    with open(result_path, 'w') as f:
        json.dump(result_data, f, indent=2, ensure_ascii=False)
    
    mem.close()
    return result_data


def merge_results(output_dir: str, num_convs: int):
    """合并所有对话结果"""
    all_details = []
    total_q = 0
    total_correct = 0
    from collections import defaultdict
    category_stats = defaultdict(lambda: {"total": 0, "correct": 0})
    
    for i in range(num_convs):
        path = os.path.join(output_dir, f"conv{i}_result.json")
        if not os.path.exists(path):
            print(f"  对话 {i} 结果不存在，跳过")
            continue
        with open(path) as f:
            data = json.load(f)
        
        all_details.extend(data["details"])
        total_q += data["total"]
        total_correct += data["correct"]
        
        for d in data["details"]:
            cat = str(d.get("category", 0))
            category_stats[cat]["total"] += 1
            if d["judgment"] == "CORRECT":
                category_stats[cat]["correct"] += 1
        
        print(f"  Conv {i}: {data['correct']}/{data['total']} = {data['accuracy']:.1f}%")
    
    accuracy = total_correct / total_q * 100 if total_q else 0
    
    merged = {
        "system": "amem_official_raw",
        "total_questions": total_q,
        "correct": total_correct,
        "accuracy": accuracy,
        "category_stats": dict(category_stats),
        "details": all_details,
    }
    
    merged"""
A-Mem 官方版 LoCoMo 并行测评脚本
每个对话一个进程，10个对话同时跑
"""
import json
import os
import sys
import time
import argparse
import subprocess
from pathlib import Path

def run_single_conv(conv_idx: int, dataset_path: str, output_dir: str, top_k: int):
    """单个对话的测评（子进程）"""
    # 加载数据集
    with open(dataset_path) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    
    entry = dataset[conv_idx]
    conversation = entry["conversation"]
    speaker_a = conversation["speaker_a"]
    speaker_b = conversation["speaker_b"]
    
    # 获取 sessions
    from locomo_eval import get_sorted_sessions, locomo_date_to_epoch, turns_to_text
    from locomo_eval import ANSWER_PROMPT, JUDGE_SYSTEM, JUDGE_PROMPT
    from llm_client import chat_completion, chat_completion_json, reset_token_stats, get_token_stats
    from amem_official_memory import OfficialAMemMemory
    
    sorted_sessions = get_sorted_sessions(conversation)
    
    qa_list = []
    all_qa = entry.get("qa", entry.get("qa_pairs", []))
    for i, qa in enumerate(all_qa):
        if "answer" not in qa or not qa["answer"]:
            continue
        qa_list.append((i, qa))
    
    user_id = f"locomo_amem_raw_{conv_idx}"
    
    # 每个对话独立的 A-Mem 实例
    mem = OfficialAMemMemory(db_path=os.path.join(output_dir, f"amem_raw_conv{conv_idx}.db"))
    
    print(f"[Conv {conv_idx}] {speaker_a} & {speaker_b} | {len(sorted_sessions)} sessions, {len(qa_list)} QA")
    
    # 写入记忆
    write_start = time.time()
    mem_count = 0
    for sess_idx, (session_key, date_str, turns) in enumerate(sorted_sessions):
        session_epoch = locomo_date_to_epoch(date_str) or time.time()
        date_header = f"[Conversation Date: {date_str}]\n"
        batch_size = 5
        for i in range(0, len(turns), batch_size):
            batch = turns[i:i+batch_size]
            batch_text = turns_to_text(batch, speaker_a, speaker_b)
            if batch_text.strip():
                try:
                    full_text = date_header + batch_text
                    mem.add(full_text, user_id=user_id, timestamp=session_epoch)
                    mem_count += 1
                except Exception as e:
                    print(f"  [Conv {conv_idx}] 写入失败: {e}")
    write_elapsed = time.time() - write_start
    print(f"[Conv {conv_idx}] 写入完成: {mem_count} batches, {write_elapsed:.1f}s")
    
    # 参考日期
    ref_date = sorted_sessions[-1][1] if sorted_sessions else "2023"
    
    # 答题
    conv_results = []
    conv_correct = 0
    answer_start = time.time()
    for qa_idx, (orig_idx, qa) in enumerate(qa_list):
        question = qa["question"]
        gold_answer = qa["answer"]
        category = qa.get("category", 0)
        
        # 检索
        try:
            search_results = mem.search(question, user_id=user_id, top_k=top_k)
            top_memories = [r.get("memory", "") for r in search_results[:top_k]]
        except Exception as e:
            print(f"  [Conv {conv_idx}] 检索失败 Q{qa_idx}: {e}")
            top_memories = []
        
        memory_text = "\n".join([f"- {m}" for m in top_memories])
        
        # 生成答案
        try:
            generated = chat_completion(
                system="You are a precise question-answering assistant.",
                user=ANSWER_PROMPT.format(
                    memories=memory_text[:8000],
                    question=question,
                    reference_date=ref_date
                ),
                temperature=0.1,
            )
            generated = generated.strip()
        except Exception as e:
            generated = ""
        
        # 裁判评分
        result = chat_completion_json(
            system=JUDGE_SYSTEM,
            user=JUDGE_PROMPT.format(
                question=question,
                gold_answer=gold_answer,
                generated_answer=generated
            ),
            temperature=0.1,
        )
        judgment = result.get("judgment", "INCORRECT")
        if judgment not in ("CORRECT", "INCORRECT"):
            judgment = "INCORRECT"
        
        is_correct = judgment == "CORRECT"
        if is_correct:
            conv_correct += 1
        
        conv_results.append({
            "conversation_idx": conv_idx,
            "qa_idx": orig_idx,
            "question": question,
            "gold_answer": gold_answer,
            "generated_answer": generated,
            "judgment": judgment,
            "judge_reason": result.get("reason", ""),
            "category": category,
            "top_memories": top_memories[:5],
        })
        
        if (qa_idx + 1) % 20 == 0:
            acc_so_far = conv_correct / (qa_idx + 1) * 100
            print(f"  [Conv {conv_idx}] Q{qa_idx+1}/{len(qa_list)} | acc={acc_so_far:.1f}%", flush=True)
    
    answer_elapsed = time.time() - answer_start
    acc = conv_correct / len(qa_list) * 100 if qa_list else 0
    print(f"[Conv {conv_idx}] 完成: {conv_correct}/{len(qa_list)} = {acc:.1f}% | write={write_elapsed:.0f}s answer={answer_elapsed:.0f}s")
    
    # 保存单对话结果
    result_data = {
        "conv_idx": conv_idx,
        "speaker_a": speaker_a,
        "speaker_b": speaker_b,
        "total": len(qa_list),
        "correct": conv_correct,
        "accuracy": acc,
        "write_time": write_elapsed,
        "answer_time": answer_elapsed,
        "mem_count": mem_count,
        "details": conv_results,
    }
    
    result_path = os.path.join(output_dir, f"conv{conv_idx}_result.json")
    with open(result_path, 'w') as f:
        json.dump(result_data, f, indent=2, ensure_ascii=False)
    
    mem.close()
    return result_data


def merge_results(output_dir: str, num_convs: int):
    """合并所有对话结果"""
    all_details = []
    total_q = 0
    total_correct = 0
    from collections import defaultdict
    category_stats = defaultdict(lambda: {"total": 0, "correct": 0})
    
    for i in range(num_convs):
        path = os.path.join(output_dir, f"conv{i}_result.json")
        if not os.path.exists(path):
            print(f"  对话 {i} 结果不存在，跳过")
            continue
        with open(path) as f:
            data = json.load(f)
        
        all_details.extend(data["details"])
        total_q += data["total"]
        total_correct += data["correct"]
        
        for d in data["details"]:
            cat = str(d.get("category", 0))
            category_stats[cat]["total"] += 1
            if d["judgment"] == "CORRECT":
                category_stats[cat]["correct"] += 1
        
        print(f"  Conv {i}: {data['correct']}/{data['total']} = {data['accuracy']:.1f}%")
    
    accuracy = total_correct / total_q * 100 if total_q else 0
    
    merged = {
        "system": "amem_official_raw",
        "total_questions": total_q,
        "correct": total_correct,
        "accuracy": accuracy,
        "category_stats": dict(category_stats),
        "details": all_details,
    }
    
    merged_path = os.path.join(output_dir, "amem_official_raw_results.json")
    with open(merged_path, 'w') as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)
    
    print"""
A-Mem 官方版 LoCoMo 并行测评脚本
每个对话一个进程，10个对话同时跑
"""
import json
import os
import sys
import time
import argparse
import subprocess
from pathlib import Path

def run_single_conv(conv_idx: int, dataset_path: str, output_dir: str, top_k: int):
    """单个对话的测评（子进程）"""
    # 加载数据集
    with open(dataset_path) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    
    entry = dataset[conv_idx]
    conversation = entry["conversation"]
    speaker_a = conversation["speaker_a"]
    speaker_b = conversation["speaker_b"]
    
    # 获取 sessions
    from locomo_eval import get_sorted_sessions, locomo_date_to_epoch, turns_to_text
    from locomo_eval import ANSWER_PROMPT, JUDGE_SYSTEM, JUDGE_PROMPT
    from llm_client import chat_completion, chat_completion_json, reset_token_stats, get_token_stats
    from amem_official_memory import OfficialAMemMemory
    
    sorted_sessions = get_sorted_sessions(conversation)
    
    qa_list = []
    all_qa = entry.get("qa", entry.get("qa_pairs", []))
    for i, qa in enumerate(all_qa):
        if "answer" not in qa or not qa["answer"]:
            continue
        qa_list.append((i, qa))
    
    user_id = f"locomo_amem_raw_{conv_idx}"
    
    # 每个对话独立的 A-Mem 实例
    mem = OfficialAMemMemory(db_path=os.path.join(output_dir, f"amem_raw_conv{conv_idx}.db"))
    
    print(f"[Conv {conv_idx}] {speaker_a} & {speaker_b} | {len(sorted_sessions)} sessions, {len(qa_list)} QA")
    
    # 写入记忆
    write_start = time.time()
    mem_count = 0
    for sess_idx, (session_key, date_str, turns) in enumerate(sorted_sessions):
        session_epoch = locomo_date_to_epoch(date_str) or time.time()
        date_header = f"[Conversation Date: {date_str}]\n"
        batch_size = 5
        for i in range(0, len(turns), batch_size):
            batch = turns[i:i+batch_size]
            batch_text = turns_to_text(batch, speaker_a, speaker_b)
            if batch_text.strip():
                try:
                    full_text = date_header + batch_text
                    mem.add(full_text, user_id=user_id, timestamp=session_epoch)
                    mem_count += 1
                except Exception as e:
                    print(f"  [Conv {conv_idx}] 写入失败: {e}")
    write_elapsed = time.time() - write_start
    print(f"[Conv {conv_idx}] 写入完成: {mem_count} batches, {write_elapsed:.1f}s")
    
    # 参考日期
    ref_date = sorted_sessions[-1][1] if sorted_sessions else "2023"
    
    # 答题
    conv_results = []
    conv_correct = 0
    answer_start = time.time()
    for qa_idx, (orig_idx, qa) in enumerate(qa_list):
        question = qa["question"]
        gold_answer = qa["answer"]
        category = qa.get("category", 0)
        
        # 检索
        try:
            search_results = mem.search(question, user_id=user_id, top_k=top_k)
            top_memories = [r.get("memory", "") for r in search_results[:top_k]]
        except Exception as e:
            print(f"  [Conv {conv_idx}] 检索失败 Q{qa_idx}: {e}")
            top_memories = []
        
        memory_text = "\n".join([f"- {m}" for m in top_memories])
        
        # 生成答案
        try:
            generated = chat_completion(
                system="You are a precise question-answering assistant.",
                user=ANSWER_PROMPT.format(
                    memories=memory_text[:8000],
                    question=question,
                    reference_date=ref_date
                ),
                temperature=0.1,
            )
            generated = generated.strip()
        except Exception as e:
            generated = ""
        
        # 裁判评分
        result = chat_completion_json(
            system=JUDGE_SYSTEM,
            user=JUDGE_PROMPT.format(
                question=question,
                gold_answer=gold_answer,
                generated_answer=generated
            ),
            temperature=0.1,
        )
        judgment = result.get("judgment", "INCORRECT")
        if judgment not in ("CORRECT", "INCORRECT"):
            judgment = "INCORRECT"
        
        is_correct = judgment == "CORRECT"
        if is_correct:
            conv_correct += 1
        
        conv_results.append({
            "conversation_idx": conv_idx,
            "qa_idx": orig_idx,
            "question": question,
            "gold_answer": gold_answer,
            "generated_answer": generated,
            "judgment": judgment,
            "judge_reason": result.get("reason", ""),
            "category": category,
            "top_memories": top_memories[:5],
        })
        
        if (qa_idx + 1) % 20 == 0:
            acc_so_far = conv_correct / (qa_idx + 1) * 100
            print(f"  [Conv {conv_idx}] Q{qa_idx+1}/{len(qa_list)} | acc={acc_so_far:.1f}%", flush=True)
    
    answer_elapsed = time.time() - answer_start
    acc = conv_correct / len(qa_list) * 100 if qa_list else 0
    print(f"[Conv {conv_idx}] 完成: {conv_correct}/{len(qa_list)} = {acc:.1f}% | write={write_elapsed:.0f}s answer={answer_elapsed:.0f}s")
    
    # 保存单对话结果
    result_data = {
        "conv_idx": conv_idx,
        "speaker_a": speaker_a,
        "speaker_b": speaker_b,
        "total": len(qa_list),
        "correct": conv_correct,
        "accuracy": acc,
        "write_time": write_elapsed,
        "answer_time": answer_elapsed,
        "mem_count": mem_count,
        "details": conv_results,
    }
    
    result_path = os.path.join(output_dir, f"conv{conv_idx}_result.json")
    with open(result_path, 'w') as f:
        json.dump(result_data, f, indent=2, ensure_ascii=False)
    
    mem.close()
    return result_data


def merge_results(output_dir: str, num_convs: int):
    """合并所有对话结果"""
    all_details = []
    total_q = 0
    total_correct = 0
    from collections import defaultdict
    category_stats = defaultdict(lambda: {"total": 0, "correct": 0})
    
    for i in range(num_convs):
        path = os.path.join(output_dir, f"conv{i}_result.json")
        if not os.path.exists(path):
            print(f"  对话 {i} 结果不存在，跳过")
            continue
        with open(path) as f:
            data = json.load(f)
        
        all_details.extend(data["details"])
        total_q += data["total"]
        total_correct += data["correct"]
        
        for d in data["details"]:
            cat = str(d.get("category", 0))
            category_stats[cat]["total"] += 1
            if d["judgment"] == "CORRECT":
                category_stats[cat]["correct"] += 1
        
        print(f"  Conv {i}: {data['correct']}/{data['total']} = {data['accuracy']:.1f}%")
    
    accuracy = total_correct / total_q * 100 if total_q else 0
    
    merged = {
        "system": "amem_official_raw",
        "total_questions": total_q,
        "correct": total_correct,
        "accuracy": accuracy,
        "category_stats": dict(category_stats),
        "details": all_details,
    }
    
    merged_path = os.path.join(output_dir, "amem_official_raw_results.json")
    with open(merged_path, 'w') as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*60}")
    print(f"A-Mem 官方版（原始用法）LoCoMo 合并结果")
    print(f""""
A-Mem 官方版 LoCoMo 并行测评脚本
每个对话一个进程，10个对话同时跑
"""
import json
import os
import sys
import time
import argparse
import subprocess
from pathlib import Path

def run_single_conv(conv_idx: int, dataset_path: str, output_dir: str, top_k: int):
    """单个对话的测评（子进程）"""
    # 加载数据集
    with open(dataset_path) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    
    entry = dataset[conv_idx]
    conversation = entry["conversation"]
    speaker_a = conversation["speaker_a"]
    speaker_b = conversation["speaker_b"]
    
    # 获取 sessions
    from locomo_eval import get_sorted_sessions, locomo_date_to_epoch, turns_to_text
    from locomo_eval import ANSWER_PROMPT, JUDGE_SYSTEM, JUDGE_PROMPT
    from llm_client import chat_completion, chat_completion_json, reset_token_stats, get_token_stats
    from amem_official_memory import OfficialAMemMemory
    
    sorted_sessions = get_sorted_sessions(conversation)
    
    qa_list = []
    all_qa = entry.get("qa", entry.get("qa_pairs", []))
    for i, qa in enumerate(all_qa):
        if "answer" not in qa or not qa["answer"]:
            continue
        qa_list.append((i, qa))
    
    user_id = f"locomo_amem_raw_{conv_idx}"
    
    # 每个对话独立的 A-Mem 实例
    mem = OfficialAMemMemory(db_path=os.path.join(output_dir, f"amem_raw_conv{conv_idx}.db"))
    
    print(f"[Conv {conv_idx}] {speaker_a} & {speaker_b} | {len(sorted_sessions)} sessions, {len(qa_list)} QA")
    
    # 写入记忆
    write_start = time.time()
    mem_count = 0
    for sess_idx, (session_key, date_str, turns) in enumerate(sorted_sessions):
        session_epoch = locomo_date_to_epoch(date_str) or time.time()
        date_header = f"[Conversation Date: {date_str}]\n"
        batch_size = 5
        for i in range(0, len(turns), batch_size):
            batch = turns[i:i+batch_size]
            batch_text = turns_to_text(batch, speaker_a, speaker_b)
            if batch_text.strip():
                try:
                    full_text = date_header + batch_text
                    mem.add(full_text, user_id=user_id, timestamp=session_epoch)
                    mem_count += 1
                except Exception as e:
                    print(f"  [Conv {conv_idx}] 写入失败: {e}")
    write_elapsed = time.time() - write_start
    print(f"[Conv {conv_idx}] 写入完成: {mem_count} batches, {write_elapsed:.1f}s")
    
    # 参考日期
    ref_date = sorted_sessions[-1][1] if sorted_sessions else "2023"
    
    # 答题
    conv_results = []
    conv_correct = 0
    answer_start = time.time()
    for qa_idx, (orig_idx, qa) in enumerate(qa_list):
        question = qa["question"]
        gold_answer = qa["answer"]
        category = qa.get("category", 0)
        
        # 检索
        try:
            search_results = mem.search(question, user_id=user_id, top_k=top_k)
            top_memories = [r.get("memory", "") for r in search_results[:top_k]]
        except Exception as e:
            print(f"  [Conv {conv_idx}] 检索失败 Q{qa_idx}: {e}")
            top_memories = []
        
        memory_text = "\n".join([f"- {m}" for m in top_memories])
        
        # 生成答案
        try:
            generated = chat_completion(
                system="You are a precise question-answering assistant.",
                user=ANSWER_PROMPT.format(
                    memories=memory_text[:8000],
                    question=question,
                    reference_date=ref_date
                ),
                temperature=0.1,
            )
            generated = generated.strip()
        except Exception as e:
            generated = ""
        
        # 裁判评分
        result = chat_completion_json(
            system=JUDGE_SYSTEM,
            user=JUDGE_PROMPT.format(
                question=question,
                gold_answer=gold_answer,
                generated_answer=generated
            ),
            temperature=0.1,
        )
        judgment = result.get("judgment", "INCORRECT")
        if judgment not in ("CORRECT", "INCORRECT"):
            judgment = "INCORRECT"
        
        is_correct = judgment == "CORRECT"
        if is_correct:
            conv_correct += 1
        
        conv_results.append({
            "conversation_idx": conv_idx,
            "qa_idx": orig_idx,
            "question": question,
            "gold_answer": gold_answer,
            "generated_answer": generated,
            "judgment": judgment,
            "judge_reason": result.get("reason", ""),
            "category": category,
            "top_memories": top_memories[:5],
        })
        
        if (qa_idx + 1) % 20 == 0:
            acc_so_far = conv_correct / (qa_idx + 1) * 100
            print(f"  [Conv {conv_idx}] Q{qa_idx+1}/{len(qa_list)} | acc={acc_so_far:.1f}%", flush=True)
    
    answer_elapsed = time.time() - answer_start
    acc = conv_correct / len(qa_list) * 100 if qa_list else 0
    print(f"[Conv {conv_idx}] 完成: {conv_correct}/{len(qa_list)} = {acc:.1f}% | write={write_elapsed:.0f}s answer={answer_elapsed:.0f}s")
    
    # 保存单对话结果
    result_data = {
        "conv_idx": conv_idx,
        "speaker_a": speaker_a,
        "speaker_b": speaker_b,
        "total": len(qa_list),
        "correct": conv_correct,
        "accuracy": acc,
        "write_time": write_elapsed,
        "answer_time": answer_elapsed,
        "mem_count": mem_count,
        "details": conv_results,
    }
    
    result_path = os.path.join(output_dir, f"conv{conv_idx}_result.json")
    with open(result_path, 'w') as f:
        json.dump(result_data, f, indent=2, ensure_ascii=False)
    
    mem.close()
    return result_data


def merge_results(output_dir: str, num_convs: int):
    """合并所有对话结果"""
    all_details = []
    total_q = 0
    total_correct = 0
    from collections import defaultdict
    category_stats = defaultdict(lambda: {"total": 0, "correct": 0})
    
    for i in range(num_convs):
        path = os.path.join(output_dir, f"conv{i}_result.json")
        if not os.path.exists(path):
            print(f"  对话 {i} 结果不存在，跳过")
            continue
        with open(path) as f:
            data = json.load(f)
        
        all_details.extend(data["details"])
        total_q += data["total"]
        total_correct += data["correct"]
        
        for d in data["details"]:
            cat = str(d.get("category", 0))
            category_stats[cat]["total"] += 1
            if d["judgment"] == "CORRECT":
                category_stats[cat]["correct"] += 1
        
        print(f"  Conv {i}: {data['correct']}/{data['total']} = {data['accuracy']:.1f}%")
    
    accuracy = total_correct / total_q * 100 if total_q else 0
    
    merged = {
        "system": "amem_official_raw",
        "total_questions": total_q,
        "correct": total_correct,
        "accuracy": accuracy,
        "category_stats": dict(category_stats),
        "details": all_details,
    }
    
    merged_path = os.path.join(output_dir, "amem_official_raw_results.json")
    with open(merged_path, 'w') as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*60}")
    print(f"A-Mem 官方版（原始用法）LoCoMo 合并结果")
    print(f"总题数: {total_q}")
    print(f"正确数: {total_correct}")
    print(f"准确率: {accuracy:.2f}%")
    print(f"{'='*60}")
    print(f"结果已保存"""
A-Mem 官方版 LoCoMo 并行测评脚本
每个对话一个进程，10个对话同时跑
"""
import json
import os
import sys
import time
import argparse
import subprocess
from pathlib import Path

def run_single_conv(conv_idx: int, dataset_path: str, output_dir: str, top_k: int):
    """单个对话的测评（子进程）"""
    # 加载数据集
    with open(dataset_path) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    
    entry = dataset[conv_idx]
    conversation = entry["conversation"]
    speaker_a = conversation["speaker_a"]
    speaker_b = conversation["speaker_b"]
    
    # 获取 sessions
    from locomo_eval import get_sorted_sessions, locomo_date_to_epoch, turns_to_text
    from locomo_eval import ANSWER_PROMPT, JUDGE_SYSTEM, JUDGE_PROMPT
    from llm_client import chat_completion, chat_completion_json, reset_token_stats, get_token_stats
    from amem_official_memory import OfficialAMemMemory
    
    sorted_sessions = get_sorted_sessions(conversation)
    
    qa_list = []
    all_qa = entry.get("qa", entry.get("qa_pairs", []))
    for i, qa in enumerate(all_qa):
        if "answer" not in qa or not qa["answer"]:
            continue
        qa_list.append((i, qa))
    
    user_id = f"locomo_amem_raw_{conv_idx}"
    
    # 每个对话独立的 A-Mem 实例
    mem = OfficialAMemMemory(db_path=os.path.join(output_dir, f"amem_raw_conv{conv_idx}.db"))
    
    print(f"[Conv {conv_idx}] {speaker_a} & {speaker_b} | {len(sorted_sessions)} sessions, {len(qa_list)} QA")
    
    # 写入记忆
    write_start = time.time()
    mem_count = 0
    for sess_idx, (session_key, date_str, turns) in enumerate(sorted_sessions):
        session_epoch = locomo_date_to_epoch(date_str) or time.time()
        date_header = f"[Conversation Date: {date_str}]\n"
        batch_size = 5
        for i in range(0, len(turns), batch_size):
            batch = turns[i:i+batch_size]
            batch_text = turns_to_text(batch, speaker_a, speaker_b)
            if batch_text.strip():
                try:
                    full_text = date_header + batch_text
                    mem.add(full_text, user_id=user_id, timestamp=session_epoch)
                    mem_count += 1
                except Exception as e:
                    print(f"  [Conv {conv_idx}] 写入失败: {e}")
    write_elapsed = time.time() - write_start
    print(f"[Conv {conv_idx}] 写入完成: {mem_count} batches, {write_elapsed:.1f}s")
    
    # 参考日期
    ref_date = sorted_sessions[-1][1] if sorted_sessions else "2023"
    
    # 答题
    conv_results = []
    conv_correct = 0
    answer_start = time.time()
    for qa_idx, (orig_idx, qa) in enumerate(qa_list):
        question = qa["question"]
        gold_answer = qa["answer"]
        category = qa.get("category", 0)
        
        # 检索
        try:
            search_results = mem.search(question, user_id=user_id, top_k=top_k)
            top_memories = [r.get("memory", "") for r in search_results[:top_k]]
        except Exception as e:
            print(f"  [Conv {conv_idx}] 检索失败 Q{qa_idx}: {e}")
            top_memories = []
        
        memory_text = "\n".join([f"- {m}" for m in top_memories])
        
        # 生成答案
        try:
            generated = chat_completion(
                system="You are a precise question-answering assistant.",
                user=ANSWER_PROMPT.format(
                    memories=memory_text[:8000],
                    question=question,
                    reference_date=ref_date
                ),
                temperature=0.1,
            )
            generated = generated.strip()
        except Exception as e:
            generated = ""
        
        # 裁判评分
        result = chat_completion_json(
            system=JUDGE_SYSTEM,
            user=JUDGE_PROMPT.format(
                question=question,
                gold_answer=gold_answer,
                generated_answer=generated
            ),
            temperature=0.1,
        )
        judgment = result.get("judgment", "INCORRECT")
        if judgment not in ("CORRECT", "INCORRECT"):
            judgment = "INCORRECT"
        
        is_correct = judgment == "CORRECT"
        if is_correct:
            conv_correct += 1
        
        conv_results.append({
            "conversation_idx": conv_idx,
            "qa_idx": orig_idx,
            "question": question,
            "gold_answer": gold_answer,
            "generated_answer": generated,
            "judgment": judgment,
            "judge_reason": result.get("reason", ""),
            "category": category,
            "top_memories": top_memories[:5],
        })
        
        if (qa_idx + 1) % 20 == 0:
            acc_so_far = conv_correct / (qa_idx + 1) * 100
            print(f"  [Conv {conv_idx}] Q{qa_idx+1}/{len(qa_list)} | acc={acc_so_far:.1f}%", flush=True)
    
    answer_elapsed = time.time() - answer_start
    acc = conv_correct / len(qa_list) * 100 if qa_list else 0
    print(f"[Conv {conv_idx}] 完成: {conv_correct}/{len(qa_list)} = {acc:.1f}% | write={write_elapsed:.0f}s answer={answer_elapsed:.0f}s")
    
    # 保存单对话结果
    result_data = {
        "conv_idx": conv_idx,
        "speaker_a": speaker_a,
        "speaker_b": speaker_b,
        "total": len(qa_list),
        "correct": conv_correct,
        "accuracy": acc,
        "write_time": write_elapsed,
        "answer_time": answer_elapsed,
        "mem_count": mem_count,
        "details": conv_results,
    }
    
    result_path = os.path.join(output_dir, f"conv{conv_idx}_result.json")
    with open(result_path, 'w') as f:
        json.dump(result_data, f, indent=2, ensure_ascii=False)
    
    mem.close()
    return result_data


def merge_results(output_dir: str, num_convs: int):
    """合并所有对话结果"""
    all_details = []
    total_q = 0
    total_correct = 0
    from collections import defaultdict
    category_stats = defaultdict(lambda: {"total": 0, "correct": 0})
    
    for i in range(num_convs):
        path = os.path.join(output_dir, f"conv{i}_result.json")
        if not os.path.exists(path):
            print(f"  对话 {i} 结果不存在，跳过")
            continue
        with open(path) as f:
            data = json.load(f)
        
        all_details.extend(data["details"])
        total_q += data["total"]
        total_correct += data["correct"]
        
        for d in data["details"]:
            cat = str(d.get("category", 0))
            category_stats[cat]["total"] += 1
            if d["judgment"] == "CORRECT":
                category_stats[cat]["correct"] += 1
        
        print(f"  Conv {i}: {data['correct']}/{data['total']} = {data['accuracy']:.1f}%")
    
    accuracy = total_correct / total_q * 100 if total_q else 0
    
    merged = {
        "system": "amem_official_raw",
        "total_questions": total_q,
        "correct": total_correct,
        "accuracy": accuracy,
        "category_stats": dict(category_stats),
        "details": all_details,
    }
    
    merged_path = os.path.join(output_dir, "amem_official_raw_results.json")
    with open(merged_path, 'w') as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*60}")
    print(f"A-Mem 官方版（原始用法）LoCoMo 合并结果")
    print(f"总题数: {total_q}")
    print(f"正确数: {total_correct}")
    print(f"准确率: {accuracy:.2f}%")
    print(f"{'='*60}")
    print(f"结果已保存到: {merged_path}")
    
    return merged


def main():
    parser = argparse.ArgumentParser(description="A-Mem 官方版 LoCoMo 并行测评")
    parser.add_argument("--dataset", type=str, default"""
A-Mem 官方版 LoCoMo 并行测评脚本
每个对话一个进程，10个对话同时跑
"""
import json
import os
import sys
import time
import argparse
import subprocess
from pathlib import Path

def run_single_conv(conv_idx: int, dataset_path: str, output_dir: str, top_k: int):
    """单个对话的测评（子进程）"""
    # 加载数据集
    with open(dataset_path) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    
    entry = dataset[conv_idx]
    conversation = entry["conversation"]
    speaker_a = conversation["speaker_a"]
    speaker_b = conversation["speaker_b"]
    
    # 获取 sessions
    from locomo_eval import get_sorted_sessions, locomo_date_to_epoch, turns_to_text
    from locomo_eval import ANSWER_PROMPT, JUDGE_SYSTEM, JUDGE_PROMPT
    from llm_client import chat_completion, chat_completion_json, reset_token_stats, get_token_stats
    from amem_official_memory import OfficialAMemMemory
    
    sorted_sessions = get_sorted_sessions(conversation)
    
    qa_list = []
    all_qa = entry.get("qa", entry.get("qa_pairs", []))
    for i, qa in enumerate(all_qa):
        if "answer" not in qa or not qa["answer"]:
            continue
        qa_list.append((i, qa))
    
    user_id = f"locomo_amem_raw_{conv_idx}"
    
    # 每个对话独立的 A-Mem 实例
    mem = OfficialAMemMemory(db_path=os.path.join(output_dir, f"amem_raw_conv{conv_idx}.db"))
    
    print(f"[Conv {conv_idx}] {speaker_a} & {speaker_b} | {len(sorted_sessions)} sessions, {len(qa_list)} QA")
    
    # 写入记忆
    write_start = time.time()
    mem_count = 0
    for sess_idx, (session_key, date_str, turns) in enumerate(sorted_sessions):
        session_epoch = locomo_date_to_epoch(date_str) or time.time()
        date_header = f"[Conversation Date: {date_str}]\n"
        batch_size = 5
        for i in range(0, len(turns), batch_size):
            batch = turns[i:i+batch_size]
            batch_text = turns_to_text(batch, speaker_a, speaker_b)
            if batch_text.strip():
                try:
                    full_text = date_header + batch_text
                    mem.add(full_text, user_id=user_id, timestamp=session_epoch)
                    mem_count += 1
                except Exception as e:
                    print(f"  [Conv {conv_idx}] 写入失败: {e}")
    write_elapsed = time.time() - write_start
    print(f"[Conv {conv_idx}] 写入完成: {mem_count} batches, {write_elapsed:.1f}s")
    
    # 参考日期
    ref_date = sorted_sessions[-1][1] if sorted_sessions else "2023"
    
    # 答题
    conv_results = []
    conv_correct = 0
    answer_start = time.time()
    for qa_idx, (orig_idx, qa) in enumerate(qa_list):
        question = qa["question"]
        gold_answer = qa["answer"]
        category = qa.get("category", 0)
        
        # 检索
        try:
            search_results = mem.search(question, user_id=user_id, top_k=top_k)
            top_memories = [r.get("memory", "") for r in search_results[:top_k]]
        except Exception as e:
            print(f"  [Conv {conv_idx}] 检索失败 Q{qa_idx}: {e}")
            top_memories = []
        
        memory_text = "\n".join([f"- {m}" for m in top_memories])
        
        # 生成答案
        try:
            generated = chat_completion(
                system="You are a precise question-answering assistant.",
                user=ANSWER_PROMPT.format(
                    memories=memory_text[:8000],
                    question=question,
                    reference_date=ref_date
                ),
                temperature=0.1,
            )
            generated = generated.strip()
        except Exception as e:
            generated = ""
        
        # 裁判评分
        result = chat_completion_json(
            system=JUDGE_SYSTEM,
            user=JUDGE_PROMPT.format(
                question=question,
                gold_answer=gold_answer,
                generated_answer=generated
            ),
            temperature=0.1,
        )
        judgment = result.get("judgment", "INCORRECT")
        if judgment not in ("CORRECT", "INCORRECT"):
            judgment = "INCORRECT"
        
        is_correct = judgment == "CORRECT"
        if is_correct:
            conv_correct += 1
        
        conv_results.append({
            "conversation_idx": conv_idx,
            "qa_idx": orig_idx,
            "question": question,
            "gold_answer": gold_answer,
            "generated_answer": generated,
            "judgment": judgment,
            "judge_reason": result.get("reason", ""),
            "category": category,
            "top_memories": top_memories[:5],
        })
        
        if (qa_idx + 1) % 20 == 0:
            acc_so_far = conv_correct / (qa_idx + 1) * 100
            print(f"  [Conv {conv_idx}] Q{qa_idx+1}/{len(qa_list)} | acc={acc_so_far:.1f}%", flush=True)
    
    answer_elapsed = time.time() - answer_start
    acc = conv_correct / len(qa_list) * 100 if qa_list else 0
    print(f"[Conv {conv_idx}] 完成: {conv_correct}/{len(qa_list)} = {acc:.1f}% | write={write_elapsed:.0f}s answer={answer_elapsed:.0f}s")
    
    # 保存单对话结果
    result_data = {
        "conv_idx": conv_idx,
        "speaker_a": speaker_a,
        "speaker_b": speaker_b,
        "total": len(qa_list),
        "correct": conv_correct,
        "accuracy": acc,
        "write_time": write_elapsed,
        "answer_time": answer_elapsed,
        "mem_count": mem_count,
        "details": conv_results,
    }
    
    result_path = os.path.join(output_dir, f"conv{conv_idx}_result.json")
    with open(result_path, 'w') as f:
        json.dump(result_data, f, indent=2, ensure_ascii=False)
    
    mem.close()
    return result_data


def merge_results(output_dir: str, num_convs: int):
    """合并所有对话结果"""
    all_details = []
    total_q = 0
    total_correct = 0
    from collections import defaultdict
    category_stats = defaultdict(lambda: {"total": 0, "correct": 0})
    
    for i in range(num_convs):
        path = os.path.join(output_dir, f"conv{i}_result.json")
        if not os.path.exists(path):
            print(f"  对话 {i} 结果不存在，跳过")
            continue
        with open(path) as f:
            data = json.load(f)
        
        all_details.extend(data["details"])
        total_q += data["total"]
        total_correct += data["correct"]
        
        for d in data["details"]:
            cat = str(d.get("category", 0))
            category_stats[cat]["total"] += 1
            if d["judgment"] == "CORRECT":
                category_stats[cat]["correct"] += 1
        
        print(f"  Conv {i}: {data['correct']}/{data['total']} = {data['accuracy']:.1f}%")
    
    accuracy = total_correct / total_q * 100 if total_q else 0
    
    merged = {
        "system": "amem_official_raw",
        "total_questions": total_q,
        "correct": total_correct,
        "accuracy": accuracy,
        "category_stats": dict(category_stats),
        "details": all_details,
    }
    
    merged_path = os.path.join(output_dir, "amem_official_raw_results.json")
    with open(merged_path, 'w') as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*60}")
    print(f"A-Mem 官方版（原始用法）LoCoMo 合并结果")
    print(f"总题数: {total_q}")
    print(f"正确数: {total_correct}")
    print(f"准确率: {accuracy:.2f}%")
    print(f"{'='*60}")
    print(f"结果已保存到: {merged_path}")
    
    return merged


def main():
    parser = argparse.ArgumentParser(description="A-Mem 官方版 LoCoMo 并行测评")
    parser.add_argument("--dataset", type=str, default="locomo10.json")
    parser.add_argument("--conversations", type=str, default="all")
    parser.add_argument("--top-k", type=int, default=20)
    parser.add_argument("--output-dir", type=str, default="results"""
A-Mem 官方版 LoCoMo 并行测评脚本
每个对话一个进程，10个对话同时跑
"""
import json
import os
import sys
import time
import argparse
import subprocess
from pathlib import Path

def run_single_conv(conv_idx: int, dataset_path: str, output_dir: str, top_k: int):
    """单个对话的测评（子进程）"""
    # 加载数据集
    with open(dataset_path) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    
    entry = dataset[conv_idx]
    conversation = entry["conversation"]
    speaker_a = conversation["speaker_a"]
    speaker_b = conversation["speaker_b"]
    
    # 获取 sessions
    from locomo_eval import get_sorted_sessions, locomo_date_to_epoch, turns_to_text
    from locomo_eval import ANSWER_PROMPT, JUDGE_SYSTEM, JUDGE_PROMPT
    from llm_client import chat_completion, chat_completion_json, reset_token_stats, get_token_stats
    from amem_official_memory import OfficialAMemMemory
    
    sorted_sessions = get_sorted_sessions(conversation)
    
    qa_list = []
    all_qa = entry.get("qa", entry.get("qa_pairs", []))
    for i, qa in enumerate(all_qa):
        if "answer" not in qa or not qa["answer"]:
            continue
        qa_list.append((i, qa))
    
    user_id = f"locomo_amem_raw_{conv_idx}"
    
    # 每个对话独立的 A-Mem 实例
    mem = OfficialAMemMemory(db_path=os.path.join(output_dir, f"amem_raw_conv{conv_idx}.db"))
    
    print(f"[Conv {conv_idx}] {speaker_a} & {speaker_b} | {len(sorted_sessions)} sessions, {len(qa_list)} QA")
    
    # 写入记忆
    write_start = time.time()
    mem_count = 0
    for sess_idx, (session_key, date_str, turns) in enumerate(sorted_sessions):
        session_epoch = locomo_date_to_epoch(date_str) or time.time()
        date_header = f"[Conversation Date: {date_str}]\n"
        batch_size = 5
        for i in range(0, len(turns), batch_size):
            batch = turns[i:i+batch_size]
            batch_text = turns_to_text(batch, speaker_a, speaker_b)
            if batch_text.strip():
                try:
                    full_text = date_header + batch_text
                    mem.add(full_text, user_id=user_id, timestamp=session_epoch)
                    mem_count += 1
                except Exception as e:
                    print(f"  [Conv {conv_idx}] 写入失败: {e}")
    write_elapsed = time.time() - write_start
    print(f"[Conv {conv_idx}] 写入完成: {mem_count} batches, {write_elapsed:.1f}s")
    
    # 参考日期
    ref_date = sorted_sessions[-1][1] if sorted_sessions else "2023"
    
    # 答题
    conv_results = []
    conv_correct = 0
    answer_start = time.time()
    for qa_idx, (orig_idx, qa) in enumerate(qa_list):
        question = qa["question"]
        gold_answer = qa["answer"]
        category = qa.get("category", 0)
        
        # 检索
        try:
            search_results = mem.search(question, user_id=user_id, top_k=top_k)
            top_memories = [r.get("memory", "") for r in search_results[:top_k]]
        except Exception as e:
            print(f"  [Conv {conv_idx}] 检索失败 Q{qa_idx}: {e}")
            top_memories = []
        
        memory_text = "\n".join([f"- {m}" for m in top_memories])
        
        # 生成答案
        try:
            generated = chat_completion(
                system="You are a precise question-answering assistant.",
                user=ANSWER_PROMPT.format(
                    memories=memory_text[:8000],
                    question=question,
                    reference_date=ref_date
                ),
                temperature=0.1,
            )
            generated = generated.strip()
        except Exception as e:
            generated = ""
        
        # 裁判评分
        result = chat_completion_json(
            system=JUDGE_SYSTEM,
            user=JUDGE_PROMPT.format(
                question=question,
                gold_answer=gold_answer,
                generated_answer=generated
            ),
            temperature=0.1,
        )
        judgment = result.get("judgment", "INCORRECT")
        if judgment not in ("CORRECT", "INCORRECT"):
            judgment = "INCORRECT"
        
        is_correct = judgment == "CORRECT"
        if is_correct:
            conv_correct += 1
        
        conv_results.append({
            "conversation_idx": conv_idx,
            "qa_idx": orig_idx,
            "question": question,
            "gold_answer": gold_answer,
            "generated_answer": generated,
            "judgment": judgment,
            "judge_reason": result.get("reason", ""),
            "category": category,
            "top_memories": top_memories[:5],
        })
        
        if (qa_idx + 1) % 20 == 0:
            acc_so_far = conv_correct / (qa_idx + 1) * 100
            print(f"  [Conv {conv_idx}] Q{qa_idx+1}/{len(qa_list)} | acc={acc_so_far:.1f}%", flush=True)
    
    answer_elapsed = time.time() - answer_start
    acc = conv_correct / len(qa_list) * 100 if qa_list else 0
    print(f"[Conv {conv_idx}] 完成: {conv_correct}/{len(qa_list)} = {acc:.1f}% | write={write_elapsed:.0f}s answer={answer_elapsed:.0f}s")
    
    # 保存单对话结果
    result_data = {
        "conv_idx": conv_idx,
        "speaker_a": speaker_a,
        "speaker_b": speaker_b,
        "total": len(qa_list),
        "correct": conv_correct,
        "accuracy": acc,
        "write_time": write_elapsed,
        "answer_time": answer_elapsed,
        "mem_count": mem_count,
        "details": conv_results,
    }
    
    result_path = os.path.join(output_dir, f"conv{conv_idx}_result.json")
    with open(result_path, 'w') as f:
        json.dump(result_data, f, indent=2, ensure_ascii=False)
    
    mem.close()
    return result_data


def merge_results(output_dir: str, num_convs: int):
    """合并所有对话结果"""
    all_details = []
    total_q = 0
    total_correct = 0
    from collections import defaultdict
    category_stats = defaultdict(lambda: {"total": 0, "correct": 0})
    
    for i in range(num_convs):
        path = os.path.join(output_dir, f"conv{i}_result.json")
        if not os.path.exists(path):
            print(f"  对话 {i} 结果不存在，跳过")
            continue
        with open(path) as f:
            data = json.load(f)
        
        all_details.extend(data["details"])
        total_q += data["total"]
        total_correct += data["correct"]
        
        for d in data["details"]:
            cat = str(d.get("category", 0))
            category_stats[cat]["total"] += 1
            if d["judgment"] == "CORRECT":
                category_stats[cat]["correct"] += 1
        
        print(f"  Conv {i}: {data['correct']}/{data['total']} = {data['accuracy']:.1f}%")
    
    accuracy = total_correct / total_q * 100 if total_q else 0
    
    merged = {
        "system": "amem_official_raw",
        "total_questions": total_q,
        "correct": total_correct,
        "accuracy": accuracy,
        "category_stats": dict(category_stats),
        "details": all_details,
    }
    
    merged_path = os.path.join(output_dir, "amem_official_raw_results.json")
    with open(merged_path, 'w') as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*60}")
    print(f"A-Mem 官方版（原始用法）LoCoMo 合并结果")
    print(f"总题数: {total_q}")
    print(f"正确数: {total_correct}")
    print(f"准确率: {accuracy:.2f}%")
    print(f"{'='*60}")
    print(f"结果已保存到: {merged_path}")
    
    return merged


def main():
    parser = argparse.ArgumentParser(description="A-Mem 官方版 LoCoMo 并行测评")
    parser.add_argument("--dataset", type=str, default="locomo10.json")
    parser.add_argument("--conversations", type=str, default="all")
    parser.add_argument("--top-k", type=int, default=20)
    parser.add_argument("--output-dir", type=str, default="results/amem_official_raw")
    parser.add_argument("--merge-only", action="store_true", help="只合并已有结果")
    args = parser.parse_args()
    
    os.makedirs(args"""
A-Mem 官方版 LoCoMo 并行测评脚本
每个对话一个进程，10个对话同时跑
"""
import json
import os
import sys
import time
import argparse
import subprocess
from pathlib import Path

def run_single_conv(conv_idx: int, dataset_path: str, output_dir: str, top_k: int):
    """单个对话的测评（子进程）"""
    # 加载数据集
    with open(dataset_path) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    
    entry = dataset[conv_idx]
    conversation = entry["conversation"]
    speaker_a = conversation["speaker_a"]
    speaker_b = conversation["speaker_b"]
    
    # 获取 sessions
    from locomo_eval import get_sorted_sessions, locomo_date_to_epoch, turns_to_text
    from locomo_eval import ANSWER_PROMPT, JUDGE_SYSTEM, JUDGE_PROMPT
    from llm_client import chat_completion, chat_completion_json, reset_token_stats, get_token_stats
    from amem_official_memory import OfficialAMemMemory
    
    sorted_sessions = get_sorted_sessions(conversation)
    
    qa_list = []
    all_qa = entry.get("qa", entry.get("qa_pairs", []))
    for i, qa in enumerate(all_qa):
        if "answer" not in qa or not qa["answer"]:
            continue
        qa_list.append((i, qa))
    
    user_id = f"locomo_amem_raw_{conv_idx}"
    
    # 每个对话独立的 A-Mem 实例
    mem = OfficialAMemMemory(db_path=os.path.join(output_dir, f"amem_raw_conv{conv_idx}.db"))
    
    print(f"[Conv {conv_idx}] {speaker_a} & {speaker_b} | {len(sorted_sessions)} sessions, {len(qa_list)} QA")
    
    # 写入记忆
    write_start = time.time()
    mem_count = 0
    for sess_idx, (session_key, date_str, turns) in enumerate(sorted_sessions):
        session_epoch = locomo_date_to_epoch(date_str) or time.time()
        date_header = f"[Conversation Date: {date_str}]\n"
        batch_size = 5
        for i in range(0, len(turns), batch_size):
            batch = turns[i:i+batch_size]
            batch_text = turns_to_text(batch, speaker_a, speaker_b)
            if batch_text.strip():
                try:
                    full_text = date_header + batch_text
                    mem.add(full_text, user_id=user_id, timestamp=session_epoch)
                    mem_count += 1
                except Exception as e:
                    print(f"  [Conv {conv_idx}] 写入失败: {e}")
    write_elapsed = time.time() - write_start
    print(f"[Conv {conv_idx}] 写入完成: {mem_count} batches, {write_elapsed:.1f}s")
    
    # 参考日期
    ref_date = sorted_sessions[-1][1] if sorted_sessions else "2023"
    
    # 答题
    conv_results = []
    conv_correct = 0
    answer_start = time.time()
    for qa_idx, (orig_idx, qa) in enumerate(qa_list):
        question = qa["question"]
        gold_answer = qa["answer"]
        category = qa.get("category", 0)
        
        # 检索
        try:
            search_results = mem.search(question, user_id=user_id, top_k=top_k)
            top_memories = [r.get("memory", "") for r in search_results[:top_k]]
        except Exception as e:
            print(f"  [Conv {conv_idx}] 检索失败 Q{qa_idx}: {e}")
            top_memories = []
        
        memory_text = "\n".join([f"- {m}" for m in top_memories])
        
        # 生成答案
        try:
            generated = chat_completion(
                system="You are a precise question-answering assistant.",
                user=ANSWER_PROMPT.format(
                    memories=memory_text[:8000],
                    question=question,
                    reference_date=ref_date
                ),
                temperature=0.1,
            )
            generated = generated.strip()
        except Exception as e:
            generated = ""
        
        # 裁判评分
        result = chat_completion_json(
            system=JUDGE_SYSTEM,
            user=JUDGE_PROMPT.format(
                question=question,
                gold_answer=gold_answer,
                generated_answer=generated
            ),
            temperature=0.1,
        )
        judgment = result.get("judgment", "INCORRECT")
        if judgment not in ("CORRECT", "INCORRECT"):
            judgment = "INCORRECT"
        
        is_correct = judgment == "CORRECT"
        if is_correct:
            conv_correct += 1
        
        conv_results.append({
            "conversation_idx": conv_idx,
            "qa_idx": orig_idx,
            "question": question,
            "gold_answer": gold_answer,
            "generated_answer": generated,
            "judgment": judgment,
            "judge_reason": result.get("reason", ""),
            "category": category,
            "top_memories": top_memories[:5],
        })
        
        if (qa_idx + 1) % 20 == 0:
            acc_so_far = conv_correct / (qa_idx + 1) * 100
            print(f"  [Conv {conv_idx}] Q{qa_idx+1}/{len(qa_list)} | acc={acc_so_far:.1f}%", flush=True)
    
    answer_elapsed = time.time() - answer_start
    acc = conv_correct / len(qa_list) * 100 if qa_list else 0
    print(f"[Conv {conv_idx}] 完成: {conv_correct}/{len(qa_list)} = {acc:.1f}% | write={write_elapsed:.0f}s answer={answer_elapsed:.0f}s")
    
    # 保存单对话结果
    result_data = {
        "conv_idx": conv_idx,
        "speaker_a": speaker_a,
        "speaker_b": speaker_b,
        "total": len(qa_list),
        "correct": conv_correct,
        "accuracy": acc,
        "write_time": write_elapsed,
        "answer_time": answer_elapsed,
        "mem_count": mem_count,
        "details": conv_results,
    }
    
    result_path = os.path.join(output_dir, f"conv{conv_idx}_result.json")
    with open(result_path, 'w') as f:
        json.dump(result_data, f, indent=2, ensure_ascii=False)
    
    mem.close()
    return result_data


def merge_results(output_dir: str, num_convs: int):
    """合并所有对话结果"""
    all_details = []
    total_q = 0
    total_correct = 0
    from collections import defaultdict
    category_stats = defaultdict(lambda: {"total": 0, "correct": 0})
    
    for i in range(num_convs):
        path = os.path.join(output_dir, f"conv{i}_result.json")
        if not os.path.exists(path):
            print(f"  对话 {i} 结果不存在，跳过")
            continue
        with open(path) as f:
            data = json.load(f)
        
        all_details.extend(data["details"])
        total_q += data["total"]
        total_correct += data["correct"]
        
        for d in data["details"]:
            cat = str(d.get("category", 0))
            category_stats[cat]["total"] += 1
            if d["judgment"] == "CORRECT":
                category_stats[cat]["correct"] += 1
        
        print(f"  Conv {i}: {data['correct']}/{data['total']} = {data['accuracy']:.1f}%")
    
    accuracy = total_correct / total_q * 100 if total_q else 0
    
    merged = {
        "system": "amem_official_raw",
        "total_questions": total_q,
        "correct": total_correct,
        "accuracy": accuracy,
        "category_stats": dict(category_stats),
        "details": all_details,
    }
    
    merged_path = os.path.join(output_dir, "amem_official_raw_results.json")
    with open(merged_path, 'w') as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*60}")
    print(f"A-Mem 官方版（原始用法）LoCoMo 合并结果")
    print(f"总题数: {total_q}")
    print(f"正确数: {total_correct}")
    print(f"准确率: {accuracy:.2f}%")
    print(f"{'='*60}")
    print(f"结果已保存到: {merged_path}")
    
    return merged


def main():
    parser = argparse.ArgumentParser(description="A-Mem 官方版 LoCoMo 并行测评")
    parser.add_argument("--dataset", type=str, default="locomo10.json")
    parser.add_argument("--conversations", type=str, default="all")
    parser.add_argument("--top-k", type=int, default=20)
    parser.add_argument("--output-dir", type=str, default="results/amem_official_raw")
    parser.add_argument("--merge-only", action="store_true", help="只合并已有结果")
    args = parser.parse_args()
    
    os.makedirs(args.output_dir, exist_ok=True)
    
    # 确定对话数
    with open(args.dataset) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    num_convs = len"""
A-Mem 官方版 LoCoMo 并行测评脚本
每个对话一个进程，10个对话同时跑
"""
import json
import os
import sys
import time
import argparse
import subprocess
from pathlib import Path

def run_single_conv(conv_idx: int, dataset_path: str, output_dir: str, top_k: int):
    """单个对话的测评（子进程）"""
    # 加载数据集
    with open(dataset_path) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    
    entry = dataset[conv_idx]
    conversation = entry["conversation"]
    speaker_a = conversation["speaker_a"]
    speaker_b = conversation["speaker_b"]
    
    # 获取 sessions
    from locomo_eval import get_sorted_sessions, locomo_date_to_epoch, turns_to_text
    from locomo_eval import ANSWER_PROMPT, JUDGE_SYSTEM, JUDGE_PROMPT
    from llm_client import chat_completion, chat_completion_json, reset_token_stats, get_token_stats
    from amem_official_memory import OfficialAMemMemory
    
    sorted_sessions = get_sorted_sessions(conversation)
    
    qa_list = []
    all_qa = entry.get("qa", entry.get("qa_pairs", []))
    for i, qa in enumerate(all_qa):
        if "answer" not in qa or not qa["answer"]:
            continue
        qa_list.append((i, qa))
    
    user_id = f"locomo_amem_raw_{conv_idx}"
    
    # 每个对话独立的 A-Mem 实例
    mem = OfficialAMemMemory(db_path=os.path.join(output_dir, f"amem_raw_conv{conv_idx}.db"))
    
    print(f"[Conv {conv_idx}] {speaker_a} & {speaker_b} | {len(sorted_sessions)} sessions, {len(qa_list)} QA")
    
    # 写入记忆
    write_start = time.time()
    mem_count = 0
    for sess_idx, (session_key, date_str, turns) in enumerate(sorted_sessions):
        session_epoch = locomo_date_to_epoch(date_str) or time.time()
        date_header = f"[Conversation Date: {date_str}]\n"
        batch_size = 5
        for i in range(0, len(turns), batch_size):
            batch = turns[i:i+batch_size]
            batch_text = turns_to_text(batch, speaker_a, speaker_b)
            if batch_text.strip():
                try:
                    full_text = date_header + batch_text
                    mem.add(full_text, user_id=user_id, timestamp=session_epoch)
                    mem_count += 1
                except Exception as e:
                    print(f"  [Conv {conv_idx}] 写入失败: {e}")
    write_elapsed = time.time() - write_start
    print(f"[Conv {conv_idx}] 写入完成: {mem_count} batches, {write_elapsed:.1f}s")
    
    # 参考日期
    ref_date = sorted_sessions[-1][1] if sorted_sessions else "2023"
    
    # 答题
    conv_results = []
    conv_correct = 0
    answer_start = time.time()
    for qa_idx, (orig_idx, qa) in enumerate(qa_list):
        question = qa["question"]
        gold_answer = qa["answer"]
        category = qa.get("category", 0)
        
        # 检索
        try:
            search_results = mem.search(question, user_id=user_id, top_k=top_k)
            top_memories = [r.get("memory", "") for r in search_results[:top_k]]
        except Exception as e:
            print(f"  [Conv {conv_idx}] 检索失败 Q{qa_idx}: {e}")
            top_memories = []
        
        memory_text = "\n".join([f"- {m}" for m in top_memories])
        
        # 生成答案
        try:
            generated = chat_completion(
                system="You are a precise question-answering assistant.",
                user=ANSWER_PROMPT.format(
                    memories=memory_text[:8000],
                    question=question,
                    reference_date=ref_date
                ),
                temperature=0.1,
            )
            generated = generated.strip()
        except Exception as e:
            generated = ""
        
        # 裁判评分
        result = chat_completion_json(
            system=JUDGE_SYSTEM,
            user=JUDGE_PROMPT.format(
                question=question,
                gold_answer=gold_answer,
                generated_answer=generated
            ),
            temperature=0.1,
        )
        judgment = result.get("judgment", "INCORRECT")
        if judgment not in ("CORRECT", "INCORRECT"):
            judgment = "INCORRECT"
        
        is_correct = judgment == "CORRECT"
        if is_correct:
            conv_correct += 1
        
        conv_results.append({
            "conversation_idx": conv_idx,
            "qa_idx": orig_idx,
            "question": question,
            "gold_answer": gold_answer,
            "generated_answer": generated,
            "judgment": judgment,
            "judge_reason": result.get("reason", ""),
            "category": category,
            "top_memories": top_memories[:5],
        })
        
        if (qa_idx + 1) % 20 == 0:
            acc_so_far = conv_correct / (qa_idx + 1) * 100
            print(f"  [Conv {conv_idx}] Q{qa_idx+1}/{len(qa_list)} | acc={acc_so_far:.1f}%", flush=True)
    
    answer_elapsed = time.time() - answer_start
    acc = conv_correct / len(qa_list) * 100 if qa_list else 0
    print(f"[Conv {conv_idx}] 完成: {conv_correct}/{len(qa_list)} = {acc:.1f}% | write={write_elapsed:.0f}s answer={answer_elapsed:.0f}s")
    
    # 保存单对话结果
    result_data = {
        "conv_idx": conv_idx,
        "speaker_a": speaker_a,
        "speaker_b": speaker_b,
        "total": len(qa_list),
        "correct": conv_correct,
        "accuracy": acc,
        "write_time": write_elapsed,
        "answer_time": answer_elapsed,
        "mem_count": mem_count,
        "details": conv_results,
    }
    
    result_path = os.path.join(output_dir, f"conv{conv_idx}_result.json")
    with open(result_path, 'w') as f:
        json.dump(result_data, f, indent=2, ensure_ascii=False)
    
    mem.close()
    return result_data


def merge_results(output_dir: str, num_convs: int):
    """合并所有对话结果"""
    all_details = []
    total_q = 0
    total_correct = 0
    from collections import defaultdict
    category_stats = defaultdict(lambda: {"total": 0, "correct": 0})
    
    for i in range(num_convs):
        path = os.path.join(output_dir, f"conv{i}_result.json")
        if not os.path.exists(path):
            print(f"  对话 {i} 结果不存在，跳过")
            continue
        with open(path) as f:
            data = json.load(f)
        
        all_details.extend(data["details"])
        total_q += data["total"]
        total_correct += data["correct"]
        
        for d in data["details"]:
            cat = str(d.get("category", 0))
            category_stats[cat]["total"] += 1
            if d["judgment"] == "CORRECT":
                category_stats[cat]["correct"] += 1
        
        print(f"  Conv {i}: {data['correct']}/{data['total']} = {data['accuracy']:.1f}%")
    
    accuracy = total_correct / total_q * 100 if total_q else 0
    
    merged = {
        "system": "amem_official_raw",
        "total_questions": total_q,
        "correct": total_correct,
        "accuracy": accuracy,
        "category_stats": dict(category_stats),
        "details": all_details,
    }
    
    merged_path = os.path.join(output_dir, "amem_official_raw_results.json")
    with open(merged_path, 'w') as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*60}")
    print(f"A-Mem 官方版（原始用法）LoCoMo 合并结果")
    print(f"总题数: {total_q}")
    print(f"正确数: {total_correct}")
    print(f"准确率: {accuracy:.2f}%")
    print(f"{'='*60}")
    print(f"结果已保存到: {merged_path}")
    
    return merged


def main():
    parser = argparse.ArgumentParser(description="A-Mem 官方版 LoCoMo 并行测评")
    parser.add_argument("--dataset", type=str, default="locomo10.json")
    parser.add_argument("--conversations", type=str, default="all")
    parser.add_argument("--top-k", type=int, default=20)
    parser.add_argument("--output-dir", type=str, default="results/amem_official_raw")
    parser.add_argument("--merge-only", action="store_true", help="只合并已有结果")
    args = parser.parse_args()
    
    os.makedirs(args.output_dir, exist_ok=True)
    
    # 确定对话数
    with open(args.dataset) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    num_convs = len(dataset)
    
    if args.conversations == "all":
        conv_indices = list(range(num_convs))
    else:
        conv_indices = [int(x.strip()) for x in args.conversations.split(",") if x.strip()]"""
A-Mem 官方版 LoCoMo 并行测评脚本
每个对话一个进程，10个对话同时跑
"""
import json
import os
import sys
import time
import argparse
import subprocess
from pathlib import Path

def run_single_conv(conv_idx: int, dataset_path: str, output_dir: str, top_k: int):
    """单个对话的测评（子进程）"""
    # 加载数据集
    with open(dataset_path) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    
    entry = dataset[conv_idx]
    conversation = entry["conversation"]
    speaker_a = conversation["speaker_a"]
    speaker_b = conversation["speaker_b"]
    
    # 获取 sessions
    from locomo_eval import get_sorted_sessions, locomo_date_to_epoch, turns_to_text
    from locomo_eval import ANSWER_PROMPT, JUDGE_SYSTEM, JUDGE_PROMPT
    from llm_client import chat_completion, chat_completion_json, reset_token_stats, get_token_stats
    from amem_official_memory import OfficialAMemMemory
    
    sorted_sessions = get_sorted_sessions(conversation)
    
    qa_list = []
    all_qa = entry.get("qa", entry.get("qa_pairs", []))
    for i, qa in enumerate(all_qa):
        if "answer" not in qa or not qa["answer"]:
            continue
        qa_list.append((i, qa))
    
    user_id = f"locomo_amem_raw_{conv_idx}"
    
    # 每个对话独立的 A-Mem 实例
    mem = OfficialAMemMemory(db_path=os.path.join(output_dir, f"amem_raw_conv{conv_idx}.db"))
    
    print(f"[Conv {conv_idx}] {speaker_a} & {speaker_b} | {len(sorted_sessions)} sessions, {len(qa_list)} QA")
    
    # 写入记忆
    write_start = time.time()
    mem_count = 0
    for sess_idx, (session_key, date_str, turns) in enumerate(sorted_sessions):
        session_epoch = locomo_date_to_epoch(date_str) or time.time()
        date_header = f"[Conversation Date: {date_str}]\n"
        batch_size = 5
        for i in range(0, len(turns), batch_size):
            batch = turns[i:i+batch_size]
            batch_text = turns_to_text(batch, speaker_a, speaker_b)
            if batch_text.strip():
                try:
                    full_text = date_header + batch_text
                    mem.add(full_text, user_id=user_id, timestamp=session_epoch)
                    mem_count += 1
                except Exception as e:
                    print(f"  [Conv {conv_idx}] 写入失败: {e}")
    write_elapsed = time.time() - write_start
    print(f"[Conv {conv_idx}] 写入完成: {mem_count} batches, {write_elapsed:.1f}s")
    
    # 参考日期
    ref_date = sorted_sessions[-1][1] if sorted_sessions else "2023"
    
    # 答题
    conv_results = []
    conv_correct = 0
    answer_start = time.time()
    for qa_idx, (orig_idx, qa) in enumerate(qa_list):
        question = qa["question"]
        gold_answer = qa["answer"]
        category = qa.get("category", 0)
        
        # 检索
        try:
            search_results = mem.search(question, user_id=user_id, top_k=top_k)
            top_memories = [r.get("memory", "") for r in search_results[:top_k]]
        except Exception as e:
            print(f"  [Conv {conv_idx}] 检索失败 Q{qa_idx}: {e}")
            top_memories = []
        
        memory_text = "\n".join([f"- {m}" for m in top_memories])
        
        # 生成答案
        try:
            generated = chat_completion(
                system="You are a precise question-answering assistant.",
                user=ANSWER_PROMPT.format(
                    memories=memory_text[:8000],
                    question=question,
                    reference_date=ref_date
                ),
                temperature=0.1,
            )
            generated = generated.strip()
        except Exception as e:
            generated = ""
        
        # 裁判评分
        result = chat_completion_json(
            system=JUDGE_SYSTEM,
            user=JUDGE_PROMPT.format(
                question=question,
                gold_answer=gold_answer,
                generated_answer=generated
            ),
            temperature=0.1,
        )
        judgment = result.get("judgment", "INCORRECT")
        if judgment not in ("CORRECT", "INCORRECT"):
            judgment = "INCORRECT"
        
        is_correct = judgment == "CORRECT"
        if is_correct:
            conv_correct += 1
        
        conv_results.append({
            "conversation_idx": conv_idx,
            "qa_idx": orig_idx,
            "question": question,
            "gold_answer": gold_answer,
            "generated_answer": generated,
            "judgment": judgment,
            "judge_reason": result.get("reason", ""),
            "category": category,
            "top_memories": top_memories[:5],
        })
        
        if (qa_idx + 1) % 20 == 0:
            acc_so_far = conv_correct / (qa_idx + 1) * 100
            print(f"  [Conv {conv_idx}] Q{qa_idx+1}/{len(qa_list)} | acc={acc_so_far:.1f}%", flush=True)
    
    answer_elapsed = time.time() - answer_start
    acc = conv_correct / len(qa_list) * 100 if qa_list else 0
    print(f"[Conv {conv_idx}] 完成: {conv_correct}/{len(qa_list)} = {acc:.1f}% | write={write_elapsed:.0f}s answer={answer_elapsed:.0f}s")
    
    # 保存单对话结果
    result_data = {
        "conv_idx": conv_idx,
        "speaker_a": speaker_a,
        "speaker_b": speaker_b,
        "total": len(qa_list),
        "correct": conv_correct,
        "accuracy": acc,
        "write_time": write_elapsed,
        "answer_time": answer_elapsed,
        "mem_count": mem_count,
        "details": conv_results,
    }
    
    result_path = os.path.join(output_dir, f"conv{conv_idx}_result.json")
    with open(result_path, 'w') as f:
        json.dump(result_data, f, indent=2, ensure_ascii=False)
    
    mem.close()
    return result_data


def merge_results(output_dir: str, num_convs: int):
    """合并所有对话结果"""
    all_details = []
    total_q = 0
    total_correct = 0
    from collections import defaultdict
    category_stats = defaultdict(lambda: {"total": 0, "correct": 0})
    
    for i in range(num_convs):
        path = os.path.join(output_dir, f"conv{i}_result.json")
        if not os.path.exists(path):
            print(f"  对话 {i} 结果不存在，跳过")
            continue
        with open(path) as f:
            data = json.load(f)
        
        all_details.extend(data["details"])
        total_q += data["total"]
        total_correct += data["correct"]
        
        for d in data["details"]:
            cat = str(d.get("category", 0))
            category_stats[cat]["total"] += 1
            if d["judgment"] == "CORRECT":
                category_stats[cat]["correct"] += 1
        
        print(f"  Conv {i}: {data['correct']}/{data['total']} = {data['accuracy']:.1f}%")
    
    accuracy = total_correct / total_q * 100 if total_q else 0
    
    merged = {
        "system": "amem_official_raw",
        "total_questions": total_q,
        "correct": total_correct,
        "accuracy": accuracy,
        "category_stats": dict(category_stats),
        "details": all_details,
    }
    
    merged_path = os.path.join(output_dir, "amem_official_raw_results.json")
    with open(merged_path, 'w') as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*60}")
    print(f"A-Mem 官方版（原始用法）LoCoMo 合并结果")
    print(f"总题数: {total_q}")
    print(f"正确数: {total_correct}")
    print(f"准确率: {accuracy:.2f}%")
    print(f"{'='*60}")
    print(f"结果已保存到: {merged_path}")
    
    return merged


def main():
    parser = argparse.ArgumentParser(description="A-Mem 官方版 LoCoMo 并行测评")
    parser.add_argument("--dataset", type=str, default="locomo10.json")
    parser.add_argument("--conversations", type=str, default="all")
    parser.add_argument("--top-k", type=int, default=20)
    parser.add_argument("--output-dir", type=str, default="results/amem_official_raw")
    parser.add_argument("--merge-only", action="store_true", help="只合并已有结果")
    args = parser.parse_args()
    
    os.makedirs(args.output_dir, exist_ok=True)
    
    # 确定对话数
    with open(args.dataset) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    num_convs = len(dataset)
    
    if args.conversations == "all":
        conv_indices = list(range(num_convs))
    else:
        conv_indices = [int(x.strip()) for x in args.conversations.split(",") if x.strip()]
    
    if args.merge_only:
        merge_results(args.output_dir, num_convs)
        return
    
    # 清除代理
    for key in ["http_proxy", "https"""
A-Mem 官方版 LoCoMo 并行测评脚本
每个对话一个进程，10个对话同时跑
"""
import json
import os
import sys
import time
import argparse
import subprocess
from pathlib import Path

def run_single_conv(conv_idx: int, dataset_path: str, output_dir: str, top_k: int):
    """单个对话的测评（子进程）"""
    # 加载数据集
    with open(dataset_path) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    
    entry = dataset[conv_idx]
    conversation = entry["conversation"]
    speaker_a = conversation["speaker_a"]
    speaker_b = conversation["speaker_b"]
    
    # 获取 sessions
    from locomo_eval import get_sorted_sessions, locomo_date_to_epoch, turns_to_text
    from locomo_eval import ANSWER_PROMPT, JUDGE_SYSTEM, JUDGE_PROMPT
    from llm_client import chat_completion, chat_completion_json, reset_token_stats, get_token_stats
    from amem_official_memory import OfficialAMemMemory
    
    sorted_sessions = get_sorted_sessions(conversation)
    
    qa_list = []
    all_qa = entry.get("qa", entry.get("qa_pairs", []))
    for i, qa in enumerate(all_qa):
        if "answer" not in qa or not qa["answer"]:
            continue
        qa_list.append((i, qa))
    
    user_id = f"locomo_amem_raw_{conv_idx}"
    
    # 每个对话独立的 A-Mem 实例
    mem = OfficialAMemMemory(db_path=os.path.join(output_dir, f"amem_raw_conv{conv_idx}.db"))
    
    print(f"[Conv {conv_idx}] {speaker_a} & {speaker_b} | {len(sorted_sessions)} sessions, {len(qa_list)} QA")
    
    # 写入记忆
    write_start = time.time()
    mem_count = 0
    for sess_idx, (session_key, date_str, turns) in enumerate(sorted_sessions):
        session_epoch = locomo_date_to_epoch(date_str) or time.time()
        date_header = f"[Conversation Date: {date_str}]\n"
        batch_size = 5
        for i in range(0, len(turns), batch_size):
            batch = turns[i:i+batch_size]
            batch_text = turns_to_text(batch, speaker_a, speaker_b)
            if batch_text.strip():
                try:
                    full_text = date_header + batch_text
                    mem.add(full_text, user_id=user_id, timestamp=session_epoch)
                    mem_count += 1
                except Exception as e:
                    print(f"  [Conv {conv_idx}] 写入失败: {e}")
    write_elapsed = time.time() - write_start
    print(f"[Conv {conv_idx}] 写入完成: {mem_count} batches, {write_elapsed:.1f}s")
    
    # 参考日期
    ref_date = sorted_sessions[-1][1] if sorted_sessions else "2023"
    
    # 答题
    conv_results = []
    conv_correct = 0
    answer_start = time.time()
    for qa_idx, (orig_idx, qa) in enumerate(qa_list):
        question = qa["question"]
        gold_answer = qa["answer"]
        category = qa.get("category", 0)
        
        # 检索
        try:
            search_results = mem.search(question, user_id=user_id, top_k=top_k)
            top_memories = [r.get("memory", "") for r in search_results[:top_k]]
        except Exception as e:
            print(f"  [Conv {conv_idx}] 检索失败 Q{qa_idx}: {e}")
            top_memories = []
        
        memory_text = "\n".join([f"- {m}" for m in top_memories])
        
        # 生成答案
        try:
            generated = chat_completion(
                system="You are a precise question-answering assistant.",
                user=ANSWER_PROMPT.format(
                    memories=memory_text[:8000],
                    question=question,
                    reference_date=ref_date
                ),
                temperature=0.1,
            )
            generated = generated.strip()
        except Exception as e:
            generated = ""
        
        # 裁判评分
        result = chat_completion_json(
            system=JUDGE_SYSTEM,
            user=JUDGE_PROMPT.format(
                question=question,
                gold_answer=gold_answer,
                generated_answer=generated
            ),
            temperature=0.1,
        )
        judgment = result.get("judgment", "INCORRECT")
        if judgment not in ("CORRECT", "INCORRECT"):
            judgment = "INCORRECT"
        
        is_correct = judgment == "CORRECT"
        if is_correct:
            conv_correct += 1
        
        conv_results.append({
            "conversation_idx": conv_idx,
            "qa_idx": orig_idx,
            "question": question,
            "gold_answer": gold_answer,
            "generated_answer": generated,
            "judgment": judgment,
            "judge_reason": result.get("reason", ""),
            "category": category,
            "top_memories": top_memories[:5],
        })
        
        if (qa_idx + 1) % 20 == 0:
            acc_so_far = conv_correct / (qa_idx + 1) * 100
            print(f"  [Conv {conv_idx}] Q{qa_idx+1}/{len(qa_list)} | acc={acc_so_far:.1f}%", flush=True)
    
    answer_elapsed = time.time() - answer_start
    acc = conv_correct / len(qa_list) * 100 if qa_list else 0
    print(f"[Conv {conv_idx}] 完成: {conv_correct}/{len(qa_list)} = {acc:.1f}% | write={write_elapsed:.0f}s answer={answer_elapsed:.0f}s")
    
    # 保存单对话结果
    result_data = {
        "conv_idx": conv_idx,
        "speaker_a": speaker_a,
        "speaker_b": speaker_b,
        "total": len(qa_list),
        "correct": conv_correct,
        "accuracy": acc,
        "write_time": write_elapsed,
        "answer_time": answer_elapsed,
        "mem_count": mem_count,
        "details": conv_results,
    }
    
    result_path = os.path.join(output_dir, f"conv{conv_idx}_result.json")
    with open(result_path, 'w') as f:
        json.dump(result_data, f, indent=2, ensure_ascii=False)
    
    mem.close()
    return result_data


def merge_results(output_dir: str, num_convs: int):
    """合并所有对话结果"""
    all_details = []
    total_q = 0
    total_correct = 0
    from collections import defaultdict
    category_stats = defaultdict(lambda: {"total": 0, "correct": 0})
    
    for i in range(num_convs):
        path = os.path.join(output_dir, f"conv{i}_result.json")
        if not os.path.exists(path):
            print(f"  对话 {i} 结果不存在，跳过")
            continue
        with open(path) as f:
            data = json.load(f)
        
        all_details.extend(data["details"])
        total_q += data["total"]
        total_correct += data["correct"]
        
        for d in data["details"]:
            cat = str(d.get("category", 0))
            category_stats[cat]["total"] += 1
            if d["judgment"] == "CORRECT":
                category_stats[cat]["correct"] += 1
        
        print(f"  Conv {i}: {data['correct']}/{data['total']} = {data['accuracy']:.1f}%")
    
    accuracy = total_correct / total_q * 100 if total_q else 0
    
    merged = {
        "system": "amem_official_raw",
        "total_questions": total_q,
        "correct": total_correct,
        "accuracy": accuracy,
        "category_stats": dict(category_stats),
        "details": all_details,
    }
    
    merged_path = os.path.join(output_dir, "amem_official_raw_results.json")
    with open(merged_path, 'w') as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*60}")
    print(f"A-Mem 官方版（原始用法）LoCoMo 合并结果")
    print(f"总题数: {total_q}")
    print(f"正确数: {total_correct}")
    print(f"准确率: {accuracy:.2f}%")
    print(f"{'='*60}")
    print(f"结果已保存到: {merged_path}")
    
    return merged


def main():
    parser = argparse.ArgumentParser(description="A-Mem 官方版 LoCoMo 并行测评")
    parser.add_argument("--dataset", type=str, default="locomo10.json")
    parser.add_argument("--conversations", type=str, default="all")
    parser.add_argument("--top-k", type=int, default=20)
    parser.add_argument("--output-dir", type=str, default="results/amem_official_raw")
    parser.add_argument("--merge-only", action="store_true", help="只合并已有结果")
    args = parser.parse_args()
    
    os.makedirs(args.output_dir, exist_ok=True)
    
    # 确定对话数
    with open(args.dataset) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    num_convs = len(dataset)
    
    if args.conversations == "all":
        conv_indices = list(range(num_convs))
    else:
        conv_indices = [int(x.strip()) for x in args.conversations.split(",") if x.strip()]
    
    if args.merge_only:
        merge_results(args.output_dir, num_convs)
        return
    
    # 清除代理
    for key in ["http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "all_proxy"]:
        os.environ.pop(key, None)
    
    # 从 ~/.hermes/.env 读 API key
    env_path = os.path.expand"""
A-Mem 官方版 LoCoMo 并行测评脚本
每个对话一个进程，10个对话同时跑
"""
import json
import os
import sys
import time
import argparse
import subprocess
from pathlib import Path

def run_single_conv(conv_idx: int, dataset_path: str, output_dir: str, top_k: int):
    """单个对话的测评（子进程）"""
    # 加载数据集
    with open(dataset_path) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    
    entry = dataset[conv_idx]
    conversation = entry["conversation"]
    speaker_a = conversation["speaker_a"]
    speaker_b = conversation["speaker_b"]
    
    # 获取 sessions
    from locomo_eval import get_sorted_sessions, locomo_date_to_epoch, turns_to_text
    from locomo_eval import ANSWER_PROMPT, JUDGE_SYSTEM, JUDGE_PROMPT
    from llm_client import chat_completion, chat_completion_json, reset_token_stats, get_token_stats
    from amem_official_memory import OfficialAMemMemory
    
    sorted_sessions = get_sorted_sessions(conversation)
    
    qa_list = []
    all_qa = entry.get("qa", entry.get("qa_pairs", []))
    for i, qa in enumerate(all_qa):
        if "answer" not in qa or not qa["answer"]:
            continue
        qa_list.append((i, qa))
    
    user_id = f"locomo_amem_raw_{conv_idx}"
    
    # 每个对话独立的 A-Mem 实例
    mem = OfficialAMemMemory(db_path=os.path.join(output_dir, f"amem_raw_conv{conv_idx}.db"))
    
    print(f"[Conv {conv_idx}] {speaker_a} & {speaker_b} | {len(sorted_sessions)} sessions, {len(qa_list)} QA")
    
    # 写入记忆
    write_start = time.time()
    mem_count = 0
    for sess_idx, (session_key, date_str, turns) in enumerate(sorted_sessions):
        session_epoch = locomo_date_to_epoch(date_str) or time.time()
        date_header = f"[Conversation Date: {date_str}]\n"
        batch_size = 5
        for i in range(0, len(turns), batch_size):
            batch = turns[i:i+batch_size]
            batch_text = turns_to_text(batch, speaker_a, speaker_b)
            if batch_text.strip():
                try:
                    full_text = date_header + batch_text
                    mem.add(full_text, user_id=user_id, timestamp=session_epoch)
                    mem_count += 1
                except Exception as e:
                    print(f"  [Conv {conv_idx}] 写入失败: {e}")
    write_elapsed = time.time() - write_start
    print(f"[Conv {conv_idx}] 写入完成: {mem_count} batches, {write_elapsed:.1f}s")
    
    # 参考日期
    ref_date = sorted_sessions[-1][1] if sorted_sessions else "2023"
    
    # 答题
    conv_results = []
    conv_correct = 0
    answer_start = time.time()
    for qa_idx, (orig_idx, qa) in enumerate(qa_list):
        question = qa["question"]
        gold_answer = qa["answer"]
        category = qa.get("category", 0)
        
        # 检索
        try:
            search_results = mem.search(question, user_id=user_id, top_k=top_k)
            top_memories = [r.get("memory", "") for r in search_results[:top_k]]
        except Exception as e:
            print(f"  [Conv {conv_idx}] 检索失败 Q{qa_idx}: {e}")
            top_memories = []
        
        memory_text = "\n".join([f"- {m}" for m in top_memories])
        
        # 生成答案
        try:
            generated = chat_completion(
                system="You are a precise question-answering assistant.",
                user=ANSWER_PROMPT.format(
                    memories=memory_text[:8000],
                    question=question,
                    reference_date=ref_date
                ),
                temperature=0.1,
            )
            generated = generated.strip()
        except Exception as e:
            generated = ""
        
        # 裁判评分
        result = chat_completion_json(
            system=JUDGE_SYSTEM,
            user=JUDGE_PROMPT.format(
                question=question,
                gold_answer=gold_answer,
                generated_answer=generated
            ),
            temperature=0.1,
        )
        judgment = result.get("judgment", "INCORRECT")
        if judgment not in ("CORRECT", "INCORRECT"):
            judgment = "INCORRECT"
        
        is_correct = judgment == "CORRECT"
        if is_correct:
            conv_correct += 1
        
        conv_results.append({
            "conversation_idx": conv_idx,
            "qa_idx": orig_idx,
            "question": question,
            "gold_answer": gold_answer,
            "generated_answer": generated,
            "judgment": judgment,
            "judge_reason": result.get("reason", ""),
            "category": category,
            "top_memories": top_memories[:5],
        })
        
        if (qa_idx + 1) % 20 == 0:
            acc_so_far = conv_correct / (qa_idx + 1) * 100
            print(f"  [Conv {conv_idx}] Q{qa_idx+1}/{len(qa_list)} | acc={acc_so_far:.1f}%", flush=True)
    
    answer_elapsed = time.time() - answer_start
    acc = conv_correct / len(qa_list) * 100 if qa_list else 0
    print(f"[Conv {conv_idx}] 完成: {conv_correct}/{len(qa_list)} = {acc:.1f}% | write={write_elapsed:.0f}s answer={answer_elapsed:.0f}s")
    
    # 保存单对话结果
    result_data = {
        "conv_idx": conv_idx,
        "speaker_a": speaker_a,
        "speaker_b": speaker_b,
        "total": len(qa_list),
        "correct": conv_correct,
        "accuracy": acc,
        "write_time": write_elapsed,
        "answer_time": answer_elapsed,
        "mem_count": mem_count,
        "details": conv_results,
    }
    
    result_path = os.path.join(output_dir, f"conv{conv_idx}_result.json")
    with open(result_path, 'w') as f:
        json.dump(result_data, f, indent=2, ensure_ascii=False)
    
    mem.close()
    return result_data


def merge_results(output_dir: str, num_convs: int):
    """合并所有对话结果"""
    all_details = []
    total_q = 0
    total_correct = 0
    from collections import defaultdict
    category_stats = defaultdict(lambda: {"total": 0, "correct": 0})
    
    for i in range(num_convs):
        path = os.path.join(output_dir, f"conv{i}_result.json")
        if not os.path.exists(path):
            print(f"  对话 {i} 结果不存在，跳过")
            continue
        with open(path) as f:
            data = json.load(f)
        
        all_details.extend(data["details"])
        total_q += data["total"]
        total_correct += data["correct"]
        
        for d in data["details"]:
            cat = str(d.get("category", 0))
            category_stats[cat]["total"] += 1
            if d["judgment"] == "CORRECT":
                category_stats[cat]["correct"] += 1
        
        print(f"  Conv {i}: {data['correct']}/{data['total']} = {data['accuracy']:.1f}%")
    
    accuracy = total_correct / total_q * 100 if total_q else 0
    
    merged = {
        "system": "amem_official_raw",
        "total_questions": total_q,
        "correct": total_correct,
        "accuracy": accuracy,
        "category_stats": dict(category_stats),
        "details": all_details,
    }
    
    merged_path = os.path.join(output_dir, "amem_official_raw_results.json")
    with open(merged_path, 'w') as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*60}")
    print(f"A-Mem 官方版（原始用法）LoCoMo 合并结果")
    print(f"总题数: {total_q}")
    print(f"正确数: {total_correct}")
    print(f"准确率: {accuracy:.2f}%")
    print(f"{'='*60}")
    print(f"结果已保存到: {merged_path}")
    
    return merged


def main():
    parser = argparse.ArgumentParser(description="A-Mem 官方版 LoCoMo 并行测评")
    parser.add_argument("--dataset", type=str, default="locomo10.json")
    parser.add_argument("--conversations", type=str, default="all")
    parser.add_argument("--top-k", type=int, default=20)
    parser.add_argument("--output-dir", type=str, default="results/amem_official_raw")
    parser.add_argument("--merge-only", action="store_true", help="只合并已有结果")
    args = parser.parse_args()
    
    os.makedirs(args.output_dir, exist_ok=True)
    
    # 确定对话数
    with open(args.dataset) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    num_convs = len(dataset)
    
    if args.conversations == "all":
        conv_indices = list(range(num_convs))
    else:
        conv_indices = [int(x.strip()) for x in args.conversations.split(",") if x.strip()]
    
    if args.merge_only:
        merge_results(args.output_dir, num_convs)
        return
    
    # 清除代理
    for key in ["http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "all_proxy"]:
        os.environ.pop(key, None)
    
    # 从 ~/.hermes/.env 读 API key
    env_path = os.path.expanduser("~/.hermes/.env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.startswith("DEEPSEEK_API_KEY="):
                    os.environ["DEEP"""
A-Mem 官方版 LoCoMo 并行测评脚本
每个对话一个进程，10个对话同时跑
"""
import json
import os
import sys
import time
import argparse
import subprocess
from pathlib import Path

def run_single_conv(conv_idx: int, dataset_path: str, output_dir: str, top_k: int):
    """单个对话的测评（子进程）"""
    # 加载数据集
    with open(dataset_path) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    
    entry = dataset[conv_idx]
    conversation = entry["conversation"]
    speaker_a = conversation["speaker_a"]
    speaker_b = conversation["speaker_b"]
    
    # 获取 sessions
    from locomo_eval import get_sorted_sessions, locomo_date_to_epoch, turns_to_text
    from locomo_eval import ANSWER_PROMPT, JUDGE_SYSTEM, JUDGE_PROMPT
    from llm_client import chat_completion, chat_completion_json, reset_token_stats, get_token_stats
    from amem_official_memory import OfficialAMemMemory
    
    sorted_sessions = get_sorted_sessions(conversation)
    
    qa_list = []
    all_qa = entry.get("qa", entry.get("qa_pairs", []))
    for i, qa in enumerate(all_qa):
        if "answer" not in qa or not qa["answer"]:
            continue
        qa_list.append((i, qa))
    
    user_id = f"locomo_amem_raw_{conv_idx}"
    
    # 每个对话独立的 A-Mem 实例
    mem = OfficialAMemMemory(db_path=os.path.join(output_dir, f"amem_raw_conv{conv_idx}.db"))
    
    print(f"[Conv {conv_idx}] {speaker_a} & {speaker_b} | {len(sorted_sessions)} sessions, {len(qa_list)} QA")
    
    # 写入记忆
    write_start = time.time()
    mem_count = 0
    for sess_idx, (session_key, date_str, turns) in enumerate(sorted_sessions):
        session_epoch = locomo_date_to_epoch(date_str) or time.time()
        date_header = f"[Conversation Date: {date_str}]\n"
        batch_size = 5
        for i in range(0, len(turns), batch_size):
            batch = turns[i:i+batch_size]
            batch_text = turns_to_text(batch, speaker_a, speaker_b)
            if batch_text.strip():
                try:
                    full_text = date_header + batch_text
                    mem.add(full_text, user_id=user_id, timestamp=session_epoch)
                    mem_count += 1
                except Exception as e:
                    print(f"  [Conv {conv_idx}] 写入失败: {e}")
    write_elapsed = time.time() - write_start
    print(f"[Conv {conv_idx}] 写入完成: {mem_count} batches, {write_elapsed:.1f}s")
    
    # 参考日期
    ref_date = sorted_sessions[-1][1] if sorted_sessions else "2023"
    
    # 答题
    conv_results = []
    conv_correct = 0
    answer_start = time.time()
    for qa_idx, (orig_idx, qa) in enumerate(qa_list):
        question = qa["question"]
        gold_answer = qa["answer"]
        category = qa.get("category", 0)
        
        # 检索
        try:
            search_results = mem.search(question, user_id=user_id, top_k=top_k)
            top_memories = [r.get("memory", "") for r in search_results[:top_k]]
        except Exception as e:
            print(f"  [Conv {conv_idx}] 检索失败 Q{qa_idx}: {e}")
            top_memories = []
        
        memory_text = "\n".join([f"- {m}" for m in top_memories])
        
        # 生成答案
        try:
            generated = chat_completion(
                system="You are a precise question-answering assistant.",
                user=ANSWER_PROMPT.format(
                    memories=memory_text[:8000],
                    question=question,
                    reference_date=ref_date
                ),
                temperature=0.1,
            )
            generated = generated.strip()
        except Exception as e:
            generated = ""
        
        # 裁判评分
        result = chat_completion_json(
            system=JUDGE_SYSTEM,
            user=JUDGE_PROMPT.format(
                question=question,
                gold_answer=gold_answer,
                generated_answer=generated
            ),
            temperature=0.1,
        )
        judgment = result.get("judgment", "INCORRECT")
        if judgment not in ("CORRECT", "INCORRECT"):
            judgment = "INCORRECT"
        
        is_correct = judgment == "CORRECT"
        if is_correct:
            conv_correct += 1
        
        conv_results.append({
            "conversation_idx": conv_idx,
            "qa_idx": orig_idx,
            "question": question,
            "gold_answer": gold_answer,
            "generated_answer": generated,
            "judgment": judgment,
            "judge_reason": result.get("reason", ""),
            "category": category,
            "top_memories": top_memories[:5],
        })
        
        if (qa_idx + 1) % 20 == 0:
            acc_so_far = conv_correct / (qa_idx + 1) * 100
            print(f"  [Conv {conv_idx}] Q{qa_idx+1}/{len(qa_list)} | acc={acc_so_far:.1f}%", flush=True)
    
    answer_elapsed = time.time() - answer_start
    acc = conv_correct / len(qa_list) * 100 if qa_list else 0
    print(f"[Conv {conv_idx}] 完成: {conv_correct}/{len(qa_list)} = {acc:.1f}% | write={write_elapsed:.0f}s answer={answer_elapsed:.0f}s")
    
    # 保存单对话结果
    result_data = {
        "conv_idx": conv_idx,
        "speaker_a": speaker_a,
        "speaker_b": speaker_b,
        "total": len(qa_list),
        "correct": conv_correct,
        "accuracy": acc,
        "write_time": write_elapsed,
        "answer_time": answer_elapsed,
        "mem_count": mem_count,
        "details": conv_results,
    }
    
    result_path = os.path.join(output_dir, f"conv{conv_idx}_result.json")
    with open(result_path, 'w') as f:
        json.dump(result_data, f, indent=2, ensure_ascii=False)
    
    mem.close()
    return result_data


def merge_results(output_dir: str, num_convs: int):
    """合并所有对话结果"""
    all_details = []
    total_q = 0
    total_correct = 0
    from collections import defaultdict
    category_stats = defaultdict(lambda: {"total": 0, "correct": 0})
    
    for i in range(num_convs):
        path = os.path.join(output_dir, f"conv{i}_result.json")
        if not os.path.exists(path):
            print(f"  对话 {i} 结果不存在，跳过")
            continue
        with open(path) as f:
            data = json.load(f)
        
        all_details.extend(data["details"])
        total_q += data["total"]
        total_correct += data["correct"]
        
        for d in data["details"]:
            cat = str(d.get("category", 0))
            category_stats[cat]["total"] += 1
            if d["judgment"] == "CORRECT":
                category_stats[cat]["correct"] += 1
        
        print(f"  Conv {i}: {data['correct']}/{data['total']} = {data['accuracy']:.1f}%")
    
    accuracy = total_correct / total_q * 100 if total_q else 0
    
    merged = {
        "system": "amem_official_raw",
        "total_questions": total_q,
        "correct": total_correct,
        "accuracy": accuracy,
        "category_stats": dict(category_stats),
        "details": all_details,
    }
    
    merged_path = os.path.join(output_dir, "amem_official_raw_results.json")
    with open(merged_path, 'w') as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*60}")
    print(f"A-Mem 官方版（原始用法）LoCoMo 合并结果")
    print(f"总题数: {total_q}")
    print(f"正确数: {total_correct}")
    print(f"准确率: {accuracy:.2f}%")
    print(f"{'='*60}")
    print(f"结果已保存到: {merged_path}")
    
    return merged


def main():
    parser = argparse.ArgumentParser(description="A-Mem 官方版 LoCoMo 并行测评")
    parser.add_argument("--dataset", type=str, default="locomo10.json")
    parser.add_argument("--conversations", type=str, default="all")
    parser.add_argument("--top-k", type=int, default=20)
    parser.add_argument("--output-dir", type=str, default="results/amem_official_raw")
    parser.add_argument("--merge-only", action="store_true", help="只合并已有结果")
    args = parser.parse_args()
    
    os.makedirs(args.output_dir, exist_ok=True)
    
    # 确定对话数
    with open(args.dataset) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    num_convs = len(dataset)
    
    if args.conversations == "all":
        conv_indices = list(range(num_convs))
    else:
        conv_indices = [int(x.strip()) for x in args.conversations.split(",") if x.strip()]
    
    if args.merge_only:
        merge_results(args.output_dir, num_convs)
        return
    
    # 清除代理
    for key in ["http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "all_proxy"]:
        os.environ.pop(key, None)
    
    # 从 ~/.hermes/.env 读 API key
    env_path = os.path.expanduser("~/.hermes/.env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.startswith("DEEPSEEK_API_KEY="):
                    os.environ["DEEPSEEK_API_KEY"] = line.strip().split("=", 1)[1]
    
    print(f"\n{'='*60}")
    print(f"A-Mem 官方版（原始用法）LoCoMo 并行测评")
    print(f"对话: {conv_indices} ({len(conv_indices)} 个并行)")
    print(f"Top-K: {args.top_k}")
    print(f"""
A-Mem 官方版 LoCoMo 并行测评脚本
每个对话一个进程，10个对话同时跑
"""
import json
import os
import sys
import time
import argparse
import subprocess
from pathlib import Path

def run_single_conv(conv_idx: int, dataset_path: str, output_dir: str, top_k: int):
    """单个对话的测评（子进程）"""
    # 加载数据集
    with open(dataset_path) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    
    entry = dataset[conv_idx]
    conversation = entry["conversation"]
    speaker_a = conversation["speaker_a"]
    speaker_b = conversation["speaker_b"]
    
    # 获取 sessions
    from locomo_eval import get_sorted_sessions, locomo_date_to_epoch, turns_to_text
    from locomo_eval import ANSWER_PROMPT, JUDGE_SYSTEM, JUDGE_PROMPT
    from llm_client import chat_completion, chat_completion_json, reset_token_stats, get_token_stats
    from amem_official_memory import OfficialAMemMemory
    
    sorted_sessions = get_sorted_sessions(conversation)
    
    qa_list = []
    all_qa = entry.get("qa", entry.get("qa_pairs", []))
    for i, qa in enumerate(all_qa):
        if "answer" not in qa or not qa["answer"]:
            continue
        qa_list.append((i, qa))
    
    user_id = f"locomo_amem_raw_{conv_idx}"
    
    # 每个对话独立的 A-Mem 实例
    mem = OfficialAMemMemory(db_path=os.path.join(output_dir, f"amem_raw_conv{conv_idx}.db"))
    
    print(f"[Conv {conv_idx}] {speaker_a} & {speaker_b} | {len(sorted_sessions)} sessions, {len(qa_list)} QA")
    
    # 写入记忆
    write_start = time.time()
    mem_count = 0
    for sess_idx, (session_key, date_str, turns) in enumerate(sorted_sessions):
        session_epoch = locomo_date_to_epoch(date_str) or time.time()
        date_header = f"[Conversation Date: {date_str}]\n"
        batch_size = 5
        for i in range(0, len(turns), batch_size):
            batch = turns[i:i+batch_size]
            batch_text = turns_to_text(batch, speaker_a, speaker_b)
            if batch_text.strip():
                try:
                    full_text = date_header + batch_text
                    mem.add(full_text, user_id=user_id, timestamp=session_epoch)
                    mem_count += 1
                except Exception as e:
                    print(f"  [Conv {conv_idx}] 写入失败: {e}")
    write_elapsed = time.time() - write_start
    print(f"[Conv {conv_idx}] 写入完成: {mem_count} batches, {write_elapsed:.1f}s")
    
    # 参考日期
    ref_date = sorted_sessions[-1][1] if sorted_sessions else "2023"
    
    # 答题
    conv_results = []
    conv_correct = 0
    answer_start = time.time()
    for qa_idx, (orig_idx, qa) in enumerate(qa_list):
        question = qa["question"]
        gold_answer = qa["answer"]
        category = qa.get("category", 0)
        
        # 检索
        try:
            search_results = mem.search(question, user_id=user_id, top_k=top_k)
            top_memories = [r.get("memory", "") for r in search_results[:top_k]]
        except Exception as e:
            print(f"  [Conv {conv_idx}] 检索失败 Q{qa_idx}: {e}")
            top_memories = []
        
        memory_text = "\n".join([f"- {m}" for m in top_memories])
        
        # 生成答案
        try:
            generated = chat_completion(
                system="You are a precise question-answering assistant.",
                user=ANSWER_PROMPT.format(
                    memories=memory_text[:8000],
                    question=question,
                    reference_date=ref_date
                ),
                temperature=0.1,
            )
            generated = generated.strip()
        except Exception as e:
            generated = ""
        
        # 裁判评分
        result = chat_completion_json(
            system=JUDGE_SYSTEM,
            user=JUDGE_PROMPT.format(
                question=question,
                gold_answer=gold_answer,
                generated_answer=generated
            ),
            temperature=0.1,
        )
        judgment = result.get("judgment", "INCORRECT")
        if judgment not in ("CORRECT", "INCORRECT"):
            judgment = "INCORRECT"
        
        is_correct = judgment == "CORRECT"
        if is_correct:
            conv_correct += 1
        
        conv_results.append({
            "conversation_idx": conv_idx,
            "qa_idx": orig_idx,
            "question": question,
            "gold_answer": gold_answer,
            "generated_answer": generated,
            "judgment": judgment,
            "judge_reason": result.get("reason", ""),
            "category": category,
            "top_memories": top_memories[:5],
        })
        
        if (qa_idx + 1) % 20 == 0:
            acc_so_far = conv_correct / (qa_idx + 1) * 100
            print(f"  [Conv {conv_idx}] Q{qa_idx+1}/{len(qa_list)} | acc={acc_so_far:.1f}%", flush=True)
    
    answer_elapsed = time.time() - answer_start
    acc = conv_correct / len(qa_list) * 100 if qa_list else 0
    print(f"[Conv {conv_idx}] 完成: {conv_correct}/{len(qa_list)} = {acc:.1f}% | write={write_elapsed:.0f}s answer={answer_elapsed:.0f}s")
    
    # 保存单对话结果
    result_data = {
        "conv_idx": conv_idx,
        "speaker_a": speaker_a,
        "speaker_b": speaker_b,
        "total": len(qa_list),
        "correct": conv_correct,
        "accuracy": acc,
        "write_time": write_elapsed,
        "answer_time": answer_elapsed,
        "mem_count": mem_count,
        "details": conv_results,
    }
    
    result_path = os.path.join(output_dir, f"conv{conv_idx}_result.json")
    with open(result_path, 'w') as f:
        json.dump(result_data, f, indent=2, ensure_ascii=False)
    
    mem.close()
    return result_data


def merge_results(output_dir: str, num_convs: int):
    """合并所有对话结果"""
    all_details = []
    total_q = 0
    total_correct = 0
    from collections import defaultdict
    category_stats = defaultdict(lambda: {"total": 0, "correct": 0})
    
    for i in range(num_convs):
        path = os.path.join(output_dir, f"conv{i}_result.json")
        if not os.path.exists(path):
            print(f"  对话 {i} 结果不存在，跳过")
            continue
        with open(path) as f:
            data = json.load(f)
        
        all_details.extend(data["details"])
        total_q += data["total"]
        total_correct += data["correct"]
        
        for d in data["details"]:
            cat = str(d.get("category", 0))
            category_stats[cat]["total"] += 1
            if d["judgment"] == "CORRECT":
                category_stats[cat]["correct"] += 1
        
        print(f"  Conv {i}: {data['correct']}/{data['total']} = {data['accuracy']:.1f}%")
    
    accuracy = total_correct / total_q * 100 if total_q else 0
    
    merged = {
        "system": "amem_official_raw",
        "total_questions": total_q,
        "correct": total_correct,
        "accuracy": accuracy,
        "category_stats": dict(category_stats),
        "details": all_details,
    }
    
    merged_path = os.path.join(output_dir, "amem_official_raw_results.json")
    with open(merged_path, 'w') as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*60}")
    print(f"A-Mem 官方版（原始用法）LoCoMo 合并结果")
    print(f"总题数: {total_q}")
    print(f"正确数: {total_correct}")
    print(f"准确率: {accuracy:.2f}%")
    print(f"{'='*60}")
    print(f"结果已保存到: {merged_path}")
    
    return merged


def main():
    parser = argparse.ArgumentParser(description="A-Mem 官方版 LoCoMo 并行测评")
    parser.add_argument("--dataset", type=str, default="locomo10.json")
    parser.add_argument("--conversations", type=str, default="all")
    parser.add_argument("--top-k", type=int, default=20)
    parser.add_argument("--output-dir", type=str, default="results/amem_official_raw")
    parser.add_argument("--merge-only", action="store_true", help="只合并已有结果")
    args = parser.parse_args()
    
    os.makedirs(args.output_dir, exist_ok=True)
    
    # 确定对话数
    with open(args.dataset) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    num_convs = len(dataset)
    
    if args.conversations == "all":
        conv_indices = list(range(num_convs))
    else:
        conv_indices = [int(x.strip()) for x in args.conversations.split(",") if x.strip()]
    
    if args.merge_only:
        merge_results(args.output_dir, num_convs)
        return
    
    # 清除代理
    for key in ["http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "all_proxy"]:
        os.environ.pop(key, None)
    
    # 从 ~/.hermes/.env 读 API key
    env_path = os.path.expanduser("~/.hermes/.env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.startswith("DEEPSEEK_API_KEY="):
                    os.environ["DEEPSEEK_API_KEY"] = line.strip().split("=", 1)[1]
    
    print(f"\n{'='*60}")
    print(f"A-Mem 官方版（原始用法）LoCoMo 并行测评")
    print(f"对话: {conv_indices} ({len(conv_indices)} 个并行)")
    print(f"Top-K: {args.top_k}")
    print(f"{'='*60}\n")
    
    start_time = time.time()
    
    # 每个对话一个子进程
    processes = []
    for conv_idx in conv_indices:
        script = f""""""
A-Mem 官方版 LoCoMo 并行测评脚本
每个对话一个进程，10个对话同时跑
"""
import json
import os
import sys
import time
import argparse
import subprocess
from pathlib import Path

def run_single_conv(conv_idx: int, dataset_path: str, output_dir: str, top_k: int):
    """单个对话的测评（子进程）"""
    # 加载数据集
    with open(dataset_path) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    
    entry = dataset[conv_idx]
    conversation = entry["conversation"]
    speaker_a = conversation["speaker_a"]
    speaker_b = conversation["speaker_b"]
    
    # 获取 sessions
    from locomo_eval import get_sorted_sessions, locomo_date_to_epoch, turns_to_text
    from locomo_eval import ANSWER_PROMPT, JUDGE_SYSTEM, JUDGE_PROMPT
    from llm_client import chat_completion, chat_completion_json, reset_token_stats, get_token_stats
    from amem_official_memory import OfficialAMemMemory
    
    sorted_sessions = get_sorted_sessions(conversation)
    
    qa_list = []
    all_qa = entry.get("qa", entry.get("qa_pairs", []))
    for i, qa in enumerate(all_qa):
        if "answer" not in qa or not qa["answer"]:
            continue
        qa_list.append((i, qa))
    
    user_id = f"locomo_amem_raw_{conv_idx}"
    
    # 每个对话独立的 A-Mem 实例
    mem = OfficialAMemMemory(db_path=os.path.join(output_dir, f"amem_raw_conv{conv_idx}.db"))
    
    print(f"[Conv {conv_idx}] {speaker_a} & {speaker_b} | {len(sorted_sessions)} sessions, {len(qa_list)} QA")
    
    # 写入记忆
    write_start = time.time()
    mem_count = 0
    for sess_idx, (session_key, date_str, turns) in enumerate(sorted_sessions):
        session_epoch = locomo_date_to_epoch(date_str) or time.time()
        date_header = f"[Conversation Date: {date_str}]\n"
        batch_size = 5
        for i in range(0, len(turns), batch_size):
            batch = turns[i:i+batch_size]
            batch_text = turns_to_text(batch, speaker_a, speaker_b)
            if batch_text.strip():
                try:
                    full_text = date_header + batch_text
                    mem.add(full_text, user_id=user_id, timestamp=session_epoch)
                    mem_count += 1
                except Exception as e:
                    print(f"  [Conv {conv_idx}] 写入失败: {e}")
    write_elapsed = time.time() - write_start
    print(f"[Conv {conv_idx}] 写入完成: {mem_count} batches, {write_elapsed:.1f}s")
    
    # 参考日期
    ref_date = sorted_sessions[-1][1] if sorted_sessions else "2023"
    
    # 答题
    conv_results = []
    conv_correct = 0
    answer_start = time.time()
    for qa_idx, (orig_idx, qa) in enumerate(qa_list):
        question = qa["question"]
        gold_answer = qa["answer"]
        category = qa.get("category", 0)
        
        # 检索
        try:
            search_results = mem.search(question, user_id=user_id, top_k=top_k)
            top_memories = [r.get("memory", "") for r in search_results[:top_k]]
        except Exception as e:
            print(f"  [Conv {conv_idx}] 检索失败 Q{qa_idx}: {e}")
            top_memories = []
        
        memory_text = "\n".join([f"- {m}" for m in top_memories])
        
        # 生成答案
        try:
            generated = chat_completion(
                system="You are a precise question-answering assistant.",
                user=ANSWER_PROMPT.format(
                    memories=memory_text[:8000],
                    question=question,
                    reference_date=ref_date
                ),
                temperature=0.1,
            )
            generated = generated.strip()
        except Exception as e:
            generated = ""
        
        # 裁判评分
        result = chat_completion_json(
            system=JUDGE_SYSTEM,
            user=JUDGE_PROMPT.format(
                question=question,
                gold_answer=gold_answer,
                generated_answer=generated
            ),
            temperature=0.1,
        )
        judgment = result.get("judgment", "INCORRECT")
        if judgment not in ("CORRECT", "INCORRECT"):
            judgment = "INCORRECT"
        
        is_correct = judgment == "CORRECT"
        if is_correct:
            conv_correct += 1
        
        conv_results.append({
            "conversation_idx": conv_idx,
            "qa_idx": orig_idx,
            "question": question,
            "gold_answer": gold_answer,
            "generated_answer": generated,
            "judgment": judgment,
            "judge_reason": result.get("reason", ""),
            "category": category,
            "top_memories": top_memories[:5],
        })
        
        if (qa_idx + 1) % 20 == 0:
            acc_so_far = conv_correct / (qa_idx + 1) * 100
            print(f"  [Conv {conv_idx}] Q{qa_idx+1}/{len(qa_list)} | acc={acc_so_far:.1f}%", flush=True)
    
    answer_elapsed = time.time() - answer_start
    acc = conv_correct / len(qa_list) * 100 if qa_list else 0
    print(f"[Conv {conv_idx}] 完成: {conv_correct}/{len(qa_list)} = {acc:.1f}% | write={write_elapsed:.0f}s answer={answer_elapsed:.0f}s")
    
    # 保存单对话结果
    result_data = {
        "conv_idx": conv_idx,
        "speaker_a": speaker_a,
        "speaker_b": speaker_b,
        "total": len(qa_list),
        "correct": conv_correct,
        "accuracy": acc,
        "write_time": write_elapsed,
        "answer_time": answer_elapsed,
        "mem_count": mem_count,
        "details": conv_results,
    }
    
    result_path = os.path.join(output_dir, f"conv{conv_idx}_result.json")
    with open(result_path, 'w') as f:
        json.dump(result_data, f, indent=2, ensure_ascii=False)
    
    mem.close()
    return result_data


def merge_results(output_dir: str, num_convs: int):
    """合并所有对话结果"""
    all_details = []
    total_q = 0
    total_correct = 0
    from collections import defaultdict
    category_stats = defaultdict(lambda: {"total": 0, "correct": 0})
    
    for i in range(num_convs):
        path = os.path.join(output_dir, f"conv{i}_result.json")
        if not os.path.exists(path):
            print(f"  对话 {i} 结果不存在，跳过")
            continue
        with open(path) as f:
            data = json.load(f)
        
        all_details.extend(data["details"])
        total_q += data["total"]
        total_correct += data["correct"]
        
        for d in data["details"]:
            cat = str(d.get("category", 0))
            category_stats[cat]["total"] += 1
            if d["judgment"] == "CORRECT":
                category_stats[cat]["correct"] += 1
        
        print(f"  Conv {i}: {data['correct']}/{data['total']} = {data['accuracy']:.1f}%")
    
    accuracy = total_correct / total_q * 100 if total_q else 0
    
    merged = {
        "system": "amem_official_raw",
        "total_questions": total_q,
        "correct": total_correct,
        "accuracy": accuracy,
        "category_stats": dict(category_stats),
        "details": all_details,
    }
    
    merged_path = os.path.join(output_dir, "amem_official_raw_results.json")
    with open(merged_path, 'w') as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*60}")
    print(f"A-Mem 官方版（原始用法）LoCoMo 合并结果")
    print(f"总题数: {total_q}")
    print(f"正确数: {total_correct}")
    print(f"准确率: {accuracy:.2f}%")
    print(f"{'='*60}")
    print(f"结果已保存到: {merged_path}")
    
    return merged


def main():
    parser = argparse.ArgumentParser(description="A-Mem 官方版 LoCoMo 并行测评")
    parser.add_argument("--dataset", type=str, default="locomo10.json")
    parser.add_argument("--conversations", type=str, default="all")
    parser.add_argument("--top-k", type=int, default=20)
    parser.add_argument("--output-dir", type=str, default="results/amem_official_raw")
    parser.add_argument("--merge-only", action="store_true", help="只合并已有结果")
    args = parser.parse_args()
    
    os.makedirs(args.output_dir, exist_ok=True)
    
    # 确定对话数
    with open(args.dataset) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    num_convs = len(dataset)
    
    if args.conversations == "all":
        conv_indices = list(range(num_convs))
    else:
        conv_indices = [int(x.strip()) for x in args.conversations.split(",") if x.strip()]
    
    if args.merge_only:
        merge_results(args.output_dir, num_convs)
        return
    
    # 清除代理
    for key in ["http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "all_proxy"]:
        os.environ.pop(key, None)
    
    # 从 ~/.hermes/.env 读 API key
    env_path = os.path.expanduser("~/.hermes/.env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.startswith("DEEPSEEK_API_KEY="):
                    os.environ["DEEPSEEK_API_KEY"] = line.strip().split("=", 1)[1]
    
    print(f"\n{'='*60}")
    print(f"A-Mem 官方版（原始用法）LoCoMo 并行测评")
    print(f"对话: {conv_indices} ({len(conv_indices)} 个并行)")
    print(f"Top-K: {args.top_k}")
    print(f"{'='*60}\n")
    
    start_time = time.time()
    
    # 每个对话一个子进程
    processes = []
    for conv_idx in conv_indices:
        script = f"""
import sys, os
sys.path.insert(0, "{os.path.dirname(os.path.abspath(__file__))}")
os.environ.pop("http_proxy", None)
os.environ.pop("https_proxy", None)
os.environ"""
A-Mem 官方版 LoCoMo 并行测评脚本
每个对话一个进程，10个对话同时跑
"""
import json
import os
import sys
import time
import argparse
import subprocess
from pathlib import Path

def run_single_conv(conv_idx: int, dataset_path: str, output_dir: str, top_k: int):
    """单个对话的测评（子进程）"""
    # 加载数据集
    with open(dataset_path) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    
    entry = dataset[conv_idx]
    conversation = entry["conversation"]
    speaker_a = conversation["speaker_a"]
    speaker_b = conversation["speaker_b"]
    
    # 获取 sessions
    from locomo_eval import get_sorted_sessions, locomo_date_to_epoch, turns_to_text
    from locomo_eval import ANSWER_PROMPT, JUDGE_SYSTEM, JUDGE_PROMPT
    from llm_client import chat_completion, chat_completion_json, reset_token_stats, get_token_stats
    from amem_official_memory import OfficialAMemMemory
    
    sorted_sessions = get_sorted_sessions(conversation)
    
    qa_list = []
    all_qa = entry.get("qa", entry.get("qa_pairs", []))
    for i, qa in enumerate(all_qa):
        if "answer" not in qa or not qa["answer"]:
            continue
        qa_list.append((i, qa))
    
    user_id = f"locomo_amem_raw_{conv_idx}"
    
    # 每个对话独立的 A-Mem 实例
    mem = OfficialAMemMemory(db_path=os.path.join(output_dir, f"amem_raw_conv{conv_idx}.db"))
    
    print(f"[Conv {conv_idx}] {speaker_a} & {speaker_b} | {len(sorted_sessions)} sessions, {len(qa_list)} QA")
    
    # 写入记忆
    write_start = time.time()
    mem_count = 0
    for sess_idx, (session_key, date_str, turns) in enumerate(sorted_sessions):
        session_epoch = locomo_date_to_epoch(date_str) or time.time()
        date_header = f"[Conversation Date: {date_str}]\n"
        batch_size = 5
        for i in range(0, len(turns), batch_size):
            batch = turns[i:i+batch_size]
            batch_text = turns_to_text(batch, speaker_a, speaker_b)
            if batch_text.strip():
                try:
                    full_text = date_header + batch_text
                    mem.add(full_text, user_id=user_id, timestamp=session_epoch)
                    mem_count += 1
                except Exception as e:
                    print(f"  [Conv {conv_idx}] 写入失败: {e}")
    write_elapsed = time.time() - write_start
    print(f"[Conv {conv_idx}] 写入完成: {mem_count} batches, {write_elapsed:.1f}s")
    
    # 参考日期
    ref_date = sorted_sessions[-1][1] if sorted_sessions else "2023"
    
    # 答题
    conv_results = []
    conv_correct = 0
    answer_start = time.time()
    for qa_idx, (orig_idx, qa) in enumerate(qa_list):
        question = qa["question"]
        gold_answer = qa["answer"]
        category = qa.get("category", 0)
        
        # 检索
        try:
            search_results = mem.search(question, user_id=user_id, top_k=top_k)
            top_memories = [r.get("memory", "") for r in search_results[:top_k]]
        except Exception as e:
            print(f"  [Conv {conv_idx}] 检索失败 Q{qa_idx}: {e}")
            top_memories = []
        
        memory_text = "\n".join([f"- {m}" for m in top_memories])
        
        # 生成答案
        try:
            generated = chat_completion(
                system="You are a precise question-answering assistant.",
                user=ANSWER_PROMPT.format(
                    memories=memory_text[:8000],
                    question=question,
                    reference_date=ref_date
                ),
                temperature=0.1,
            )
            generated = generated.strip()
        except Exception as e:
            generated = ""
        
        # 裁判评分
        result = chat_completion_json(
            system=JUDGE_SYSTEM,
            user=JUDGE_PROMPT.format(
                question=question,
                gold_answer=gold_answer,
                generated_answer=generated
            ),
            temperature=0.1,
        )
        judgment = result.get("judgment", "INCORRECT")
        if judgment not in ("CORRECT", "INCORRECT"):
            judgment = "INCORRECT"
        
        is_correct = judgment == "CORRECT"
        if is_correct:
            conv_correct += 1
        
        conv_results.append({
            "conversation_idx": conv_idx,
            "qa_idx": orig_idx,
            "question": question,
            "gold_answer": gold_answer,
            "generated_answer": generated,
            "judgment": judgment,
            "judge_reason": result.get("reason", ""),
            "category": category,
            "top_memories": top_memories[:5],
        })
        
        if (qa_idx + 1) % 20 == 0:
            acc_so_far = conv_correct / (qa_idx + 1) * 100
            print(f"  [Conv {conv_idx}] Q{qa_idx+1}/{len(qa_list)} | acc={acc_so_far:.1f}%", flush=True)
    
    answer_elapsed = time.time() - answer_start
    acc = conv_correct / len(qa_list) * 100 if qa_list else 0
    print(f"[Conv {conv_idx}] 完成: {conv_correct}/{len(qa_list)} = {acc:.1f}% | write={write_elapsed:.0f}s answer={answer_elapsed:.0f}s")
    
    # 保存单对话结果
    result_data = {
        "conv_idx": conv_idx,
        "speaker_a": speaker_a,
        "speaker_b": speaker_b,
        "total": len(qa_list),
        "correct": conv_correct,
        "accuracy": acc,
        "write_time": write_elapsed,
        "answer_time": answer_elapsed,
        "mem_count": mem_count,
        "details": conv_results,
    }
    
    result_path = os.path.join(output_dir, f"conv{conv_idx}_result.json")
    with open(result_path, 'w') as f:
        json.dump(result_data, f, indent=2, ensure_ascii=False)
    
    mem.close()
    return result_data


def merge_results(output_dir: str, num_convs: int):
    """合并所有对话结果"""
    all_details = []
    total_q = 0
    total_correct = 0
    from collections import defaultdict
    category_stats = defaultdict(lambda: {"total": 0, "correct": 0})
    
    for i in range(num_convs):
        path = os.path.join(output_dir, f"conv{i}_result.json")
        if not os.path.exists(path):
            print(f"  对话 {i} 结果不存在，跳过")
            continue
        with open(path) as f:
            data = json.load(f)
        
        all_details.extend(data["details"])
        total_q += data["total"]
        total_correct += data["correct"]
        
        for d in data["details"]:
            cat = str(d.get("category", 0))
            category_stats[cat]["total"] += 1
            if d["judgment"] == "CORRECT":
                category_stats[cat]["correct"] += 1
        
        print(f"  Conv {i}: {data['correct']}/{data['total']} = {data['accuracy']:.1f}%")
    
    accuracy = total_correct / total_q * 100 if total_q else 0
    
    merged = {
        "system": "amem_official_raw",
        "total_questions": total_q,
        "correct": total_correct,
        "accuracy": accuracy,
        "category_stats": dict(category_stats),
        "details": all_details,
    }
    
    merged_path = os.path.join(output_dir, "amem_official_raw_results.json")
    with open(merged_path, 'w') as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*60}")
    print(f"A-Mem 官方版（原始用法）LoCoMo 合并结果")
    print(f"总题数: {total_q}")
    print(f"正确数: {total_correct}")
    print(f"准确率: {accuracy:.2f}%")
    print(f"{'='*60}")
    print(f"结果已保存到: {merged_path}")
    
    return merged


def main():
    parser = argparse.ArgumentParser(description="A-Mem 官方版 LoCoMo 并行测评")
    parser.add_argument("--dataset", type=str, default="locomo10.json")
    parser.add_argument("--conversations", type=str, default="all")
    parser.add_argument("--top-k", type=int, default=20)
    parser.add_argument("--output-dir", type=str, default="results/amem_official_raw")
    parser.add_argument("--merge-only", action="store_true", help="只合并已有结果")
    args = parser.parse_args()
    
    os.makedirs(args.output_dir, exist_ok=True)
    
    # 确定对话数
    with open(args.dataset) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    num_convs = len(dataset)
    
    if args.conversations == "all":
        conv_indices = list(range(num_convs))
    else:
        conv_indices = [int(x.strip()) for x in args.conversations.split(",") if x.strip()]
    
    if args.merge_only:
        merge_results(args.output_dir, num_convs)
        return
    
    # 清除代理
    for key in ["http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "all_proxy"]:
        os.environ.pop(key, None)
    
    # 从 ~/.hermes/.env 读 API key
    env_path = os.path.expanduser("~/.hermes/.env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.startswith("DEEPSEEK_API_KEY="):
                    os.environ["DEEPSEEK_API_KEY"] = line.strip().split("=", 1)[1]
    
    print(f"\n{'='*60}")
    print(f"A-Mem 官方版（原始用法）LoCoMo 并行测评")
    print(f"对话: {conv_indices} ({len(conv_indices)} 个并行)")
    print(f"Top-K: {args.top_k}")
    print(f"{'='*60}\n")
    
    start_time = time.time()
    
    # 每个对话一个子进程
    processes = []
    for conv_idx in conv_indices:
        script = f"""
import sys, os
sys.path.insert(0, "{os.path.dirname(os.path.abspath(__file__))}")
os.environ.pop("http_proxy", None)
os.environ.pop("https_proxy", None)
os.environ.pop("HTTP_PROXY", None)
os.environ.pop("HTTPS_PROXY", None)
os.environ.pop("ALL_PROXY", None)
os.environ.pop("all_proxy", None)

env_path = os.path.expanduser("~/.hermes/.env")
if os"""
A-Mem 官方版 LoCoMo 并行测评脚本
每个对话一个进程，10个对话同时跑
"""
import json
import os
import sys
import time
import argparse
import subprocess
from pathlib import Path

def run_single_conv(conv_idx: int, dataset_path: str, output_dir: str, top_k: int):
    """单个对话的测评（子进程）"""
    # 加载数据集
    with open(dataset_path) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    
    entry = dataset[conv_idx]
    conversation = entry["conversation"]
    speaker_a = conversation["speaker_a"]
    speaker_b = conversation["speaker_b"]
    
    # 获取 sessions
    from locomo_eval import get_sorted_sessions, locomo_date_to_epoch, turns_to_text
    from locomo_eval import ANSWER_PROMPT, JUDGE_SYSTEM, JUDGE_PROMPT
    from llm_client import chat_completion, chat_completion_json, reset_token_stats, get_token_stats
    from amem_official_memory import OfficialAMemMemory
    
    sorted_sessions = get_sorted_sessions(conversation)
    
    qa_list = []
    all_qa = entry.get("qa", entry.get("qa_pairs", []))
    for i, qa in enumerate(all_qa):
        if "answer" not in qa or not qa["answer"]:
            continue
        qa_list.append((i, qa))
    
    user_id = f"locomo_amem_raw_{conv_idx}"
    
    # 每个对话独立的 A-Mem 实例
    mem = OfficialAMemMemory(db_path=os.path.join(output_dir, f"amem_raw_conv{conv_idx}.db"))
    
    print(f"[Conv {conv_idx}] {speaker_a} & {speaker_b} | {len(sorted_sessions)} sessions, {len(qa_list)} QA")
    
    # 写入记忆
    write_start = time.time()
    mem_count = 0
    for sess_idx, (session_key, date_str, turns) in enumerate(sorted_sessions):
        session_epoch = locomo_date_to_epoch(date_str) or time.time()
        date_header = f"[Conversation Date: {date_str}]\n"
        batch_size = 5
        for i in range(0, len(turns), batch_size):
            batch = turns[i:i+batch_size]
            batch_text = turns_to_text(batch, speaker_a, speaker_b)
            if batch_text.strip():
                try:
                    full_text = date_header + batch_text
                    mem.add(full_text, user_id=user_id, timestamp=session_epoch)
                    mem_count += 1
                except Exception as e:
                    print(f"  [Conv {conv_idx}] 写入失败: {e}")
    write_elapsed = time.time() - write_start
    print(f"[Conv {conv_idx}] 写入完成: {mem_count} batches, {write_elapsed:.1f}s")
    
    # 参考日期
    ref_date = sorted_sessions[-1][1] if sorted_sessions else "2023"
    
    # 答题
    conv_results = []
    conv_correct = 0
    answer_start = time.time()
    for qa_idx, (orig_idx, qa) in enumerate(qa_list):
        question = qa["question"]
        gold_answer = qa["answer"]
        category = qa.get("category", 0)
        
        # 检索
        try:
            search_results = mem.search(question, user_id=user_id, top_k=top_k)
            top_memories = [r.get("memory", "") for r in search_results[:top_k]]
        except Exception as e:
            print(f"  [Conv {conv_idx}] 检索失败 Q{qa_idx}: {e}")
            top_memories = []
        
        memory_text = "\n".join([f"- {m}" for m in top_memories])
        
        # 生成答案
        try:
            generated = chat_completion(
                system="You are a precise question-answering assistant.",
                user=ANSWER_PROMPT.format(
                    memories=memory_text[:8000],
                    question=question,
                    reference_date=ref_date
                ),
                temperature=0.1,
            )
            generated = generated.strip()
        except Exception as e:
            generated = ""
        
        # 裁判评分
        result = chat_completion_json(
            system=JUDGE_SYSTEM,
            user=JUDGE_PROMPT.format(
                question=question,
                gold_answer=gold_answer,
                generated_answer=generated
            ),
            temperature=0.1,
        )
        judgment = result.get("judgment", "INCORRECT")
        if judgment not in ("CORRECT", "INCORRECT"):
            judgment = "INCORRECT"
        
        is_correct = judgment == "CORRECT"
        if is_correct:
            conv_correct += 1
        
        conv_results.append({
            "conversation_idx": conv_idx,
            "qa_idx": orig_idx,
            "question": question,
            "gold_answer": gold_answer,
            "generated_answer": generated,
            "judgment": judgment,
            "judge_reason": result.get("reason", ""),
            "category": category,
            "top_memories": top_memories[:5],
        })
        
        if (qa_idx + 1) % 20 == 0:
            acc_so_far = conv_correct / (qa_idx + 1) * 100
            print(f"  [Conv {conv_idx}] Q{qa_idx+1}/{len(qa_list)} | acc={acc_so_far:.1f}%", flush=True)
    
    answer_elapsed = time.time() - answer_start
    acc = conv_correct / len(qa_list) * 100 if qa_list else 0
    print(f"[Conv {conv_idx}] 完成: {conv_correct}/{len(qa_list)} = {acc:.1f}% | write={write_elapsed:.0f}s answer={answer_elapsed:.0f}s")
    
    # 保存单对话结果
    result_data = {
        "conv_idx": conv_idx,
        "speaker_a": speaker_a,
        "speaker_b": speaker_b,
        "total": len(qa_list),
        "correct": conv_correct,
        "accuracy": acc,
        "write_time": write_elapsed,
        "answer_time": answer_elapsed,
        "mem_count": mem_count,
        "details": conv_results,
    }
    
    result_path = os.path.join(output_dir, f"conv{conv_idx}_result.json")
    with open(result_path, 'w') as f:
        json.dump(result_data, f, indent=2, ensure_ascii=False)
    
    mem.close()
    return result_data


def merge_results(output_dir: str, num_convs: int):
    """合并所有对话结果"""
    all_details = []
    total_q = 0
    total_correct = 0
    from collections import defaultdict
    category_stats = defaultdict(lambda: {"total": 0, "correct": 0})
    
    for i in range(num_convs):
        path = os.path.join(output_dir, f"conv{i}_result.json")
        if not os.path.exists(path):
            print(f"  对话 {i} 结果不存在，跳过")
            continue
        with open(path) as f:
            data = json.load(f)
        
        all_details.extend(data["details"])
        total_q += data["total"]
        total_correct += data["correct"]
        
        for d in data["details"]:
            cat = str(d.get("category", 0))
            category_stats[cat]["total"] += 1
            if d["judgment"] == "CORRECT":
                category_stats[cat]["correct"] += 1
        
        print(f"  Conv {i}: {data['correct']}/{data['total']} = {data['accuracy']:.1f}%")
    
    accuracy = total_correct / total_q * 100 if total_q else 0
    
    merged = {
        "system": "amem_official_raw",
        "total_questions": total_q,
        "correct": total_correct,
        "accuracy": accuracy,
        "category_stats": dict(category_stats),
        "details": all_details,
    }
    
    merged_path = os.path.join(output_dir, "amem_official_raw_results.json")
    with open(merged_path, 'w') as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*60}")
    print(f"A-Mem 官方版（原始用法）LoCoMo 合并结果")
    print(f"总题数: {total_q}")
    print(f"正确数: {total_correct}")
    print(f"准确率: {accuracy:.2f}%")
    print(f"{'='*60}")
    print(f"结果已保存到: {merged_path}")
    
    return merged


def main():
    parser = argparse.ArgumentParser(description="A-Mem 官方版 LoCoMo 并行测评")
    parser.add_argument("--dataset", type=str, default="locomo10.json")
    parser.add_argument("--conversations", type=str, default="all")
    parser.add_argument("--top-k", type=int, default=20)
    parser.add_argument("--output-dir", type=str, default="results/amem_official_raw")
    parser.add_argument("--merge-only", action="store_true", help="只合并已有结果")
    args = parser.parse_args()
    
    os.makedirs(args.output_dir, exist_ok=True)
    
    # 确定对话数
    with open(args.dataset) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    num_convs = len(dataset)
    
    if args.conversations == "all":
        conv_indices = list(range(num_convs))
    else:
        conv_indices = [int(x.strip()) for x in args.conversations.split(",") if x.strip()]
    
    if args.merge_only:
        merge_results(args.output_dir, num_convs)
        return
    
    # 清除代理
    for key in ["http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "all_proxy"]:
        os.environ.pop(key, None)
    
    # 从 ~/.hermes/.env 读 API key
    env_path = os.path.expanduser("~/.hermes/.env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.startswith("DEEPSEEK_API_KEY="):
                    os.environ["DEEPSEEK_API_KEY"] = line.strip().split("=", 1)[1]
    
    print(f"\n{'='*60}")
    print(f"A-Mem 官方版（原始用法）LoCoMo 并行测评")
    print(f"对话: {conv_indices} ({len(conv_indices)} 个并行)")
    print(f"Top-K: {args.top_k}")
    print(f"{'='*60}\n")
    
    start_time = time.time()
    
    # 每个对话一个子进程
    processes = []
    for conv_idx in conv_indices:
        script = f"""
import sys, os
sys.path.insert(0, "{os.path.dirname(os.path.abspath(__file__))}")
os.environ.pop("http_proxy", None)
os.environ.pop("https_proxy", None)
os.environ.pop("HTTP_PROXY", None)
os.environ.pop("HTTPS_PROXY", None)
os.environ.pop("ALL_PROXY", None)
os.environ.pop("all_proxy", None)

env_path = os.path.expanduser("~/.hermes/.env")
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            if line.startswith("DEEPSEEK_API_KEY="):
                os.environ["DEEPSEEK_API_KEY"] = line.strip().split(""""
A-Mem 官方版 LoCoMo 并行测评脚本
每个对话一个进程，10个对话同时跑
"""
import json
import os
import sys
import time
import argparse
import subprocess
from pathlib import Path

def run_single_conv(conv_idx: int, dataset_path: str, output_dir: str, top_k: int):
    """单个对话的测评（子进程）"""
    # 加载数据集
    with open(dataset_path) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    
    entry = dataset[conv_idx]
    conversation = entry["conversation"]
    speaker_a = conversation["speaker_a"]
    speaker_b = conversation["speaker_b"]
    
    # 获取 sessions
    from locomo_eval import get_sorted_sessions, locomo_date_to_epoch, turns_to_text
    from locomo_eval import ANSWER_PROMPT, JUDGE_SYSTEM, JUDGE_PROMPT
    from llm_client import chat_completion, chat_completion_json, reset_token_stats, get_token_stats
    from amem_official_memory import OfficialAMemMemory
    
    sorted_sessions = get_sorted_sessions(conversation)
    
    qa_list = []
    all_qa = entry.get("qa", entry.get("qa_pairs", []))
    for i, qa in enumerate(all_qa):
        if "answer" not in qa or not qa["answer"]:
            continue
        qa_list.append((i, qa))
    
    user_id = f"locomo_amem_raw_{conv_idx}"
    
    # 每个对话独立的 A-Mem 实例
    mem = OfficialAMemMemory(db_path=os.path.join(output_dir, f"amem_raw_conv{conv_idx}.db"))
    
    print(f"[Conv {conv_idx}] {speaker_a} & {speaker_b} | {len(sorted_sessions)} sessions, {len(qa_list)} QA")
    
    # 写入记忆
    write_start = time.time()
    mem_count = 0
    for sess_idx, (session_key, date_str, turns) in enumerate(sorted_sessions):
        session_epoch = locomo_date_to_epoch(date_str) or time.time()
        date_header = f"[Conversation Date: {date_str}]\n"
        batch_size = 5
        for i in range(0, len(turns), batch_size):
            batch = turns[i:i+batch_size]
            batch_text = turns_to_text(batch, speaker_a, speaker_b)
            if batch_text.strip():
                try:
                    full_text = date_header + batch_text
                    mem.add(full_text, user_id=user_id, timestamp=session_epoch)
                    mem_count += 1
                except Exception as e:
                    print(f"  [Conv {conv_idx}] 写入失败: {e}")
    write_elapsed = time.time() - write_start
    print(f"[Conv {conv_idx}] 写入完成: {mem_count} batches, {write_elapsed:.1f}s")
    
    # 参考日期
    ref_date = sorted_sessions[-1][1] if sorted_sessions else "2023"
    
    # 答题
    conv_results = []
    conv_correct = 0
    answer_start = time.time()
    for qa_idx, (orig_idx, qa) in enumerate(qa_list):
        question = qa["question"]
        gold_answer = qa["answer"]
        category = qa.get("category", 0)
        
        # 检索
        try:
            search_results = mem.search(question, user_id=user_id, top_k=top_k)
            top_memories = [r.get("memory", "") for r in search_results[:top_k]]
        except Exception as e:
            print(f"  [Conv {conv_idx}] 检索失败 Q{qa_idx}: {e}")
            top_memories = []
        
        memory_text = "\n".join([f"- {m}" for m in top_memories])
        
        # 生成答案
        try:
            generated = chat_completion(
                system="You are a precise question-answering assistant.",
                user=ANSWER_PROMPT.format(
                    memories=memory_text[:8000],
                    question=question,
                    reference_date=ref_date
                ),
                temperature=0.1,
            )
            generated = generated.strip()
        except Exception as e:
            generated = ""
        
        # 裁判评分
        result = chat_completion_json(
            system=JUDGE_SYSTEM,
            user=JUDGE_PROMPT.format(
                question=question,
                gold_answer=gold_answer,
                generated_answer=generated
            ),
            temperature=0.1,
        )
        judgment = result.get("judgment", "INCORRECT")
        if judgment not in ("CORRECT", "INCORRECT"):
            judgment = "INCORRECT"
        
        is_correct = judgment == "CORRECT"
        if is_correct:
            conv_correct += 1
        
        conv_results.append({
            "conversation_idx": conv_idx,
            "qa_idx": orig_idx,
            "question": question,
            "gold_answer": gold_answer,
            "generated_answer": generated,
            "judgment": judgment,
            "judge_reason": result.get("reason", ""),
            "category": category,
            "top_memories": top_memories[:5],
        })
        
        if (qa_idx + 1) % 20 == 0:
            acc_so_far = conv_correct / (qa_idx + 1) * 100
            print(f"  [Conv {conv_idx}] Q{qa_idx+1}/{len(qa_list)} | acc={acc_so_far:.1f}%", flush=True)
    
    answer_elapsed = time.time() - answer_start
    acc = conv_correct / len(qa_list) * 100 if qa_list else 0
    print(f"[Conv {conv_idx}] 完成: {conv_correct}/{len(qa_list)} = {acc:.1f}% | write={write_elapsed:.0f}s answer={answer_elapsed:.0f}s")
    
    # 保存单对话结果
    result_data = {
        "conv_idx": conv_idx,
        "speaker_a": speaker_a,
        "speaker_b": speaker_b,
        "total": len(qa_list),
        "correct": conv_correct,
        "accuracy": acc,
        "write_time": write_elapsed,
        "answer_time": answer_elapsed,
        "mem_count": mem_count,
        "details": conv_results,
    }
    
    result_path = os.path.join(output_dir, f"conv{conv_idx}_result.json")
    with open(result_path, 'w') as f:
        json.dump(result_data, f, indent=2, ensure_ascii=False)
    
    mem.close()
    return result_data


def merge_results(output_dir: str, num_convs: int):
    """合并所有对话结果"""
    all_details = []
    total_q = 0
    total_correct = 0
    from collections import defaultdict
    category_stats = defaultdict(lambda: {"total": 0, "correct": 0})
    
    for i in range(num_convs):
        path = os.path.join(output_dir, f"conv{i}_result.json")
        if not os.path.exists(path):
            print(f"  对话 {i} 结果不存在，跳过")
            continue
        with open(path) as f:
            data = json.load(f)
        
        all_details.extend(data["details"])
        total_q += data["total"]
        total_correct += data["correct"]
        
        for d in data["details"]:
            cat = str(d.get("category", 0))
            category_stats[cat]["total"] += 1
            if d["judgment"] == "CORRECT":
                category_stats[cat]["correct"] += 1
        
        print(f"  Conv {i}: {data['correct']}/{data['total']} = {data['accuracy']:.1f}%")
    
    accuracy = total_correct / total_q * 100 if total_q else 0
    
    merged = {
        "system": "amem_official_raw",
        "total_questions": total_q,
        "correct": total_correct,
        "accuracy": accuracy,
        "category_stats": dict(category_stats),
        "details": all_details,
    }
    
    merged_path = os.path.join(output_dir, "amem_official_raw_results.json")
    with open(merged_path, 'w') as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*60}")
    print(f"A-Mem 官方版（原始用法）LoCoMo 合并结果")
    print(f"总题数: {total_q}")
    print(f"正确数: {total_correct}")
    print(f"准确率: {accuracy:.2f}%")
    print(f"{'='*60}")
    print(f"结果已保存到: {merged_path}")
    
    return merged


def main():
    parser = argparse.ArgumentParser(description="A-Mem 官方版 LoCoMo 并行测评")
    parser.add_argument("--dataset", type=str, default="locomo10.json")
    parser.add_argument("--conversations", type=str, default="all")
    parser.add_argument("--top-k", type=int, default=20)
    parser.add_argument("--output-dir", type=str, default="results/amem_official_raw")
    parser.add_argument("--merge-only", action="store_true", help="只合并已有结果")
    args = parser.parse_args()
    
    os.makedirs(args.output_dir, exist_ok=True)
    
    # 确定对话数
    with open(args.dataset) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    num_convs = len(dataset)
    
    if args.conversations == "all":
        conv_indices = list(range(num_convs))
    else:
        conv_indices = [int(x.strip()) for x in args.conversations.split(",") if x.strip()]
    
    if args.merge_only:
        merge_results(args.output_dir, num_convs)
        return
    
    # 清除代理
    for key in ["http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "all_proxy"]:
        os.environ.pop(key, None)
    
    # 从 ~/.hermes/.env 读 API key
    env_path = os.path.expanduser("~/.hermes/.env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.startswith("DEEPSEEK_API_KEY="):
                    os.environ["DEEPSEEK_API_KEY"] = line.strip().split("=", 1)[1]
    
    print(f"\n{'='*60}")
    print(f"A-Mem 官方版（原始用法）LoCoMo 并行测评")
    print(f"对话: {conv_indices} ({len(conv_indices)} 个并行)")
    print(f"Top-K: {args.top_k}")
    print(f"{'='*60}\n")
    
    start_time = time.time()
    
    # 每个对话一个子进程
    processes = []
    for conv_idx in conv_indices:
        script = f"""
import sys, os
sys.path.insert(0, "{os.path.dirname(os.path.abspath(__file__))}")
os.environ.pop("http_proxy", None)
os.environ.pop("https_proxy", None)
os.environ.pop("HTTP_PROXY", None)
os.environ.pop("HTTPS_PROXY", None)
os.environ.pop("ALL_PROXY", None)
os.environ.pop("all_proxy", None)

env_path = os.path.expanduser("~/.hermes/.env")
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            if line.startswith("DEEPSEEK_API_KEY="):
                os.environ["DEEPSEEK_API_KEY"] = line.strip().split("=", 1)[1]

from amem_parallel_eval import run_single_conv
run_single_conv({conv_idx}, "{args.dataset}", "{args.output_dir}", {args.top_k})
"""
        log_file = os.path.join"""
A-Mem 官方版 LoCoMo 并行测评脚本
每个对话一个进程，10个对话同时跑
"""
import json
import os
import sys
import time
import argparse
import subprocess
from pathlib import Path

def run_single_conv(conv_idx: int, dataset_path: str, output_dir: str, top_k: int):
    """单个对话的测评（子进程）"""
    # 加载数据集
    with open(dataset_path) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    
    entry = dataset[conv_idx]
    conversation = entry["conversation"]
    speaker_a = conversation["speaker_a"]
    speaker_b = conversation["speaker_b"]
    
    # 获取 sessions
    from locomo_eval import get_sorted_sessions, locomo_date_to_epoch, turns_to_text
    from locomo_eval import ANSWER_PROMPT, JUDGE_SYSTEM, JUDGE_PROMPT
    from llm_client import chat_completion, chat_completion_json, reset_token_stats, get_token_stats
    from amem_official_memory import OfficialAMemMemory
    
    sorted_sessions = get_sorted_sessions(conversation)
    
    qa_list = []
    all_qa = entry.get("qa", entry.get("qa_pairs", []))
    for i, qa in enumerate(all_qa):
        if "answer" not in qa or not qa["answer"]:
            continue
        qa_list.append((i, qa))
    
    user_id = f"locomo_amem_raw_{conv_idx}"
    
    # 每个对话独立的 A-Mem 实例
    mem = OfficialAMemMemory(db_path=os.path.join(output_dir, f"amem_raw_conv{conv_idx}.db"))
    
    print(f"[Conv {conv_idx}] {speaker_a} & {speaker_b} | {len(sorted_sessions)} sessions, {len(qa_list)} QA")
    
    # 写入记忆
    write_start = time.time()
    mem_count = 0
    for sess_idx, (session_key, date_str, turns) in enumerate(sorted_sessions):
        session_epoch = locomo_date_to_epoch(date_str) or time.time()
        date_header = f"[Conversation Date: {date_str}]\n"
        batch_size = 5
        for i in range(0, len(turns), batch_size):
            batch = turns[i:i+batch_size]
            batch_text = turns_to_text(batch, speaker_a, speaker_b)
            if batch_text.strip():
                try:
                    full_text = date_header + batch_text
                    mem.add(full_text, user_id=user_id, timestamp=session_epoch)
                    mem_count += 1
                except Exception as e:
                    print(f"  [Conv {conv_idx}] 写入失败: {e}")
    write_elapsed = time.time() - write_start
    print(f"[Conv {conv_idx}] 写入完成: {mem_count} batches, {write_elapsed:.1f}s")
    
    # 参考日期
    ref_date = sorted_sessions[-1][1] if sorted_sessions else "2023"
    
    # 答题
    conv_results = []
    conv_correct = 0
    answer_start = time.time()
    for qa_idx, (orig_idx, qa) in enumerate(qa_list):
        question = qa["question"]
        gold_answer = qa["answer"]
        category = qa.get("category", 0)
        
        # 检索
        try:
            search_results = mem.search(question, user_id=user_id, top_k=top_k)
            top_memories = [r.get("memory", "") for r in search_results[:top_k]]
        except Exception as e:
            print(f"  [Conv {conv_idx}] 检索失败 Q{qa_idx}: {e}")
            top_memories = []
        
        memory_text = "\n".join([f"- {m}" for m in top_memories])
        
        # 生成答案
        try:
            generated = chat_completion(
                system="You are a precise question-answering assistant.",
                user=ANSWER_PROMPT.format(
                    memories=memory_text[:8000],
                    question=question,
                    reference_date=ref_date
                ),
                temperature=0.1,
            )
            generated = generated.strip()
        except Exception as e:
            generated = ""
        
        # 裁判评分
        result = chat_completion_json(
            system=JUDGE_SYSTEM,
            user=JUDGE_PROMPT.format(
                question=question,
                gold_answer=gold_answer,
                generated_answer=generated
            ),
            temperature=0.1,
        )
        judgment = result.get("judgment", "INCORRECT")
        if judgment not in ("CORRECT", "INCORRECT"):
            judgment = "INCORRECT"
        
        is_correct = judgment == "CORRECT"
        if is_correct:
            conv_correct += 1
        
        conv_results.append({
            "conversation_idx": conv_idx,
            "qa_idx": orig_idx,
            "question": question,
            "gold_answer": gold_answer,
            "generated_answer": generated,
            "judgment": judgment,
            "judge_reason": result.get("reason", ""),
            "category": category,
            "top_memories": top_memories[:5],
        })
        
        if (qa_idx + 1) % 20 == 0:
            acc_so_far = conv_correct / (qa_idx + 1) * 100
            print(f"  [Conv {conv_idx}] Q{qa_idx+1}/{len(qa_list)} | acc={acc_so_far:.1f}%", flush=True)
    
    answer_elapsed = time.time() - answer_start
    acc = conv_correct / len(qa_list) * 100 if qa_list else 0
    print(f"[Conv {conv_idx}] 完成: {conv_correct}/{len(qa_list)} = {acc:.1f}% | write={write_elapsed:.0f}s answer={answer_elapsed:.0f}s")
    
    # 保存单对话结果
    result_data = {
        "conv_idx": conv_idx,
        "speaker_a": speaker_a,
        "speaker_b": speaker_b,
        "total": len(qa_list),
        "correct": conv_correct,
        "accuracy": acc,
        "write_time": write_elapsed,
        "answer_time": answer_elapsed,
        "mem_count": mem_count,
        "details": conv_results,
    }
    
    result_path = os.path.join(output_dir, f"conv{conv_idx}_result.json")
    with open(result_path, 'w') as f:
        json.dump(result_data, f, indent=2, ensure_ascii=False)
    
    mem.close()
    return result_data


def merge_results(output_dir: str, num_convs: int):
    """合并所有对话结果"""
    all_details = []
    total_q = 0
    total_correct = 0
    from collections import defaultdict
    category_stats = defaultdict(lambda: {"total": 0, "correct": 0})
    
    for i in range(num_convs):
        path = os.path.join(output_dir, f"conv{i}_result.json")
        if not os.path.exists(path):
            print(f"  对话 {i} 结果不存在，跳过")
            continue
        with open(path) as f:
            data = json.load(f)
        
        all_details.extend(data["details"])
        total_q += data["total"]
        total_correct += data["correct"]
        
        for d in data["details"]:
            cat = str(d.get("category", 0))
            category_stats[cat]["total"] += 1
            if d["judgment"] == "CORRECT":
                category_stats[cat]["correct"] += 1
        
        print(f"  Conv {i}: {data['correct']}/{data['total']} = {data['accuracy']:.1f}%")
    
    accuracy = total_correct / total_q * 100 if total_q else 0
    
    merged = {
        "system": "amem_official_raw",
        "total_questions": total_q,
        "correct": total_correct,
        "accuracy": accuracy,
        "category_stats": dict(category_stats),
        "details": all_details,
    }
    
    merged_path = os.path.join(output_dir, "amem_official_raw_results.json")
    with open(merged_path, 'w') as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*60}")
    print(f"A-Mem 官方版（原始用法）LoCoMo 合并结果")
    print(f"总题数: {total_q}")
    print(f"正确数: {total_correct}")
    print(f"准确率: {accuracy:.2f}%")
    print(f"{'='*60}")
    print(f"结果已保存到: {merged_path}")
    
    return merged


def main():
    parser = argparse.ArgumentParser(description="A-Mem 官方版 LoCoMo 并行测评")
    parser.add_argument("--dataset", type=str, default="locomo10.json")
    parser.add_argument("--conversations", type=str, default="all")
    parser.add_argument("--top-k", type=int, default=20)
    parser.add_argument("--output-dir", type=str, default="results/amem_official_raw")
    parser.add_argument("--merge-only", action="store_true", help="只合并已有结果")
    args = parser.parse_args()
    
    os.makedirs(args.output_dir, exist_ok=True)
    
    # 确定对话数
    with open(args.dataset) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    num_convs = len(dataset)
    
    if args.conversations == "all":
        conv_indices = list(range(num_convs))
    else:
        conv_indices = [int(x.strip()) for x in args.conversations.split(",") if x.strip()]
    
    if args.merge_only:
        merge_results(args.output_dir, num_convs)
        return
    
    # 清除代理
    for key in ["http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "all_proxy"]:
        os.environ.pop(key, None)
    
    # 从 ~/.hermes/.env 读 API key
    env_path = os.path.expanduser("~/.hermes/.env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.startswith("DEEPSEEK_API_KEY="):
                    os.environ["DEEPSEEK_API_KEY"] = line.strip().split("=", 1)[1]
    
    print(f"\n{'='*60}")
    print(f"A-Mem 官方版（原始用法）LoCoMo 并行测评")
    print(f"对话: {conv_indices} ({len(conv_indices)} 个并行)")
    print(f"Top-K: {args.top_k}")
    print(f"{'='*60}\n")
    
    start_time = time.time()
    
    # 每个对话一个子进程
    processes = []
    for conv_idx in conv_indices:
        script = f"""
import sys, os
sys.path.insert(0, "{os.path.dirname(os.path.abspath(__file__))}")
os.environ.pop("http_proxy", None)
os.environ.pop("https_proxy", None)
os.environ.pop("HTTP_PROXY", None)
os.environ.pop("HTTPS_PROXY", None)
os.environ.pop("ALL_PROXY", None)
os.environ.pop("all_proxy", None)

env_path = os.path.expanduser("~/.hermes/.env")
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            if line.startswith("DEEPSEEK_API_KEY="):
                os.environ["DEEPSEEK_API_KEY"] = line.strip().split("=", 1)[1]

from amem_parallel_eval import run_single_conv
run_single_conv({conv_idx}, "{args.dataset}", "{args.output_dir}", {args.top_k})
"""
        log_file = os.path.join(args.output_dir, f"conv{conv_idx}.log")
        proc = subprocess.Popen(
            [sys.executable, "-u", "-c", script],
            stdout=open(log_file, 'w'),
            stderr=subprocess"""
A-Mem 官方版 LoCoMo 并行测评脚本
每个对话一个进程，10个对话同时跑
"""
import json
import os
import sys
import time
import argparse
import subprocess
from pathlib import Path

def run_single_conv(conv_idx: int, dataset_path: str, output_dir: str, top_k: int):
    """单个对话的测评（子进程）"""
    # 加载数据集
    with open(dataset_path) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    
    entry = dataset[conv_idx]
    conversation = entry["conversation"]
    speaker_a = conversation["speaker_a"]
    speaker_b = conversation["speaker_b"]
    
    # 获取 sessions
    from locomo_eval import get_sorted_sessions, locomo_date_to_epoch, turns_to_text
    from locomo_eval import ANSWER_PROMPT, JUDGE_SYSTEM, JUDGE_PROMPT
    from llm_client import chat_completion, chat_completion_json, reset_token_stats, get_token_stats
    from amem_official_memory import OfficialAMemMemory
    
    sorted_sessions = get_sorted_sessions(conversation)
    
    qa_list = []
    all_qa = entry.get("qa", entry.get("qa_pairs", []))
    for i, qa in enumerate(all_qa):
        if "answer" not in qa or not qa["answer"]:
            continue
        qa_list.append((i, qa))
    
    user_id = f"locomo_amem_raw_{conv_idx}"
    
    # 每个对话独立的 A-Mem 实例
    mem = OfficialAMemMemory(db_path=os.path.join(output_dir, f"amem_raw_conv{conv_idx}.db"))
    
    print(f"[Conv {conv_idx}] {speaker_a} & {speaker_b} | {len(sorted_sessions)} sessions, {len(qa_list)} QA")
    
    # 写入记忆
    write_start = time.time()
    mem_count = 0
    for sess_idx, (session_key, date_str, turns) in enumerate(sorted_sessions):
        session_epoch = locomo_date_to_epoch(date_str) or time.time()
        date_header = f"[Conversation Date: {date_str}]\n"
        batch_size = 5
        for i in range(0, len(turns), batch_size):
            batch = turns[i:i+batch_size]
            batch_text = turns_to_text(batch, speaker_a, speaker_b)
            if batch_text.strip():
                try:
                    full_text = date_header + batch_text
                    mem.add(full_text, user_id=user_id, timestamp=session_epoch)
                    mem_count += 1
                except Exception as e:
                    print(f"  [Conv {conv_idx}] 写入失败: {e}")
    write_elapsed = time.time() - write_start
    print(f"[Conv {conv_idx}] 写入完成: {mem_count} batches, {write_elapsed:.1f}s")
    
    # 参考日期
    ref_date = sorted_sessions[-1][1] if sorted_sessions else "2023"
    
    # 答题
    conv_results = []
    conv_correct = 0
    answer_start = time.time()
    for qa_idx, (orig_idx, qa) in enumerate(qa_list):
        question = qa["question"]
        gold_answer = qa["answer"]
        category = qa.get("category", 0)
        
        # 检索
        try:
            search_results = mem.search(question, user_id=user_id, top_k=top_k)
            top_memories = [r.get("memory", "") for r in search_results[:top_k]]
        except Exception as e:
            print(f"  [Conv {conv_idx}] 检索失败 Q{qa_idx}: {e}")
            top_memories = []
        
        memory_text = "\n".join([f"- {m}" for m in top_memories])
        
        # 生成答案
        try:
            generated = chat_completion(
                system="You are a precise question-answering assistant.",
                user=ANSWER_PROMPT.format(
                    memories=memory_text[:8000],
                    question=question,
                    reference_date=ref_date
                ),
                temperature=0.1,
            )
            generated = generated.strip()
        except Exception as e:
            generated = ""
        
        # 裁判评分
        result = chat_completion_json(
            system=JUDGE_SYSTEM,
            user=JUDGE_PROMPT.format(
                question=question,
                gold_answer=gold_answer,
                generated_answer=generated
            ),
            temperature=0.1,
        )
        judgment = result.get("judgment", "INCORRECT")
        if judgment not in ("CORRECT", "INCORRECT"):
            judgment = "INCORRECT"
        
        is_correct = judgment == "CORRECT"
        if is_correct:
            conv_correct += 1
        
        conv_results.append({
            "conversation_idx": conv_idx,
            "qa_idx": orig_idx,
            "question": question,
            "gold_answer": gold_answer,
            "generated_answer": generated,
            "judgment": judgment,
            "judge_reason": result.get("reason", ""),
            "category": category,
            "top_memories": top_memories[:5],
        })
        
        if (qa_idx + 1) % 20 == 0:
            acc_so_far = conv_correct / (qa_idx + 1) * 100
            print(f"  [Conv {conv_idx}] Q{qa_idx+1}/{len(qa_list)} | acc={acc_so_far:.1f}%", flush=True)
    
    answer_elapsed = time.time() - answer_start
    acc = conv_correct / len(qa_list) * 100 if qa_list else 0
    print(f"[Conv {conv_idx}] 完成: {conv_correct}/{len(qa_list)} = {acc:.1f}% | write={write_elapsed:.0f}s answer={answer_elapsed:.0f}s")
    
    # 保存单对话结果
    result_data = {
        "conv_idx": conv_idx,
        "speaker_a": speaker_a,
        "speaker_b": speaker_b,
        "total": len(qa_list),
        "correct": conv_correct,
        "accuracy": acc,
        "write_time": write_elapsed,
        "answer_time": answer_elapsed,
        "mem_count": mem_count,
        "details": conv_results,
    }
    
    result_path = os.path.join(output_dir, f"conv{conv_idx}_result.json")
    with open(result_path, 'w') as f:
        json.dump(result_data, f, indent=2, ensure_ascii=False)
    
    mem.close()
    return result_data


def merge_results(output_dir: str, num_convs: int):
    """合并所有对话结果"""
    all_details = []
    total_q = 0
    total_correct = 0
    from collections import defaultdict
    category_stats = defaultdict(lambda: {"total": 0, "correct": 0})
    
    for i in range(num_convs):
        path = os.path.join(output_dir, f"conv{i}_result.json")
        if not os.path.exists(path):
            print(f"  对话 {i} 结果不存在，跳过")
            continue
        with open(path) as f:
            data = json.load(f)
        
        all_details.extend(data["details"])
        total_q += data["total"]
        total_correct += data["correct"]
        
        for d in data["details"]:
            cat = str(d.get("category", 0))
            category_stats[cat]["total"] += 1
            if d["judgment"] == "CORRECT":
                category_stats[cat]["correct"] += 1
        
        print(f"  Conv {i}: {data['correct']}/{data['total']} = {data['accuracy']:.1f}%")
    
    accuracy = total_correct / total_q * 100 if total_q else 0
    
    merged = {
        "system": "amem_official_raw",
        "total_questions": total_q,
        "correct": total_correct,
        "accuracy": accuracy,
        "category_stats": dict(category_stats),
        "details": all_details,
    }
    
    merged_path = os.path.join(output_dir, "amem_official_raw_results.json")
    with open(merged_path, 'w') as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*60}")
    print(f"A-Mem 官方版（原始用法）LoCoMo 合并结果")
    print(f"总题数: {total_q}")
    print(f"正确数: {total_correct}")
    print(f"准确率: {accuracy:.2f}%")
    print(f"{'='*60}")
    print(f"结果已保存到: {merged_path}")
    
    return merged


def main():
    parser = argparse.ArgumentParser(description="A-Mem 官方版 LoCoMo 并行测评")
    parser.add_argument("--dataset", type=str, default="locomo10.json")
    parser.add_argument("--conversations", type=str, default="all")
    parser.add_argument("--top-k", type=int, default=20)
    parser.add_argument("--output-dir", type=str, default="results/amem_official_raw")
    parser.add_argument("--merge-only", action="store_true", help="只合并已有结果")
    args = parser.parse_args()
    
    os.makedirs(args.output_dir, exist_ok=True)
    
    # 确定对话数
    with open(args.dataset) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    num_convs = len(dataset)
    
    if args.conversations == "all":
        conv_indices = list(range(num_convs))
    else:
        conv_indices = [int(x.strip()) for x in args.conversations.split(",") if x.strip()]
    
    if args.merge_only:
        merge_results(args.output_dir, num_convs)
        return
    
    # 清除代理
    for key in ["http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "all_proxy"]:
        os.environ.pop(key, None)
    
    # 从 ~/.hermes/.env 读 API key
    env_path = os.path.expanduser("~/.hermes/.env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.startswith("DEEPSEEK_API_KEY="):
                    os.environ["DEEPSEEK_API_KEY"] = line.strip().split("=", 1)[1]
    
    print(f"\n{'='*60}")
    print(f"A-Mem 官方版（原始用法）LoCoMo 并行测评")
    print(f"对话: {conv_indices} ({len(conv_indices)} 个并行)")
    print(f"Top-K: {args.top_k}")
    print(f"{'='*60}\n")
    
    start_time = time.time()
    
    # 每个对话一个子进程
    processes = []
    for conv_idx in conv_indices:
        script = f"""
import sys, os
sys.path.insert(0, "{os.path.dirname(os.path.abspath(__file__))}")
os.environ.pop("http_proxy", None)
os.environ.pop("https_proxy", None)
os.environ.pop("HTTP_PROXY", None)
os.environ.pop("HTTPS_PROXY", None)
os.environ.pop("ALL_PROXY", None)
os.environ.pop("all_proxy", None)

env_path = os.path.expanduser("~/.hermes/.env")
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            if line.startswith("DEEPSEEK_API_KEY="):
                os.environ["DEEPSEEK_API_KEY"] = line.strip().split("=", 1)[1]

from amem_parallel_eval import run_single_conv
run_single_conv({conv_idx}, "{args.dataset}", "{args.output_dir}", {args.top_k})
"""
        log_file = os.path.join(args.output_dir, f"conv{conv_idx}.log")
        proc = subprocess.Popen(
            [sys.executable, "-u", "-c", script],
            stdout=open(log_file, 'w'),
            stderr=subprocess.STDOUT,
        )
        processes.append((conv_idx, proc, log_file))
        print(f"  启动 Conv {conv_idx} (PID {proc.pid}) ->"""
A-Mem 官方版 LoCoMo 并行测评脚本
每个对话一个进程，10个对话同时跑
"""
import json
import os
import sys
import time
import argparse
import subprocess
from pathlib import Path

def run_single_conv(conv_idx: int, dataset_path: str, output_dir: str, top_k: int):
    """单个对话的测评（子进程）"""
    # 加载数据集
    with open(dataset_path) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    
    entry = dataset[conv_idx]
    conversation = entry["conversation"]
    speaker_a = conversation["speaker_a"]
    speaker_b = conversation["speaker_b"]
    
    # 获取 sessions
    from locomo_eval import get_sorted_sessions, locomo_date_to_epoch, turns_to_text
    from locomo_eval import ANSWER_PROMPT, JUDGE_SYSTEM, JUDGE_PROMPT
    from llm_client import chat_completion, chat_completion_json, reset_token_stats, get_token_stats
    from amem_official_memory import OfficialAMemMemory
    
    sorted_sessions = get_sorted_sessions(conversation)
    
    qa_list = []
    all_qa = entry.get("qa", entry.get("qa_pairs", []))
    for i, qa in enumerate(all_qa):
        if "answer" not in qa or not qa["answer"]:
            continue
        qa_list.append((i, qa))
    
    user_id = f"locomo_amem_raw_{conv_idx}"
    
    # 每个对话独立的 A-Mem 实例
    mem = OfficialAMemMemory(db_path=os.path.join(output_dir, f"amem_raw_conv{conv_idx}.db"))
    
    print(f"[Conv {conv_idx}] {speaker_a} & {speaker_b} | {len(sorted_sessions)} sessions, {len(qa_list)} QA")
    
    # 写入记忆
    write_start = time.time()
    mem_count = 0
    for sess_idx, (session_key, date_str, turns) in enumerate(sorted_sessions):
        session_epoch = locomo_date_to_epoch(date_str) or time.time()
        date_header = f"[Conversation Date: {date_str}]\n"
        batch_size = 5
        for i in range(0, len(turns), batch_size):
            batch = turns[i:i+batch_size]
            batch_text = turns_to_text(batch, speaker_a, speaker_b)
            if batch_text.strip():
                try:
                    full_text = date_header + batch_text
                    mem.add(full_text, user_id=user_id, timestamp=session_epoch)
                    mem_count += 1
                except Exception as e:
                    print(f"  [Conv {conv_idx}] 写入失败: {e}")
    write_elapsed = time.time() - write_start
    print(f"[Conv {conv_idx}] 写入完成: {mem_count} batches, {write_elapsed:.1f}s")
    
    # 参考日期
    ref_date = sorted_sessions[-1][1] if sorted_sessions else "2023"
    
    # 答题
    conv_results = []
    conv_correct = 0
    answer_start = time.time()
    for qa_idx, (orig_idx, qa) in enumerate(qa_list):
        question = qa["question"]
        gold_answer = qa["answer"]
        category = qa.get("category", 0)
        
        # 检索
        try:
            search_results = mem.search(question, user_id=user_id, top_k=top_k)
            top_memories = [r.get("memory", "") for r in search_results[:top_k]]
        except Exception as e:
            print(f"  [Conv {conv_idx}] 检索失败 Q{qa_idx}: {e}")
            top_memories = []
        
        memory_text = "\n".join([f"- {m}" for m in top_memories])
        
        # 生成答案
        try:
            generated = chat_completion(
                system="You are a precise question-answering assistant.",
                user=ANSWER_PROMPT.format(
                    memories=memory_text[:8000],
                    question=question,
                    reference_date=ref_date
                ),
                temperature=0.1,
            )
            generated = generated.strip()
        except Exception as e:
            generated = ""
        
        # 裁判评分
        result = chat_completion_json(
            system=JUDGE_SYSTEM,
            user=JUDGE_PROMPT.format(
                question=question,
                gold_answer=gold_answer,
                generated_answer=generated
            ),
            temperature=0.1,
        )
        judgment = result.get("judgment", "INCORRECT")
        if judgment not in ("CORRECT", "INCORRECT"):
            judgment = "INCORRECT"
        
        is_correct = judgment == "CORRECT"
        if is_correct:
            conv_correct += 1
        
        conv_results.append({
            "conversation_idx": conv_idx,
            "qa_idx": orig_idx,
            "question": question,
            "gold_answer": gold_answer,
            "generated_answer": generated,
            "judgment": judgment,
            "judge_reason": result.get("reason", ""),
            "category": category,
            "top_memories": top_memories[:5],
        })
        
        if (qa_idx + 1) % 20 == 0:
            acc_so_far = conv_correct / (qa_idx + 1) * 100
            print(f"  [Conv {conv_idx}] Q{qa_idx+1}/{len(qa_list)} | acc={acc_so_far:.1f}%", flush=True)
    
    answer_elapsed = time.time() - answer_start
    acc = conv_correct / len(qa_list) * 100 if qa_list else 0
    print(f"[Conv {conv_idx}] 完成: {conv_correct}/{len(qa_list)} = {acc:.1f}% | write={write_elapsed:.0f}s answer={answer_elapsed:.0f}s")
    
    # 保存单对话结果
    result_data = {
        "conv_idx": conv_idx,
        "speaker_a": speaker_a,
        "speaker_b": speaker_b,
        "total": len(qa_list),
        "correct": conv_correct,
        "accuracy": acc,
        "write_time": write_elapsed,
        "answer_time": answer_elapsed,
        "mem_count": mem_count,
        "details": conv_results,
    }
    
    result_path = os.path.join(output_dir, f"conv{conv_idx}_result.json")
    with open(result_path, 'w') as f:
        json.dump(result_data, f, indent=2, ensure_ascii=False)
    
    mem.close()
    return result_data


def merge_results(output_dir: str, num_convs: int):
    """合并所有对话结果"""
    all_details = []
    total_q = 0
    total_correct = 0
    from collections import defaultdict
    category_stats = defaultdict(lambda: {"total": 0, "correct": 0})
    
    for i in range(num_convs):
        path = os.path.join(output_dir, f"conv{i}_result.json")
        if not os.path.exists(path):
            print(f"  对话 {i} 结果不存在，跳过")
            continue
        with open(path) as f:
            data = json.load(f)
        
        all_details.extend(data["details"])
        total_q += data["total"]
        total_correct += data["correct"]
        
        for d in data["details"]:
            cat = str(d.get("category", 0))
            category_stats[cat]["total"] += 1
            if d["judgment"] == "CORRECT":
                category_stats[cat]["correct"] += 1
        
        print(f"  Conv {i}: {data['correct']}/{data['total']} = {data['accuracy']:.1f}%")
    
    accuracy = total_correct / total_q * 100 if total_q else 0
    
    merged = {
        "system": "amem_official_raw",
        "total_questions": total_q,
        "correct": total_correct,
        "accuracy": accuracy,
        "category_stats": dict(category_stats),
        "details": all_details,
    }
    
    merged_path = os.path.join(output_dir, "amem_official_raw_results.json")
    with open(merged_path, 'w') as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*60}")
    print(f"A-Mem 官方版（原始用法）LoCoMo 合并结果")
    print(f"总题数: {total_q}")
    print(f"正确数: {total_correct}")
    print(f"准确率: {accuracy:.2f}%")
    print(f"{'='*60}")
    print(f"结果已保存到: {merged_path}")
    
    return merged


def main():
    parser = argparse.ArgumentParser(description="A-Mem 官方版 LoCoMo 并行测评")
    parser.add_argument("--dataset", type=str, default="locomo10.json")
    parser.add_argument("--conversations", type=str, default="all")
    parser.add_argument("--top-k", type=int, default=20)
    parser.add_argument("--output-dir", type=str, default="results/amem_official_raw")
    parser.add_argument("--merge-only", action="store_true", help="只合并已有结果")
    args = parser.parse_args()
    
    os.makedirs(args.output_dir, exist_ok=True)
    
    # 确定对话数
    with open(args.dataset) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    num_convs = len(dataset)
    
    if args.conversations == "all":
        conv_indices = list(range(num_convs))
    else:
        conv_indices = [int(x.strip()) for x in args.conversations.split(",") if x.strip()]
    
    if args.merge_only:
        merge_results(args.output_dir, num_convs)
        return
    
    # 清除代理
    for key in ["http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "all_proxy"]:
        os.environ.pop(key, None)
    
    # 从 ~/.hermes/.env 读 API key
    env_path = os.path.expanduser("~/.hermes/.env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.startswith("DEEPSEEK_API_KEY="):
                    os.environ["DEEPSEEK_API_KEY"] = line.strip().split("=", 1)[1]
    
    print(f"\n{'='*60}")
    print(f"A-Mem 官方版（原始用法）LoCoMo 并行测评")
    print(f"对话: {conv_indices} ({len(conv_indices)} 个并行)")
    print(f"Top-K: {args.top_k}")
    print(f"{'='*60}\n")
    
    start_time = time.time()
    
    # 每个对话一个子进程
    processes = []
    for conv_idx in conv_indices:
        script = f"""
import sys, os
sys.path.insert(0, "{os.path.dirname(os.path.abspath(__file__))}")
os.environ.pop("http_proxy", None)
os.environ.pop("https_proxy", None)
os.environ.pop("HTTP_PROXY", None)
os.environ.pop("HTTPS_PROXY", None)
os.environ.pop("ALL_PROXY", None)
os.environ.pop("all_proxy", None)

env_path = os.path.expanduser("~/.hermes/.env")
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            if line.startswith("DEEPSEEK_API_KEY="):
                os.environ["DEEPSEEK_API_KEY"] = line.strip().split("=", 1)[1]

from amem_parallel_eval import run_single_conv
run_single_conv({conv_idx}, "{args.dataset}", "{args.output_dir}", {args.top_k})
"""
        log_file = os.path.join(args.output_dir, f"conv{conv_idx}.log")
        proc = subprocess.Popen(
            [sys.executable, "-u", "-c", script],
            stdout=open(log_file, 'w'),
            stderr=subprocess.STDOUT,
        )
        processes.append((conv_idx, proc, log_file))
        print(f"  启动 Conv {conv_idx} (PID {proc.pid}) -> {log_file}")
    
    # 等待所有进程
    for conv_idx, proc, log_file in processes:
        proc.wait()
        print(f"  Conv {conv_idx} 完成"""
A-Mem 官方版 LoCoMo 并行测评脚本
每个对话一个进程，10个对话同时跑
"""
import json
import os
import sys
import time
import argparse
import subprocess
from pathlib import Path

def run_single_conv(conv_idx: int, dataset_path: str, output_dir: str, top_k: int):
    """单个对话的测评（子进程）"""
    # 加载数据集
    with open(dataset_path) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    
    entry = dataset[conv_idx]
    conversation = entry["conversation"]
    speaker_a = conversation["speaker_a"]
    speaker_b = conversation["speaker_b"]
    
    # 获取 sessions
    from locomo_eval import get_sorted_sessions, locomo_date_to_epoch, turns_to_text
    from locomo_eval import ANSWER_PROMPT, JUDGE_SYSTEM, JUDGE_PROMPT
    from llm_client import chat_completion, chat_completion_json, reset_token_stats, get_token_stats
    from amem_official_memory import OfficialAMemMemory
    
    sorted_sessions = get_sorted_sessions(conversation)
    
    qa_list = []
    all_qa = entry.get("qa", entry.get("qa_pairs", []))
    for i, qa in enumerate(all_qa):
        if "answer" not in qa or not qa["answer"]:
            continue
        qa_list.append((i, qa))
    
    user_id = f"locomo_amem_raw_{conv_idx}"
    
    # 每个对话独立的 A-Mem 实例
    mem = OfficialAMemMemory(db_path=os.path.join(output_dir, f"amem_raw_conv{conv_idx}.db"))
    
    print(f"[Conv {conv_idx}] {speaker_a} & {speaker_b} | {len(sorted_sessions)} sessions, {len(qa_list)} QA")
    
    # 写入记忆
    write_start = time.time()
    mem_count = 0
    for sess_idx, (session_key, date_str, turns) in enumerate(sorted_sessions):
        session_epoch = locomo_date_to_epoch(date_str) or time.time()
        date_header = f"[Conversation Date: {date_str}]\n"
        batch_size = 5
        for i in range(0, len(turns), batch_size):
            batch = turns[i:i+batch_size]
            batch_text = turns_to_text(batch, speaker_a, speaker_b)
            if batch_text.strip():
                try:
                    full_text = date_header + batch_text
                    mem.add(full_text, user_id=user_id, timestamp=session_epoch)
                    mem_count += 1
                except Exception as e:
                    print(f"  [Conv {conv_idx}] 写入失败: {e}")
    write_elapsed = time.time() - write_start
    print(f"[Conv {conv_idx}] 写入完成: {mem_count} batches, {write_elapsed:.1f}s")
    
    # 参考日期
    ref_date = sorted_sessions[-1][1] if sorted_sessions else "2023"
    
    # 答题
    conv_results = []
    conv_correct = 0
    answer_start = time.time()
    for qa_idx, (orig_idx, qa) in enumerate(qa_list):
        question = qa["question"]
        gold_answer = qa["answer"]
        category = qa.get("category", 0)
        
        # 检索
        try:
            search_results = mem.search(question, user_id=user_id, top_k=top_k)
            top_memories = [r.get("memory", "") for r in search_results[:top_k]]
        except Exception as e:
            print(f"  [Conv {conv_idx}] 检索失败 Q{qa_idx}: {e}")
            top_memories = []
        
        memory_text = "\n".join([f"- {m}" for m in top_memories])
        
        # 生成答案
        try:
            generated = chat_completion(
                system="You are a precise question-answering assistant.",
                user=ANSWER_PROMPT.format(
                    memories=memory_text[:8000],
                    question=question,
                    reference_date=ref_date
                ),
                temperature=0.1,
            )
            generated = generated.strip()
        except Exception as e:
            generated = ""
        
        # 裁判评分
        result = chat_completion_json(
            system=JUDGE_SYSTEM,
            user=JUDGE_PROMPT.format(
                question=question,
                gold_answer=gold_answer,
                generated_answer=generated
            ),
            temperature=0.1,
        )
        judgment = result.get("judgment", "INCORRECT")
        if judgment not in ("CORRECT", "INCORRECT"):
            judgment = "INCORRECT"
        
        is_correct = judgment == "CORRECT"
        if is_correct:
            conv_correct += 1
        
        conv_results.append({
            "conversation_idx": conv_idx,
            "qa_idx": orig_idx,
            "question": question,
            "gold_answer": gold_answer,
            "generated_answer": generated,
            "judgment": judgment,
            "judge_reason": result.get("reason", ""),
            "category": category,
            "top_memories": top_memories[:5],
        })
        
        if (qa_idx + 1) % 20 == 0:
            acc_so_far = conv_correct / (qa_idx + 1) * 100
            print(f"  [Conv {conv_idx}] Q{qa_idx+1}/{len(qa_list)} | acc={acc_so_far:.1f}%", flush=True)
    
    answer_elapsed = time.time() - answer_start
    acc = conv_correct / len(qa_list) * 100 if qa_list else 0
    print(f"[Conv {conv_idx}] 完成: {conv_correct}/{len(qa_list)} = {acc:.1f}% | write={write_elapsed:.0f}s answer={answer_elapsed:.0f}s")
    
    # 保存单对话结果
    result_data = {
        "conv_idx": conv_idx,
        "speaker_a": speaker_a,
        "speaker_b": speaker_b,
        "total": len(qa_list),
        "correct": conv_correct,
        "accuracy": acc,
        "write_time": write_elapsed,
        "answer_time": answer_elapsed,
        "mem_count": mem_count,
        "details": conv_results,
    }
    
    result_path = os.path.join(output_dir, f"conv{conv_idx}_result.json")
    with open(result_path, 'w') as f:
        json.dump(result_data, f, indent=2, ensure_ascii=False)
    
    mem.close()
    return result_data


def merge_results(output_dir: str, num_convs: int):
    """合并所有对话结果"""
    all_details = []
    total_q = 0
    total_correct = 0
    from collections import defaultdict
    category_stats = defaultdict(lambda: {"total": 0, "correct": 0})
    
    for i in range(num_convs):
        path = os.path.join(output_dir, f"conv{i}_result.json")
        if not os.path.exists(path):
            print(f"  对话 {i} 结果不存在，跳过")
            continue
        with open(path) as f:
            data = json.load(f)
        
        all_details.extend(data["details"])
        total_q += data["total"]
        total_correct += data["correct"]
        
        for d in data["details"]:
            cat = str(d.get("category", 0))
            category_stats[cat]["total"] += 1
            if d["judgment"] == "CORRECT":
                category_stats[cat]["correct"] += 1
        
        print(f"  Conv {i}: {data['correct']}/{data['total']} = {data['accuracy']:.1f}%")
    
    accuracy = total_correct / total_q * 100 if total_q else 0
    
    merged = {
        "system": "amem_official_raw",
        "total_questions": total_q,
        "correct": total_correct,
        "accuracy": accuracy,
        "category_stats": dict(category_stats),
        "details": all_details,
    }
    
    merged_path = os.path.join(output_dir, "amem_official_raw_results.json")
    with open(merged_path, 'w') as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*60}")
    print(f"A-Mem 官方版（原始用法）LoCoMo 合并结果")
    print(f"总题数: {total_q}")
    print(f"正确数: {total_correct}")
    print(f"准确率: {accuracy:.2f}%")
    print(f"{'='*60}")
    print(f"结果已保存到: {merged_path}")
    
    return merged


def main():
    parser = argparse.ArgumentParser(description="A-Mem 官方版 LoCoMo 并行测评")
    parser.add_argument("--dataset", type=str, default="locomo10.json")
    parser.add_argument("--conversations", type=str, default="all")
    parser.add_argument("--top-k", type=int, default=20)
    parser.add_argument("--output-dir", type=str, default="results/amem_official_raw")
    parser.add_argument("--merge-only", action="store_true", help="只合并已有结果")
    args = parser.parse_args()
    
    os.makedirs(args.output_dir, exist_ok=True)
    
    # 确定对话数
    with open(args.dataset) as f:
        dataset = json.load(f)
    if isinstance(dataset, dict):
        dataset = [dataset]
    num_convs = len(dataset)
    
    if args.conversations == "all":
        conv_indices = list(range(num_convs))
    else:
        conv_indices = [int(x.strip()) for x in args.conversations.split(",") if x.strip()]
    
    if args.merge_only:
        merge_results(args.output_dir, num_convs)
        return
    
    # 清除代理
    for key in ["http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "all_proxy"]:
        os.environ.pop(key, None)
    
    # 从 ~/.hermes/.env 读 API key
    env_path = os.path.expanduser("~/.hermes/.env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.startswith("DEEPSEEK_API_KEY="):
                    os.environ["DEEPSEEK_API_KEY"] = line.strip().split("=", 1)[1]
    
    print(f"\n{'='*60}")
    print(f"A-Mem 官方版（原始用法）LoCoMo 并行测评")
    print(f"对话: {conv_indices} ({len(conv_indices)} 个并行)")
    print(f"Top-K: {args.top_k}")
    print(f"{'='*60}\n")
    
    start_time = time.time()
    
    # 每个对话一个子进程
    processes = []
    for conv_idx in conv_indices:
        script = f"""
import sys, os
sys.path.insert(0, "{os.path.dirname(os.path.abspath(__file__))}")
os.environ.pop("http_proxy", None)
os.environ.pop("https_proxy", None)
os.environ.pop("HTTP_PROXY", None)
os.environ.pop("HTTPS_PROXY", None)
os.environ.pop("ALL_PROXY", None)
os.environ.pop("all_proxy", None)

env_path = os.path.expanduser("~/.hermes/.env")
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            if line.startswith("DEEPSEEK_API_KEY="):
                os.environ["DEEPSEEK_API_KEY"] = line.strip().split("=", 1)[1]

from amem_parallel_eval import run_single_conv
run_single_conv({conv_idx}, "{args.dataset}", "{args.output_dir}", {args.top_k})
"""
        log_file = os.path.join(args.output_dir, f"conv{conv_idx}.log")
        proc = subprocess.Popen(
            [sys.executable, "-u", "-c", script],
            stdout=open(log_file, 'w'),
            stderr=subprocess.STDOUT,
        )
        processes.append((conv_idx, proc, log_file))
        print(f"  启动 Conv {conv_idx} (PID {proc.pid}) -> {log_file}")
    
    # 等待所有进程
    for conv_idx, proc, log_file in processes:
        proc.wait()
        print(f"  Conv {conv_idx} 完成 (exit code: {proc.returncode})")
    
    elapsed = time.time() - start_time
    print(f"\n全部完成，耗时 {