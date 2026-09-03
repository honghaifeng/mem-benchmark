"""
中文检索工具函数
解决 FTS5 对中文分词支持不好的问题

核心策略：
1. 优先提取高信息量关键词（专名、日期、核心名词）
2. bigram 仅作为补充，不抢占核心词位置
3. 日期感知检索：从问题中提取日期，优先返回该日期的记忆
"""
import re
from datetime import datetime, timezone


# 中文停用词（单字 + 常见无意义词）
_CN_STOP_WORDS = {
    '的', '了', '是', '我', '你', '他', '她', '它', '和', '与', '过',
    '什么', '哪', '哪个', '哪里', '多少', '在', '有', '不', '也', '都',
    '这', '那', '个', '就', '还', '把', '被', '给', '对', '到',
    '吗', '呢', '吧', '啊', '哦', '嗯', '要', '会', '能', '可以',
    '着', '地', '得', '所', '以', '但', '而', '及', '或',
    '跟', '同', '向', '从', '往', '为', '于', '由', '按',
    '关于', '根据', '通过', '按照', '对于', '至于', '虽然', '因为', '所以',
    '如果', '尽管', '即使', '除非', '只要', '只有', '无论',
    '怎么', '怎样', '如何', '为何', '为什么', '谁', '哪位',
    '何时', '何地', '何事', '何物', '哪种', '哪些', '几', '几号',
    '一次', '一样', '这种', '那种', '这样', '那样',
    '曾经', '通常', '一般', '之前', '之后', '之间',
    '一个', '一部', '一本', '一首', '一位', '一种',
    '我和', '和你', '你聊', '聊了', '聊到', '到了', '了一',
    '分享', '享过', '过我', '我看', '我曾', '经在', '在4',
    '月2', '号这', '这天', '我和你', '你分享',
}

# 低信息量 bigram（单独出现无意义）
_LOW_VALUE_BIGRAMS = {
    '我和', '和你', '你聊', '聊了', '聊到', '到了', '了一',
    '我曾', '经在', '在4', '月2', '号这', '这天',
    '你分', '分享', '享过', '过我', '我看',
    '你分', '享过', '是一', '是一',
    '我通', '常打', '打哪', '哪个', '个位',
    '是什', '什么', '么', '名的',
}


def contains_cjk(text: str) -> bool:
    """检查文本是否包含 CJK 字符"""
    for ch in text:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False


def extract_cn_keywords(query: str) -> list[str]:
    """
    从中文查询中提取高信息量关键词

    策略（按优先级）:
    1. 专名：书名号《》、引号内容、英文人名/地名
    2. 日期：X月X日, X年, X月等
    3. 核心名词：2-4字有意义片段（去停用词后）
    4. 补充 bigram：仅当关键词不足时
    """
    # --- 1. 提取专名（书名号、引号包裹的内容）---
    proper_nouns = []
    # 《xxx》格式
    for m in re.finditer(r'《([^》]+)》', query):
        proper_nouns.append(m.group(1))
    # 英文人名/地名（连续的英文字母）
    for m in re.finditer(r'[A-Za-z]{2,}', query):
        proper_nouns.append(m.group(0))

    # --- 2. 提取日期模式 ---
    date_patterns = []
    # X月X日 或 X月X号
    for m in re.finditer(r'\d{1,2}月\d{1,2}[日号]', query):
        date_patterns.append(m.group(0))
    # X月
    for m in re.finditer(r'(?<!\d)\d{1,2}月(?!d)', query):
        date_patterns.append(m.group(0))
    # X年
    for m in re.finditer(r'\d{4}年', query):
        date_patterns.append(m.group(0))
    # X日
    for m in re.finditer(r'\d{1,2}日', query):
        date_patterns.append(m.group(0))

    # --- 3. 按标点分割，提取核心名词 ---
    parts = re.split(
        r"[\uff0c\u3002\uff1f\uff01\u3001\uff1b\uff1a\u201c\u201d\u2018\u2019\uff08\uff09\(\)\[\]\u3010\u3011\u300a\u300b\s\?\.\,\!\;\:\'\-—_/\\]+",
        query
    )

    core_terms = []
    for part in parts:
        part = part.strip()
        if len(part) < 2:
            continue
        if part in _CN_STOP_WORDS:
            continue

        # 去掉纯数字
        if part.isdigit():
            continue

        # 提取有意义的子串
        # 对于 2-3 字的片段，直接保留
        if 2 <= len(part) <= 3:
            if part not in _CN_STOP_WORDS and part not in _LOW_VALUE_BIGRAMS:
                core_terms.append(part)
        # 对于 4 字以上的片段，提取 2-3 字子串
        elif len(part) > 3:
            # 先保留完整片段
            if part not in _CN_STOP_WORDS:
                core_terms.append(part)

            # 提取有意义的 2 字 bigram（跳过停用词组合）
            for j in range(len(part) - 1):
                bi = part[j:j+2]
                if len(bi) >= 2 and bi not in _CN_STOP_WORDS and bi not in _LOW_VALUE_BIGRAMS:
                    # 检查是否是数字+单位的组合（如"4月"）
                    if re.match(r'^[\d月年日号]$', bi[0]) and re.match(r'^[\d月年日号]$', bi[1]):
                        continue  # 日期模式已在上面提取
                    core_terms.append(bi)

            # 提取 3 字 trigram（前3和后3）
            if len(part) >= 5:
                tri_start = part[:3]
                tri_end = part[-3:]
                for tri in [tri_start, tri_end]:
                    if tri not in _CN_STOP_WORDS and len(tri) >= 3:
                        if tri not in _LOW_VALUE_BIGRAMS:
                            core_terms.append(tri)

    # --- 合并去重，按优先级排序 ---
    # 优先级：专名 > 日期 > 核心名词 > bigram
    all_keywords = []
    seen = set()

    # 专名优先
    for kw in proper_nouns:
        if kw not in seen and len(kw) >= 2:
            seen.add(kw)
            all_keywords.append(kw)

    # 日期次之
    for kw in date_patterns:
        if kw not in seen:
            seen.add(kw)
            all_keywords.append(kw)

    # 核心名词
    for kw in core_terms:
        if kw not in seen:
            seen.add(kw)
            all_keywords.append(kw)

    # 限制总数但保证覆盖查询各部分
    # 策略：每个分割部分至少贡献一个关键词
    if len(all_keywords) > 20:
        # 按来源部分均衡截取
        result = []
        # 保证专名和日期都在
        result.extend(all_keywords[:len(proper_nouns) + len(date_patterns)])
        remaining = all_keywords[len(proper_nouns) + len(date_patterns):]
        # 从剩余中取，尽量覆盖不同部分
        result.extend(remaining[:20 - len(result)])
        all_keywords = result

    return all_keywords[:25]  # 放宽到25个，覆盖更多


def extract_date_from_query(query: str) -> str | None:
    """
    从查询中提取日期字符串
    返回格式如 '04月27日' 或 '04月' 或 None
    """
    # 尝试匹配 X月X日 或 X月X号
    m = re.search(r'(\d{1,2})月(\d{1,2})[日号]', query)
    if m:
        month = m.group(1).zfill(2)
        day = m.group(2).zfill(2)
        return f"{month}月{day}日"

    # 匹配 X月X号
    m = re.search(r'(\d{1,2})月(\d{1,2})号', query)
    if m:
        month = m.group(1).zfill(2)
        day = m.group(2).zfill(2)
        return f"{month}月{day}日"

    # 匹配 X日（无月份）
    m = re.search(r'(\d{1,2})日', query)
    if m:
        day = m.group(1).zfill(2)
        return f"{day}日"

    return None


def cn_like_search(conn, query: str, user_id: str, top_k: int, table_name: str = "memories",
                    reference_year: int = 2023) -> list[tuple]:
    """
    对中文查询使用 LIKE 多关键词匹配 + 时间戳日期感知
    返回 [(id, content, created_at, score), ...]

    改进：
    1. 使用改进的关键词提取（优先专名、日期、核心词）
    2. 内容日期匹配：记忆内容中包含日期字符串的加权
    3. 时间戳日期感知：记忆的 created_at 落在查询日期范围内的加权（关键改进）
    4. 兜底策略更智能
    """
    keywords = extract_cn_keywords(query)
    query_date = extract_date_from_query(query)

    content_col = "content"

    if not keywords:
        # 无关键词，返回最近的记忆
        cursor = conn.execute(
            f"SELECT id, {content_col}, created_at, 0.0 as score FROM {table_name} "
            f"WHERE user_id = ? OR user_id = '' ORDER BY created_at DESC LIMIT ?",
            (user_id, top_k)
        )
        return cursor.fetchall()

    # 对每个关键词做 LIKE 查询，统计匹配数作为分数
    match_counts = {}  # id -> [content, created_at, match_count, matched_keywords]

    for kw in keywords:
        like_pattern = f"%{kw}%"
        try:
            cursor = conn.execute(
                f"SELECT id, {content_col}, created_at FROM {table_name} "
                f"WHERE {content_col} LIKE ? AND (user_id = ? OR user_id = '')",
                (like_pattern, user_id)
            )
            for row in cursor.fetchall():
                mem_id = row[0]
                if mem_id not in match_counts:
                    match_counts[mem_id] = [row[1], row[2], 0, set()]
                match_counts[mem_id][2] += 1
                match_counts[mem_id][3].add(kw)
        except Exception:
            continue

    # 如果查询包含日期，额外用日期做 LIKE 匹配（内容中含日期字符串）
    if query_date:
        date_patterns_to_try = [query_date]
        parts = re.match(r'(\d+)月(\d+)日', query_date)
        if parts:
            m, d = parts.group(1), parts.group(2)
            if m.startswith('0'):
                date_patterns_to_try.append(f"{int(m)}月{d}日")
                date_patterns_to_try.append(f"{int(m)}月{int(d)}日")
            date_patterns_to_try.append(f"{m}月{d}日")
            date_patterns_to_try.append(f"{m}月{int(d)}日")

        for dp in date_patterns_to_try:
            like_pattern = f"%{dp}%"
            try:
                cursor = conn.execute(
                    f"SELECT id, {content_col}, created_at FROM {table_name} "
                    f"WHERE {content_col} LIKE ? AND (user_id = ? OR user_id = '')",
                    (like_pattern, user_id)
                )
                for row in cursor.fetchall():
                    mem_id = row[0]
                    if mem_id not in match_counts:
                        match_counts[mem_id] = [row[1], row[2], 0, set()]
                    match_counts[mem_id][2] += 2  # 日期匹配加权
                    match_counts[mem_id][3].add(f"date:{dp}")
            except Exception:
                continue

    # === 时间戳日期感知（关键改进）===
    # 如果查询包含日期，用 created_at 时间戳范围 boost 对应日期的记忆
    # 这解决了"记忆内容不含日期但创建于该日期"的问题
    if query_date:
        m = re.match(r'(\d+)月(\d+)日', query_date)
        if m:
            month, day = int(m.group(1)), int(m.group(2))
            try:
                from datetime import datetime as _dt, timezone as _tz
                start_dt = _dt(reference_year, month, day, tzinfo=_tz.utc)
                end_dt = _dt(reference_year, month, day, 23, 59, 59, tzinfo=_tz.utc)
                start_ts = start_dt.timestamp()
                end_ts = end_dt.timestamp()

                # 对已有匹配结果中，created_at 在日期范围内的加权
                for mem_id in match_counts:
                    created_at = match_counts[mem_id][1]
                    if start_ts <= created_at <= end_ts:
                        match_counts[mem_id][2] += 3  # 时间戳日期匹配加权（比内容匹配更高）
                        match_counts[mem_id][3].add(f"ts_date:{month}月{day}日")

                # 还要额外检索该日期范围内的所有记忆（即使不匹配任何关键词）
                # 给它们一个基础分数，让它们有机会进入结果
                try:
                    cursor = conn.execute(
                        f"SELECT id, {content_col}, created_at FROM {table_name} "
                        f"WHERE created_at >= ? AND created_at <= ? "
                        f"AND (user_id = ? OR user_id = '')",
                        (start_ts, end_ts, user_id)
                    )
                    for row in cursor.fetchall():
                        mem_id = row[0]
                        if mem_id not in match_counts:
                            # 该日期的记忆但未匹配关键词，给中等分数
                            match_counts[mem_id] = [row[1], row[2], 2, {f"ts_date:{month}月{day}日"}]
                except Exception:
                    pass
            except Exception:
                pass

    # 按匹配数排序
    sorted_matches = sorted(
        match_counts.items(),
        key=lambda x: (-x[1][2], -x[1][1])  # 匹配数降序，时间降序
    )

    results = []
    for mem_id, (content, created_at, count, matched_kws) in sorted_matches[:top_k]:
        score = count / max(len(keywords), 1)  # 匹配比例作为分数
        results.append((mem_id, content, created_at, score))

    # 兜底：如果匹配结果太少，补充最近的记忆
    if len(results) < max(top_k // 2, 10):
        existing_ids = {r[0] for r in results}
        try:
            if existing_ids:
                placeholders = ",".join("?" * len(existing_ids))
                cursor = conn.execute(
                    f"SELECT id, {content_col}, created_at FROM {table_name} "
                    f"WHERE (user_id = ? OR user_id = '') AND id NOT IN ({placeholders}) "
                    f"ORDER BY created_at DESC LIMIT ?",
                    (user_id, *existing_ids, top_k - len(results))
                )
            else:
                cursor = conn.execute(
                    f"SELECT id, {content_col}, created_at FROM {table_name} "
                    f"WHERE (user_id = ? OR user_id = '') "
                    f"ORDER BY created_at DESC LIMIT ?",
                    (user_id, top_k - len(results))
                )
            for row in cursor.fetchall():
                results.append((row[0], row[1], row[2], 0.05))  # 低分补充
        except Exception:
            pass

    return results[:top_k]


def build_fts_query(query: str) -> str:
    """为 FTS5 构建查询（英文用）"""
    # 提取英文单词
    words = re.findall(r'[a-zA-Z]+', query)
    if not words:
        return ""

    # 过滤太短的词
    words = [w for w in words if len(w) >= 2]
    if not words:
        return ""

    # 用 OR 连接
    return " OR ".join(words)
