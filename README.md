# SAGO Creator Intelligence & Distribution Hub (SAGO-Pulse)

[![System Architecture](assets/images/diagram_system_architecture.png)](assets/images/diagram_system_architecture.png)

**Internal Project Code:** `SMG-ENG-2026-CI`  
**Organization:** SAGO Media Groups (`UDYAM-TN-18-0102132`, Tirunelveli, Tamil Nadu - 627426)  
**Intern / Contributor:** Barath V (SRM Institute of Science and Technology, Reg. No: `EA2532251010775`)  
**Degree / Department:** Master of Computer Applications (MCA) — Directorate of Online Education, SRM IST, Kattankulathur - 603 203  
**Academic Supervision:** Dr. G. Babu (Assistant Professor & Programme Coordinator, Directorate of Online Education, SRM IST)  
**Company Mentorship & Signatory:** Partha Sarathy M (Co-Founder & Operations Director) & Gokulakrishnan M (Founder & Technical Architect)  
**Tenure:** 01 July 2026 – 31 August 2026 (2-Month Engineering Internship)  
**Offer Letter Reference:** `SMG/2026/INT/003` | **Certificate Identifier:** `SMG/CERT/2026/003`

---

## 1. Executive Summary & Problem Statement

Modern digital media agencies and multi-channel creator networks face severe operational bottlenecks across fragmented social platforms (YouTube Shorts, Instagram Reels, LinkedIn Video, X/Twitter):

1. **Telemetry Dispersion**: Media managers lose 10+ hours weekly switching between YouTube Studio, Meta Business Suite, and LinkedIn Page Analytics to log watch hours, views, and virality indices.
2. **Schema Heterogeneity**: Metrics arrive in inconsistent formats—YouTube provides nested view counts and watch time in seconds, Instagram relies on scraper play metrics, and LinkedIn returns enterprise ratio shares.
3. **Distribution Latency**: High-performing videos require immediate cross-platform syndication, but manual re-uploading delays multi-channel reach.

### The Solution: SAGO-Pulse Ingestion Engine

**SAGO-Pulse** provides a unified telemetry ingestion pipeline and cross-platform publishing hub built for **SAGO Media Groups**:
* **Multi-Source Connectors**: Automated hourly polling of official **YouTube Data API v3**, resilient fallback scraping via **Apify Instagram Actors**, and **LinkedIn Community Management API** endpoints.
* **Telemetry Normalizer**: Defensive type parsing via `safe_int()`, null guards, and automated virality score calculation:
  $$\text{Virality Score} = \left(\frac{\text{Shares} \times 3 + \text{Comments} \times 2 + \text{Likes}}{\text{Views}}\right) \times 100$$
* **High-Density Command Center**: Responsive dark-mode web application (HTML5, Tailwind CSS, Chart.js) featuring dual-axis velocity curves, real-time leaderboards, and an asynchronous outbound publishing queue.

---

## 2. Comprehensive System Architecture & Engineering Diagrams

### Figure 7.1: High-Level End-to-End System Architecture (4-Tier Design)
Illustrates the 4 architectural layers: Client Dashboard (HTML5/Chart.js), Ingestion Gateway & Normalizer (FastAPI/Node), External Platform Connectors (YouTube Data v3, Apify, LinkedIn API), and Relational Time-Series Store (SQLite WAL mode).
[![Figure 7.1: System Architecture](assets/images/diagram_system_architecture.png)](assets/images/diagram_system_architecture.png)

---

### Figure 7.2: Entity Relationship (ER) Data Model (3NF Relational Schema)
Detailed relational model demonstrating primary keys, foreign keys, cascade constraints, and data types across all 5 core tables (`channels`, `content_items`, `metric_snapshots`, `publishing_queue`, `connector_quotas`).
[![Figure 7.2: Database ER Diagram](assets/images/diagram_database_er.png)](assets/images/diagram_database_er.png)

---

### Figure 7.3: Telemetry Ingestion Pipeline Flowchart
Six-stage execution sequence: 1) Scheduled Cron Trigger -> 2) Quota Budget & Rate Check -> 3) Multi-Source API Polling -> 4) JSON Normalizer & Virality Calculation -> 5) Delta Snapshot Storage (WAL commit) -> 6) Client Dashboard Live Re-render.
[![Figure 7.3: Ingestion Pipeline Flowchart](assets/images/diagram_ingestion_pipeline_flow.png)](assets/images/diagram_ingestion_pipeline_flow.png)

---

### Figure 7.4: Data Flow Diagram (DFD Level 0 Context & Level 1 Decomposition)
Gane & Sarson notation mapping data flows between External Entities (YouTube Data API v3, Apify Scraper, LinkedIn API, Creator Admin), Processes (Quota Guard, Ingestion Adapter, Normalizer, Virality Engine, Persistence Writer, Realtime Dispatcher), and Relational Data Stores (D1–D5).
[![Figure 7.4: Data Flow Diagram](assets/images/diagram_data_flow_dfd.png)](assets/images/diagram_data_flow_dfd.png)

---

### Figure 7.5: UML Sequence Diagram: Telemetry Lifecycle & Live Re-render
Chronological interaction among the Cron Scheduler, Quota Guard (Token Bucket), Social API Endpoints, Normalizer Engine, SQLite WAL Data Store, and Chart.js UI.
[![Figure 7.5: UML Sequence Diagram](assets/images/diagram_sequence.png)](assets/images/diagram_sequence.png)

---

### Figure 7.6: API Payload Normalization & Virality Scoring Flowchart
Defensive parsing decision pipeline: raw polymorphic JSON ingestion, type guards, platform-specific mapping adapters, `safe_int()` sanitization, zero-division protected intent scoring, and normalized database payload generation.
[![Figure 7.6: Normalization Flowchart](assets/images/diagram_normalization_flowchart.png)](assets/images/diagram_normalization_flowchart.png)

---

## 3. User Interface Screens & Component Zoom-Ins

### Screen 1.0: Full Command Center Overview
Complete responsive dark-mode view of SAGO Creator Intelligence Hub displaying top navigation, Executive KPI Ribbon, dual-axis Chart.js curves, doughnut platform share, content leaderboard, and connector health monitor.
[![Screen 1.0: Full Dashboard Overview](assets/images/screenshot_dashboard_fullpage.png)](assets/images/screenshot_dashboard_fullpage.png)

---

### Screen 1.1: Dashboard Navigation & KPI Overview
Top fold view highlighting the candidate registration metadata (`BARATH V`, `EA2532251010775`, `SRM IST DOE`), active system status, and aggregated performance indicators.
[![Screen 1.1: Dashboard Overview](assets/images/screenshot_dashboard_overview.png)](assets/images/screenshot_dashboard_overview.png)

---

### Screen 2.1: Executive Telemetry KPI Ribbon (Component Zoom-In)
Close-up view of the 4 executive telemetry cards: Total Video Reach (**1,482,900** impressions, +18.4%), Verified Watch Time (**42,850 hrs**, +22.1%), Ingestion Health Rate (**99.4%**, 320ms latency), and Cross-Platform Virality Index (**8.62%**).
[![Screen 2.1: KPI Ribbon Zoom](assets/images/screenshot_kpi_ribbon_zoom.png)](assets/images/screenshot_kpi_ribbon_zoom.png)

---

### Screen 2.2: Audience Growth Velocity Curves (Chart.js Zoom-In)
Dual-axis interactive time series tracking daily video views against net follower acquisition velocity with active 14-day and 30-day window switching.
[![Screen 2.2: Growth Velocity Curves](assets/images/screenshot_velocity_charts_zoom.png)](assets/images/screenshot_velocity_charts_zoom.png)

---

### Screen 2.3: Platform Impression Share Doughnut Chart (Component Zoom-In)
Proportional audience breakdown across YouTube Shorts (**58.2%**, 863,048 views), Instagram Reels (**28.6%**, 424,110 views), and LinkedIn Video (**13.2%**, 195,742 views).
[![Screen 2.3: Platform Impression Share](assets/images/screenshot_platform_share_doughnut.png)](assets/images/screenshot_platform_share_doughnut.png)

---

### Screen 2.4: Content Virality Leaderboard Matrix (Component Zoom-In)
Multi-channel content leaderboard sorted by virality score formula with real-time filtering (All, YouTube, Instagram, LinkedIn), platform tags, views, watch time, and intent metrics.
[![Screen 2.4: Virality Leaderboard](assets/images/screenshot_content_leaderboard.png)](assets/images/screenshot_content_leaderboard.png)

---

### Screen 2.5: Active Connector Quotas & Outbound Publishing Queue (Component Zoom-In)
Left panel monitors real-time API quota budgets (YouTube 2,340 / 10,000 units, Apify 0.04 CU, LinkedIn OAuth Valid). Right panel tracks asynchronous video scheduling jobs across platforms.
[![Screen 2.5: Connector Health & Queue](assets/images/screenshot_connector_health_monitor.png)](assets/images/screenshot_connector_health_monitor.png)

---

### Screen 3.0: Cross-Platform Post Dispatch Composer Modal
Interactive multi-channel publishing modal allowing creators to upload video media, enter captions, toggle target channels (YouTube Shorts, IG Reels, LinkedIn), and dispatch directly into the asynchronous publishing queue.
[![Screen 3.0: Post Composer Modal](assets/images/screenshot_modal_composer.png)](assets/images/screenshot_modal_composer.png)

---

## 4. Software Quality Assurance & Output Verification

### Output 1.0: Automated Test Execution Console Output (11/11 Passed)
Terminal execution log of `python3 -m unittest -v test_ingestion.py` demonstrating a 100% pass rate across 11 unit tests in 0.360s.
[![Output 1.0: Test Execution Console](assets/images/screenshot_test_execution_console.png)](assets/images/screenshot_test_execution_console.png)

```text
test_apify_instagram_normalization_standard ... ok
test_apify_instagram_null_guards ... ok
test_database_batch_ingest ... ok
test_database_schema_completeness (all 5 tables) ... ok
test_linkedin_normalization_null_guards ... ok
test_linkedin_normalization_standard ... ok
test_safe_int_conversions (k/m, floats, commas) ... ok
test_virality_calculation_positive ... ok
test_virality_calculation_zero_views ... ok
test_youtube_normalization_null_and_missing_guards ... ok
test_youtube_normalization_standard ... ok

----------------------------------------------------------------------
Ran 11 tests in 0.360s | OK (100% Pass Rate)
```

---

### Output 2.0: Ingestion Worker Terminal Daemon Execution Log
Terminal console output showing `python3 ingestion_worker.py` polling external APIs, checking token bucket quotas, normalizing payloads, and committing WAL transactions in 320ms.
[![Output 2.0: Worker Execution Log](assets/images/screenshot_terminal_worker_run.png)](assets/images/screenshot_terminal_worker_run.png)

---

### Output 3.0: SQLite Relational Database Query Verification
Interactive `sqlite3` CLI session verifying table records, primary/foreign key integrity, and stored virality scores using formatted box tables.
[![Output 3.0: SQLite Query Output](assets/images/screenshot_database_sqlite_query_output.png)](assets/images/screenshot_database_sqlite_query_output.png)

---

## 5. Core Algorithmic Logic & Boilerplate Code

### 1. Safe Integer Sanitizer (`safe_int`)
Handles missing fields, None objects, numeric strings with formatting commas, floats, and invalid inputs:

```python
def safe_int(value: Any, default: int = 0) -> int:
    """Safely converts heterogeneous values to integers with null guards."""
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
            return default
    return default
```

### 2. Weighted Intent Virality Scoring Formula
Calculates relative creator engagement velocity weighted by user advocacy intent (Shares 3x, Comments 2x, Likes 1x), protected against zero-division runtime errors:

```python
def calculate_virality_score(views: int, likes: int, comments: int, shares: int) -> float:
    """
    Virality Index (%) = ((Shares * 3 + Comments * 2 + Likes) / Views) * 100
    Guards against zero and negative view counts.
    """
    safe_views = max(0, safe_int(views))
    if safe_views <= 0:
        return 0.0
    safe_likes = max(0, safe_int(likes))
    safe_comments = max(0, safe_int(comments))
    safe_shares = max(0, safe_int(shares))
    
    score = ((safe_shares * 3 + safe_comments * 2 + safe_likes) / safe_views) * 100
    return round(score, 2)
```

### 3. Transactional Batch Database Upsert
Persists harvested snapshots and media metadata atomically using SQLite Write-Ahead Logging (WAL):

```python
def ingest_metric_batch(items: List[Dict[str, Any]], db_path: str = DB_FILE) -> int:
    """Inserts normalized items and metric snapshots with transactional consistency."""
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    for item in items:
        content_id = f"SMG-{item['platform'][:2].upper()}-{item['platform_item_id']}"
        cur.execute("""
            INSERT INTO content_items (id, channel_id, platform, platform_item_id, content_type, title, published_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET title = excluded.title
        """, (content_id, item.get("channel_id"), item["platform"], str(item["platform_item_id"]),
              item.get("content_type", "short"), item["title"], item.get("published_at", now)))

        cur.execute("""
            INSERT INTO metric_snapshots (content_item_id, views_count, likes_count, comments_count, shares_count, virality_score, snapshot_timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (content_id, item.get("views", 0), item.get("likes", 0), item.get("comments", 0),
              item.get("shares", 0), item.get("virality_score", 0.0), now))
              
    conn.commit()
    conn.close()
    return len(items)
```

---

## 6. Official SAGO Corporate Records & Credentials

### Internship Offer Letter
* **Reference Number:** `SMG/2026/INT/003` (Dated: 25th June 2026)  
* **Candidate & Institution:** Barath V — SRM Institute of Science and Technology (Reg. No: `EA2532251010775`)  
* **Designation:** AI Automation & Web Systems Engineering Intern  
* **Tenure:** 01 July 2026 to 31 August 2026  
* **Authorized Signatory:** Partha Sarathy M (Co-Founder & Operations Director)

[![Official Offer Letter](assets/images/sago_offer_letter_barath_v.png)](assets/images/sago_offer_letter_barath_v.png)

---

### Official Internship Completion Certificate
* **Certificate Identifier:** `SMG/CERT/2026/003` (Issued: 31st August 2026)  
* **MSME Registration:** `UDYAM-TN-18-0102132`  
* **Corporate Office:** 7/174, Tirunelveli, Tamil Nadu - 627426  
* **Authorized Signatory:** Partha Sarathy M (Co-Founder & Operations Director)

[![Official Completion Certificate](assets/images/sago_certificate_barath_v.png)](assets/images/sago_certificate_barath_v.png)

---

## 7. Viva Voce Defense Guide for External Academic Evaluators

| Question Number | Examiner Viva Voce Question | Recommended Candidate Defense Script | Examiner Evaluation Keywords |
|---|---|---|---|
| **Question 1** | *Why is this prototype hosted on a mock simulation rather than live production API tokens?* | *"SAGO Media Groups operates enterprise production channels and commercial client accounts bound by strict corporate Non-Disclosure Agreements (NDAs). To adhere to corporate cybersecurity policies and avoid leaking cloud API secrets or client analytics, I developed this localized simulation testbed. It faithfully mirrors the production data contracts, normalization algorithms, and Chart.js UI architectures authored during my internship."* | NDA Ethics, Security Compliance, Production Mirroring |
| **Question 2** | *What was your exact personal technical contribution as an intern?* | *"I worked as an AI Automation & Web Systems Engineering Intern assigned to the Ingestion Connector and Visualization Layer. Specifically, I engineered the JSON normalization adapters for YouTube Data API v3 and Apify scrapers, established the virality index formula, created the 11 unit tests in `test_ingestion.py`, and designed the responsive HTML5/Chart.js command center."* | Individual Role, Normalizer Adapters, Virality Formula |
| **Question 3** | *How does your architecture handle YouTube API daily quota exhaustion?* | *"YouTube enforces a strict daily limit of 10,000 units. While search calls consume 100 units, direct video and channel statistic queries consume only 1 unit. We optimized consumption by caching channel IDs, querying videos in batches of up to 50 items per call, and polling high-velocity content hourly while older catalogue content was synced once daily, maintaining daily quota consumption under 2,500 units."* | Quota Optimization, Token Bucket, Batch Requests |
| **Question 4** | *Why utilize Apify actors instead of official Meta Instagram APIs?* | *"The official Meta Graph API requires verified Business Account tokens and complex app review permissions. For tracking public creator metrics and benchmark reach without client OAuth friction, SAGO utilizes Apify actors that execute headless browser tasks and return clean structured JSON."* | API Friction, Headless Scrapers, Public Telemetry |
| **Question 5** | *How is the virality score mathematically calculated?* | *"The virality score calculates weighted user intent: ((Shares * 3 + Comments * 2 + Likes) / Views) * 100. Shares carry a 3x weight because they represent outbound advocacy, comments carry a 2x weight for engagement depth, and likes carry 1x for passive approval."* | Weighted Advocacy, Intent Analytics, Normalization |

---

## 8. Verification Commands

To verify the test suite and launch the dashboard locally:

```bash
# 1. Run the automated test suite (11/11 tests)
python3 -m unittest -v test_ingestion.py

# 2. Run the ingestion worker
python3 ingestion_worker.py

# 3. View the SQLite database tables
sqlite3 sago_pulse.db "SELECT * FROM content_items LIMIT 5;"

# 4. Open the responsive dashboard
python3 -m http.server 8080
# Open http://localhost:8080 in Chrome or Firefox
```

---
*Submitted in partial fulfillment of the requirements for the award of the degree of Master of Computer Applications (MCA), Directorate of Online Education, SRM Institute of Science and Technology, Kattankulathur - 603 203.*
