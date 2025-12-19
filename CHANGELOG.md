# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Added
- Initial project setup with TR Result Analyzer
- Configuration file with 22 test suites
  - CoreHR-MasterSuite-STG
  - HRIS-CoreHR-QA
  - HRIS-US-CoreHR
  - HRIS-US-CoreHR-QA
  - HRIS-US-PAY-QA
  - HRIS-US-PAY
  - Payroll-QA
  - Payroll-MasterSuite-STG
  - HRIS-US-TA-QA
  - HRIS-US-TA
  - Time and Attendance-QA
  - Time and Attendance-MasterSuite-STG
  - Benefits-QA
  - Benefits-MasterSuite-STG
  - HRIS-US-BEN
  - HRIS-US-BEN-QA
  - HRIS-US-SCHD-QA
  - HRIS-US-SCHD
  - Schedule-QA
  - Schedule-MasterSuite-STG
  - Neogov Common-QA
  - Neogov Common
- Screenshot validation with fallback logic - 2025-12-17 [@pjayaprakash]
  - Validates screenshot URLs using HTTP HEAD requests before including in report
  - Falls back to `_highlighted.png` version if original `.png` fails
  - Displays "No screenshot available" if both URLs fail
  - Only working screenshot links are added to the report

### Changed
- Optimized screenshot validation performance - 2025-12-17 [@pjayaprakash]
  - Implemented concurrent validation using ThreadPoolExecutor (up to 10 parallel requests)
  - Reduced HTTP timeout from 5 seconds to 2 seconds per request
  - Added session-based connection pooling for request reuse
  - Batch validation processes all screenshots for a test case simultaneously
  - Improved report generation speed from 30 seconds to ~5 seconds for 2 test cases
- Merged "Rerun Failed Tests" feature from external contributor - 2025-12-17 [@pjayaprakash]
  - Added `/api/rerun-failed` endpoint to trigger reruns of failed test cases
  - Adapted rerun functionality to work with multi-suite configuration
  - UI now displays "Rerun" button when failed tests are present in report
- Added "View Report" feature - 2025-12-17 [@pjayaprakash]
  - Added in-browser report viewer that opens in new window
  - Report displays all failure details in formatted HTML table
  - Includes suite info, run details, test statistics, and failure breakdown
  - Shows "No command found" for empty test steps (same as Excel reports)
  - View Report and Download Excel buttons now displayed side-by-side
- Transformed UI into 3-tab dashboard - 2025-12-17 [@pjayaprakash, @Jagriti]
  - Added fixed navigation bar with professional gradient design
  - Tab 1 "Error Report Check": Preserved all existing functionality (View Report, Rerun, optimizations)
  - Tab 2 "Rerun Failed Tests": Advanced test selection and filtering page
    - Filter by single or multiple Case IDs (comma-separated)
    - Filter by error message text
    - Real-time selection counts (Selected/Filtered/Total)
    - Select All / Deselect All / Select All Visible options
    - Apply Filters & Auto-select matching tests
    - Rerun Selected or Rerun All options with confirmation dialogs
    - Functional rerun integration with TestRigor API
    - Returns task ID and queue ID for tracking rerun progress
    - Smart button enabling: Rerun Selected enabled only when tests selected, Rerun All disabled when tests selected
  - Tab 3 "Compare Reports": Side-by-side comparison of 3 test runs
    - Compare results from 3 different Run IDs simultaneously
    - Summary cards showing Total and Failed counts for each run
    - Detailed comparison table with status badges
    - Highlights test case differences across runs
  - Modern card-based responsive design with smooth page transitions
  - Rerun feature automatically uses correct suite credentials
  - Returns task ID and queue ID from TestRigor API for tracking

### Fixed

### Removed

---

## How to Use This Changelog

- **Added**: New features or functionality
- **Changed**: Changes in existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security vulnerability fixes

Format for entries:
```
## [Version] - YYYY-MM-DD
### Category
- Description of change [@PersonName]
```

**Note**: Each entry should include the name of the person who made the change in square brackets with @ prefix (e.g., [@pjayaprakash])
