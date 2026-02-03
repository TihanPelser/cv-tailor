import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY"))

with open("test_output.txt", "w") as f:
    try:
        response = client.models.generate_content(
            model='gemini-3-flash-preview',
            contents="Hello! Are you Gemini 3 Flash?"
        )
        f.write(f"Response: {response.text}\n")
    except Exception as e:
        f.write(f"Error: {e}\n")
