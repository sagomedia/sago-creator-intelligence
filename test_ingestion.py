import unittest
import os
import sqlite3
from ingestion_worker import (
    safe_int,
    calculate_virality_score,
    normalize_youtube_payload,
    normalize_apify_instagram_payload,
    normalize_linkedin_payload,
    init_db,
    ingest_metric_batch
)

class TestIngestionWorker(unittest.TestCase):
    def setUp(self):
        self.test_db = "test_sago_pulse.db"
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
        init_db(self.test_db)

    def tearDown(self):
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_safe_int_conversions(self):
        """Validates safe_int across edge cases and malformed inputs."""
        self.assertEqual(safe_int(None), 0)
        self.assertEqual(safe_int(""), 0)
        self.assertEqual(safe_int("   "), 0)
        self.assertEqual(safe_int("1,250"), 1250)
        self.assertEqual(safe_int("25.5"), 25)
        self.assertEqual(safe_int("12k"), 12000)
        self.assertEqual(safe_int("1.5M"), 1500000)
        self.assertEqual(safe_int("N/A"), 0)
        self.assertEqual(safe_int(42), 42)
        self.assertEqual(safe_int(42.8), 42)

    def test_virality_calculation_zero_views(self):
        """Zero and negative views should yield 0.0 virality without division error."""
        self.assertEqual(calculate_virality_score(0, 10, 5, 2), 0.0)
        self.assertEqual(calculate_virality_score(-100, 10, 5, 2), 0.0)

    def test_virality_calculation_positive(self):
        """Verifies mathematical formula: ((shares * 3 + comments * 2 + likes) / views) * 100."""
        # ((10 * 3 + 5 * 2 + 50) / 1000) * 100 = (90 / 1000) * 100 = 9.0
        score = calculate_virality_score(1000, 50, 5, 10)
        self.assertEqual(score, 9.0)

    def test_youtube_normalization_standard(self):
        raw = {
            "id": "test_yt_01",
            "snippet": {"title": "Test Title #shorts", "publishedAt": "2026-10-01T00:00:00Z"},
            "statistics": {"viewCount": "10000", "likeCount": "500", "commentCount": "50"}
        }
        res = normalize_youtube_payload(raw)
        self.assertEqual(res["platform"], "youtube")
        self.assertEqual(res["platform_item_id"], "test_yt_01")
        self.assertEqual(res["content_type"], "short")
        self.assertEqual(res["views"], 10000)
        self.assertEqual(res["likes"], 500)
        self.assertEqual(res["comments"], 50)
        self.assertGreater(res["virality_score"], 0)

    def test_youtube_normalization_null_and_missing_guards(self):
        """Ensures None or missing fields do not raise TypeError or ValueError."""
        raw_nulls = {
            "id": None,
            "snippet": None,
            "statistics": {"viewCount": None, "likeCount": None, "commentCount": ""}
        }
        res = normalize_youtube_payload(raw_nulls)
        self.assertEqual(res["views"], 0)
        self.assertEqual(res["likes"], 0)
        self.assertEqual(res["comments"], 0)
        self.assertEqual(res["shares"], 0)
        self.assertEqual(res["virality_score"], 0.0)

        # Empty dict payload
        res_empty = normalize_youtube_payload({})
        self.assertEqual(res_empty["platform"], "youtube")
        self.assertEqual(res_empty["views"], 0)

    def test_apify_instagram_normalization_standard(self):
        raw = {
            "shortCode": "test_ig_01",
            "caption": "Viral Reel Caption",
            "videoPlayCount": 20000,
            "likesCount": 1500,
            "commentsCount": 100,
            "sharesCount": 300,
            "timestamp": "2026-10-02T00:00:00Z"
        }
        res = normalize_apify_instagram_payload(raw)
        self.assertEqual(res["platform"], "instagram")
        self.assertEqual(res["content_type"], "reel")
        self.assertEqual(res["views"], 20000)
        self.assertEqual(res["shares"], 300)
        self.assertGreater(res["virality_score"], 0)

    def test_apify_instagram_null_guards(self):
        """Apify scraper payloads often return nulls when metrics are hidden."""
        raw_nulls = {
            "likesCount": None,
            "commentsCount": None,
            "sharesCount": None,
            "videoViewCount": None,
            "caption": None
        }
        res = normalize_apify_instagram_payload(raw_nulls)
        self.assertEqual(res["views"], 0)
        self.assertEqual(res["likes"], 0)
        self.assertEqual(res["virality_score"], 0.0)

    def test_linkedin_normalization_standard(self):
        raw = {
            "activityUrn": "urn:li:activity:9999",
            "commentary": "Deep Dive into Enterprise AI",
            "createdAt": "2026-10-03T00:00:00Z",
            "totalShareStatistics": {
                "impressionCount": 5000,
                "likeCount": 200,
                "commentCount": 30,
                "shareCount": 45
            }
        }
        res = normalize_linkedin_payload(raw)
        self.assertEqual(res["platform"], "linkedin")
        self.assertEqual(res["content_type"], "post")
        self.assertEqual(res["views"], 5000)
        self.assertEqual(res["shares"], 45)

    def test_linkedin_normalization_null_guards(self):
        """Handles completely null totalShareStatistics object."""
        res = normalize_linkedin_payload({"totalShareStatistics": None, "commentary": None})
        self.assertEqual(res["views"], 0)
        self.assertEqual(res["likes"], 0)
        self.assertEqual(res["virality_score"], 0.0)

    def test_database_schema_completeness(self):
        """Verifies all 5 relational tables and master seed data are present in init_db."""
        conn = sqlite3.connect(self.test_db)
        cur = conn.cursor()
        tables = [t[0] for t in cur.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()]
        expected_tables = ["channels", "content_items", "metric_snapshots", "publishing_queue", "connector_quotas"]
        for expected in expected_tables:
            self.assertIn(expected, tables, f"Expected table '{expected}' missing from database.")
        
        # Verify seed records
        cur.execute("SELECT count(*) FROM channels;")
        self.assertGreaterEqual(cur.fetchone()[0], 3)
        cur.execute("SELECT count(*) FROM connector_quotas;")
        self.assertGreaterEqual(cur.fetchone()[0], 3)
        conn.close()

    def test_database_batch_ingest(self):
        item = {
            "platform": "youtube",
            "channel_id": "sago_media_yt",
            "platform_item_id": "item_123",
            "content_type": "short",
            "title": "Batch Test Item",
            "published_at": "2026-10-01T00:00:00Z",
            "views": 5000,
            "likes": 200,
            "comments": 20,
            "shares": 30,
            "virality_score": 7.0
        }
        count = ingest_metric_batch([item], self.test_db)
        self.assertEqual(count, 1)

        conn = sqlite3.connect(self.test_db)
        cur = conn.cursor()
        cur.execute("SELECT count(*) FROM content_items;")
        c_count = cur.fetchone()[0]
        cur.execute("SELECT count(*) FROM metric_snapshots;")
        s_count = cur.fetchone()[0]
        cur.execute("SELECT channel_id, content_type FROM content_items WHERE id = 'SMG-YO-item_123';")
        row = cur.fetchone()
        conn.close()

        self.assertEqual(c_count, 1)
        self.assertEqual(s_count, 1)
        self.assertEqual(row[0], "sago_media_yt")
        self.assertEqual(row[1], "short")

if __name__ == "__main__":
    unittest.main()
