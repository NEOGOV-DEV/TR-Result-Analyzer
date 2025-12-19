# Test Rigor Analyzer - Architectural Diagrams

## 1. High-Level System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              USER INTERFACE                                  │
│                         (Browser - Port 5000)                                │
│ ┌─────────────┐  ┌──────────────────┐  ┌────────────────────────────────┐  │
│ │   Tab 1:    │  │     Tab 2:       │  │        Tab 3:                  │  │
│ │  Generate   │  │  Compare Runs &  │  │   Cumulative RTR               │  │
│ │   Report    │  │  Calculate RTR   │  │     Calculator                 │  │
│ │             │  │                  │  │                                │  │
│ │ - Single    │  │ - Up to 7 runs   │  │ - TestRigor + POM + JMeter    │  │
│ │   Run       │  │ - Side by side   │  │ - Overall success rate        │  │
│ │ - Failures  │  │ - Search & filter│  │ - Aggregate metrics           │  │
│ │ - Rerun     │  │ - Excel export   │  │                                │  │
│ └─────────────┘  └──────────────────┘  └────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
                    ▼               ▼               ▼
        ┌───────────────┐  ┌───────────────┐  ┌──────────────────┐
        │ /api/generate │  │ /api/compare  │  │ /api/calculate   │
        │   -report     │  │    -runs      │  │  -cumulative-rtr │
        │               │  │               │  │                  │
        └───────────────┘  └───────────────┘  └──────────────────┘
                    │               │               │
                    └───────────────┼───────────────┘
                                    │
┌─────────────────────────────────────────────────────────────────────────────┐
│                         FLASK APPLICATION SERVER                             │
│                              (app.py)                                        │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │                        API ENDPOINTS LAYER                          │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌─────────────────────────┐  │    │
│  │  │ POST /api/   │  │ POST /api/   │  │ POST /api/download-     │  │    │
│  │  │ generate-    │  │ compare-     │  │ summary-report          │  │    │
│  │  │ report       │  │ runs         │  │                         │  │    │
│  │  └──────────────┘  └──────────────┘  └─────────────────────────┘  │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                                    │                                         │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │                      BUSINESS LOGIC LAYER                           │    │
│  │                                                                      │    │
│  │  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────────┐  │    │
│  │  │ fetch_run_details│  │ process_failures │  │  calculate_rtr  │  │    │
│  │  └──────────────────┘  └──────────────────┘  └─────────────────┘  │    │
│  │                                                                      │    │
│  │  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────────┐  │    │
│  │  │fetch_test_cases  │  │extract_test_case │  │ merge_run_data  │  │    │
│  │  │(ThreadPoolExec.) │  │      _id          │  │                 │  │    │
│  │  └──────────────────┘  └──────────────────┘  └─────────────────┘  │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                                    │                                         │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │                      REPORT GENERATION LAYER                        │    │
│  │                      (report_generator.py)                          │    │
│  │                                                                      │    │
│  │  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────────┐  │    │
│  │  │ generate_excel_  │  │ embed_screenshot │  │  format_cells   │  │    │
│  │  │    report        │  │                  │  │                 │  │    │
│  │  └──────────────────┘  └──────────────────┘  └─────────────────┘  │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                                    │                                         │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │                    CONFIGURATION LAYER                              │    │
│  │                       (config.json)                                 │    │
│  │                                                                      │    │
│  │  ┌──────────────────────────────────────────────────────────────┐  │    │
│  │  │  Suite Configurations (16+ suites):                          │  │    │
│  │  │  {                                                            │  │    │
│  │  │    "HRIS-CoreHR-QA": {                                        │  │    │
│  │  │      "auth_token": "xxxx-xxxx-xxxx",                         │  │    │
│  │  │      "base_url": "https://api2.testrigor.com/api/v1/..."    │  │    │
│  │  │    }                                                          │  │    │
│  │  │  }                                                            │  │    │
│  │  └──────────────────────────────────────────────────────────────┘  │    │
│  └────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    │ HTTPS         │ REST API      │
                    ▼               ▼               ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                       TESTRIGOR API (EXTERNAL)                               │
│                   https://api2.testrigor.com/api/v1                          │
│                                                                              │
│  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────────────────┐  │
│  │ GET /apps/{id}/  │  │ GET /apps/{id}/  │  │ GET /apps/{id}/runs/    │  │
│  │ runs/{runId}     │  │ runs/{runId}/    │  │ {runId}/tests/{testId}  │  │
│  │                  │  │ tests            │  │                         │  │
│  └──────────────────┘  └──────────────────┘  └─────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Component Interaction Diagram

```
┌──────────────────┐
│   Web Browser    │
│                  │
│  ┌────────────┐  │
│  │ index.html │  │ ◄──── 3287 lines
│  │            │  │       Single Page Application
│  │  JavaScript│  │
│  │  + CSS     │  │
│  └────────────┘  │
└────────┬─────────┘
         │ HTTP/JSON
         │ fetch() / XMLHttpRequest
         ▼
┌─────────────────────────────────────┐
│      Flask Web Server               │
│                                     │
│  ┌──────────────────────────────┐  │
│  │       app.py (1136 lines)    │  │
│  │                              │  │
│  │  Routes:                     │  │
│  │  • / → index.html            │  │
│  │  • /api/generate-report      │  │
│  │  • /api/compare-runs         │  │
│  │  • /api/download-summary     │  │
│  │  • /api/calculate-cumulative │  │
│  └──────────────────────────────┘  │
│           │                         │
│           ▼                         │
│  ┌──────────────────────────────┐  │
│  │   report_generator.py        │  │
│  │                              │  │
│  │  Classes:                    │  │
│  │  • ReportGenerator           │  │
│  │                              │  │
│  │  Methods:                    │  │
│  │  • generate_excel_report()   │  │
│  │  • embed_screenshot()        │  │
│  │  • format_cells()            │  │
│  └──────────────────────────────┘  │
│           │                         │
│           ▼                         │
│  ┌──────────────────────────────┐  │
│  │      config.json             │  │
│  │                              │  │
│  │  16+ Suite Configurations:   │  │
│  │  • auth_token                │  │
│  │  • base_url                  │  │
│  └──────────────────────────────┘  │
└────────┬────────────────────────────┘
         │ HTTPS
         │ requests.get()
         ▼
┌─────────────────────────────────────┐
│      TestRigor REST API             │
│                                     │
│  Endpoints Used:                    │
│  • GET /runs/{runId}                │
│  • GET /runs/{runId}/tests          │
│  • GET /runs/{runId}/tests/{testId} │
└─────────────────────────────────────┘
```

---

## 3. Data Flow - Compare 7 Runs Feature

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           USER ACTIONS                                   │
└─────────────────────────────────────────────────────────────────────────┘
                                   │
                 ┌─────────────────┼─────────────────┐
                 │                 │                 │
                 ▼                 ▼                 ▼
         ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
         │Select Suite  │  │ Enter Run IDs│  │Click Compare │
         │(dropdown)    │  │  (1 to 7)    │  │   Button     │
         └──────────────┘  └──────────────┘  └──────────────┘
                 │                 │                 │
                 └─────────────────┼─────────────────┘
                                   │
                                   ▼
         ┌───────────────────────────────────────────────────┐
         │         CLIENT-SIDE VALIDATION                    │
         │                                                   │
         │  1. Check all Run IDs filled (at least 1)        │
         │  2. Validate no duplicate Run IDs                │
         │  3. Enable/disable Compare button                │
         └───────────────────────────────────────────────────┘
                                   │
                                   ▼
         ┌───────────────────────────────────────────────────┐
         │    POST /api/compare-runs                         │
         │    Request Body:                                  │
         │    {                                              │
         │      "suite": "HRIS-CoreHR-QA",                   │
         │      "run_id1": "RUNNER04_20251217_180003",      │
         │      "run_id2": "RUNNER04_20251216_180003",      │
         │      "run_id3": "Baseline: scheduler retest",    │
         │      "run_id4": "...",                            │
         │      "run_id5": "...",                            │
         │      "run_id6": "...",                            │
         │      "run_id7": "..."                             │
         │    }                                              │
         └───────────────────────────────────────────────────┘
                                   │
┌─────────────────────────────────────────────────────────────────────────┐
│                        BACKEND PROCESSING                                │
└─────────────────────────────────────────────────────────────────────────┘
                                   │
                 ┌─────────────────┼─────────────────┐
                 │                 │                 │
                 ▼                 ▼                 ▼
         ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
         │ Fetch Run 1  │  │ Fetch Run 2  │  │ Fetch Run 3  │
         │              │  │              │  │              │
         │ • Run details│  │ • Run details│  │ • Run details│
         │ • Test cases │  │ • Test cases │  │ • Test cases │
         │ • Results    │  │ • Results    │  │ • Results    │
         └──────────────┘  └──────────────┘  └──────────────┘
                 │                 │                 │
                 │                 ▼                 │
                 │         ┌──────────────┐         │
                 │         │ Fetch Run 4-7│         │
                 │         │ (if provided)│         │
                 │         └──────────────┘         │
                 │                 │                 │
                 └─────────────────┼─────────────────┘
                                   │
                                   ▼
         ┌───────────────────────────────────────────────────┐
         │         DATA NORMALIZATION & PROCESSING           │
         │                                                   │
         │  For each run:                                    │
         │  1. Extract test case IDs (C###### pattern)      │
         │  2. Map test names to results (passed/failed)    │
         │  3. Calculate statistics:                        │
         │     • total_tests                                │
         │     • passed_count = countPassed()               │
         │     • failed_count = countFailed()               │
         │     • rtr = ((passed + valid_fail) / total) × 100│
         │  4. Create unified test case map                 │
         └───────────────────────────────────────────────────┘
                                   │
                                   ▼
         ┌───────────────────────────────────────────────────┐
         │             RESPONSE CONSTRUCTION                 │
         │                                                   │
         │  {                                                │
         │    "run1": {                                      │
         │      "run_name": "...",                           │
         │      "run_date": "...",                           │
         │      "total_tests": 217,                          │
         │      "tests": {                                   │
         │        "C1234567": {                              │
         │          "name": "Test Name",                     │
         │          "status": "passed"                       │
         │        }                                          │
         │      }                                            │
         │    },                                             │
         │    "run2": { ... },                               │
         │    "run3": { ... },                               │
         │    ...                                            │
         │    "run7": { ... }                                │
         │  }                                                │
         └───────────────────────────────────────────────────┘
                                   │
┌─────────────────────────────────────────────────────────────────────────┐
│                      FRONTEND RENDERING                                  │
└─────────────────────────────────────────────────────────────────────────┘
                                   │
                 ┌─────────────────┼─────────────────┐
                 │                 │                 │
                 ▼                 ▼                 ▼
         ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
         │   Display    │  │   Display    │  │   Display    │
         │ Comparison   │  │  Detailed    │  │ Excel Export │
         │    Cards     │  │   Table      │  │    Button    │
         │              │  │              │  │              │
         │ • Run name   │  │ • Test Case  │  │ • Overall    │
         │ • Date       │  │   ID column  │  │   Summary    │
         │ • Statistics │  │ • Test Name  │  │ • Detailed   │
         │ • Valid Fail │  │ • Run1...Run7│  │   Summary    │
         │   input      │  │   status cols│  │              │
         │ • RTR %      │  │ • Search row │  │              │
         └──────────────┘  └──────────────┘  └──────────────┘
                                   │
                                   ▼
         ┌───────────────────────────────────────────────────┐
         │            ADAPTIVE UI LAYOUT                     │
         │                                                   │
         │  IF visibleRuns <= 3:                             │
         │    → Use CSS Grid (3 columns)                     │
         │                                                   │
         │  IF visibleRuns >= 4:                             │
         │    → Use Flexbox + Horizontal Scroll              │
         │    → Show scroll hint if runs > 5                 │
         │                                                   │
         │  Hide cards/columns where data is null            │
         │  Hide search inputs for non-visible runs          │
         └───────────────────────────────────────────────────┘
```

---

## 4. Sequence Diagram - Compare Runs Flow

```
User          Browser          Flask Server         TestRigor API
 │                │                   │                    │
 │   Fill form    │                   │                    │
 │   (7 Run IDs)  │                   │                    │
 │───────────────>│                   │                    │
 │                │                   │                    │
 │  Click Compare │                   │                    │
 │───────────────>│                   │                    │
 │                │                   │                    │
 │                │ POST /api/        │                    │
 │                │ compare-runs      │                    │
 │                │ {run_id1..run_id7}│                    │
 │                │──────────────────>│                    │
 │                │                   │                    │
 │                │                   │ GET /runs/{run_id1}│
 │                │                   │───────────────────>│
 │                │                   │                    │
 │                │                   │ Run 1 Details      │
 │                │                   │<───────────────────│
 │                │                   │                    │
 │                │                   │ GET /runs/{run_id1}│
 │                │                   │      /tests        │
 │                │                   │───────────────────>│
 │                │                   │                    │
 │                │                   │ Test Cases (1-n)   │
 │                │                   │<───────────────────│
 │                │                   │                    │
 │                │                   │ ╔═══════════════╗  │
 │                │                   │ ║ ThreadPool    ║  │
 │                │                   │ ║ Executor:     ║  │
 │                │                   │ ║ Parallel GET  ║  │
 │                │                   │ ║ for each test ║  │
 │                │                   │ ╚═══════════════╝  │
 │                │                   │                    │
 │                │                   │ GET /tests/{id1}   │
 │                │                   │───────────────────>│
 │                │                   │ GET /tests/{id2}   │
 │                │                   │───────────────────>│
 │                │                   │ GET /tests/{id3}   │
 │                │                   │───────────────────>│
 │                │                   │      ...           │
 │                │                   │                    │
 │                │                   │ Test Results       │
 │                │                   │<───────────────────│
 │                │                   │                    │
 │                │                   │ ╔═══════════════╗  │
 │                │                   │ ║ Repeat for    ║  │
 │                │                   │ ║ Run 2..Run 7  ║  │
 │                │                   │ ╚═══════════════╝  │
 │                │                   │                    │
 │                │                   │                    │
 │                │                   │ ┌────────────────┐ │
 │                │                   │ │Process & merge │ │
 │                │                   │ │all run data    │ │
 │                │                   │ │into unified map│ │
 │                │                   │ └────────────────┘ │
 │                │                   │                    │
 │                │  JSON Response:   │                    │
 │                │  {run1...run7}    │                    │
 │                │<──────────────────│                    │
 │                │                   │                    │
 │                │ ┌──────────────┐  │                    │
 │                │ │ displayComp- │  │                    │
 │                │ │ arison()     │  │                    │
 │                │ │              │  │                    │
 │                │ │ • Show cards │  │                    │
 │                │ │ • Build table│  │                    │
 │                │ │ • Enable RTR │  │                    │
 │                │ │   recalc     │  │                    │
 │                │ └──────────────┘  │                    │
 │                │                   │                    │
 │  UI Updated    │                   │                    │
 │<───────────────│                   │                    │
 │                │                   │                    │
```

---

## 5. Database/Storage Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    NO PERSISTENT DATABASE                        │
│                  (Stateless Architecture)                        │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────┐         ┌──────────────────┐
│  config.json     │         │  reports/        │
│                  │         │  (Generated      │
│  Structure:      │         │   Excel files)   │
│  {                │         │                  │
│    "suites": {   │         │  • FailureReport_│
│      "Suite1": { │         │    {runId}_{ts}  │
│        "auth_    │         │    .xlsx         │
│         token",  │         │                  │
│        "base_url"│         │  • Summary_      │
│      },           │         │    {suite}_{ts}  │
│      "Suite2": { │         │    .xlsx         │
│        ...       │         │                  │
│      }            │         └──────────────────┘
│    }              │
│  }                │         ┌──────────────────┐
└──────────────────┘         │  Browser         │
                             │  Storage:        │
                             │                  │
                             │  • comparisonData│
                             │    (global var)  │
                             │                  │
                             │  • Form inputs   │
                             │    (session only)│
                             └──────────────────┘

Data Flow:
1. Configuration read from config.json on app startup
2. API requests fetch fresh data from TestRigor
3. Results processed in-memory
4. Excel reports saved to reports/ directory
5. Browser maintains state in JavaScript variables
6. No caching - each request fetches fresh data
```

---

## 6. Frontend Architecture (SPA)

```
┌───────────────────────────────────────────────────────────────────────┐
│                          index.html (3287 lines)                       │
│                                                                        │
│  ┌──────────────────────────────────────────────────────────────┐    │
│  │                        NAVIGATION BAR                         │    │
│  │                                                               │    │
│  │   [Generate Report] [Compare Runs] [Cumulative RTR]          │    │
│  │                                                               │    │
│  │   Active tab styling + click handlers                         │    │
│  └──────────────────────────────────────────────────────────────┘    │
│                               │                                        │
│              ┌────────────────┼────────────────┐                      │
│              │                │                │                      │
│              ▼                ▼                ▼                      │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐         │
│  │   TAB 1 PAGE   │  │   TAB 2 PAGE   │  │   TAB 3 PAGE   │         │
│  │  (display:none)│  │  (display:none)│  │  (display:none)│         │
│  │                │  │                │  │                │         │
│  │  ┌──────────┐  │  │  ┌──────────┐  │  │  ┌──────────┐  │         │
│  │  │  Suite   │  │  │  │  Suite   │  │  │  │ Test Type│  │         │
│  │  │ Dropdown │  │  │  │ Dropdown │  │  │  │  Inputs  │  │         │
│  │  └──────────┘  │  │  └──────────┘  │  │  └──────────┘  │         │
│  │                │  │                │  │                │         │
│  │  ┌──────────┐  │  │  ┌──────────┐  │  │  ┌──────────┐  │         │
│  │  │  Run ID  │  │  │  │ Run ID 1 │  │  │  │  Total   │  │         │
│  │  │  Input   │  │  │  │ Input    │  │  │  │  Tests   │  │         │
│  │  └──────────┘  │  │  └──────────┘  │  │  └──────────┘  │         │
│  │                │  │  ┌──────────┐  │  │                │         │
│  │  ┌──────────┐  │  │  │ Run ID 2 │  │  │  ┌──────────┐  │         │
│  │  │ Generate │  │  │  │ (Optional)│  │  │  │Calculate │  │         │
│  │  │  Button  │  │  │  └──────────┘  │  │  │  Button  │  │         │
│  │  └──────────┘  │  │      ...       │  │  └──────────┘  │         │
│  │                │  │  ┌──────────┐  │  │                │         │
│  │  ┌──────────┐  │  │  │ Run ID 7 │  │  │  ┌──────────┐  │         │
│  │  │ Results  │  │  │  │ (Optional)│  │  │  │ Results  │  │         │
│  │  │  Table   │  │  │  └──────────┘  │  │  │  Display │  │         │
│  │  └──────────┘  │  │                │  │  └──────────┘  │         │
│  │                │  │  ┌──────────┐  │  │                │         │
│  │  ┌──────────┐  │  │  │ Compare  │  │  └────────────────┘         │
│  │  │ Download │  │  │  │  Button  │  │                             │
│  │  │  Excel   │  │  │  └──────────┘  │                             │
│  │  └──────────┘  │  │                │                             │
│  │                │  │  ┌──────────┐  │                             │
│  └────────────────┘  │  │Comparison│  │                             │
│                      │  │  Cards   │  │                             │
│                      │  │ (1 to 7) │  │                             │
│                      │  └──────────┘  │                             │
│                      │                │                             │
│                      │  ┌──────────┐  │                             │
│                      │  │ Detailed │  │                             │
│                      │  │  Table   │  │                             │
│                      │  │          │  │                             │
│                      │  │ + Search │  │                             │
│                      │  │   Inputs │  │                             │
│                      │  └──────────┘  │                             │
│                      │                │                             │
│                      │  ┌──────────┐  │                             │
│                      │  │Recalculate│ │                             │
│                      │  │   RTR     │  │                             │
│                      │  └──────────┘  │                             │
│                      │                │                             │
│                      │  ┌──────────┐  │                             │
│                      │  │ Download │  │                             │
│                      │  │  Excel   │  │                             │
│                      │  └──────────┘  │                             │
│                      └────────────────┘                             │
│                                                                        │
│  ┌──────────────────────────────────────────────────────────────┐    │
│  │                     GLOBAL JAVASCRIPT STATE                   │    │
│  │                                                               │    │
│  │  • comparisonData = {}  // Stores all 7 run datasets         │    │
│  │  • currentTab = 1       // Active tab number                 │    │
│  │                                                               │    │
│  └──────────────────────────────────────────────────────────────┘    │
│                                                                        │
│  ┌──────────────────────────────────────────────────────────────┐    │
│  │                    KEY JAVASCRIPT FUNCTIONS                   │    │
│  │                                                               │    │
│  │  Navigation:                                                  │    │
│  │  • showTab(tabNumber)                                         │    │
│  │                                                               │    │
│  │  Tab 1 Functions:                                             │    │
│  │  • generateReport()                                           │    │
│  │  • displayReport(data)                                        │    │
│  │                                                               │    │
│  │  Tab 2 Functions (Compare Runs):                              │    │
│  │  • compareRuns()                     // Fetch & compare       │    │
│  │  • displayComparison(data1...data7)  // Render UI            │    │
│  │  • updateCompareButtons()            // Enable/disable        │    │
│  │  • validateNoDuplicateRunIds()       // Check duplicates      │    │
│  │  • recalculateRtr()                  // Update with valid fail│    │
│  │  • searchTableColumns()              // Filter table rows     │    │
│  │  • downloadSummaryReport()           // Generate Excel        │    │
│  │                                                               │    │
│  │  Tab 3 Functions:                                             │    │
│  │  • calculateCumulativeRtr()                                   │    │
│  │                                                               │    │
│  │  Utility Functions:                                           │    │
│  │  • countPassed(runData)              // Count passed tests    │    │
│  │  • countFailed(runData)              // Count failed tests    │    │
│  │  • calculateRtr(runData)             // Compute RTR %         │    │
│  │  • extractTestCaseId(testName)       // Parse C###### ID      │    │
│  │  • formatDate(dateString)            // Format timestamp      │    │
│  │  • formatShortDate(dateString)       // Abbreviated date      │    │
│  │                                                               │    │
│  └──────────────────────────────────────────────────────────────┘    │
│                                                                        │
│  ┌──────────────────────────────────────────────────────────────┐    │
│  │                      EVENT LISTENERS                          │    │
│  │                                                               │    │
│  │  • Tab navigation clicks                                      │    │
│  │  • Run ID inputs: oninput → validate & enable buttons        │    │
│  │  • Valid Fail inputs: oninput → enable Recalculate button    │    │
│  │  • Search inputs: oninput → filter table rows                │    │
│  │  • Button clicks: onclick → API calls                        │    │
│  │                                                               │    │
│  └──────────────────────────────────────────────────────────────┘    │
└───────────────────────────────────────────────────────────────────────┘
```

---

## 7. RTR Calculation Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    RTR CALCULATION LOGIC                         │
└─────────────────────────────────────────────────────────────────┘

For Each Run:

  ┌───────────────────────────────────────────┐
  │     Fetch Run Data from TestRigor API     │
  │                                           │
  │  • run_name: "RUNNER04_20251217_180003"   │
  │  • run_date: "2025-12-17T02:00:00Z"      │
  │  • status: "completed"                    │
  │  • tests: [ {...}, {...}, ... ]          │
  └───────────────────────────────────────────┘
                    │
                    ▼
  ┌───────────────────────────────────────────┐
  │         Count Tests by Status             │
  │                                           │
  │  total_tests = tests.length               │
  │  passed_count = 0                         │
  │  failed_count = 0                         │
  │                                           │
  │  for each test:                           │
  │    if test.status == "passed":            │
  │      passed_count++                       │
  │    else if test.status == "failed":       │
  │      failed_count++                       │
  └───────────────────────────────────────────┘
                    │
                    ▼
  ┌───────────────────────────────────────────┐
  │       Initial RTR Calculation             │
  │       (No Valid Fail)                     │
  │                                           │
  │  valid_fail = 0                           │
  │                                           │
  │  RTR = ((passed + valid_fail) / total) ×  │
  │        100                                │
  │                                           │
  │  Example:                                 │
  │  total = 217                              │
  │  passed = 135                             │
  │  valid_fail = 0                           │
  │  RTR = (135 / 217) × 100 = 62.2%         │
  └───────────────────────────────────────────┘
                    │
                    ▼
  ┌───────────────────────────────────────────┐
  │      User Enters Valid Fail Count         │
  │      (Optional Override)                  │
  │                                           │
  │  User inputs: valid_fail = 10             │
  └───────────────────────────────────────────┘
                    │
                    ▼
  ┌───────────────────────────────────────────┐
  │       Recalculated RTR                    │
  │       (With Valid Fail)                   │
  │                                           │
  │  valid_fail_count = user_input            │
  │                                           │
  │  actual_failed = failed - valid_fail      │
  │                                           │
  │  RTR = ((passed + valid_fail) / total) ×  │
  │        100                                │
  │                                           │
  │  Example:                                 │
  │  total = 217                              │
  │  passed = 135                             │
  │  valid_fail = 10                          │
  │  RTR = ((135 + 10) / 217) × 100 = 66.8%  │
  └───────────────────────────────────────────┘
                    │
                    ▼
  ┌───────────────────────────────────────────┐
  │       Display Updated Statistics          │
  │                                           │
  │  • Total: 217                             │
  │  • Passed: 135                            │
  │  • Failed: 82 → 72 (after valid fail)    │
  │  • Valid Fail: 10                         │
  │  • RTR: 66.8%                             │
  └───────────────────────────────────────────┘

Cumulative RTR (Across Multiple Test Types):

  ┌───────────────────────────────────────────┐
  │    Aggregate Across TestRigor + POM +     │
  │              JMeter                       │
  │                                           │
  │  total = TR_total + POM_total + JMeter_   │
  │          total                            │
  │                                           │
  │  passed = TR_passed + POM_passed +        │
  │           JMeter_passed                   │
  │                                           │
  │  valid_fail = TR_valid + POM_valid +      │
  │               JMeter_valid                │
  │                                           │
  │  Overall RTR = ((total_passed +           │
  │                 total_valid_fail) /       │
  │                total_tests) × 100         │
  └───────────────────────────────────────────┘
```

---

## 8. Excel Report Structure

```
┌─────────────────────────────────────────────────────────────────────┐
│                    EXCEL WORKBOOK STRUCTURE                          │
│               (Generated by report_generator.py)                     │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                       SHEET 1: Overall Summary                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │ Merged Header: "Overall Summary - {Suite Name} - {Timestamp}"│  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  ┌────────┬────────┬────────┬────────┬─────────┬────────┬────────┐ │
│  │  Run   │ Run    │ Total  │ Passed │ Failed  │ Valid  │  RTR   │ │
│  │  ID    │ Name   │ Tests  │ Tests  │ Tests   │ Fail   │   %    │ │
│  ├────────┼────────┼────────┼────────┼─────────┼────────┼────────┤ │
│  │ RUN1   │ Name1  │  217   │  135   │   82    │   0    │ 62.2%  │ │
│  ├────────┼────────┼────────┼────────┼─────────┼────────┼────────┤ │
│  │ RUN2   │ Name2  │  217   │  130   │   87    │   0    │ 59.9%  │ │
│  ├────────┼────────┼────────┼────────┼─────────┼────────┼────────┤ │
│  │ RUN3   │ Name3  │  254   │   9    │  245    │   0    │  3.5%  │ │
│  ├────────┼────────┼────────┼────────┼─────────┼────────┼────────┤ │
│  │ RUN4   │ Name4  │  217   │  119   │   98    │   0    │ 54.8%  │ │
│  ├────────┼────────┼────────┼────────┼─────────┼────────┼────────┤ │
│  │  ...   │  ...   │  ...   │  ...   │   ...   │  ...   │  ...   │ │
│  └────────┴────────┴────────┴────────┴─────────┴────────┴────────┘ │
│                                                                      │
│  Formatting:                                                         │
│  • Header row: Bold, centered, border                               │
│  • Cells: Bordered, aligned                                         │
│  • Column widths: Auto-sized                                        │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                    SHEET 2: Detailed Summary                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │Merged Header:"Detailed Test Comparison-{Suite}-{Timestamp}" │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  ┌──────────┬──────────┬────────┬────────┬────────┬───────────┐   │
│  │  Test    │  Test    │  Run 1 │  Run 2 │  Run 3 │  ... Run 7│   │
│  │  Case ID │  Name    │ Status │ Status │ Status │   Status  │   │
│  ├──────────┼──────────┼────────┼────────┼────────┼───────────┤   │
│  │ C1027571 │ Test Edit│ Failed │ Failed │Not Run │  Passed   │   │
│  │          │ Secondary│        │        │        │           │   │
│  ├──────────┼──────────┼────────┼────────┼────────┼───────────┤   │
│  │ C3140066 │ Create PR│ Failed │ Failed │Not Run │  Failed   │   │
│  │          │ security │        │        │        │           │   │
│  ├──────────┼──────────┼────────┼────────┼────────┼───────────┤   │
│  │ C3140081 │ Edit     │ Passed │ Passed │Not Run │  Passed   │   │
│  │          │ assignment│       │        │        │           │   │
│  ├──────────┼──────────┼────────┼────────┼────────┼───────────┤   │
│  │   ...    │   ...    │  ...   │  ...   │  ...   │    ...    │   │
│  └──────────┴──────────┴────────┴────────┴────────┴───────────┘   │
│                                                                      │
│  Cell Formatting:                                                    │
│  • "Passed"   → Green background (#90EE90)                          │
│  • "Failed"   → Red background (#FFB6C1)                            │
│  • "Not Run"  → Gray background (#D3D3D3)                           │
│  • Header row: Bold, centered, border                               │
│  • Text: Wrapped, aligned left/center                               │
│                                                                      │
│  Dynamic Columns:                                                    │
│  • Columns added based on number of runs (1-7)                      │
│  • Run columns only created if run data exists                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 9. Security & Configuration Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                    SECURITY ARCHITECTURE                             │
└─────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────┐
│         config.json (Local)          │
│                                      │
│  Contains sensitive data:            │
│  • API authentication tokens         │
│  • Base URLs per suite               │
│                                      │
│  ⚠️  NOT committed to version control│
│  ⚠️  Read-only access by Flask app   │
└──────────────────────────────────────┘
                  │
                  │ Read on startup
                  ▼
┌──────────────────────────────────────┐
│         Flask Application            │
│                                      │
│  SUITES = load_config()              │
│                                      │
│  Security measures:                  │
│  • CORS enabled for localhost        │
│  • No authentication layer           │
│    (internal tool)                   │
│  • Input validation on all endpoints │
│  • Error handling prevents token     │
│    exposure in responses             │
└──────────────────────────────────────┘
                  │
                  │ HTTPS
                  ▼
┌──────────────────────────────────────┐
│         TestRigor API                │
│                                      │
│  Authentication:                     │
│  • Bearer token in request headers   │
│  • Per-suite token isolation         │
│                                      │
│  Rate Limiting:                      │
│  • Handled by TestRigor              │
│  • ThreadPool limits concurrent      │
│    requests to 10 per run            │
└──────────────────────────────────────┘

Data Flow Security:
1. User selects suite from dropdown (public info)
2. Backend looks up auth_token from config.json
3. Token sent via HTTPS to TestRigor API
4. Results returned without exposing token
5. Frontend never sees authentication details
```

---

## 10. Deployment Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    DEPLOYMENT MODEL                                  │
│                 (Local Development Server)                           │
└─────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────┐
│              Windows Environment                       │
│                                                       │
│  ┌─────────────────────────────────────────────────┐ │
│  │  Launch_TR_Reporter.bat                         │ │
│  │                                                 │ │
│  │  @echo off                                      │ │
│  │  python app.py                                  │ │
│  └─────────────────────────────────────────────────┘ │
│                        │                              │
│                        ▼                              │
│  ┌─────────────────────────────────────────────────┐ │
│  │  Python 3.8+ Environment                        │ │
│  │                                                 │ │
│  │  Dependencies (requirements.txt):               │ │
│  │  • Flask==3.0.0                                 │ │
│  │  • flask-cors==4.0.0                            │ │
│  │  • requests==2.31.0                             │ │
│  │  • openpyxl==3.1.2                              │ │
│  │  • Pillow==10.1.0                               │ │
│  └─────────────────────────────────────────────────┘ │
│                        │                              │
│                        ▼                              │
│  ┌─────────────────────────────────────────────────┐ │
│  │  Flask Development Server                       │ │
│  │                                                 │ │
│  │  • Host: localhost                              │ │
│  │  • Port: 5000                                   │ │
│  │  • Debug mode: Enabled                          │ │
│  │  • Auto-reload: Enabled                         │ │
│  └─────────────────────────────────────────────────┘ │
│                        │                              │
│                        │                              │
└────────────────────────┼──────────────────────────────┘
                         │
                         │ HTTP
                         ▼
┌─────────────────────────────────────────────────────────┐
│              User's Web Browser                         │
│                                                         │
│  Access: http://localhost:5000                          │
│                                                         │
│  Supported Browsers:                                    │
│  • Chrome/Edge (recommended)                            │
│  • Firefox                                              │
│  • Safari                                               │
└─────────────────────────────────────────────────────────┘

Production Considerations (if needed):
┌─────────────────────────────────────────────────────────┐
│  • Replace Flask dev server with Gunicorn/uWSGI         │
│  • Add Nginx reverse proxy                              │
│  • Implement authentication (OAuth/LDAP)                │
│  • Use environment variables for config                 │
│  • Add logging and monitoring                           │
│  • Implement rate limiting                              │
│  • Add HTTPS certificates                               │
└─────────────────────────────────────────────────────────┘
```

---

## Summary

This architecture provides:

✅ **Scalability**: Handles 1-7 concurrent run comparisons with parallel API calls  
✅ **Maintainability**: Clear separation of concerns (frontend/backend/reporting)  
✅ **Flexibility**: Multi-suite support with configuration-driven design  
✅ **Performance**: ThreadPool for concurrent test fetching, client-side filtering  
✅ **User Experience**: Responsive UI with adaptive layouts and real-time validation  
✅ **Stateless Design**: No database required, fresh data on every request  
✅ **Extensibility**: Easy to add new suites, features, or calculation methods
