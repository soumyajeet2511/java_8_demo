import requests
import json
from config import API_KEY

# Updated HCL AI Cafe Endpoint based on provided documentation
API_URL = "https://aicafe.hcl.com/AICafeService/api/v1/subscription/openai/deployments/gpt-4.1/chat/completions?api-version=2024-12-01-preview"

def call_ai_cafe(prompt):
    headers = {
        "Content-Type": "application/json",
        "api-key": API_KEY
    }

    # Payload for Azure OpenAI style (which HCL AI Cafe likely uses)
    payload = {
        "messages": [
            {
                "role": "system",
                "content": "You are a Java 8 to 11 migration expert. Always return changes in a structured JSON block."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.1,
        "max_tokens": 4000 # Increased max_tokens to allow for full pom.xml responses
    }

    try:
        print(f"DEBUG: Calling HCL AI Cafe (GPT-4.1) Gateway...")
        response = requests.post(API_URL, headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            result = response.json()
            # Azure OpenAI / HCL response structure
            return result['choices'][0]['message']['content']
        else:
            return f"API Error: {response.status_code} - {response.text}"

    except Exception as e:
        return f"Connection Error: {str(e)}"
