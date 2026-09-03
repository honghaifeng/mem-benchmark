"""
LLM 客户端封装
三通道故障转移：DeepSeek 官方 → 来也托管 → TokenSpace
"""
import json
import os
import re
import time
import requests
from typing import Optional


# =============================================================================
# 三通道配置
# =============================================================================
def _load_env() -> dict:
    """从 ~/.hermes/.env 加载环境变量"""
    env = {}
    env_path = os.path.expanduser("~/.hermes/.env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if "=" in line and not line.startswith("#"):
                    k, v = line.split("=", 1)
                    env[k] = v
    return env


_env = _load_env()

# LLM 后端选择：deepseek（默认）或 qwen
_LLM_BACKEND = os.getenv("LLM_BACKEND", "deepseek").lower()

# DeepSeek 三通道配置
_DEEPSEEK_CHANNELS = [
    {
        "name": "deepseek-official",
        "base_url": "https://api.deepseek.com/v1",
        "model": "deepseek-chat",
        "api_key": _env.get("DEEPSEEK_API_KEY", os.getenv("DEEPSEEK_API_KEY", "")),
    },
    {
        "name": "clawworker-managed",
        "base_url": "https://worker-cn.laiye.com/open/clawworker_service/laiye/v1",
        "model": "pro",
        "api_key": _env.get("CLAWWORKER_MANAGED_API_KEY", os.getenv("CLAWWORKER_MANAGED_API_KEY", "")),
    },
    {
        "name": "tokenspace",
        "base_url": "https://tokenspace.io/v1",
        "model": "claude-fable-5",
        "api_key": _env.get("TOKENSPACE_API_KEY", os.getenv("TOKENSPACE_API_KEY", "")),
    },
]

# Qwen 通道配置
_QWEN_CHANNELS = [
    {
        "name": "qwen-max",
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "model": "qwen-max",
        "api_key": _env.get("QWEN_API_KEY", os.getenv("QWEN_API_KEY", "")),
    },
]

# Qwen3.8-Flash 免费通道配置
_QWEN_FLASH_CHANNELS = [
    {
        "name": "qwen3.8-flash",
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "model": "qwen3.8-flash",
        "api_key": _env.get("QWEN_API_KEY", os.getenv("QWEN_API_KEY", "")),
    },
]

# GPT (TokenSpace) 通道配置
_GPT_CHANNELS = [
    {
        "name": "gpt-5.6-sol",
        "base_url": "https://tokenspace.io/v1",
        "model": "gpt-5.6-sol",
        "api_key": _env.get("GPT_TOKENSPACE_API_KEY", os.getenv("GPT_TOKENSPACE_API_KEY", "")),
    },
]

# DeepSeek-V4-Flash (火山引擎 ARK) 通道配置
_ARK_CHANNELS = [
    {
        "name": "deepseek-v4-flash-ark",
        "base_url": "https://ark.cn-beijing.volces.com/api/v3",
        "model": "deepseek-v4-flash-ga-260731",
        "api_key": _env.get("ARK_API_KEY", os.getenv("ARK_API_KEY", "")),
    },
]

# 根据 LLM_BACKEND 环境变量选择通道
if _LLM_BACKEND == "qwen":
    CHANNELS = _QWEN_CHANNELS
    print(f"[LLM] 使用 Qwen 后端 (model: qwen-max)")
elif _LLM_BACKEND == "qwen-flash":
    CHANNELS = _QWEN_FLASH_CHANNELS
    print(f"[LLM] 使用 Qwen3.8-Flash 后端 (model: qwen3.8-flash, 免费)")
elif _LLM_BACKEND == "gpt":
    CHANNELS = _GPT_CHANNELS
    print(f"[LLM] 使用 GPT 后端 (model: gpt-5.6-sol, TokenSpace)")
elif _LLM_BACKEND == "ark":
    CHANNELS = _ARK_CHANNELS
    print(f"[LLM] 使用 ARK 后端 (model: deepseek-v4-flash-ga-260731, 火山引擎)")
else:
    CHANNELS = _DEEPSEEK_CHANNELS

# 当前活跃通道索引
_active_channel = 0
# 通道失败时间记录（用于跳过最近失败的通道）
_channel_fail_time = {}

# 通道失败冷却时间（秒）：失败后 60 秒内跳过
_CHANNEL_COOLDOWN = 60


def _get_active_channel() -> dict:
    """获取当前活跃通道"""
    return CHANNELS[_active_channel]


def _try_next_channel(failed_idx: int):
    """切换到下一个可用通道"""
    global _active_channel
    _channel_fail_time[failed_idx] = time.time()

    for i in range(len(CHANNELS)):
        if i == failed_idx:
            continue
        fail_time = _channel_fail_time.get(i, 0)
        if time.time() - fail_time < _CHANNEL_COOLDOWN:
            continue
        ch = CHANNELS[i]
        if not ch["api_key"]:
            continue
        _active_channel = i
        print(f"[LLM] 通道切换: {CHANNELS[failed_idx]['name']} → {ch['name']}")
        return ch

    # 所有通道都失败了，强制重试第一个
    _active_channel = 0
    return CHANNELS[0]


# 兼容旧代码
API_KEY = CHANNELS[0]["api_key"]
BASE_URL = CHANNELS[0]["base_url"]
MODEL = CHANNELS[0]["model"]


def _get_api_key() -> str:
    """兼容旧代码：返回第一个有 key 的通道的 API key"""
    for ch in CHANNELS:
        if ch["api_key"]:
            return ch["api_key"]
    return ""

# 速率控制
_last_call = 0
_min_interval = 0.3

# Token 统计
_token_stats = {
    "prompt_tokens": 0,
    "completion_tokens": 0,
    "total_tokens": 0,
    "call_count": 0,
}


def reset_token_stats():
    """重置 token 统计"""
    global _token_stats
    _token_stats = {
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "total_tokens": 0,
        "call_count": 0,
    }


def get_token_stats():
    """获取当前 token 统计"""
    return dict(_token_stats)


def _rate_limit():
    global _last_call
    now = time.time()
    elapsed = now - _last_call
    if elapsed < _min_interval:
        time.sleep(_min_interval - elapsed)
    _last_call = time.time()


def chat_completion(
    system: str,
    user: str,
    temperature: float = 0.1,
    max_retries: int = 3,
) -> str:
    """调用 LLM 聊天接口（三通道故障转移）"""
    global _active_channel
    _rate_limit()

    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": user})

    tried_channels = set()
    total_channels = len(CHANNELS)

    for attempt in range(max_retries):
        # 获取当前活跃通道
        ch = _get_active_channel()

        # 跳过无 key 的通道
        if not ch["api_key"] or _active_channel in tried_channels:
            _try_next_channel(_active_channel)
            ch = _get_active_channel()
            if _active_channel in tried_channels:
                break

        tried_channels.add(_active_channel)

        try:
            resp = requests.post(
                f"{ch['base_url']}/chat/completions",
                headers={
                    "Authorization": f"Bearer {ch['api_key']}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": ch["model"],
                    "messages": messages,
                    "temperature": temperature,
                },
                timeout=120,
            )

            # 402/401/403 = 余额不足/认证失败，切换通道
            if resp.status_code in (401, 402, 403):
                print(f"[LLM] 通道 {ch['name']} 返回 {resp.status_code}，切换...")
                _try_next_channel(_active_channel)
                continue

            resp.raise_for_status()
            data = resp.json()

            # 统计 token 使用
            usage = data.get("usage", {})
            if usage:
                _token_stats["prompt_tokens"] += usage.get("prompt_tokens", 0)
                _token_stats["completion_tokens"] += usage.get("completion_tokens", 0)
                _token_stats["total_tokens"] += usage.get("total_tokens", 0)
            _token_stats["call_count"] += 1

            return data["choices"][0]["message"]["content"]

        except requests.exceptions.ConnectionError:
            print(f"[LLM] 通道 {ch['name']} 连接失败，切换...")
            _try_next_channel(_active_channel)
            continue
        except requests.exceptions.Timeout:
            print(f"[LLM] 通道 {ch['name']} 超时，切换...")
            _try_next_channel(_active_channel)
            continue
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
                # 重试时也尝试切换通道
                _try_next_channel(_active_channel)
                continue
            raise

    # 所有重试用完，最后尝试所有通道各一次
    for i, ch in enumerate(CHANNELS):
        if not ch["api_key"]:
            continue
        try:
            resp = requests.post(
                f"{ch['base_url']}/chat/completions",
                headers={
                    "Authorization": f"Bearer {ch['api_key']}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": ch["model"],
                    "messages": messages,
                    "temperature": temperature,
                },
                timeout=120,
            )
            resp.raise_for_status()
            data = resp.json()
            usage = data.get("usage", {})
            if usage:
                _token_stats["prompt_tokens"] += usage.get("prompt_tokens", 0)
                _token_stats["completion_tokens"] += usage.get("completion_tokens", 0)
                _token_stats["total_tokens"] += usage.get("total_tokens", 0)
            _token_stats["call_count"] += 1
            _active_channel = i
            print(f"[LLM] 恢复使用通道: {ch['name']}")
            return data["choices"][0]["message"]["content"]
        except Exception:
            continue

    raise RuntimeError("所有 LLM 通道均不可用")


def extract_json(text: str) -> Optional[dict]:
    """从 LLM 返回文本中提取 JSON 对象"""
    if not text:
        return None

    # 尝试直接解析
    try:
        return json.loads(text.strip())
    except:
        pass

    # 尝试提取 ```json ... ``` 代码块
    match = re.search(r'```(?:json)?\s*\n?(.*?)\n?```', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1).strip())
        except:
            pass

    # 尝试提取第一个 { 到最后一个 }
    start = text.find("{")
    end = text.rfind("}")
    if start >= 0 and end > start:
        try:
            return json.loads(text[start:end+1])
        except:
            pass

    return None


def chat_completion_json(system: str, user: str, temperature: float = 0.1, max_retries: int = 2) -> dict:
    """调用 LLM，返回 JSON 对象（自动重试以确保格式正确）"""
    for attempt in range(max_retries):
        text = chat_completion(system, user, temperature=temperature)
        result = extract_json(text)
        if result is not None:
            return result
        # 重试时加更明确的 JSON 指令
        user = user + "\n\n重要：你的回复必须是严格有效的JSON格式，不要包含任何其他文字、解释或代码块标记。"

    # 最后实在解析不了，返回空结构
    return {}
