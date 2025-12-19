# Test Rigor Analyzer & Rerunner - Architectural Overview

## **Project Purpose**
A comprehensive web-based testing dashboard that integrates with TestRigor API to generate failure reports, compare multiple test runs, calculate Run-Through Rate (RTR), and provide cumulative RTR metrics across different test execution runs.

---

## **Architecture Pattern**
**Client-Server Architecture** with Flask-based REST API backend and vanilla JavaScript frontend

```
┌─────────────────────────────────────────────────────────┐
│                    Browser (Client)                      │
│  ┌──────────────────────────────────────────────────┐  │
│  │   Single Page Application (SPA)                  │  │
│  │   - 3 Tab Interface (HTML/CSS/JS)                │  │
│  │   - Dynamic UI rendering                         │  │
│  │   - Column-specific search                       │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                         ↕ HTTP/JSON
┌─────────────────────────────────────────────────────────┐
│              Flask Web Server (Python)                   │
│  ┌──────────────────────────────────────────────────┐  │
│  │   REST API Endpoints                             │  │
│  │   - /api/generate-report                         │  │
│  │   - /api/compare-runs                            │  │
│  │   - /api/download-summary-report                 │  │
│  │   - /api/calculate-cumulative-rtr                │  │
│  └──────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────┐  │
│  │   Business Logic Layer                           │  │
│  │   - Test result processing                       │  │
│  │   - RTR calculations                             │  │
│  │   - Failure detection & analysis                 │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                         ↕ HTTPS/JSON
┌─────────────────────────────────────────────────────────┐
│              TestRigor API (External)                    │
│  - Fetch run details                                     │
│  - Retrieve test cases                                   │
│  - Get test execution results                            │
└─────────────────────────────────────────────────────────┘
```

---

## **Technology Stack**

### **Frontend:**
- HTML5, CSS3 (Flexbox, Grid, Animations)
- Vanilla JavaScript (ES6+)
- No frameworks - pure DOM manipulation

### **Backend:**
- Python 3.8+
- Flask 3.0.0 (Web framework)
- Flask-CORS (Cross-origin support)
- Requests library (HTTP client)

### **Data Processing:**
- OpenpyXL 3.1.2 (Excel generation)
- Pillow 10.1.0 (Image processing for screenshots)

### **External Integration:**
- TestRigor REST API v1/v2

---

## **Core Components**

### **1. Frontend (templates/index.html) - 3287 lines**
**Three Main Tabs:**

**Tab 1: Generate Failure Report & Rerun**
- Single run analysis
- Failure detection and screenshot capture
- Excel report generation
- Rerun command generation

**Tab 2: Compare TR Runs & Calculate RTR** ⭐ *Main Feature*
- Compare up to **7 test runs simultaneously**
- Side-by-side statistics (Total/Passed/Failed/Valid Fail/RTR)
- Responsive layout:
  - Grid layout (3 columns) for ≤3 runs
  - Horizontal scroll layout for 4-7 runs
- Detailed comparison table with:
  - Test Case ID and Name columns
  - Status columns for each run (Passed/Failed/Not Run)
  - Column-specific search functionality
- Valid Fail override capability
- RTR recalculation with custom valid fails
- Excel export with Overall Summary + Detailed Summary sheets

**Tab 3: Cumulative RTR Calculator**
- Aggregate RTR across TestRigor, POM, and JMeter
- Multi-suite analysis
- Overall success rate calculation

### **2. Backend (app.py) - 1136 lines**

**Key Endpoints:**

```python
# Generate failure report for single run
POST /api/generate-report
  Input: {suite, run_id}
  Output: {report_data, failures[], download_link}

# Compare multiple runs (up to 7)
POST /api/compare-runs
  Input: {suite, run_ids: [id1...id7]}
  Output: {run1_data...run7_data, comparison_table}

# Download Excel comparison report
POST /api/download-summary-report
  Input: {suite, run_ids[], test_data[]}
  Output: Excel file stream

# Calculate cumulative RTR
POST /api/calculate-cumulative-rtr
  Input: {test_rigor_data, pom_data, jmeter_data}
  Output: {aggregated_stats, overall_rtr}
```

**Core Functions:**
- `fetch_run_details()` - API call to get run metadata
- `fetch_test_cases()` - Retrieve all tests in a run
- `process_failures()` - Identify and analyze failed tests
- `extract_test_case_id()` - Parse test identifiers
- Multi-threaded test case fetching for performance

### **3. Report Generator (report_generator.py)**
- Excel workbook creation with formatting
- Screenshot embedding in cells
- Multi-sheet reports with styling
- Column auto-sizing and cell formatting

### **4. Configuration (config.json)**
- Multi-suite support (16+ TestRigor suites)
- Per-suite authentication tokens
- Base URL configuration per suite
- Centralized credential management

---

## **Data Flow - Compare Runs Feature**

```
1. User enters 1-7 Run IDs + selects suite
          ↓
2. Frontend validates input (no duplicates, proper IDs)
          ↓
3. AJAX POST to /api/compare-runs
          ↓
4. Backend fetches data for each run ID in parallel:
   - Run metadata (name, date, status)
   - All test cases
   - Test results (passed/failed/skipped)
          ↓
5. Backend processes and normalizes data:
   - Extract Test Case IDs (C###### format)
   - Map test names to results
   - Calculate statistics per run
          ↓
6. Return JSON with 7 run datasets
          ↓
7. Frontend displays:
   - Comparison cards (overall stats)
   - Detailed table (test-by-test comparison)
   - Search functionality
   - Excel download option
```

---

## **Key Design Patterns**

### **1. Multi-Suite Architecture**
- Configuration-driven suite selection
- Dynamic API endpoint resolution
- Per-suite authentication

### **2. Progressive Enhancement**
- Base functionality for 1 run
- Scales to 7 runs with adaptive UI
- Conditional features (scroll hints, compact layout)

### **3. Lazy Loading & Visibility Management**
- Cards hidden by default (`display: none`)
- Shown dynamically based on data availability
- Search inputs follow same pattern

### **4. Client-Side State Management**
- `comparisonData` global object stores all run data
- Event-driven validation (real-time duplicate checking)
- Button state management (enable/disable based on validity)

### **5. Excel Generation**
- Two-sheet structure:
  - **Overall Summary**: Aggregated stats for all runs
  - **Detailed Summary**: Test-by-test breakdown with all runs
- Dynamic column generation (adapts to number of runs)
- Formatted cells with borders, alignment, colors

---

## **File Structure**

```
TR Result Analyzer & Rerunner/
├── app.py                      # Flask application & API endpoints
├── report_generator.py         # Excel report generation logic
├── config.json                 # Suite configurations & API keys
├── requirements.txt            # Python dependencies
├── README.md                   # Documentation
├── Launch_TR_Reporter.bat      # Windows launcher
├── templates/
│   └── index.html             # SPA frontend (3287 lines)
├── reports/                    # Generated Excel reports
└── __pycache__/               # Python bytecode cache
```

---

## **Scalability & Performance**

- **Concurrent API Calls**: Uses `ThreadPoolExecutor` for parallel test case fetching
- **Horizontal Scrolling**: Handles 7 runs without layout issues
- **Column-Specific Search**: Filters 1000s of test rows efficiently
- **Lazy Rendering**: Only visible run data is processed

---

## **Security Considerations**

- API keys stored in `config.json` (not in code)
- CORS enabled for local development
- Input validation on both client and server
- Error handling with proper HTTP status codes

---

## **RTR Calculation Logic**

### Individual Run RTR:
```
RTR = ((Passed Tests + Valid Fail) / Total Tests) × 100

Where:
- Passed Tests: Test cases that passed successfully
- Valid Fail: Expected failures (e.g., negative test cases)
- Total Tests: All test cases executed
- Failed Tests: Total - Passed - Valid Fail (unexpected failures)
```

### Cumulative RTR (Across Multiple Test Types):
```
Overall RTR = ((Total Passed + Total Valid Fail) / Total Test Cases) × 100

Where:
- Total Test Cases = Sum of all tests across TestRigor + POM + JMeter
- Total Passed = Sum of passed tests across all types
- Total Valid Fail = Sum of valid failures across all types
```

---

## **Key Features Summary**

✅ **Multi-Run Comparison**: Compare up to 7 TestRigor runs side-by-side  
✅ **Adaptive UI**: Responsive layout that adjusts based on number of runs  
✅ **Advanced Filtering**: Column-specific search across all test results  
✅ **Valid Fail Override**: Recalculate RTR with custom valid failure counts  
✅ **Excel Export**: Comprehensive reports with multiple sheets and formatting  
✅ **Real-Time Validation**: Duplicate detection and input validation  
✅ **Multi-Suite Support**: 16+ pre-configured TestRigor suites  
✅ **Parallel Processing**: Concurrent API calls for improved performance  
✅ **Stateless Design**: No database required, fresh data on every request  

---

## **Deployment**

### Local Development:
```bash
# Install dependencies
pip install -r requirements.txt

# Configure API credentials in config.json

# Run the application
python app.py
# OR
Launch_TR_Reporter.bat

# Access in browser
http://localhost:5000
```

### Production Considerations:
- Replace Flask dev server with Gunicorn/uWSGI
- Add Nginx reverse proxy
- Implement authentication (OAuth/LDAP)
- Use environment variables for sensitive config
- Add logging and monitoring
- Implement rate limiting
- Add HTTPS certificates

---

This architecture provides a robust, scalable solution for TestRigor test analysis with support for complex multi-run comparisons and comprehensive reporting capabilities.
