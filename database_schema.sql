-- ==============================================================================
-- SAGO MEDIA GROUPS — Unified Telemetry & Publishing Data Store
-- Module: Ingestion Engine & Time-Series Metric Normalization
-- Intern Contributor: Barath V (SRM IST, Reg: EA2532251010775)
-- Project: SAGO Creator Intelligence & Distribution Hub (SAGO-Pulse)
-- ==============================================================================

-- 1. Tracked Social Media Channels & Creator Accounts
CREATE TABLE IF NOT EXISTS channels (
    id VARCHAR(64) PRIMARY KEY,
    platform VARCHAR(32) NOT NULL, -- 'youtube', 'instagram', 'linkedin', 'x'
    handle VARCHAR(128) NOT NULL,
    title VARCHAR(256) NOT NULL,
    profile_pic_url TEXT,
    subscribers_count INTEGER DEFAULT 0,
    total_views_count BIGINT DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_synced_at TIMESTAMP WITH TIME ZONE,
    status VARCHAR(32) DEFAULT 'ACTIVE'
);

-- 2. Individual Published Content Items (Videos, Shorts, Reels, Articles)
CREATE TABLE IF NOT EXISTS content_items (
    id VARCHAR(128) PRIMARY KEY,
    channel_id VARCHAR(64) REFERENCES channels(id) ON DELETE CASCADE,
    platform VARCHAR(32) NOT NULL,
    platform_item_id VARCHAR(128) NOT NULL,
    content_type VARCHAR(32) NOT NULL, -- 'short', 'reel', 'long_video', 'post'
    title TEXT NOT NULL,
    caption TEXT,
    published_at TIMESTAMP WITH TIME ZONE,
    thumbnail_url TEXT,
    permalink TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. Time-Series Telemetry Metric Snapshots (Captured Hourly)
CREATE TABLE IF NOT EXISTS metric_snapshots (
    id SERIAL PRIMARY KEY,
    content_item_id VARCHAR(128) REFERENCES content_items(id) ON DELETE CASCADE,
    views_count INTEGER DEFAULT 0,
    watch_time_seconds INTEGER DEFAULT 0,
    likes_count INTEGER DEFAULT 0,
    comments_count INTEGER DEFAULT 0,
    shares_count INTEGER DEFAULT 0,
    virality_score NUMERIC(6, 2) DEFAULT 0.00,
    snapshot_timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 4. Outbound Cross-Platform Publishing & Distribution Queue
CREATE TABLE IF NOT EXISTS publishing_queue (
    job_id VARCHAR(64) PRIMARY KEY,
    media_url TEXT NOT NULL,
    title VARCHAR(256) NOT NULL,
    caption TEXT,
    target_platforms TEXT NOT NULL, -- Comma-separated: 'youtube_shorts,instagram_reels,linkedin'
    status VARCHAR(32) DEFAULT 'PENDING', -- 'PENDING', 'QUEUED', 'PROCESSING', 'PUBLISHED', 'FAILED'
    scheduled_for TIMESTAMP WITH TIME ZONE,
    executed_at TIMESTAMP WITH TIME ZONE,
    retry_count INTEGER DEFAULT 0,
    error_log TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 5. API Connector Quota & Rate-Limit Tracking
CREATE TABLE IF NOT EXISTS connector_quotas (
    connector_name VARCHAR(64) PRIMARY KEY,
    daily_quota_limit INTEGER NOT NULL,
    units_used_today INTEGER DEFAULT 0,
    last_reset_date DATE DEFAULT CURRENT_DATE,
    avg_latency_ms INTEGER DEFAULT 0,
    health_status VARCHAR(32) DEFAULT 'HEALTHY'
);

-- Indexing for Rapid Time-Series Aggregations
CREATE INDEX IF NOT EXISTS idx_snapshots_content_time ON metric_snapshots(content_item_id, snapshot_timestamp);
CREATE INDEX IF NOT EXISTS idx_content_platform ON content_items(platform, published_at);
CREATE INDEX IF NOT EXISTS idx_queue_status ON publishing_queue(status, scheduled_for);
