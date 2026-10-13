# SAGO Creator Intelligence & Distribution Hub (SAGO-Pulse)

[![System Architecture](assets/images/diagram_system_architecture.png)](assets/images/diagram_system_architecture.png)

**Internal Project Code:** `SMG-ENG-2026-CI`  
**Organization:** SAGO Media Groups (`UDYAM-TN-18-0102132`, Tirunelveli, Tamil Nadu - 627426)  
**Intern / Contributor:** Barath V (SRM Institute of Science and Technology, Reg. No: `EA2532251010775`)  
**Degree / Department:** Master of Computer Applications (MCA) — Directorate of Online Education, SRM IST, Kattankulathur - 603 203  
**Academic Supervision:** Dr. G. Babu (Assistant Professor & Programme Coordinator, Directorate of Online Education, SRM IST)  
**Company Mentorship & Signatory:** Partha Sarathy M (Co-Founder & Operations Director) & Gokulakrishnan M (Founder & Technical Architect)  
**Tenure:** 01 July 2026 – 31 August 2026 (2-Month Engineering Internship)  
**Offer Letter Reference:** `SMG/2026/INT/003` | **Certificate Identifier:** `SMG/CERT/2026/003` | **Evaluation Rubric:** `SMG/EVAL/2026/003`  
**Live Academic Documentation:**
* 📄 **Official Google Doc Full Project Report:** [Open Google Doc Report](https://docs.google.com/document/d/1-vqEDcXmGAo_tEdK4sPkOVdXfa3p13jvlTVbBO-xupc/edit)
* 📊 **Official Google Sheets Defense Ledger:** [Open Google Sheets Submission](https://docs.google.com/spreadsheets/d/1GIGdGZwGtNk1lOss2nFT8kWQ8jXnS6jY-n953kMVVvY/edit?usp=drivesdk)
* 🌐 **Public GitHub Repository:** [https://github.com/sagomedia/sago-creator-intelligence](https://github.com/sagomedia/sago-creator-intelligence)

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

### Figure 7.2: Entity Relationship (ER) Data Model (3NF Relational Schema)
Detailed relational model demonstrating primary keys, foreign keys, cascade constraints, and data types across all 5 core tables (`channels`, `content_items`, `metric_snapshots`, `publishing_queue`, `connector_quotas`).
[![Figure 7.2: Database ER Diagram](assets/images/diagram_database_er.png)](assets/images/diagram_database_er.png)

### Figure 7.3: Telemetry Ingestion Pipeline Flowchart
Six-stage execution sequence: 1) Scheduled Cron Trigger -> 2) Quota Budget & Rate Check -> 3) Multi-Source API Polling -> 4) JSON Normalizer & Virality Calculation -> 5) Delta Snapshot Storage (WAL commit) -> 6) Client Dashboard Live Re-render.
[![Figure 7.3: Ingestion Pipeline Flowchart](assets/images/diagram_ingestion_pipeline_flow.png)](assets/images/diagram_ingestion_pipeline_flow.png)

### Figure 7.4: Data Flow Diagram (DFD Level 0 Context & Level 1 Decomposition)
Gane & Sarson notation mapping data flows between External Entities (YouTube Data API v3, Apify Scraper, LinkedIn API, Creator Admin), Processes (Quota Guard, Ingestion Adapter, Normalizer, Virality Engine, Persistence Writer, Realtime Dispatcher), and Relational Data Stores (D1–D5).
[![Figure 7.4: Data Flow Diagram](assets/images/diagram_data_flow_dfd.png)](assets/images/diagram_data_flow_dfd.png)

### Figure 7.5: UML Sequence Diagram: Telemetry Lifecycle & Live Re-render
Chronological interaction among the Cron Scheduler, Quota Guard (Token Bucket), Social API Endpoints, Normalizer Engine, SQLite WAL Data Store, and Chart.js UI.
[![Figure 7.5: UML Sequence Diagram](assets/images/diagram_sequence.png)](assets/images/diagram_sequence.png)

### Figure 7.6: API Payload Normalization & Virality Scoring Flowchart
Defensive parsing decision pipeline: raw polymorphic JSON ingestion, type guards, platform-specific mapping adapters, `safe_int()` sanitization, zero-division protected intent scoring, and normalized database payload generation.
[![Figure 7.6: Normalization Flowchart](assets/images/diagram_normalization_flowchart.png)](assets/images/diagram_normalization_flowchart.png)

### Figure 7.7: UML Class & Component Architecture Diagram
Object-oriented class hierarchy detailing abstract adapters, platform implementations, token-bucket guards, and WAL snapshot stores.
[![Figure 7.7: UML Class Diagram](assets/images/diagram_class_hierarchy.png)](assets/images/diagram_class_hierarchy.png)

### Figure 7.8: End-to-End System Deployment & Network Topology Diagram
Physical node and network architecture illustrating client edge workstations, reverse proxy gateway, Python daemon processes, and TLS 1.3 external cloud connectors.
[![Figure 7.8: Deployment Topology](assets/images/diagram_deployment_topology.png)](assets/images/diagram_deployment_topology.png)

### Figure 7.9: Content Item & Publishing Queue State Transition Diagram
Finite State Automaton governing media asset lifecycle transitions from draft composition to active hourly telemetry harvesting.
[![Figure 7.9: State Machine](assets/images/diagram_state_machine.png)](assets/images/diagram_state_machine.png)

---

## 3. User Interface Screens & Component Zoom-Ins

### Screen 1.0: Full Command Center Overview
Complete responsive dark-mode view of SAGO Creator Intelligence Hub displaying top navigation, Executive KPI Ribbon, dual-axis Chart.js curves, doughnut platform share, content leaderboard, and connector health monitor.
[![Screen 1.0: Full Dashboard Overview](assets/images/screenshot_dashboard_fullpage.png)](assets/images/screenshot_dashboard_fullpage.png)

### Screen 1.1: Dashboard Navigation & KPI Overview
Top fold view highlighting the candidate registration metadata (`BARATH V`, `EA2532251010775`, `SRM IST DOE`), active system status, and aggregated performance indicators.
[![Screen 1.1: Dashboard Overview](assets/images/screenshot_dashboard_overview.png)](assets/images/screenshot_dashboard_overview.png)

### Screen 2.1: Executive Telemetry KPI Ribbon (Component Zoom-In)
Close-up view of the 4 executive telemetry cards: Total Video Reach (**1,482,900** impressions, +18.4%), Verified Watch Time (**42,850 hrs**, +22.1%), Ingestion Health Rate (**99.4%**, 320ms latency), and Cross-Platform Virality Index (**8.62%**).
[![Screen 2.1: KPI Ribbon Zoom](assets/images/screenshot_kpi_ribbon_zoom.png)](assets/images/screenshot_kpi_ribbon_zoom.png)

### Screen 2.2: Growth Velocity Curves (Dual-Axis Chart.js Zoom-In)
Dual-axis interactive time series tracking daily video views against net follower acquisition velocity with active 14-day and 30-day window switching.
[![Screen 2.2: Growth Velocity Curves](assets/images/screenshot_velocity_charts_zoom.png)](assets/images/screenshot_velocity_charts_zoom.png)

### Screen 2.3: Platform Impression Share Doughnut Chart (Component Zoom-In)
Proportional audience breakdown across YouTube Shorts (58.2%, 863k views), Instagram Reels (28.6%, 424k views), and LinkedIn Video (13.2%, 195k views).
[![Screen 2.3: Platform Impression Share](assets/images/screenshot_platform_share_doughnut.png)](assets/images/screenshot_platform_share_doughnut.png)

### Screen 2.4: Content Virality Leaderboard Matrix (Component Zoom-In)
Multi-channel content leaderboard sorted by virality score formula with real-time filtering (All, YouTube, Instagram, LinkedIn), platform tags, views, watch time, and intent metrics.
[![Screen 2.4: Virality Leaderboard](assets/images/screenshot_content_leaderboard.png)](assets/images/screenshot_content_leaderboard.png)

### Screen 2.5: Active Connector Quotas & Outbound Publishing Queue (Component Zoom-In)
Left panel monitors real-time API quota budgets (YouTube 2,340 / 10,000 units, Apify 0.04 CU, LinkedIn OAuth Valid). Right panel tracks asynchronous video scheduling jobs across platforms.
[![Screen 2.5: Connector Health & Queue](assets/images/screenshot_connector_health_monitor.png)](assets/images/screenshot_connector_health_monitor.png)

### Screen 3.0: Cross-Platform Post Dispatch Composer Modal
Interactive multi-channel scheduling composer allowing the user to select video media, input unified captions, toggle target platforms (YouTube Shorts, IG Reels, LinkedIn), and dispatch directly into the asynchronous publishing queue.
[![Screen 3.0: Post Composer Modal](assets/images/screenshot_modal_composer.png)](assets/images/screenshot_modal_composer.png)

### Screen 3.1: Video Performance Drilldown Analytics Modal
Granular single-video performance drilldown tracking 24-hour hourly velocity trajectory, 92.7% audience retention, and 3x share conversion drivers.
[![Screen 3.1: Video Analytics Drilldown](assets/images/screenshot_video_analytics_modal.png)](assets/images/screenshot_video_analytics_modal.png)

---

## 4. Test Execution & Terminal Outputs

### Output 1.0: Automated Test Execution Console Output (11/11 Passed in 0.360s)
Terminal execution log verifying 100% pass rate across all 11 unit tests with zero regressions.
[![Output 1.0: Test Execution Console](assets/images/screenshot_test_execution_console.png)](assets/images/screenshot_test_execution_console.png)

### Output 2.0: Ingestion Worker Terminal Daemon Execution Log
Daemon process output demonstrating hourly external polling, quota consumption checks, and sub-second WAL commits.
[![Output 2.0: Worker Execution Log](assets/images/screenshot_terminal_worker_run.png)](assets/images/screenshot_terminal_worker_run.png)

### Output 3.0: SQLite Relational Database Query Verification
Interactive `sqlite3` CLI session verifying table records, primary/foreign key integrity, and stored virality scores using formatted box tables.
[![Output 3.0: SQLite Query Output](assets/images/screenshot_database_sqlite_query_output.png)](assets/images/screenshot_database_sqlite_query_output.png)

### Output 4.0: High-Concurrency Benchmark & Profiling Console Output
Terminal execution of `benchmark_ingestion.py` demonstrating 63,291 writes/sec in SQLite WAL mode and lean 38.2 MB memory footprint.
[![Output 4.0: Benchmark Console Output](assets/images/screenshot_benchmark_profiling.png)](assets/images/screenshot_benchmark_profiling.png)

### Output 5.0: Git Repository Audit & Tree Graph Output
Rich terminal output of `git log --graph --oneline --decorate --all` and repo structure verifying production Git hygiene.
[![Output 5.0: Git Log Tree](assets/images/screenshot_git_log_tree.png)](assets/images/screenshot_git_log_tree.png)

---

## 5. Official Internship Credentials & Evaluation Rubric

### Official Offer Letter
[![Official Offer Letter](assets/images/sago_offer_letter_barath_v.png)](assets/images/sago_offer_letter_barath_v.png)

### Official Completion Certificate
[![Official Completion Certificate](assets/images/sago_certificate_barath_v.png)](assets/images/sago_certificate_barath_v.png)

### Corporate Mentor Appraisal & Evaluation Rubric
[![Corporate Mentor Appraisal Rubric](assets/images/sago_mentor_evaluation_barath_v.png)](assets/images/sago_mentor_evaluation_barath_v.png)

---

## 6. Viva Voce Defense & Examiner Evaluation Guide

* **Q1: Why is this prototype evaluated locally rather than connecting live production keys?**  
  *Defense:* "SAGO Media Groups operates enterprise production accounts governed under Non-Disclosure Agreements (NDAs). To adhere to corporate cybersecurity policies and avoid exposing proprietary cloud API secrets or client analytics, I developed this localized simulation testbed. It faithfully mirrors the production schemas, normalization algorithms, and Chart.js UI architectures authored during my internship."
* **Q2: What was your specific personal technical contribution?**  
  *Defense:* "I was responsible for the Ingestion Connector and Visualization Layer. Specifically, I engineered the JSON normalization adapters for YouTube Data API v3 and Apify scrapers, established the virality index formula, created the 11 unit tests in `test_ingestion.py`, and developed the responsive frontend command dashboard in HTML5, CSS, and Chart.js."
* **Q3: How does the system handle YouTube API daily quota limits?**  
  *Defense:* "YouTube enforces a strict daily limit of 10,000 units. A standard `videos.list` call costs 1 unit, whereas search calls consume 100 units. We optimized consumption by querying channels and videos directly via cached IDs, batching up to 50 items per call, and polling high-velocity content hourly while older catalogue content was synced once daily, maintaining daily quota consumption under 2,500 units."

---

## 7. Technology Stack & Verification Record

- **Backend Runtime:** Python 3.10+
- **Persistence Engine:** SQLite 3.35+ with Write-Ahead Logging (`WAL` mode)
- **Frontend Command Center:** HTML5, CSS3, Tailwind utility classes, Chart.js 4.4.1 (UMD)
- **Automated Testing:** Python `unittest` standard library (11/11 Passed, 0.360s runtime)
- **Git Repository:** `https://github.com/sagomedia/sago-creator-intelligence`
