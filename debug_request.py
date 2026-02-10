"""Debug script to inspect request/response details."""
import os
from dotenv import load_dotenv
import json
import requests

load_dotenv()

base_url = os.getenv('WATSONX_BASE_URL')
api_key = os.getenv('WATSONX_API_KEY')
project_id = os.getenv('WATSONX_PROJECT_ID')
model = os.getenv('MODEL')
infer_path = os.getenv('INFER_PATH', '/v1/generate')

# Build URL with placeholders replaced
url = f"{base_url}{infer_path}"
if '{project_id}' in url:
    url = url.replace('{project_id}', project_id)
if '{model}' in url:
    url = url.replace('{model}', model)

print(f"Base URL: {base_url}")
print(f"Infer Path: {infer_path}")
print(f"Full URL: {url}")
print(f"Project ID: {project_id}")
print(f"Model: {model}")
print(f"API Key (first 10 chars): {api_key[:10] if api_key else 'MISSING'}...")
print("\n" + "="*60 + "\n")

# Prepare headers and payload
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json',
}

payload = {
    "model_id": model or "granite-1",
    "input": "What is AI?",
    "parameters": {
        "max_tokens": 200,
        "decoding_method": "greedy"
    }
}

print(f"Headers: {json.dumps({k: v[:15]+'...' if len(str(v))>15 else v for k, v in headers.items()}, indent=2)}")
print(f"Payload: {json.dumps(payload, indent=2)}")
print("\n" + "="*60 + "\n")

# Try the request
try:
    print("Sending request...")
    resp = requests.post(url, headers=headers, json=payload, timeout=10)
    print(f"Status Code: {resp.status_code}")
    print(f"Response Headers: {dict(resp.headers)}")
    print(f"Response Body: {resp.text[:500]}")
    resp.raise_for_status()
except requests.exceptions.HTTPError as e:
    print(f"HTTP Error: {e}")
    print(f"Response: {e.response.text[:500] if e.response else 'N/A'}")
except Exception as e:
    print(f"Error: {e}")
