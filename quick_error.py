"""Quick test to see full error message from WatsonX."""
import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()

api_key = os.getenv('WATSONX_API_KEY')
iam_url = 'https://iam.cloud.ibm.com/identity/token'
iam_data = {'grant_type': 'urn:ibm:params:oauth:grant-type:apikey', 'apikey': api_key, 'response_type': 'cloud_iam'}

resp = requests.post(iam_url, headers={'Content-Type': 'application/x-www-form-urlencoded'}, data=iam_data, timeout=10)
token = resp.json()['access_token']

url = f"{os.getenv('WATSONX_BASE_URL')}{os.getenv('INFER_PATH')}".replace('{project_id}', os.getenv('WATSONX_PROJECT_ID'))
headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
payload = {"model_id": os.getenv('MODEL'), "input": "test", "parameters": {"max_tokens": 100}}

print(f"URL: {url}\n")
r = requests.post(url, headers=headers, json=payload, timeout=10)
print(f"Status: {r.status_code}")
print(f"Error Details:\n{r.text}")
