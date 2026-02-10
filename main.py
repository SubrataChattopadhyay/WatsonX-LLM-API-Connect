"""Small CLI to interactively ask questions to WatsonX or OpenAI.

Usage: create a `.env` file (see `.env.example`) then run `python main.py`.
"""
import os
from dotenv import load_dotenv

from watsonx_client import WatsonXClient, OpenAIClient, extract_text_from_response


def get_env(name, default=None):
    v = os.getenv(name, default)
    if v is None:
        raise RuntimeError(f'Missing environment variable: {name}')
    return v


def main():
    load_dotenv(override=True)
    provider = os.getenv('PROVIDER', 'watsonx').lower()
    if provider == 'openai':
        api_key = get_env('OPENAI_API_KEY')
        model = os.getenv('MODEL', 'gpt-4o')
        client = OpenAIClient(api_key=api_key, model=model)
    else:
        base_url = get_env('WATSONX_BASE_URL')
        api_key = get_env('WATSONX_API_KEY')
        project_id = get_env('WATSONX_PROJECT_ID')
        model = get_env('MODEL')
        use_api_key_direct = os.getenv('WATSONX_USE_APIKEY_DIRECT', 'false').lower() in ('1', 'true', 'yes')
        client = WatsonXClient(base_url=base_url, api_key=api_key, project_id=project_id, model=model, use_api_key_direct=use_api_key_direct)

    print(f"Provider: {provider}")
    print('Enter a question (empty to quit)')
    while True:
        try:
            prompt = input('\n> ').strip()
        except (EOFError, KeyboardInterrupt):
            print('\nExiting')
            break
        if not prompt:
            break
        try:
            resp = client.generate(prompt)
            text = extract_text_from_response(resp)
            print('\n--- Answer ---')
            print(text)
        except Exception as e:
            print(f'Error calling model: {e}')


if __name__ == '__main__':
    main()
