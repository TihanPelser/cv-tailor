import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel('gemini-3-flash-preview')

with open("test_output.txt", "w") as f:
    try:
        response = model.generate_content("Hello! Are you Gemini 3 Flash?")
        f.write(f"Response: {response.text}\n")
    except Exception as e:
        f.write(f"Error: {e}\n")
