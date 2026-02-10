# How to Generate API Details for IBM WatsonX

This guide walks you through the process of setting up IBM WatsonX authentication and obtaining the necessary API credentials to connect to the WatsonX service via REST API.

## Prerequisites

- An IBM Cloud account
- Access to the IBM Cloud console

## Steps

### Step 1: Sign Up to IBM WatsonX (if you haven't done already)

1. Visit [IBM Cloud](https://cloud.ibm.com/)
2. Click **Create account** if you don't have one
3. Follow the registration process and verify your email
4. Once registered, log in to your IBM Cloud account

### Step 2: Create a Project in WatsonX

1. Log in to your IBM Cloud account
2. Navigate to **WatsonX** (search for it in the catalog if needed)
3. Click **Create a new project** or **New project**
4. Fill in the project details (name, description, etc.)
5. Click **Create**
6. **Important:** Once the project is created, go to **Project settings** and copy the **Project ID**
   - Save this ID in a safe place—you'll need it later
   - Do **NOT** create an access token here; we'll use a Service ID instead

### Step 3: Go to IAM and Create a Service ID

1. In the IBM Cloud console, click the **Manage** menu (top-right)
2. Select **Access (IAM)**
3. In the left sidebar, click **Users** → **Service IDs**
4. Click **Create service ID**
5. Fill in:
   - **Name:** e.g., `watsonx-api-client`
   - **Description:** e.g., `Service ID for WatsonX API access`
6. Click **Create**

### Step 4: Create an API Key for the Service ID

1. In the Service ID details page, go to the **API keys** section
2. Click **Create** (or **Create IBM Cloud API key**)
3. A new API key will be generated and displayed
4. **Important:** Copy and save this API key immediately—you won't be able to see it again
   - Save it in a secure location (e.g., password manager, secure file)
   - Example format: `_efb3vMvplN3ngN9U_pkqFmCggzibgBMHRfD0gZQy5G8f`

### Step 5: Add the Service ID to Your WatsonX Project (Grant Permissions)

1. Go back to your **WatsonX project** in the console
2. Navigate to **Access control** or **Manage access**
3. Click **Add collaborator** or **Assign role**
4. Search for the Service ID you created in Step 3
5. Select it and assign a role (typically **Editor** or **Contributor**)
6. Click **Save** or **Invite**

This grants the Service ID permission to access your WatsonX project.

### Step 6: Generate an Access Token Using the Service ID's API Key

The WatsonX REST API requires an **access token** (not the API key directly). Use your Service ID's API key to exchange for a temporary access token from IBM's IAM endpoint.

**Using cURL:**
```bash
curl -X POST "https://iam.cloud.ibm.com/identity/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -H "Accept: application/json" \
  -d "grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey=YOUR_API_KEY&response_type=cloud_iam"
```

Replace `YOUR_API_KEY` with your Service ID's API key from Step 4.

**Response example:**
```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_in": 3600,
  "token_type": "Bearer"
}
```

- **`access_token`**: Use this in your API requests
- **`expires_in`**: Token validity (3600 seconds = 1 hour)

**Using Python (requests library):**
```python
import requests

api_key = "YOUR_API_KEY"
iam_url = "https://iam.cloud.ibm.com/identity/token"

response = requests.post(
    iam_url,
    headers={
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
    },
    data={
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": api_key,
        "response_type": "cloud_iam",
    },
)

token_data = response.json()
access_token = token_data["access_token"]
print(f"Access Token: {access_token}")
```

### Step 7: Use the Access Token and Project ID in API Calls

Now you have everything needed to call the WatsonX REST API:

- **Access Token:** From Step 6
- **Project ID:** From Step 2

**Example API call to WatsonX Chat Endpoint:**
```bash
curl -X POST "https://us-south.ml.cloud.ibm.com/ml/v1/text/chat?version=2023-05-29" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model_id": "ibm/granite-4-h-small",
    "project_id": "YOUR_PROJECT_ID",
    "messages": [
      {
        "role": "user",
        "content": "What is artificial intelligence?"
      }
    ],
    "max_tokens": 2000
  }'
```

**Python example:**
```python
import requests

access_token = "YOUR_ACCESS_TOKEN"
project_id = "YOUR_PROJECT_ID"

url = "https://us-south.ml.cloud.ibm.com/ml/v1/text/chat?version=2023-05-29"

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json",
}

payload = {
    "model_id": "ibm/granite-4-h-small",
    "project_id": project_id,
    "messages": [
        {
            "role": "user",
            "content": "What is artificial intelligence?"
        }
    ],
    "max_tokens": 2000,
}

response = requests.post(url, headers=headers, json=payload)
print(response.json())
```

## Summary

| Item | Where to Use |
|------|-------------|
| **API Key** | Exchange for access token via IAM endpoint |
| **Access Token** | Use in `Authorization: Bearer` header for API calls |
| **Project ID** | Include in request payload for WatsonX API calls |
| **Model ID** | Specify which model to use (e.g., `ibm/granite-4-h-small`) |

## Important Notes

- **Token Expiration:** Access tokens expire after 3600 seconds (1 hour). Regenerate as needed.
- **API Key Security:** Keep your Service ID's API key secret. Don't commit it to version control.
- **Region:** Make sure your endpoint URL matches your project's region (e.g., `us-south`, `eu-gb`).
- **Rate Limits:** Check IBM's documentation for API rate limits and quotas.

## Troubleshooting

- **401 Unauthorized:** Access token is invalid or expired. Regenerate a new token.
- **403 Forbidden:** Service ID doesn't have access to the project. Verify it was added to project access controls.
- **404 Not Found:** Model ID doesn't exist. Check available models in your project.

For more information, visit the [IBM WatsonX API Documentation](https://cloud.ibm.com/apidocs/watsonx-ai).
