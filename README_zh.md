# mem-benchmark

**统一评测 LLM 记忆系统的双语长对话基准测试。**

在 CLongEval（中文）和 LoCoMo（英文）上使用相同 LLM 后端评测四个记忆系统，确保公平对比。

[English](README.md) | 中文

## 评测系统

| 系统 | 方法 | 实现代码 |
|------|------|---------|
| **Baseline** | FTS5 扁平记忆 + 关键词检索 | `systems/baseline_memory.py` |
| **CogMem** | FTS5 + 向量检索 + 扩散激活 | `systems/cognitive_vector_memory.py` |
| **Mem0** | 官方 mem0ai SDK（Qdrant + 向量） | `systems/mem0_official_eval.py` |
| **A-Mem** | 官方 A-Mem 代理记忆（笔记+链接+进化） | `systems/amem_official_memory.py` + `A-mem-official/` |

## 评测数据集

| 数据集 | 语言 | 对话组 | 问题数 | 文件 |
|--------|------|:------:|:------:|------|
| CLongEval | 中文 | 70 | 358 | `data/clongeval_zh.jsonl` |
| LoCoMo | 英文 | 10 | 1,540 | `data/locomo10_en.json` |

### 数据格式

**CLongEval（`clongeval_zh.jsonl`）** — 每行一个对话组：
```json
{"id": 1, "conversation": "...", "qa_pairs": [{"question": "...", "answer": "..."}]}
```

**LoCoMo（`locomo10_en.json`）** — 对话对象数组：
```json
[{"conversation_id": 1, "conversation": {...}, "qa_pairs": [...]}]
```

### 下载

```bash
# 克隆仓库（私有，需认证）
git clone https://github.com/honghaifeng/mem-benchmark.git
# 数据已包含在仓库中：data/clongeval_zh.jsonl, data/locomo10_en.json
```

## 主要结果

### CLongEval（中文，358 题）

| 系统 | 准确率 | 正确数 | 写入 Token | 数据库大小 |
|------|:------:|:------:|:----------:|:----------:|
| Baseline (FTS5) | 90.50% | 324/358 | 1.07M | 0.4 MB |
| CogMem (bge-small-en) | 89.11% | 319/358 | 2.88M | 83.5 MB |
| **CogMem (bge-small-zh)** | **92.18%** | 330/358 | — | — |
| Mem0（官方 SDK） | 85.47% | 306/358 | 4.85M | 9.1 MB |
| A-Mem（官方） | 87.43% | 313/358 | — | — |

**LLM 后端**：DeepSeek-V3（所有系统使用相同 LLM 确保公平对比）

### LoCoMo（英文，1,540 题）

| 系统 | 准确率 | 正确数 |
|------|:------:|:------:|
| Baseline (FTS5) | 64.85% | 999/1540 |
| CogMem | 75.16% | 1159/1540 |
| Mem0（官方 SDK） | **81.91%** | 1254/1540 |
| A-Mem（官方） | 75.94% | — |

### LoCoMo 分类别准确率

| 类别 | 问题数 | Baseline | CogMem | Mem0 | A-Mem |
|------|:------:|:--------:|:------:|:----:|:-----:|
| 单跳跃 | 282 | 64.9% | 71.3% | **82.3%** | 80.5% |
| 多跳跃 | 321 | 63.2% | **82.2%** | 78.2% | 65.7% |
| 时间推理 | 96 | 54.2% | **62.5%** | **62.5%** | 58.3% |
| 对话理解 | 841 | 66.6% | 75.1% | **85.5%** | 80.3% |

### 关键发现

1. **没有单一系统在两种语言上同时领先。** CogMem (bge-small-zh) 中文最高 92.18%，Mem0 英文最高 81.91%。
2. **CogMem 在多跳推理上最强**（LoCoMo 82.2%），验证了实体-关系扩散激活架构的价值。
3. **嵌入语言很重要。** CogMem 使用英文嵌入在中文上降至 89.11%，但切换 `bge-small-zh-v1.5` 后升至 **92.18%**，超过 Baseline。
4. **A-Mem 以成本换稳定。** 三步 LLM 流程（笔记→链接→进化）的写入时间为 Baseline 的 30 倍，但跨语言表现稳定（中文 87.4% / 英文 75.9%）。

## 多 LLM 后端对比

同一 CogMem 系统使用 6 种配置（5 个 LLM 后端 + 1 个中文嵌入变体）在 CLongEval（中文）上评测：

| LLM 后端 | 提供商 | 类型 | 准确率 | 正确/总数 |
|----------|--------|:----:|:------:|:---------:|
| CogMem (bge-small-zh) | DeepSeek | 付费 | **92.18%** | 330/358 |
| DeepSeek-V3 | DeepSeek | 付费 | 89.11% | 319/358 |
| GPT-5.6-sol | TokenSpace | 付费 | 81.28% | 291/358 |
| DS-V4-Flash | 火山引擎 | 免费 | 80.73% | 289/358 |
| Qwen-Max | DashScope | 付费 | 78.39% | 243/310* |
| Qwen3.8-Flash | DashScope | 免费 | 75.98% | 272/358 |

*Qwen-Max 因 API 限流仅完成 13/70 组对话。

### 错误模式分析

| LLM 后端 | 错误数 | 诚实（"未记录"） | 编造 | 诚实率 | 编造率 |
|----------|:------:|:----------------:|:----:|:------:|:------:|
| DeepSeek-V3 | 39 | 31 | 3 | 79.5% | 7.7% |
| DS-V4-Flash | 69 | 29 | 14 | 42.0% | 20.3% |
| Qwen3.8-Flash | 86 | 23 | 38 | 26.7% | 44.2% |
| Qwen-Max | 67† | 31 | 36 | 46.3%† | 53.7%† |
| GPT-5.6-sol | 67 | 9 | 37 | 13.4% | 55.2% |

*†Qwen-Max 错误分类来自早期分析运行；总错误数已按 310−243=67 重新计算。*

### 关键洞察

模型的"诚实校准"（愿意承认"我没有该记录"）与准确率的相关性比模型等级更强。免费模型（DS-V4-Flash，80.7%）可以超越付费旗舰模型（Qwen-Max，78.4%）。

## 项目结构

```
mem-benchmark/
├── systems/                  # 记忆系统实现
│   ├── baseline_memory.py    # 基线：FTS5 扁平记忆
│   ├── cognitive_memory.py   # 认知检索：FTS5 + 扩散激活（消融）
│   ├── cognitive_vector_memory.py  # CogMem：FTS5 + 向量 + 扩散激活
│   ├── mem0_official_eval.py       # Mem0：官方 SDK（LoCoMo）
│   ├── mem0_official_clong_eval.py # Mem0：官方 SDK（CLongEval）
│   └── amem_official_memory.py     # A-Mem：官方代理记忆
├── A-mem-official/           # A-Mem 官方代码库
│   ├── memory_layer_robust.py
│   ├── memory_layer.py
│   └── llm_text_parsers.py
├── eval_scripts/             # 评测框架
│   ├── clong_eval.py         # CLongEval 评测脚本
│   ├── locomo_eval.py        # LoCoMo 评测脚本
│   ├── mem0_official_clong_parallel.py
│   ├── mem0_official_locomo_parallel.py
│   ├── amem_parallel_eval.py
│   └── compare_results.py    # 结果对比工具
├── utils/                    # 共享工具
│   ├── llm_client.py         # 多通道 LLM 客户端
│   └── cn_search_utils.py    # 中文关键词提取
├── data/                     # 评测数据集
│   ├── clongeval_zh.jsonl    # CLongEval（70 组，358 题，15 MB）
│   └── locomo10_en.json      # LoCoMo（10 组，1,540 题，2.7 MB）
├── results/                  # 评测结果
│   ├── clong_eval/           # CLongEval 结果（4 系统）
│   │   ├── baseline/
│   │   ├── cogmem/
│   │   ├── mem0_official/
│   │   └── amem_official/
│   ├── locomo_eval/          # LoCoMo 结果（4 系统）
│   │   ├── baseline/         # 从记忆竞技场提取
│   │   ├── cogmem/
│   │   ├── mem0_official/
│   │   └── amem_official/
│   └── multi_llm/            # 多 LLM CogMem 结果（6 配置）
│       ├── deepseek_v3/
│       ├── cogmem_bge_small_zh/
│       ├── gpt_5_6_sol/
│       ├── ds_v4_flash/
│       ├── qwen3_8_flash/
│       └── qwen_max/
├── .env.example              # API 密钥模板
├── .gitignore
├── LICENSE
├── README.md                 # 英文版
└── README_zh.md              # 中文版
```

## 快速开始

### 1. 环境配置

```bash
git clone https://github.com/honghaifeng/mem-benchmark.git
cd mem-benchmark
pip install -r requirements.txt
cp .env.example .env  # 填入你的 API 密钥
```

### 2. 运行 CLongEval（中文）

```bash
# Baseline
python eval_scripts/clong_eval.py --system baseline --data data/clongeval_zh.jsonl

# CogMem
python eval_scripts/clong_eval.py --system cognitive_vector --data data/clongeval_zh.jsonl

# Mem0（官方 SDK）
python eval_scripts/mem0_official_clong_parallel.py --data data/clongeval_zh.jsonl

# A-Mem（官方）
python eval_scripts/amem_parallel_eval.py --data data/clongeval_zh.jsonl
```

### 3. 运行 LoCoMo（英文）

```bash
# Baseline
python eval_scripts/locomo_eval.py --system baseline --data data/locomo10_en.json

# CogMem
python eval_scripts/locomo_eval.py --system cognitive_vector --data data/locomo10_en.json

# Mem0（官方 SDK）
python eval_scripts/mem0_official_locomo_parallel.py --data data/locomo10_en.json
```

### 4. 对比结果

```bash
python eval_scripts/compare_results.py --results-dir results/
```

## 评测协议

- **LLM 后端**：DeepSeek-V3（主对比使用相同 LLM 确保公平）
- **并行测试**：CLongEval 最多 10 进程并行，LoCoMo 顺序执行
- **指标**：准确率（%）、正确数、写入时间、写入 Token、数据库大小、错误分类
- **多 LLM**：同一 CogMem 系统使用 6 种配置测试：5 个 LLM 后端（DeepSeek、GPT、ARK、Qwen Flash、Qwen Max）+ 1 个中文嵌入变体（bge-small-zh）

## 系统概述

### Baseline (FTS5)
扁平记忆片段 + SQLite FTS5 全文检索。LLM 从对话中提取原子事实，BM25 排序。中文使用关键词提取 + LIKE 匹配。简单、快速、中文表现意外强劲。

### CogMem
三路径混合检索：(1) FTS5 符号检索，(2) 稠密向量余弦相似度，(3) 实体-关系扩散激活。加权融合（FTS: 0.4, Vector: 0.6）+ 去重。英文用 `all-MiniLM-L6-v2`，中文用 `BAAI/bge-small-zh-v1.5`。

### Mem0（官方 SDK）
使用 `from mem0 import Memory` + Qdrant 向量数据库。自动事实提取与去重。英文用默认嵌入，中文用 `bge-small-zh-v1.5`（384维/512维）。

### A-Mem（官方）
使用 A-Mem 官方代码库的 `RobustAgenticMemorySystem`。三步 LLM 流程：笔记构造 → 链接生成 → 记忆进化。自组织记忆图谱，受艾宾浩斯遗忘曲线启发。

## 许可证

MIT
