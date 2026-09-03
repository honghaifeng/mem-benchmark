"""
官方 A-Mem 记忆系统封装
直接使用 A-Mem 官方代码的 RobustAgenticMemorySystem
用 sentence-transformers 嵌入检索（官方原版实现）
"""
import sys
import os
import time
import uuid
from typing import Optional

# 把官方 A-Mem 目录加入 path
AMEM_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "A-mem-official")
sys.path.insert(0, AMEM_DIR)

from memory_layer_robust import RobustAgenticMemorySystem, RobustMemoryNote
from llm_client import chat_completion_json, chat_completion, _get_api_key
from cn_search_utils import contains_cjk


def _get_deepseek_key():
    """从 ~/.hermes/.env 读取 DeepSeek API key"""
    env_path = os.path.expanduser("~/.hermes/.env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.startswith("DEEPSEEK_API_KEY="):
                    return line.strip().split("=", 1)[1]
    return os.getenv("DEEPSEEK_API_KEY", "")


class OfficialAMemMemory:
    """
    官方 A-Mem 记忆系统封装
    直接调用 RobustAgenticMemorySystem，保留其完整的：
    - 笔记构造（keywords/context/tags）
    - 链接生成
    - 记忆进化
    - sentence-transformers 嵌入检索
    """
    
    def __init__(self, db_path: str = "amem_official.db", 
                 llm_model: str = "deepseek-chat",
                 embed_model: str = "all-MiniLM-L6-v2"):
        self.db_path = db_path
        
        # 初始化官方 A-Mem 系统
        # 用 OpenAI 兼容后端指向 DeepSeek
        api_key = _get_deepseek_key()
        
        self.mem_system = RobustAgenticMemorySystem(
            model_name=embed_model,
            llm_backend="openai",
            llm_model=llm_model,
            api_key=api_key,
            api_base="https://api.deepseek.com/v1",
            check_connection=False,
        )
        
        # 为不同 user_id 维护独立的内存存储
        # 官方 A-Mem 是单用户内存式的，我们手动按 user_id 分隔
        self._user_systems = {}
    
    def _get_system(self, user_id: str) -> RobustAgenticMemorySystem:
        """获取指定用户的记忆系统（每个用户独立）"""
        if user_id not in self._user_systems:
            api_key = _get_deepseek_key()
            self._user_systems[user_id] = RobustAgenticMemorySystem(
                model_name="all-MiniLM-L6-v2",
                llm_backend="openai",
                llm_model="deepseek-chat",
                api_key=api_key,
                api_base="https://api.deepseek.com/v1",
                check_connection=False,
            )
        return self._user_systems[user_id]
    
    def add(self, conversation: str, user_id: str = "", timestamp: Optional[float] = None) -> int:
        """
        官方 A-Mem 用法：直接将原始对话传给 add_note()
        A-Mem 内部自动完成：
        1. analyze_content() — LLM 提取 keywords/context/tags
        2. find_related_memories() — 找最近邻
        3. evolution — 记忆进化（更新 tags/context/links）
        不做任何预处理，保持与官方一致
        """
        if timestamp is None:
            timestamp = time.time()

        time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))

        system = self._get_system(user_id)
        try:
            system.add_note(conversation, time=time_str)
            return 1
        except Exception as e:
            print(f"    [警告] A-Mem add_note 失败: {e}")
            return 0
    
    def search(self, query: str, user_id: str = "", top_k: int = 15) -> list[dict]:
        """检索记忆，返回与其他系统一致的格式"""
        system = self._get_system(user_id)
        
        if not system.memories:
            return []
        
        # 用官方检索方法
        memory_str, indices = system.find_related_memories(query, k=top_k)
        
        all_memories = list(system.memories.values())
        results = []
        for i, idx in enumerate(indices):
            if idx < len(all_memories):
                note = all_memories[idx]
                results.append({
                    "memory": note.content,
                    "context": note.context,
                    "keywords": note.keywords,
                    "tags": note.tags,
                    "score": 1.0 - (i * 0.05),  # 按排名给分
                })
        
        return results[:top_k]
    
    def count_memories(self, user_id: str = "") -> int:
        """统计记忆卡片数"""
        if user_id:
            system = self._get_system(user_id)
            return len(system.memories)
        else:
            total = 0
            for sys in self._user_systems.values():
                total += len(sys.memories)
            return total
    
    def close(self):
        """关闭（内存式，不需要关闭操作）"""
        pass
