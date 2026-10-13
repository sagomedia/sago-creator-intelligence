"""
SAGO MEDIA GROUPS — Creator Intelligence & Distribution Hub (SAGO-Pulse)
Module: Telemetry Ingestion Worker & Normalization Pipeline
Author / Intern: Barath V (SRM IST, Reg: EA2532251010775)
Company: SAGO Media Groups / SAGO Automation
"""

import json
import sqlite3
import datetime
import re
from typing import Dict, Any, List, Optional

DB_FILE = "sago_pulse.db"

def safe_int(value: Any, default: int = 0) -> int:
    """
    Safely converts arbitrary input to an integer.
    Handles None, empty strings, comma-formatted numbers, floats, and malformed strings.
    """
    if value is None:
        return default
    if isinstance(value, (int, float)):
        return int(value)
    if isinstance(value, str):
        cleaned = value.strip().replace(",", "")
        if not cleaned:
            return default
        try:
            return int(float(cleaned))
        except (ValueError, TypeError):
            # Check for suffixes like 'k' or 'm' if scrapers return formatted strings
            m = re.match(r"^([\d.]+)\s*([kKmM])$", cleaned)
            if m:
                num, suffix = float(m.group(1)), m.group(2).lower()
                mult = 1_000 if suffix == "k" else 1_000_000
                return int(num * mult)
            return default
    return default

def init_db(db_path: str = DB_FILE):
    """
    Initializes local SQLite database with normalized schema adhering to database_schema.sql.
    Creates all 5 core tables and seeds initial channels and connector quotas.
    """
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    # 1. Channels
    cur.execute("""
    CREATE TABLE IF NOT EXISTS channels (
        id TEXT PRIMARY KEY,
        platform TEXT NOT NULL,
        handle TEXT NOT NULL,
        title TEXT NOT NULL,
        profile_pic_url TEXT,
        subscribers_count INTEGER DEFAULT 0,
        total_views_count INTEGER DEFAULT 0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        last_synced_at TEXT,
        status TEXT DEFAULT 'ACTIVE'
    );
    """)

    # 2. Content Items
    cur.execute("""
    CREATE TABLE IF NOT EXISTS content_items (
        id TEXT PRIMARY KEY,
        channel_id TEXT,
        platform TEXT NOT NULL,
        platform_item_id TEXT NOT NULL,
        content_type TEXT NOT NULL,
        title TEXT NOT NULL,
        caption TEXT,
        published_at TEXT,
        thumbnail_url TEXT,
        permalink TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(channel_id) REFERENCES channels(id) ON DELETE CASCADE
    );
    """)

    # 3. Metric Snapshots
    cur.execute("""
    CREATE TABLE IF NOT EXISTS metric_snapshots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content_item_id TEXT,
        views_count INTEGER DEFAULT 0,
        watch_time_seconds INTEGER DEFAULT 0,
        likes_count INTEGER DEFAULT 0,
        comments_count INTEGER DEFAULT 0,
        shares_count INTEGER DEFAULT 0,
        virality_score REAL DEFAULT 0.0,
        snapshot_timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(content_item_id) REFERENCES content_items(id) ON DELETE CASCADE
    );
    """)

    # 4. Publishing Queue
    cur.execute("""
    CREATE TABLE IF NOT EXISTS publishing_queue (
        job_id TEXT PRIMARY KEY,
        media_url TEXT NOT NULL,
        title TEXT NOT NULL,
        caption TEXT,
        target_platforms TEXT NOT NULL,
        status TEXT DEFAULT 'PENDING',
        scheduled_for TEXT,
        executed_at TEXT,
        retry_count INTEGER DEFAULT 0,
        error_log TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 5. Connector Quotas
    cur.execute("""
    CREATE TABLE IF NOT EXISTS connector_quotas (
        connector_name TEXT PRIMARY KEY,
        daily_quota_limit INTEGER NOT NULL,
        units_used_today INTEGER DEFAULT 0,
        last_reset_date TEXT DEFAULT CURRENT_DATE,
        avg_latency_ms INTEGER DEFAULT 0,
        health_status TEXT DEFAULT 'HEALTHY'
    );
    """)

    # Seed master channels if empty
    cur.execute("SELECT count(*) FROM channels;")
    if cur.fetchone()[0] == 0:
        cur.executemany("""
        INSERT INTO channels (id, platform, handle, title, subscribers_count, total_views_count)
        VALUES (?, ?, ?, ?, ?, ?)
        """, [
            ("sago_media_yt", "youtube", "@sagomedia", "SAGO Media Groups Official", 184000, 1420000),
            ("sago_media_ig", "instagram", "@sagomedia.official", "SAGO Media Groups", 92400, 890000),
            ("sago_media_li", "linkedin", "sago-media-groups", "SAGO Media Groups Corporate", 34500, 240000)
        ])

    # Seed connector quotas if empty
    cur.execute("SELECT count(*) FROM connector_quotas;")
    if cur.fetchone()[0] == 0:
        cur.executemany("""
        INSERT INTO connector_quotas (connector_name, daily_quota_limit, units_used_today, avg_latency_ms, health_status)
        VALUES (?, ?, ?, ?, ?)
        """, [
            ("YouTube Data API v3", 10000, 2340, 185, "HEALTHY"),
            ("Apify Instagram Scraper", 5000, 1420, 320, "HEALTHY"),
            ("LinkedIn Community API", 2000, 310, 210, "HEALTHY")
        ])

    conn.commit()
    conn.close()

def calculate_virality_score(views: int, likes: int, comments: int, shares: int) -> float:
    """
    Computes virality index: ((shares * 3 + comments * 2 + likes) / views) * 100.
    Guards against division by zero and negative metric values.
    """
    safe_views = max(0, safe_int(views))
    if safe_views <= 0:
        return 0.0
    safe_likes = max(0, safe_int(likes))
    safe_comments = max(0, safe_int(comments))
    safe_shares = max(0, safe_int(shares))
    score = ((safe_shares * 3 + safe_comments * 2 + safe_likes) / safe_views) * 100
    return round(score, 2)

def normalize_youtube_payload(raw_json: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Normalizes official YouTube Data API v3 response.
    Expected raw structure contains 'snippet' and 'statistics'.
    Safely handles None or malformed sub-dictionaries.
    """
    if not isinstance(raw_json, dict):
        raw_json = {}
    
    snippet = raw_json.get("snippet") or {}
    stats = raw_json.get("statistics") or {}
    
    views = safe_int(stats.get("viewCount"))
    likes = safe_int(stats.get("likeCount"))
    comments = safe_int(stats.get("commentCount"))
    # YouTube Data API v3 doesn't expose public shares directly, estimated via standard engagement factor
    estimated_shares = int(likes * 0.12)
    
    # Determine content type: default to short if title/description indicates, else video
    title = snippet.get("title") or "Untitled YouTube Video"
    content_type = "short" if ("#shorts" in title.lower() or "short" in title.lower()) else "video"

    return {
        "platform": "youtube",
        "channel_id": "sago_media_yt",
        "platform_item_id": str(raw_json.get("id") or "yt_unknown"),
        "content_type": content_type,
        "title": title,
        "published_at": snippet.get("publishedAt"),
        "views": views,
        "likes": likes,
        "comments": comments,
        "shares": estimated_shares,
        "virality_score": calculate_virality_score(views, likes, comments, estimated_shares)
    }

def normalize_apify_instagram_payload(raw_json: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Normalizes Apify Actor scraper JSON payload for Instagram Reels.
    Safely handles None, null fields, and alternative scraper property names.
    """
    if not isinstance(raw_json, dict):
        raw_json = {}

    views = safe_int(raw_json.get("videoViewCount") or raw_json.get("videoPlayCount") or raw_json.get("viewsCount"))
    likes = safe_int(raw_json.get("likesCount"))
    comments = safe_int(raw_json.get("commentsCount"))
    shares_raw = raw_json.get("sharesCount")
    shares = safe_int(shares_raw) if shares_raw is not None else int(likes * 0.18)
    
    caption = raw_json.get("caption") or "Instagram Reel"
    title = caption[:60].strip()

    return {
        "platform": "instagram",
        "channel_id": "sago_media_ig",
        "platform_item_id": str(raw_json.get("shortCode") or raw_json.get("id") or "ig_unknown"),
        "content_type": "reel",
        "title": title,
        "published_at": raw_json.get("timestamp"),
        "views": views,
        "likes": likes,
        "comments": comments,
        "shares": shares,
        "virality_score": calculate_virality_score(views, likes, comments, shares)
    }

def normalize_linkedin_payload(raw_json: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Normalizes LinkedIn Community Management API share statistics JSON.
    Safely handles None totalShareStatistics or null sub-fields.
    """
    if not isinstance(raw_json, dict):
        raw_json = {}

    stats = raw_json.get("totalShareStatistics") or {}
    views = safe_int(stats.get("impressionCount") or stats.get("viewCount"))
    likes = safe_int(stats.get("likeCount") or stats.get("reactionCount"))
    comments = safe_int(stats.get("commentCount"))
    shares = safe_int(stats.get("shareCount") or stats.get("resharesCount"))
    
    commentary = raw_json.get("commentary") or "LinkedIn Post"
    title = commentary[:60].strip()

    return {
        "platform": "linkedin",
        "channel_id": "sago_media_li",
        "platform_item_id": str(raw_json.get("activityUrn") or raw_json.get("id") or "urn:li:activity:0"),
        "content_type": "post",
        "title": title,
        "published_at": raw_json.get("createdAt"),
        "views": views,
        "likes": likes,
        "comments": comments,
        "shares": shares,
        "virality_score": calculate_virality_score(views, likes, comments, shares)
    }

def ingest_metric_batch(items: List[Dict[str, Any]], db_path: str = DB_FILE) -> int:
    """
    Persists normalized metric items into SQLite database.
    Inserts or updates content_items and appends time-series metric_snapshots.
    """
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    inserted = 0
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    for item in items:
        platform = item.get("platform", "unknown")
        item_id = item.get("platform_item_id", "0")
        content_id = f"SMG-{platform[:2].upper()}-{item_id}"
        channel_id = item.get("channel_id") or f"sago_media_{platform[:2].lower()}"
        content_type = item.get("content_type", "short")
        title = item.get("title", "Untitled Content")
        pub_at = item.get("published_at") or now

        # Upsert content item
        cur.execute("""
        INSERT INTO content_items (id, channel_id, platform, platform_item_id, content_type, title, published_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            title=excluded.title,
            published_at=COALESCE(excluded.published_at, content_items.published_at)
        """, (content_id, channel_id, platform, str(item_id), content_type, title, pub_at))
        
        # Insert time-series snapshot
        cur.execute("""
        INSERT INTO metric_snapshots (content_item_id, views_count, likes_count, comments_count, shares_count, virality_score, snapshot_timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (content_id, item.get("views", 0), item.get("likes", 0), item.get("comments", 0), item.get("shares", 0), item.get("virality_score", 0.0), now))
        inserted += 1

    conn.commit()
    conn.close()
    return inserted

if __name__ == "__main__":
    print("Initializing SAGO Creator Intelligence Telemetry Engine...")
    init_db()
    
    # Mock Raw API Payloads
    sample_yt = {
        "id": "yt_sample_01",
        "snippet": {"title": "AI Controls Humans — Short Film Teaser #shorts", "publishedAt": "2026-10-01T10:00:00Z"},
        "statistics": {"viewCount": "485200", "likeCount": "38400", "commentCount": "1820"}
    }
    sample_ig = {
        "shortCode": "ig_sample_02",
        "caption": "Somrat Director's Cut Kinetic Teaser",
        "videoPlayCount": 612400,
        "likesCount": 52800,
        "commentsCount": 2940,
        "sharesCount": 8920,
        "timestamp": "2026-10-03T14:30:00Z"
    }
    sample_li = {
        "activityUrn": "li_sample_03",
        "commentary": "Autonomous Agent Workflows for Agencies",
        "createdAt": "2026-10-05T09:15:00Z",
        "totalShareStatistics": {
            "impressionCount": 124300,
            "likeCount": 12100,
            "commentCount": 640,
            "shareCount": 1890
        }
    }
    
    norm_yt = normalize_youtube_payload(sample_yt)
    norm_ig = normalize_apify_instagram_payload(sample_ig)
    norm_li = normalize_linkedin_payload(sample_li)
    
    print("Normalized YouTube:", norm_yt)
    print("Normalized Instagram:", norm_ig)
    print("Normalized LinkedIn:", norm_li)
    
    count = ingest_metric_batch([norm_yt, norm_ig, norm_li])
    print(f"Successfully ingested {count} snapshots into {DB_FILE}!")
