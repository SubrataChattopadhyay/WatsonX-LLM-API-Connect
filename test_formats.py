"""Test different payload and auth formats to find what works."""
import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()

base_url = os.getenv('WATSONX_BASE_URL')
token = os.getenv('WATSONX_TOKEN')
project_id = os.getenv('WATSONX_PROJECT_ID')
model = os.getenv('MODEL')
infer_path = os.getenv('INFER_PATH', '/v1/generate')

url = f"{base_url}{infer_path}".replace('{project_id}', project_id)
print(f"URL: {url}")
print(f"Model: {model}")
print(f"Token (first 20 chars): {token[:20] if token else 'MISSING'}...")

test_cases = [
    {
        "name": "Bearer + model_id/input/parameters",
        "headers": {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'},
        "payload": {"model_id": model, "input": "What is AI?", "parameters": {"max_tokens": 100, "decoding_method": "greedy"}}
    },
    {
        "name": "Bearer + prompt only",
        "headers": {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'},
        "payload": {"prompt": "What is AI?"}
    },
    {
        "name": "Direct token (no Bearer) + model_id/input",
        "headers": {'Authorization': token, 'Content-Type': 'application/json'},
        "payload": {"model_id": model, "input": "What is AI?", "parameters": {"max_tokens": 100}}
    },
    {
        "name": "Bearer + messages array",
        "headers": {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'},
        "payload": {"messages": [{"role": "user", "content": "What is AI?"}]}
    },
]

for test in test_cases:
    print(f"\n{'='*70}")
    print(f"Test: {test['name']}")
    print(f"Headers: Authorization={test['headers']['Authorization'][:30]}...")
    print(f"Payload: {json.dumps(test['payload'], indent=2)[:200]}")
    try:
        r = requests.post(url, headers=test['headers'], json=test['payload'], timeout=10)
        print(f"Status: {r.status_code}")
        if r.status_code == 200:
            print(f"✅ SUCCESS!")
            print(f"Response (first 300 chars): {r.text[:300]}")
            break
        else:
            print(f"Response (first 200 chars): {r.text[:200]}")
    except Exception as e:
        print(f"Exception: {e}")
