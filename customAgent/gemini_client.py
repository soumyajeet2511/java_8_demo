from google import genai
from config import API_KEY

# Using the Unified SDK
client = genai.Client(api_key=API_KEY)

def call_gemini(prompt):
    # From your ListModels output: ['models/gemini-2.0-flash', 'models/gemini-pro-latest', ...]
    # We will use 'gemini-2.0-flash' as it's the most modern and was clearly in your list.
    target_model = 'gemini-2.0-flash'

    try:
        response = client.models.generate_content(
            model=target_model,
            contents=prompt
        )
        if response and response.text:
            return response.text
        return "Error: Empty AI response."
    except Exception as e:
        return f"API Error: {str(e)}"
