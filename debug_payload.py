"""Debug script to see full error response from WatsonX."""
import os
from dotenv import load_dotenv
import json
import requests

load_dotenv()

# Get access token first
api_key = os.getenv('WATSONX_API_KEY')
iam_url = 'https://iam.cloud.ibm.com/identity/token'
iam_headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'application/json'}
iam_data = {'grant_type': 'urn:ibm:params:oauth:grant-type:apikey', 'apikey': api_key, 'response_type': 'cloud_iam'}

print("Getting access token...")
iam_resp = requests.post(iam_url, headers=iam_headers, data=iam_data, timeout=10)
iam_resp.raise_for_status()
access_token = iam_resp.json().get('access_token')
print(f"Access token obtained: {access_token[:20]}...")

base_url = os.getenv('WATSONX_BASE_URL')
project_id = os.getenv('WATSONX_PROJECT_ID')
model = os.getenv('MODEL')
infer_path = os.getenv('INFER_PATH', '/v1/generate')

# Build URL with placeholders replaced
url = f"{base_url}{infer_path}"
if '{project_id}' in url:
    url = url.replace('{project_id}', project_id)
if '{model}' in url:
    url = url.replace('{model}', model)

print(f"\nFull URL: {url}")
print(f"Model: {model}")

# Try different payload formats
payloads = [
    {
        "name": "Format 1: model_id + input + parameters",
        "data": {
            "model_id": model,
            "input": "What is AI?",
            "parameters": {
                "max_tokens": 200,
                "decoding_method": "greedy"
            }
        }
    },
    {
        "name": "Format 2: prompt only",
        "data": {
            "prompt": "What is AI?"
        }
    },
    {
        "name": "Format 3: messages array (chat style)",
        "data": {
            "messages": [{"role": "user", "content": "What is AI?"}]
        }
    }
]

headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json',
}

for payload_test in payloads:
    print(f"\n{'='*60}")
    print(f"Testing: {payload_test['name']}")
    print(f"Payload: {json.dumps(payload_test['data'], indent=2)}")
    try:
        resp = requests.post(url, headers=headers, json=payload_test['data'], timeout=10)
        print(f"Status: {resp.status_code}")
        if resp.status_code >= 400:
            print(f"Error Response: {resp.text[:800]}")
        else:
            print(f"Success! Response: {resp.text[:800]}")
    except Exception as e:
        print(f"Exception: {e}")
