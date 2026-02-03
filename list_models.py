import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY"))

with open("models_output.txt", "w") as f:
    f.write("Listing available models:\n")
    try:
        for m in client.models.list():
            # In the new SDK, supported_methods is a list of strings
            f.write(f"{m.name}\n")
    except Exception as e:
        f.write(f"Error: {e}\n")
