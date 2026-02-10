"""Test script: send questions to WatsonX/OpenAI LLM and print answers."""
import os
from dotenv import load_dotenv
from watsonx_client import WatsonXClient, OpenAIClient, extract_text_from_response

load_dotenv(override=True)

provider = os.getenv('PROVIDER', 'watsonx').lower()

# Initialize client based on provider
if provider == 'openai':
    api_key = os.getenv('OPENAI_API_KEY')
    model = os.getenv('MODEL', 'gpt-4o')
    client = OpenAIClient(api_key=api_key, model=model)
else:
    base_url = os.getenv('WATSONX_BASE_URL')
    api_key = os.getenv('WATSONX_API_KEY')
    project_id = os.getenv('WATSONX_PROJECT_ID')
    model = os.getenv('MODEL')
    # Optionally use the API key directly instead of exchanging for an IAM token
    use_api_key_direct = os.getenv('WATSONX_USE_APIKEY_DIRECT', 'false').lower() in ('1', 'true', 'yes')
    client = WatsonXClient(
        base_url=base_url,
        api_key=api_key,
        project_id=project_id,
        model=model,
        use_api_key_direct=use_api_key_direct,
    )

print(f'Provider: {provider}')
print(f'Model: {os.getenv("MODEL")}')
print('=' * 60)

# Test questions
questions = [
    'What is the capital of France?',
    'Explain machine learning in one sentence.',
    'What is 2+2?',
]

for i, q in enumerate(questions, 1):
    print(f'\nQuestion {i}: {q}')
    try:
        resp = client.generate(q, max_tokens=200)
        answer = extract_text_from_response(resp)
        print(f'Answer: {answer}')
    except Exception as e:
        print(f'Error: {e}')
    print('-' * 60)

print('\nTest complete!')
