"""WatsonX client for text generation using IAM authentication.

This client exchanges IBM API keys for access tokens via IBM Cloud IAM,
then uses those tokens to query the WatsonX text generation endpoint.
No external SDK required—uses standard requests library.
"""
from typing import Any, Dict, Optional
import requests

try:
    import openai
except Exception:
    openai = None


class WatsonXClient:
    """Client for WatsonX text generation with automatic token refresh."""
    
    def __init__(self, base_url: str, api_key: str, project_id: str, model: str, use_api_key_direct: bool = False):
        """Initialize WatsonX client with API key (exchanges for access token internally).
        
        Args:
            base_url: e.g., 'https://us-south.ml.cloud.ibm.com'
            api_key: IBM API key
            project_id: WatsonX project ID
            model: Model ID (e.g., 'pb-2', 'PB14250', etc.)
        """
        self.base_url = base_url.rstrip('/')
        self.project_id = project_id
        self.model = model
        self.api_key = api_key
        self.access_token = None
        self.use_api_key_direct = bool(use_api_key_direct)

        # If configured to use API key directly, use it as the auth token
        if self.use_api_key_direct:
            # Note: Some IBM endpoints may reject raw API keys; use only if supported.
            self.access_token = self.api_key
        else:
            # Exchange API key for access token on initialization
            self._refresh_access_token()

    def _refresh_access_token(self) -> str:
        """Exchange IBM API key for access token via IBM Cloud IAM."""
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
        
        print(f"[DEBUG] Requesting access token from IBM IAM...")
        resp = requests.post(iam_url, headers=headers, data=data, timeout=10)
        resp.raise_for_status()
        
        token_response = resp.json()
        self.access_token = token_response.get('access_token')
        expires_in = token_response.get('expires_in', 0)
        
        if not self.access_token:
            raise RuntimeError('Failed to obtain access token from IBM IAM')
        
        print(f"[DEBUG] Access token obtained (expires in {expires_in}s, length: {len(self.access_token)})")
        return self.access_token

    def generate(self, prompt: str, max_tokens: int = 512, **kwargs) -> Dict[str, Any]:
        """Generate text using WatsonX chat endpoint.
        
        Args:
            prompt: The input text to generate from
            max_tokens: Maximum tokens to generate (default 512)
            **kwargs: Additional parameters (temperature, top_p, etc.)
            
        Returns:
            Response JSON from WatsonX
        """
        # WatsonX chat API uses messages format
        url = f"{self.base_url}/ml/v1/text/chat?version=2023-05-29"
        
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        
        # WatsonX chat API payload with messages format
        payload = {
            "model_id": self.model,
            "project_id": self.project_id,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": 0.7,
            "top_p": 1.0,
            "frequency_penalty": 0,
            "presence_penalty": 0,
        }
        # Merge any additional kwargs
        for key in ['temperature', 'top_p', 'frequency_penalty', 'presence_penalty', 'max_tokens']:
            if key in kwargs:
                payload[key] = kwargs[key]
        
        print(f"[DEBUG] Calling WatsonX: POST {url}")
        
        resp = requests.post(url, headers=headers, json=payload, timeout=60)
        
        if resp.status_code != 200:
            print(f"[DEBUG] Error {resp.status_code}: {resp.text[:500]}")
        
        resp.raise_for_status()
        return resp.json()


class OpenAIClient:
    def __init__(self, api_key: str, model: str = 'gpt-4o'):
        if openai is None:
            raise RuntimeError('openai package not installed')
        openai.api_key = api_key
        self.model = model

    def generate(self, prompt: str, max_tokens: int = 512, **kwargs) -> Dict[str, Any]:
        # Use Chat Completions style for modern OpenAI models
        messages = [{'role': 'user', 'content': prompt}]
        resp = openai.ChatCompletion.create(model=self.model, messages=messages, max_tokens=max_tokens, **kwargs)
        return resp


def extract_text_from_response(resp: Any) -> str:
    """Try to extract a reasonable text answer from common LLM response shapes."""
    if resp is None:
        return ''
    # Common fields
    if isinstance(resp, dict):
        # OpenAI-like
        choices = resp.get('choices')
        if choices and isinstance(choices, list):
            first = choices[0]
            # chat-style
            if isinstance(first.get('message'), dict):
                return first['message'].get('content', '')
            # text-style
            if 'text' in first:
                return first['text']
        # WatsonX response format: { "results": [{ "generated_text": "..." }] }
        results = resp.get('results')
        if results and isinstance(results, list) and len(results) > 0:
            first = results[0]
            if isinstance(first, dict):
                if 'generated_text' in first:
                    return first['generated_text']
                if 'text' in first:
                    return first['text']
        # fallback: look for 'output', 'text' fields
        if 'output' in resp:
            out = resp['output']
            if isinstance(out, str):
                return out
            if isinstance(out, dict):
                return out.get('text', '') or out.get('content', '')
        if 'text' in resp:
            return resp['text']
    # fallback: convert to string
    return str(resp)
