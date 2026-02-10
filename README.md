# Final Watson API Connect

A lightweight, single-file Python application for connecting to IBM WatsonX and chatting with the Granite LLM via REST API.

## Features

- ✅ IBM Cloud IAM authentication (Service ID API key exchange)
- ✅ WatsonX chat endpoint integration
- ✅ Interactive CLI for real-time Q&A
- ✅ Automatic token refresh
- ✅ Error handling and debugging

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure .env

Edit `.env` with your credentials:

```env
WATSONX_BASE_URL=https://us-south.ml.cloud.ibm.com
WATSONX_API_KEY=your_service_id_api_key
WATSONX_PROJECT_ID=your_project_id
MODEL=ibm/granite-4-h-small
```

See [How_to_generate_API_details.md](../watsonxAPIconnect/How_to_generate_API_details.md) for detailed steps.

### 3. Run

```bash
python watson_connect.py
```

### 4. Chat

Type your questions at the `>` prompt:

```
> What is artificial intelligence?
AI, or Artificial Intelligence, refers to the simulation of human intelligence...

> How to book a flight?
Here are the steps to book a flight...

> exit
```

## Architecture

**Single File:** `watson_connect.py`
- `WatsonXConnector` class: Handles authentication and API calls
- `load_config()`: Loads credentials from .env
- `interactive_chat()`: Provides the CLI loop
- `main()`: Entry point

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `WATSONX_BASE_URL` | API endpoint | `https://us-south.ml.cloud.ibm.com` |
| `WATSONX_API_KEY` | Service ID API key | `_abc123xyz...` |
| `WATSONX_PROJECT_ID` | WatsonX project ID | `7398bce0-...` |
| `MODEL` | Model identifier | `ibm/granite-4-h-small` |

## Dependencies

- **requests** (2.28.0+): HTTP library for API calls
- **python-dotenv** (1.0.0+): Environment variable management

## How It Works

1. **Authentication**: Exchanges Service ID API key for temporary access token via IBM IAM
2. **Chat Request**: Sends user prompt to WatsonX chat endpoint with token
3. **Response**: Extracts and displays model response
4. **Loop**: Continues accepting questions until user exits

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| `Missing environment variables` | .env file not configured | Copy and fill .env with your credentials |
| `401 Unauthorized` | Invalid/expired token | Ensure API key is correct; tokens refresh automatically |
| `403 Forbidden` | No access to project | Add Service ID to project collaborators |
| `404 Not Found` | Model doesn't exist | Verify model name in your WatsonX project |

## Files

- `watson_connect.py` - Main application
- `.env` - Configuration (credentials)
- `requirements.txt` - Dependencies

## Notes

- Keep `.env` secure—don't commit to version control
- Access tokens expire after 1 hour and are refreshed automatically
- Responses can be adjusted by modifying `temperature` parameter (0-1)
- Maximum response length controlled by `max_tokens` parameter

## More Information

For detailed setup instructions, see: [How_to_generate_API_details.md](../watsonxAPIconnect/How_to_generate_API_details.md)
