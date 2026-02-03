import json
import os

PROFILE_FILE = "user_profile.json"

def load_profile():
    """Loads the user profile from the JSON file or returns a default template."""
    if os.path.exists(PROFILE_FILE):
        try:
            with open(PROFILE_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            pass # Return default if file is corrupted
            
    return {
        "personal_info": {
            "name": "",
            "email": "",
            "phone": "",
            "linkedin": "",
            "github": "",
            "location": ""
        },
        "work_history": [],
        "education": [],
        "skills_certs": ""
    }

def save_profile(data):
    """Saves the user profile data to the JSON file."""
    try:
        with open(PROFILE_FILE, "w") as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving profile: {e}")
        return False

def profile_to_markdown(profile):
    """Converts the structured profile dictionary to a Markdown resume string."""
    md = ""
    
    # Personal Info
    p = profile.get("personal_info", {})
    md += f"# {p.get('name', 'Your Name')}\n\n"
    
    contact_parts = []
    if p.get("location"): contact_parts.append(p["location"])
    if p.get("phone"): contact_parts.append(p["phone"])
    if p.get("email"): contact_parts.append(p["email"])
    if p.get("linkedin"): contact_parts.append(f"[LinkedIn]({p['linkedin']})")
    if p.get("github"): contact_parts.append(f"[GitHub]({p['github']})")
    
    md += " | ".join(contact_parts) + "\n\n"
    
    # Work History
    md += "## Experience\n\n"
    for job in profile.get("work_history", []):
        md += f"### {job.get('role', 'Role')} at {job.get('company', 'Company')}\n"
        md += f"**{job.get('start_date', '')} - {job.get('end_date', 'Present')}**\n\n"
        md += f"{job.get('description', '')}\n\n"
        
    # Education
    md += "## Education\n\n"
    for edu in profile.get("education", []):
        md += f"### {edu.get('degree', 'Degree')}\n"
        md += f"**{edu.get('institution', 'Institution')}** | {edu.get('year', '')}\n\n"

    # Skills & Certs
    if profile.get("skills_certs"):
        md += "## Skills & Certifications\n\n"
        md += f"{profile['skills_certs']}\n"
        
    return md
