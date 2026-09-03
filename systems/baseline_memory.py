"""
基线记忆系统：扁平记忆 + FTS5 全文检索
模拟基础的向量检索记忆系统（用 FTS5 替代向量，原理相似：都是基于相似度的扁平检索）
"""
import sqlite3
import time
from typing import Optional

from llm_client import chat_completion_json
from cn_search_utils import contains_cjk, cn_like_search, build_fts_query


EXTRACTION_PROMPT_EN = """You are a memory extraction assistant. Extract all memorable facts from the conversation below.

Rules:
1. Extract specific, verifiable facts (people, places, events, preferences, plans, status, etc.)
2. One fact per memory, concise and clear
3. Don't extract small talk or greetings
4. If nothing worth remembering, return empty list
5. Memories should be independent atomic facts

Return ONLY valid JSON:
{{
  "memories": [
    "memory content 1",
    "memory content 2"
  ]
}}

Conversation:
{conversation}
"""

EXTRACTION_PROMPT_CN = """你是一个记忆提取助手。从以下对话中提取所有值得记住的事实。

规则:
1. 提取具体的、可验证的事实（人物、地点、事件、偏好、计划、状态等）
2. 每条记忆一个事实，简洁明了
3. 不要提取闲聊或问候
4. 如果没有值得记住的内容，返回空列表
5. 记忆应是独立的原子事实
6. 用中文输出记忆内容
7. 保留原文中的人名、地名、书名、电影名等专有名词

只返回有效的 JSON:
{{
  "memories": [
    "记忆内容1",
    "记忆内容2"
  ]
}}

对话:
{conversation}
"""


class BaselineMemory:
    """基线：扁平记忆 + FTS5 全文检索"""
    
    def __init__(self, db_path: str = "baseline_memory.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("PRAGMA journal_mode=WAL")
        self._init_db()
    
    def _init_db(self):
        # FTS5 虚拟表用于全文检索
        self.conn.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS memory_fts USING fts5(
                content,
                content_rowid,
                tokenize = 'unicode61'
            )
        """)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                created_at REAL NOT NULL,
                user_id TEXT DEFAULT ''
            )
        """)
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_mem_user ON memories(user_id)")
        self.conn.commit()
    
    def add(self, conversation_text: str, user_id: str = "", timestamp: Optional[float] = None):
        """从对话中提取记忆并存入"""
        if timestamp is None:
            timestamp = time.time()
        
        # 调用 LLM 提取记忆（根据对话语言选择 prompt）
        if contains_cjk(conversation_text):
            prompt = EXTRACTION_PROMPT_CN
            system_msg = "你是一个精确的记忆提取助手。只返回有效的 JSON。"
        else:
            prompt = EXTRACTION_PROMPT_EN
            system_msg = "You are a precise memory extraction assistant. Return ONLY valid JSON."
        
        result = chat_completion_json(
            system=system_msg,
            user=prompt.format(conversation=conversation_text[:2000]),
            temperature=0.1,
        )
        
        memories = result.get("memories", [])
        if not memories or not isinstance(memories, list):
            return []
        
        stored = []
        for mem_text in memories:
            if not mem_text or not isinstance(mem_text, str) or len(mem_text.strip()) < 3:
                continue
            
            mem_text = mem_text.strip()
            
            # 避免完全重复
            cursor = self.conn.execute(
                "SELECT id FROM memories WHERE content = ? AND (user_id = ? OR user_id = '')",
                (mem_text, user_id)
            )
            if cursor.fetchone():
                continue
            
            cursor = self.conn.execute(
                "INSERT INTO memories (content, created_at, user_id) VALUES (?, ?, ?)",
                (mem_text, timestamp, user_id)
            )
            mem_id = cursor.lastrowid
            
            # 写入 FTS 索引
            self.conn.execute(
                "INSERT INTO memory_fts (rowid, content) VALUES (?, ?)",
                (mem_id, mem_text)
            )
            
            stored.append({"memory": mem_text, "created_at": timestamp})
        
        self.conn.commit()
        return stored
    
    def search(self, query: str, user_id: str = "", top_k: int = 30) -> list[dict]:
        """检索相关记忆（兼容中英文，中文用改进的关键词+时间戳感知检索）"""
        # 中文查询走 LIKE 多关键词匹配 + 时间戳日期感知
        if contains_cjk(query):
            rows = cn_like_search(self.conn, query, user_id, top_k, table_name="memories")
            results = [{"memory": r[1], "score": r[3], "created_at": r[2]} for r in rows]
            return results if results else []

        # 英文查询走 FTS5
        fts_query = build_fts_query(query)
        if not fts_query:
            cursor = self.conn.execute(
                "SELECT id, content, created_at FROM memories WHERE user_id = ? OR user_id = '' ORDER BY created_at DESC LIMIT ?",
                (user_id, top_k)
            )
            rows = cursor.fetchall()
            return [{"memory": r[1], "score": 1.0, "created_at": r[2]} for r in rows]

        try:
            cursor = self.conn.execute(
                """
                SELECT m.id, m.content, m.created_at, bm25(memory_fts) as score
                FROM memory_fts
                JOIN memories m ON m.id = memory_fts.rowid
                WHERE memory_fts MATCH ?
                  AND (m.user_id = ? OR m.user_id = '')
                ORDER BY score
                LIMIT ?
                """,
                (fts_query, user_id, top_k)
            )
            rows = cursor.fetchall()
        except Exception:
            words = [w.strip() for w in query.split() if w.strip() and len(w.strip()) > 1]
            like_query = f"%{words[0]}%" if words else "%%"
            cursor = self.conn.execute(
                "SELECT id, content, created_at, 0.0 as score FROM memories WHERE content LIKE ? AND (user_id = ? OR user_id = '') ORDER BY created_at DESC LIMIT ?",
                (like_query, user_id, top_k)
            )
            rows = cursor.fetchall()

        # bm25 分数越低越好，转成相似度
        if rows and rows[0][3] > 0:
            max_score = max(r[3] for r in rows)
            min_score = min(r[3] for r in rows)
            if max_score != min_score:
                results = [
                    {
                        "memory": r[1],
                        "score": 1.0 - (r[3] - min_score) / (max_score - min_score + 0.001),
                        "created_at": r[2],
                    }
                    for r in rows
                ]
            else:
                results = [{"memory": r[1], "score": 1.0, "created_at": r[2]} for r in rows]
        else:
            results = [{"memory": r[1], "score": 1.0, "created_at": r[2]} for r in rows]

        return results
    
    def count_memories(self, user_id: str = "") -> int:
        """统计记忆条目数"""
        if user_id:
            cur = self.conn.execute(
                "SELECT COUNT(*) FROM memories WHERE user_id = ?", (user_id,))
        else:
            cur = self.conn.execute("SELECT COUNT(*) FROM memories")
        return cur.fetchone()[0]
    
    def close(self):
        self.conn.close()
