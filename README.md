# Watsonx API Connect Foundation Model (LLM)

This small project provides a minimal Python client and CLI to interact with IBM watsonx-like endpoints (Granite) or OpenAI (gpt-5). It is intentionally generic — configure the endpoint path that matches your watsonx deployment.

Quick start

1. Create a virtual environment and install deps:

```bash
python -m venv .venv
.venv\Scripts\activate    # Windows
pip install -r requirements.txt
```

2. Copy `.env.example` to `.env` and fill values (set `PROVIDER=watsonx` or `PROVIDER=openai`).

3. Run the CLI:

```bash
python main.py
```

Notes
- For WatsonX, provide a correct `WATSONX_BASE_URL` and `INFER_PATH` if your deployment uses a non-standard path. The `INFER_PATH` may include placeholders `{project_id}` and `{model}` which will be replaced from env.
- For OpenAI, set `PROVIDER=openai` and `OPENAI_API_KEY` and `MODEL`.

Files
- `watsonx_client.py`: client wrappers for generic REST-based watsonx endpoints and OpenAI.
- `main.py`: interactive CLI.
- `.env.example`: environment variable examples.

