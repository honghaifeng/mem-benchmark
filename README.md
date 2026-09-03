# mem-benchmark

**A unified benchmark for evaluating LLM memory systems on bilingual long-term conversation datasets.**

Four memory systems evaluated on CLongEval (Chinese) and LoCoMo (English) with a shared LLM backend for fair comparison.

English | [中文](README_zh.md)

## Systems

| System | Method | Implementation |
|--------|--------|----------------|
| **Baseline** | FTS5 flat memory + keyword search | `systems/baseline_memory.py` |
| **CogMem** | FTS5 + vector retrieval + spreading activation | `systems/cognitive_vector_memory.py` |
| **Mem0** | Official mem0ai SDK (Qdrant + vector) | `systems/mem0_official_eval.py` |
| **A-Mem** | Official A-Mem agentic memory (note + link + evolve) | `systems/amem_official_memory.py` + `A-mem-official/` |

## Evaluation Datasets

| Dataset | Language | Conversations | Questions | Source |
|---------|----------|:------------:|:---------:|--------|
| CLongEval | Chinese | 70 | 358 | `data/clongeval_zh.jsonl` |
| LoCoMo | English | 10 | 1,540 | `data/locomo10_en.json` |

### Data Format

**CLongEval (`clongeval_zh.jsonl`)** — one JSON line per conversation group:
```json
{"id": 1, "conversation": "...", "qa_pairs": [{"question": "...", "answer": "..."}]}
```

**LoCoMo (`locomo10_en.json`)** — array of conversation objects:
```json
[{"conversation_id": 1, "conversation": {...}, "qa_pairs": [...]}]
```

### Download

```bash
# Clone this repo (private, requires authentication)
git clone https://github.com/honghaifeng/mem-benchmark.git
# Data is included in the repo: data/clongeval_zh.jsonl, data/locomo10_en.json
```

## Main Results

### CLongEval (Chinese, 358 questions)

| System | Accuracy | Correct | Write Tokens | DB Size |
|--------|:--------:|:-------:|:------------:|:-------:|
| **Baseline (FTS5)** | **90.50%** | 324/358 | 1.07M | 0.4 MB |
| CogMem (bge-small-en) | 89.11% | 319/358 | 2.88M | 83.5 MB |
| CogMem (bge-small-zh) | **92.18%** | 330/358 | — | — |
| Mem0 (official SDK) | 85.47% | 306/358 | 4.85M | 9.1 MB |
| A-Mem (official) | 87.43% | 313/358 | — | — |

**LLM backend**: DeepSeek-V3 (all systems use the same LLM for fair comparison).

### LoCoMo (English, 1,540 questions)

| System | Accuracy | Correct |
|--------|:--------:|:-------:|
| Baseline (FTS5) | 64.85% | 999/1540 |
| CogMem | **75.16%** | 1159/1540 |
| Mem0 (official SDK) | **81.91%** | 1254/1540 |
| A-Mem (official) | 75.94% | — |

### LoCoMo Category Breakdown

| Category | # Q | Baseline | CogMem | Mem0 | A-Mem |
|----------|:---:|:--------:|:------:|:----:|:-----:|
| Single-hop | 282 | 64.9% | 71.3% | **82.3%** | 80.5% |
| Multi-hop | 321 | 63.2% | **82.2%** | 78.2% | 65.7% |
| Temporal | 96 | 54.2% | **62.5%** | **62.5%** | 58.3% |
| Conversation understanding | 841 | 66.6% | 75.1% | **85.5%** | 80.3% |

### Key Findings

1. **No single system wins on both languages.** Baseline (FTS5) leads Chinese at 90.50%, while Mem0 leads English at 81.91%.
2. **CogMem excels at multi-hop reasoning** (82.2% on LoCoMo), validating the entity-relation spreading activation approach.
3. **Embedding language matters.** CogMem with English embeddings drops to 89.11% on Chinese, but switching to `bge-small-zh-v1.5` raises it to **92.18%**, surpassing Baseline.
4. **A-Mem trades cost for stability.** Its 3-step LLM process (note → link → evolve) produces 30× write time vs Baseline but achieves stable cross-language performance (87.4% ZH / 75.9% EN).

## Multi-LLM Backend Comparison

Same CogMem system evaluated with 5 LLM backends on CLongEval (Chinese):

| LLM Backend | Provider | Tier | Accuracy | Correct/Total |
|-------------|----------|:----:|:--------:|:-------------:|
| CogMem (bge-small-zh) | DeepSeek | Paid | **92.18%** | 330/358 |
| DeepSeek-V3 | DeepSeek | Paid | 89.11% | 319/358 |
| GPT-5.6-sol | TokenSpace | Paid | 81.28% | 291/358 |
| DS-V4-Flash | Volcengine | Free | 80.73% | 289/358 |
| Qwen-Max | DashScope | Paid | 78.39% | 243/310* |
| Qwen3.8-Flash | DashScope | Free | 75.98% | 272/358 |

*Qwen-Max completed only 13/70 conversation groups due to API rate limiting.

### Error Pattern Analysis

| LLM Backend | # Errors | Honest ("not recorded") | Fabrication | Honesty Rate | Fab. Rate |
|-------------|:--------:|:----------------------:|:-----------:|:------------:|:---------:|
| DeepSeek-V3 | 39 | 31 | 3 | 79.5% | 7.7% |
| DS-V4-Flash | 69 | 29 | 14 | 42.0% | 20.3% |
| Qwen3.8-Flash | 86 | 23 | 38 | 26.7% | 44.2% |
| Qwen-Max | 67† | 31 | 36 | 46.3%† | 53.7%† |
| GPT-5.6-sol | 67 | 9 | 37 | 13.4% | 55.2% |

*†Qwen-Max error breakdown is from an earlier analysis run; total errors recalculated as 310−243=67.*

### Key Insight

A model's "honest calibration" (willingness to say "I don't have that record") correlates with accuracy more strongly than model tier. Free models (DS-V4-Flash, 80.7%) can outperform paid flagships (Qwen-Max, 78.4%).

## Project Structure

```
mem-benchmark/
├── systems/                  # Memory system implementations
│   ├── baseline_memory.py    # Baseline: FTS5 flat memory
│   ├── cognitive_memory.py   # Cognitive: FTS5 + spreading activation (ablation)
│   ├── cognitive_vector_memory.py  # CogMem: FTS5 + vector + SA
│   ├── mem0_official_eval.py       # Mem0: official SDK (LoCoMo)
│   ├── mem0_official_clong_eval.py # Mem0: official SDK (CLongEval)
│   └── amem_official_memory.py     # A-Mem: official agentic memory
├── A-mem-official/           # A-Mem official codebase
│   ├── memory_layer_robust.py
│   ├── memory_layer.py
│   └── llm_text_parsers.py
├── eval_scripts/             # Evaluation framework
│   ├── clong_eval.py         # CLongEval runner
│   ├── locomo_eval.py        # LoCoMo runner
│   ├── mem0_official_clong_parallel.py
│   ├── mem0_official_locomo_parallel.py
│   ├── amem_parallel_eval.py
│   └── compare_results.py    # Results comparison tool
├── utils/                    # Shared utilities
│   ├── llm_client.py         # Multi-channel LLM client
│   └── cn_search_utils.py    # Chinese keyword extraction
├── data/                     # Evaluation datasets
│   ├── clongeval_zh.jsonl    # CLongEval (70 conv, 358 Q, 15 MB)
│   └── locomo10_en.json      # LoCoMo (10 conv, 1,540 Q, 2.7 MB)
├── results/                  # Evaluation results
│   ├── clong_eval/           # CLongEval results (4 systems)
│   │   ├── baseline/
│   │   ├── cogmem/
│   │   ├── mem0_official/
│   │   └── amem_official/
│   ├── locomo_eval/          # LoCoMo results (4 systems)
│   │   ├── baseline/         # Extracted from memory-arena
│   │   ├── cogmem/
│   │   ├── mem0_official/
│   │   └── amem_official/
│   └── multi_llm/            # Multi-LLM CogMem results (6 configs)
│       ├── deepseek_v3/
│       ├── cogmem_bge_small_zh/
│       ├── gpt_5_6_sol/
│       ├── ds_v4_flash/
│       ├── qwen3_8_flash/
│       └── qwen_max/
├── .env.example              # API key template
├── .gitignore
├── LICENSE
├── README.md                 # This file (English)
└── README_zh.md              # Chinese version
```

## Quick Start

### 1. Setup

```bash
git clone https://github.com/honghaifeng/mem-benchmark.git
cd mem-benchmark
pip install -r requirements.txt
cp .env.example .env  # Fill in your API keys
```

### 2. Run CLongEval (Chinese)

```bash
# Baseline
python eval_scripts/clong_eval.py --system baseline --data data/clongeval_zh.jsonl

# CogMem
python eval_scripts/clong_eval.py --system cognitive_vector --data data/clongeval_zh.jsonl

# Mem0 (official SDK)
python eval_scripts/mem0_official_clong_parallel.py --data data/clongeval_zh.jsonl

# A-Mem (official)
python eval_scripts/amem_parallel_eval.py --data data/clongeval_zh.jsonl
```

### 3. Run LoCoMo (English)

```bash
# Baseline
python eval_scripts/locomo_eval.py --system baseline --data data/locomo10_en.json

# CogMem
python eval_scripts/locomo_eval.py --system cognitive_vector --data data/locomo10_en.json

# Mem0 (official SDK)
python eval_scripts/mem0_official_locomo_parallel.py --data data/locomo10_en.json
```

### 4. Compare Results

```bash
python eval_scripts/compare_results.py --results-dir results/
```

## Evaluation Protocol

- **LLM backend**: DeepSeek-V3 for all systems (main comparison) to ensure fair comparison
- **Parallel testing**: Up to 10 processes for CLongEval, sequential for LoCoMo
- **Metrics**: Accuracy (%), correct count, write time, write tokens, DB size, error breakdown
- **Multi-LLM**: Same CogMem system tested with 5 LLM backends (DeepSeek, GPT, ARK, Qwen Flash, Qwen Max)

## Systems Overview

### Baseline (FTS5)
Flat memory fragments with SQLite FTS5 full-text search. LLM extracts atomic facts from conversations, stored with BM25 ranking. Chinese uses keyword extraction + LIKE matching. Simple, fast, surprisingly strong on Chinese.

### CogMem
Three-path hybrid retrieval: (1) FTS5 symbolic, (2) dense vector cosine similarity, (3) entity-relation spreading activation. Weighted fusion (FTS: 0.4, Vector: 0.6) with deduplication. English uses `all-MiniLM-L6-v2`, Chinese uses `BAAI/bge-small-zh-v1.5`.

### Mem0 (Official SDK)
Uses `from mem0 import Memory` with Qdrant vector database. Automatic fact extraction and deduplication. English uses default embeddings, Chinese uses `bge-small-zh-v1.5` (384-dim/512-dim).

### A-Mem (Official)
Uses `RobustAgenticMemorySystem` from the A-Mem official codebase. Three-step LLM process: note construction → link generation → memory evolution. Self-organizing memory graph with Ebbinghaus-inspired decay.

## License

MIT
