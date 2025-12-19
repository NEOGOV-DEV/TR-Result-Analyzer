from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
import requests
import json
from datetime import datetime
import os
from report_generator import ReportGenerator

app = Flask(__name__)
CORS(app)

# Load configuration
with open('config.json', 'r') as f:
    config = json.load(f)

TESTRIGOR_API_KEY = config.get('testrigor_api_key')
TESTRIGOR_BASE_URL = config.get('testrigor_base_url')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate-report', methods=['POST'])
def generate_report():
    try:
        data = request.json
        run_id = data.get('run_id')
        
        if not run_id:
            return jsonify({'error': 'Run ID is required'}), 400
        
        # Fetch test run details from Test Rigor API
        run_details = fetch_run_details(run_id)
        
        if not run_details:
            return jsonify({'error': 'Failed to fetch run details. Please check Run ID and API credentials.'}), 400
        
        # Fetch test cases in the run
        test_cases = fetch_test_cases(run_id)
        
        # Process failures
        failures = process_failures(run_id, test_cases)
        
        # Generate report
        report_generator = ReportGenerator()
        report_path = report_generator.generate_excel_report(run_id, run_details, failures)
        
        return jsonify({
            'success': True,
            'message': 'Report generated successfully',
            'report_path': report_path,
            'total_tests': len(test_cases),
            'failed_tests': len(failures)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download-report/<filename>')
def download_report(filename):
    try:
        report_path = os.path.join('reports', filename)
        if os.path.exists(report_path):
            return send_file(report_path, as_attachment=True)
        else:
            return jsonify({'error': 'Report not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def fetch_run_details(run_id):
    """Fetch test run details from Test Rigor API"""
    try:
        headers = {
            'auth-token': TESTRIGOR_API_KEY
        }
        
        url = f'{TESTRIGOR_BASE_URL}/runs/{run_id}'
        print(f"\n=== FETCHING RUN DETAILS ===")
        print(f"URL: {url}")
        
        response = requests.get(url, headers=headers)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            response_json = response.json()
            print(f"Response Keys: {list(response_json.keys())}")
            data = response_json.get('data', response_json)
            print(f"Run Details: {json.dumps(data, indent=2)[:1000]}")
            return data
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
    
    except Exception as e:
        print(f"Exception in fetch_run_details: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def fetch_test_cases(run_id):
    """Fetch all test cases for a given run with pagination"""
    try:
        headers = {
            'auth-token': TESTRIGOR_API_KEY
        }
        
        print(f"\n=== FETCHING TEST CASES ===")
        all_test_cases = []
        page = 0
        page_size = 100
        
        while True:
            url = f'{TESTRIGOR_BASE_URL}/runs/{run_id}/testcases?page={page}&size={page_size}'
            print(f"Fetching page {page}: {url}")
            
            response = requests.get(url, headers=headers)
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                response_json = response.json()
                data = response_json.get('data', {})
                test_cases = data.get('content', [])
                
                print(f"Test Cases on page {page}: {len(test_cases)}")
                
                if not test_cases:
                    break
                
                all_test_cases.extend(test_cases)
                
                # Check if there are more pages
                total_elements = data.get('totalElements', 0)
                print(f"Total elements: {total_elements}, Fetched so far: {len(all_test_cases)}")
                
                if len(all_test_cases) >= total_elements:
                    break
                
                page += 1
            else:
                print(f"Error: {response.status_code} - {response.text}")
                break
        
        print(f"Total Test Cases Fetched: {len(all_test_cases)}")
        return all_test_cases
    
    except Exception as e:
        print(f"Exception in fetch_test_cases: {str(e)}")
        import traceback
        traceback.print_exc()
        return []

def process_failures(run_id, test_cases):
    """Process failed test cases and extract failure details"""
    failures = []
    
    print(f"\n=== PROCESSING FAILURES ===")
    print(f"Total test cases: {len(test_cases)}")
    
    for test in test_cases:
        # Check if test failed (Test Rigor uses 'Failed' with capital F)
        status = test.get('status', '')
        if status in ['Failed', 'failed', 'error', 'Error']:
            # Extract Test Case ID from name (C followed by numbers)
            test_name = test.get('name', 'Unknown Test')
            import re
            match = re.search(r'C\d+', test_name)
            test_case_id = match.group(0) if match else 'N/A'
            
            # Get execution details
            test_case_uuid = test.get('testCaseUuid')
            executions = test.get('executions', [])
            
            failure_step = 'N/A'
            error_message = 'No error details available'
            screenshot_url = None
            
            if executions and test_case_uuid:
                execution_uuid = executions[0].get('uuid')
                
                # Fetch detailed execution info to get failed step
                execution_details = fetch_execution_details(run_id, test_case_uuid, execution_uuid)
                
                print(f"Execution details type: {type(execution_details)}")
                print(f"Execution details length: {len(execution_details) if execution_details else 0}")
                
                if execution_details:
                    # execution_details is either a dict with 'steps' key or directly a list of steps
                    steps = execution_details if isinstance(execution_details, list) else execution_details.get('steps', [])
                    
                    print(f"Steps type: {type(steps)}, Steps count: {len(steps)}")
                    
                    for step in steps:
                        step_status = step.get('status')
                        
                        if step_status in ['Failed', 'failed', 'Error', 'error']:
                            failure_step = step.get('step', 'N/A')
                            
                            # DEBUG: Print all fields in the step to find the command field
                            print(f"\n=== FAILED STEP DATA ===")
                            print(f"All step keys: {list(step.keys())}")
                            for key, value in step.items():
                                print(f"{key}: {value}")
                            print("=" * 50)
                            
                            # Get the error message (full stepDescription)
                            error_message = step.get('stepDescription', 'No error details available')
                            
                            # Get the actual command that was executed (TestRigor script line)
                            # Checking multiple possible field names:
                            failed_command = (
                                step.get('command') or 
                                step.get('action') or 
                                step.get('instruction') or 
                                step.get('testCommand') or 
                                step.get('scriptLine') or
                                step.get('commandText') or
                                'N/A'
                            )
                            
                            # Get screenshot - need to construct URL or fetch it
                            screenshot_url = step.get('screenshot', step.get('screenshotUrl'))
                            
                            print(f"\nExtracted Command: {failed_command}")
                            print(f"Error Message: {error_message}")
                            break
            
            failure_info = {
                'test_case_id': test_case_id,
                'test_name': test_name,
                'status': status,
                'screenshot_number': failure_step,
                'failed_command': failed_command if 'failed_command' in locals() else 'N/A',
                'error_message': error_message,
                'screenshot_url': screenshot_url
            }
            
            failures.append(failure_info)
            print(f"Found failure: {test_case_id} - Screenshot {failure_step} - {error_message[:50]}...")
    
    print(f"Total failures found: {len(failures)}")
    return failures

def fetch_test_details(run_id, test_id):
    """Fetch detailed information for a specific test"""
    try:
        headers = {
            'auth-token': TESTRIGOR_API_KEY
        }
        
        url = f'{TESTRIGOR_BASE_URL}/runs/{run_id}/testcases/{test_id}'
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching test details: {response.status_code} - {response.text}")
            return None
    
    except Exception as e:
        print(f"Exception in fetch_test_details: {str(e)}")
        return None

def fetch_execution_details(run_id, test_case_uuid, execution_uuid):
    """Fetch detailed execution information including steps"""
    try:
        headers = {
            'auth-token': TESTRIGOR_API_KEY
        }
        
        url = f'{TESTRIGOR_BASE_URL}/runs/{run_id}/testcases/{test_case_uuid}/executions/{execution_uuid}'
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            response_json = response.json()
            
            # Handle different response structures
            if isinstance(response_json, dict):
                # Check if data is present and is a list (steps array)
                data = response_json.get('data', response_json)
                if isinstance(data, list):
                    return data  # Return the list of steps directly
                else:
                    return data  # Return dict as is
            elif isinstance(response_json, list):
                return response_json  # Return list of steps directly
            else:
                return []
        else:
            print(f"Error fetching execution details: {response.status_code}")
            return None
    
    except Exception as e:
        print(f"Exception in fetch_execution_details: {str(e)}")
        return None

if __name__ == '__main__':
    # Create reports directory if it doesn't exist
    os.makedirs('reports', exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
