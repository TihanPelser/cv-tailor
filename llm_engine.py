import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

# Global client variable to be initialized
_client = None

def get_client(api_key=None):
    """Returns a GenAI client, initializing it if necessary."""
    global _client
    if _client is None or api_key:
        key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not key:
            raise ValueError("API Key not found. Please set GEMINI_API_KEY or GOOGLE_API_KEY in .env or provide it directly.")
        _client = genai.Client(api_key=key)
    return _client

def configure_gemini(api_key=None):
    """Configures the Gemini API for legacy compatibility."""
    get_client(api_key)

def tailor_resume(resume_text, job_description):
    """
    Uses Gemini to tailor the resume to the job description.
    
    Args:
        resume_text (str): The content of the user's current resume in Markdown.
        job_description (str): The job description to target.
        
    Returns:
        str: The tailored resume in Markdown.
    """
    client = get_client()
    
    prompt = f"""
    You are an expert career coach and professional resume writer.
    
    Your task is to rewrite the provided resume to better align with the job description, 
    making the candidate stand out.
    
    STRICT RULES:
    1. **NO LYING**: Do not invent experiences, skills, or qualifications that are not present in the original resume.
    2. **FORMAT**: Keep the exact same structure and markdown format as the original resume. Only change the content (bullet points, summaries).
    3. **HIGHLIGHT**: emphasize relevant skills and experiences found in the resume that match the job description. Rephrase bullet points to use keywords from the job description where truthful.
    4. **BULLET POINTS**: Use concise bullet points for responsibilities and achievements instead of long paragraphs.
    5. **TONE**: Professional, punchy, and results-oriented.
    
    Job Description:
    {job_description}
    
    Original Resume (Markdown):
    {resume_text}
    
    Output the tailored resume in Markdown format. return ONLY the markdown code.
    """
    
    response = client.models.generate_content(
        model='gemini-3-flash-preview',
        contents=prompt
    )
    return response.text
