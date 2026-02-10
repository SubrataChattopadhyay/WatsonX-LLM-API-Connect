from dotenv import load_dotenv
import os

load_dotenv()

from watsonx_client import WatsonXClient, OpenAIClient, extract_text_from_response

provider = os.getenv('PROVIDER', 'watsonx').lower()
print('PROVIDER=', provider)

def mask(s):
    return (s[:6] + '...' + s[-6:]) if s and len(s) > 12 else (s or '')

print('WATSONX_BASE_URL=', mask(os.getenv('WATSONX_BASE_URL')))
print('WATSONX_API_KEY=', 'SET' if os.getenv('WATSONX_API_KEY') else 'MISSING')
print('WATSONX_PROJECT_ID=', mask(os.getenv('WATSONX_PROJECT_ID')))
print('OPENAI_API_KEY=', 'SET' if os.getenv('OPENAI_API_KEY') else 'MISSING')

ok = False
try:
    if provider == 'openai':
        key = os.getenv('OPENAI_API_KEY')
        if not key:
            print('OpenAI key missing')
        else:
            OpenAIClient(api_key=key)
            print('OpenAI client instantiated')
            ok = True
    else:
        key = os.getenv('WATSONX_API_KEY')
        if not key:
            print('WatsonX key missing')
        else:
            WatsonXClient(
                base_url=os.getenv('WATSONX_BASE_URL') or '',
                api_key=key,
                project_id=os.getenv('WATSONX_PROJECT_ID'),
                model=os.getenv('MODEL'),
                infer_path=os.getenv('INFER_PATH'),
            )
            print('WatsonX client instantiated')
            ok = True
except Exception as e:
    print('Instantiation error:', e)

print('extract_text:', extract_text_from_response({'choices': [{'message': {'content': 'hello from mock'}}]}))
print('SMOKE_OK' if ok else 'SMOKE_PARTIAL')
