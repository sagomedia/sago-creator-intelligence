"""
SAGO MEDIA GROUPS — Creator Intelligence & Distribution Hub
Module: Telemetry Ingestion Worker & Normalization Pipeline
Author / Intern: Barath V (SRM IST, Reg: EA2532251010775)
Company: SAGO Media Groups / SAGO Automation
"""

import json
import sqlite3
import datetime
from typing import Dict, Any, List

DB_FILE = "sago_pulse.db"

def init_db(db_path: str = DB_FILE):
    """Initializes local SQLite database with normalized schema."""
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS channels (
        id TEXT PRIMARY KEY,
        platform TEXT NOT NULL,
        handle TEXT NOT NULL,
        title TEXT NOT NULL,
        subscribers_count INTEGER DEFAULT 0,
        total_views_count INTEGER DEFAULT 0,
        last_synced_at TEXT
    );
    """)
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
        FOREIGN KEY(channel_id) REFERENCES channels(id)
    );
    """)
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
        snapshot_timestamp TEXT,
        FOREIGN KEY(content_item_id) REFERENCES content_items(id)
    );
    """)
    conn.commit()
    conn.close()

def calculate_virality_score(views: int, likes: int, comments: int, shares: int) -> float:
    """Computes virality index: ((shares * 3 + comments * 2 + likes) / views) * 100."""
    if views <= 0:
        return 0.0
    score = ((shares * 3 + comments * 2 + likes) / views) * 100
    return round(score, 2)

def normalize_youtube_payload(raw_json: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalizes official YouTube Data API v3 response.
    Expected raw structure contains 'snippet' and 'statistics'.
    """
    snippet = raw_json.get("snippet", {})
    stats = raw_json.get("statistics", {})
    
    views = int(stats.get("viewCount", 0))
    likes = int(stats.get("likeCount", 0))
    comments = int(stats.get("commentCount", 0))
    # YouTube doesn't expose public direct shares via data v3, estimated based on interaction coefficient
    estimated_shares = int(likes * 0.12)
    
    return {
        "platform": "youtube",
        "platform_item_id": raw_json.get("id"),
        "title": snippet.get("title", "Untitled YouTube Video"),
        "published_at": snippet.get("publishedAt"),
        "views": views,
        "likes": likes,
        "comments": comments,
        "shares": estimated_shares,
        "virality_score": calculate_virality_score(views, likes, comments, estimated_shares)
    }

def normalize_apify_instagram_payload(raw_json: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalizes Apify Actor scraper JSON payload for Instagram Reels.
    """
    views = int(raw_json.get("videoViewCount") or raw_json.get("videoPlayCount") or 0)
    likes = int(raw_json.get("likesCount", 0))
    comments = int(raw_json.get("commentsCount", 0))
    shares = int(raw_json.get("sharesCount", 0) or (likes * 0.18))
    
    return {
        "platform": "instagram",
        "platform_item_id": raw_json.get("shortCode") or raw_json.get("id"),
        "title": raw_json.get("caption", "Instagram Reel")[:60],
        "published_at": raw_json.get("timestamp"),
        "views": views,
        "likes": likes,
        "comments": comments,
        "shares": shares,
        "virality_score": calculate_virality_score(views, likes, comments, shares)
    }

def normalize_linkedin_payload(raw_json: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalizes LinkedIn Community Management API share statistics JSON.
    """
    stats = raw_json.get("totalShareStatistics", {})
    views = int(stats.get("impressionCount", 0))
    likes = int(stats.get("likeCount", 0))
    comments = int(stats.get("commentCount", 0))
    shares = int(stats.get("shareCount", 0))
    
    return {
        "platform": "linkedin",
        "platform_item_id": raw_json.get("activityUrn", "urn:li:activity:0"),
        "title": raw_json.get("commentary", "LinkedIn Post")[:60],
        "published_at": raw_json.get("createdAt"),
        "views": views,
        "likes": likes,
        "comments": comments,
        "shares": shares,
        "virality_score": calculate_virality_score(views, likes, comments, shares)
    }

def ingest_metric_batch(items: List[Dict[str, Any]], db_path: str = DB_FILE) -> int:
    """Saves normalized metric items into SQLite database."""
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    inserted = 0
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    for item in items:
        content_id = f"SMG-{item['platform'][:2].upper()}-{item['platform_item_id']}"
        # Upsert content item
        cur.execute("""
        INSERT OR REPLACE INTO content_items (id, platform, platform_item_id, content_type, title, published_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (content_id, item["platform"], str(item["platform_item_id"]), "short", item["title"], item.get("published_at", now)))
        
        # Insert time-series snapshot
        cur.execute("""
        INSERT INTO metric_snapshots (content_item_id, views_count, likes_count, comments_count, shares_count, virality_score, snapshot_timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (content_id, item["views"], item["likes"], item["comments"], item["shares"], item["virality_score"], now))
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
        "snippet": {"title": "AI Controls Humans — Short Film Teaser", "publishedAt": "2026-10-01T10:00:00Z"},
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
