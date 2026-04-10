import requests
import json
from config import API_KEY

# HCL AI Cafe Endpoint for GPT-4 (Deployment version: 2024-12-01-preview)
API_URL = "https://aicafe.hcl.com/AICafeService/api/v1/subscription/openai/deployments/gpt-4.1/chat/completions?api-version=2024-12-01-preview"

def call_ai_cafe(user_prompt):
    """
    Communicates with the HCL AI Cafe Gateway (GPT-4) to process migration tasks.
    The model is instructed as a Java migration expert to return structured JSON.
    """
    # Define request headers including the API key
    headers = {
        "Content-Type": "application/json",
        "api-key": API_KEY
    }

    # Define the request payload. System message establishes the context.
    # We use a low temperature for more consistent and deterministic responses.
    payload_data = {
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are an expert in migrating Java 8 applications to Java 11. "
                    "Your primary goal is to provide code updates that are safe, "
                    "minimal, and follow modern Java practices. Always respond "
                    "using the requested JSON schema for easy programmatic parsing."
                )
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        "temperature": 0.1,
        "max_tokens": 4000 # Enough tokens to accommodate full pom.xml files
    }

    try:
        # Perform the POST request to the AI gateway
        print("Calling AI Gateway for analysis and proposed changes...")
        api_response = requests.post(
            API_URL,
            headers=headers,
            data=json.dumps(payload_data),
            timeout=120 # Add a timeout for robustness
        )

        if api_response.status_code == 200:
            # Parse the successful JSON response
            response_json = api_response.json()
            # Extract and return the model's message content
            return response_json['choices'][0]['message']['content']
        else:
            return f"API Connection Error: HTTP Status {api_response.status_code} - {api_response.text}"

    except requests.exceptions.RequestException as req_err:
        return f"Network Exception: {str(req_err)}"
    except Exception as general_err:
        return f"Unexpected Error: {str(general_err)}"
