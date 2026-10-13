import unittest
import os
import sqlite3
from ingestion_worker import (
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

    def test_virality_calculation_zero_views(self):
        score = calculate_virality_score(0, 10, 5, 2)
        self.assertEqual(score, 0.0)

    def test_virality_calculation_positive(self):
        # ((shares * 3 + comments * 2 + likes) / views) * 100
        # ((10 * 3 + 5 * 2 + 50) / 1000) * 100 = ((30 + 10 + 50) / 1000) * 100 = (90 / 1000) * 100 = 9.0
        score = calculate_virality_score(1000, 50, 5, 10)
        self.assertEqual(score, 9.0)

    def test_youtube_normalization(self):
        raw = {
            "id": "test_yt_01",
            "snippet": {"title": "Test Title", "publishedAt": "2026-10-01T00:00:00Z"},
            "statistics": {"viewCount": "10000", "likeCount": "500", "commentCount": "50"}
        }
        res = normalize_youtube_payload(raw)
        self.assertEqual(res["platform"], "youtube")
        self.assertEqual(res["platform_item_id"], "test_yt_01")
        self.assertEqual(res["views"], 10000)
        self.assertEqual(res["likes"], 500)
        self.assertEqual(res["comments"], 50)
        self.assertGreater(res["virality_score"], 0)

    def test_apify_instagram_normalization(self):
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
        self.assertEqual(res["views"], 20000)
        self.assertEqual(res["shares"], 300)
        self.assertGreater(res["virality_score"], 0)

    def test_linkedin_normalization(self):
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
        self.assertEqual(res["views"], 5000)
        self.assertEqual(res["shares"], 45)

    def test_database_batch_ingest(self):
        item = {
            "platform": "youtube",
            "platform_item_id": "item_123",
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
        conn.close()

        self.assertEqual(c_count, 1)
        self.assertEqual(s_count, 1)

if __name__ == "__main__":
    unittest.main()
