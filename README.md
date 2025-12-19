# Test Rigor Failure Reporter

A one-click solution to generate comprehensive failure reports from Test Rigor test runs.

## Features

- ✅ Fetch test run details using Test Rigor API
- ✅ Identify failed test cases automatically
- ✅ Capture failure step number, error messages, and screenshots
- ✅ Generate Excel reports with detailed failure information
- ✅ Simple web UI for easy report generation
- ✅ One-click operation - just enter Run ID and submit

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Test Rigor API key

### Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API credentials:**
   - Open `config.json`
   - Replace `YOUR_TESTRIGOR_API_KEY_HERE` with your actual Test Rigor API key
   - Update `testrigor_base_url` if needed (default: https://api.testrigor.com/v1)

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Access the UI:**
   - Open your browser and navigate to: `http://localhost:5000`

## Usage

1. Open the web interface at `http://localhost:5000`
2. Enter the Test Rigor Run ID in the input field
3. Click "Generate Report" button
4. Wait for the report generation to complete
5. Download the Excel report with all failure details

## Report Contents

The generated Excel report includes:

- **Run Information**: Run ID, name, status, generation date
- **Failure Summary**: Total tests run and failed count
- **Detailed Failure Table**:
  - Test ID
  - Test Name
  - Status (failed/error)
  - Failure Step Number
  - Error Message
  - Screenshot Link

## RTR Calculation Formulas

### Individual RTR Calculation
For each test type (Test Rigor, POM, JMeter):

```
RTR = ((Passed + Valid Fail) / Total Test Cases) × 100
Failed = Total Test Cases - Passed - Valid Fail
```

**Where:**
- **Passed** = Number of test cases that passed successfully
- **Valid Fail** = Number of test cases with expected/valid failures
- **Total Test Cases** = Total number of test cases executed
- **Failed** = Number of unexpected failures

### Cumulative RTR Calculation
For overall cumulative RTR across all test types:

```
Overall RTR = ((Total Passed + Total Valid Fail) / Total Test Cases) × 100
Total Failed = Total Test Cases - Total Passed - Total Valid Fail
```

**Where:**
- **Total Test Cases** = Sum of all test cases across Test Rigor, POM, and JMeter
- **Total Passed** = Sum of passed test cases across all test types
- **Total Valid Fail** = Sum of valid failures across all test types
- **Total Failed** = Sum of unexpected failures across all test types

**Logic:**
- RTR (Run-Through Rate) represents the percentage of test cases that either passed OR had valid/expected failures
- Valid Fail counts are included in RTR because they represent expected behavior (e.g., negative test cases)
- Only unexpected failures are excluded from the RTR calculation
- The cumulative calculation aggregates all values across the three test types before applying the formula

## Project Structure

```
Hackathon/
├── app.py                 # Flask application (main entry point)
├── report_generator.py    # Excel report generation logic
├── config.json           # Configuration file for API credentials
├── requirements.txt      # Python dependencies
├── templates/
│   └── index.html       # Web UI
└── reports/             # Generated reports (auto-created)
```

## API Endpoints

### POST `/api/generate-report`
Generate a failure report for a specific run.

**Request Body:**
```json
{
  "run_id": "12345"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Report generated successfully",
  "report_path": "TestRigor_FailureReport_12345_20231216_120000.xlsx",
  "total_tests": 50,
  "failed_tests": 5
}
```

### GET `/api/download-report/<filename>`
Download the generated report file.

## Test Rigor API Integration

This tool uses the following Test Rigor API endpoints:

- `GET /runs/{run_id}` - Fetch run details
- `GET /runs/{run_id}/tests` - Fetch all tests in a run
- `GET /runs/{run_id}/tests/{test_id}` - Fetch detailed test information

**Note**: Make sure your API key has appropriate permissions to access these endpoints.

## Troubleshooting

### Common Issues

1. **"Failed to fetch run details"**
   - Verify your API key in `config.json`
   - Check if the Run ID exists in Test Rigor
   - Ensure API key has necessary permissions

2. **Module not found errors**
   - Run `pip install -r requirements.txt` again
   - Verify Python version is 3.8+

3. **Port already in use**
   - Change the port in `app.py`: `app.run(port=5001)`
   - Or kill the process using port 5000

## Customization

### Changing Report Format

To modify the Excel report format, edit the `report_generator.py` file:
- Adjust column widths
- Modify styling (colors, fonts, borders)
- Add/remove columns

### Adding PDF Support

To add PDF report generation:
1. Install: `pip install reportlab`
2. Create a new method in `ReportGenerator` class
3. Update the UI to allow format selection

## Security Notes

- Keep your `config.json` file secure and never commit it to version control
- Add `config.json` to `.gitignore`
- Use environment variables for production deployments

## Future Enhancements

- [ ] Support for PDF reports
- [ ] Email notification upon report generation
- [ ] Schedule automated report generation
- [ ] Support for multiple run IDs in batch
- [ ] Historical trend analysis
- [ ] Integration with Slack/Teams for notifications

## License

MIT License - Feel free to use and modify as needed.

## Support

For issues or questions:
1. Check the Test Rigor API documentation
2. Review the troubleshooting section
3. Contact your Test Rigor support team
