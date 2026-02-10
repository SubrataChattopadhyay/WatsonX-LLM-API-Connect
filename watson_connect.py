"""
Consolidated WatsonX API Connect - Single file for IBM WatsonX text generation.

This script:
1. Exchanges IBM Service ID API key for an access token via IBM Cloud IAM
2. Connects to WatsonX chat endpoint
3. Provides interactive CLI for asking questions to Granite LLM

Usage:
    python watson_connect.py
"""

import os
import sys
from typing import Any, Dict, Optional
import requests
from dotenv import load_dotenv


class WatsonXConnector:
    """Handles WatsonX authentication and API requests."""
    
    def __init__(self, base_url: str, api_key: str, project_id: str, model: str):
        """Initialize WatsonX connector with credentials.
        
        Args:
            base_url: WatsonX base URL (e.g., 'https://us-south.ml.cloud.ibm.com')
            api_key: IBM Service ID API key
            project_id: WatsonX project ID
            model: Model ID (e.g., 'ibm/granite-4-h-small')
        """
        self.base_url = base_url.rstrip('/')
        self.project_id = project_id
        self.model = model
        self.api_key = api_key
        self.access_token = None
        
        # Exchange API key for access token on initialization
        self._refresh_access_token()
    
    def _refresh_access_token(self) -> str:
        """Exchange IBM Service ID API key for access token via IBM Cloud IAM."""
        iam_url = 'https://iam.cloud.ibm.com/identity/token'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
        }
        data = {
            'grant_type': 'urn:ibm:params:oauth:grant-type:apikey',
            'apikey': self.api_key,
            'response_type': 'cloud_iam',
        }
        
        print("[INFO] Requesting access token from IBM IAM...")
        resp = requests.post(iam_url, headers=headers, data=data, timeout=10)
        resp.raise_for_status()
        
        token_response = resp.json()
        self.access_token = token_response.get('access_token')
        expires_in = token_response.get('expires_in', 0)
        
        if not self.access_token:
            raise RuntimeError('Failed to obtain access token from IBM IAM')
        
        print(f"[INFO] Access token obtained (expires in {expires_in}s)")
        return self.access_token
    
    def chat(self, prompt: str, max_tokens: int = 2000, temperature: float = 0.7) -> str:
        """Send a message to WatsonX and get a response.
        
        Args:
            prompt: User question/message
            max_tokens: Maximum response length (default 2000)
            temperature: Response creativity (0-1, default 0.7)
            
        Returns:
            Response text from the model
        """
        url = f"{self.base_url}/ml/v1/text/chat?version=2023-05-29"
        
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        
        payload = {
            "model_id": self.model,
            "project_id": self.project_id,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": 1.0,
            "frequency_penalty": 0,
            "presence_penalty": 0,
        }
        
        print(f"[DEBUG] POST {url}")
        resp = requests.post(url, headers=headers, json=payload, timeout=60)
        
        if resp.status_code != 200:
            print(f"[ERROR] Status {resp.status_code}: {resp.text[:500]}")
        
        resp.raise_for_status()
        return self._extract_response(resp.json())
    
    @staticmethod
    def _extract_response(response_json: Dict[str, Any]) -> str:
        """Extract text from WatsonX chat response."""
        try:
            # WatsonX chat format: { "choices": [{ "message": { "content": "..." } }] }
            choices = response_json.get('choices', [])
            if choices and isinstance(choices, list):
                first = choices[0]
                if isinstance(first.get('message'), dict):
                    return first['message'].get('content', '').strip()
        except Exception:
            pass
        
        return response_json.get('text', str(response_json))


def load_config() -> Dict[str, str]:
    """Load configuration from .env file."""
    load_dotenv(override=True)
    
    required_vars = {
        'WATSONX_BASE_URL': os.getenv('WATSONX_BASE_URL'),
        'WATSONX_API_KEY': os.getenv('WATSONX_API_KEY'),
        'WATSONX_PROJECT_ID': os.getenv('WATSONX_PROJECT_ID'),
        'MODEL': os.getenv('MODEL'),
    }
    
    missing = [k for k, v in required_vars.items() if not v]
    if missing:
        print(f"[ERROR] Missing environment variables: {', '.join(missing)}")
        print("[ERROR] Please configure .env file with required credentials")
        sys.exit(1)
    
    return required_vars


def interactive_chat(connector: WatsonXConnector):
    """Run interactive chat loop."""
    print("\n" + "="*60)
    print("WatsonX Interactive Chat")
    print("Type 'exit' or 'quit' to exit")
    print("="*60 + "\n")
    
    while True:
        try:
            user_input = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n[INFO] Exiting...")
            break
        
        if not user_input:
            continue
        
        if user_input.lower() in ('exit', 'quit'):
            print("[INFO] Exiting...")
            break
        
        try:
            response = connector.chat(user_input)
            print(f"\n{response}\n")
        except Exception as e:
            print(f"[ERROR] {e}\n")


def main():
    """Main entry point."""
    print("[INFO] Loading configuration...")
    config = load_config()
    
    try:
        print("[INFO] Initializing WatsonX connector...")
        connector = WatsonXConnector(
            base_url=config['WATSONX_BASE_URL'],
            api_key=config['WATSONX_API_KEY'],
            project_id=config['WATSONX_PROJECT_ID'],
            model=config['MODEL'],
        )
        
        print("[SUCCESS] Connected to WatsonX\n")
        interactive_chat(connector)
        
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
