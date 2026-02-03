from llm_engine import tailor_resume, configure_gemini

def process_resume(resume_content: str, job_description: str, api_key: str = None) -> str:
    """
    Orchestrates the resume tailoring process.
    
    Args:
        resume_content (str): The raw string content of the resume (Markdown).
        job_description (str): The job description text.
        api_key (str, optional): API key if provided by user input.
        
    Returns:
        str: The tailored resume content.
    """
    # Configure API
    try:
        configure_gemini(api_key)
    except ValueError as e:
        return f"Error: {str(e)}"

    # Clean inputs if necessary (basic stripping)
    resume_content = resume_content.strip()
    job_description = job_description.strip()

    if not resume_content:
        return "Error: Resume content is empty."
    if not job_description:
        return "Error: Job description is empty."

    # Call LLM
    try:
        tailored_content = tailor_resume(resume_content, job_description)
        # Attempt to clean up if the model wrapped it in markdown code blocks
        if tailored_content.startswith("```markdown"):
            tailored_content = tailored_content[11:]
        if tailored_content.startswith("```"):
            tailored_content = tailored_content[3:]
        if tailored_content.endswith("```"):
            tailored_content = tailored_content[:-3]
            
        return tailored_content.strip()
    except Exception as e:
        return f"Error processing resume: {str(e)}"
