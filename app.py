import streamlit as st
import os
from dotenv import load_dotenv
from processor import process_resume

# Load environment variables
load_dotenv()

# Page Configuration
st.set_page_config(
    page_title="AI Resume Matcher",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a "premium" feel
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #4CAF50;
        color: white;
    }
    .stTextArea textarea {
        background-color: #ffffff;
        color: #333333;
    }
</style>
""", unsafe_allow_html=True)


import streamlit as st
import os
from dotenv import load_dotenv
from processor import process_resume
import profile_manager

# Load environment variables
load_dotenv()

# Page Configuration
st.set_page_config(
    page_title="AI Resume Matcher",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #4CAF50; color: white; }
    .stTextArea textarea { background-color: #ffffff; color: #333333; }
</style>
""", unsafe_allow_html=True)

def main():
    st.title("📄 AI Resume Matcher")
    
    # Sidebar Navigation
    with st.sidebar:
        st.header("Configuration")
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            api_key = st.text_input("Enter Gemini API Key", type="password", help="Get your key from Google AI Studio")
            if not api_key: st.warning("⚠️ API Key is required.")
        
        st.markdown("---")
        mode = st.radio("Mode", ["Tailor CV", "Profile Builder"])
        
        st.markdown("---")
        st.caption("Powered by Google Gemini 3 Flash")

    if mode == "Profile Builder":
        render_profile_builder()
    else:
        render_tailor_cv(api_key)

def render_profile_builder():
    st.header("👤 Profile Builder")
    st.markdown("Build your master profile here. This data will be saved locally.")
    
    profile = profile_manager.load_profile()
    
    with st.form("profile_form"):
        st.subheader("Personal Details")
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name", value=profile['personal_info'].get('name', ''))
            email = st.text_input("Email", value=profile['personal_info'].get('email', ''))
            phone = st.text_input("Phone", value=profile['personal_info'].get('phone', ''))
        with col2:
            location = st.text_input("Location", value=profile['personal_info'].get('location', ''))
            linkedin = st.text_input("LinkedIn URL", value=profile['personal_info'].get('linkedin', ''))
            github = st.text_input("GitHub URL", value=profile['personal_info'].get('github', ''))
            
        st.markdown("---")
        st.subheader("Experience")
        
        # Simple text area for now to allow bulk entry, parsing complex lists in Streamlit forms is tricky without session state acrobatics
        # For a v1, we will trust the user to format this or provide structured slots.
        # Let's try 3 slots for now, scalable later.
        
        work_history = profile.get('work_history', [])
        # Ensure we have at least 3 slots to show
        while len(work_history) < 3:
            work_history.append({})
            
        for i, work in enumerate(work_history):
            with st.expander(f"Job {i+1}", expanded=False):
                work['company'] = st.text_input(f"Company {i+1}", value=work.get('company', ''))
                work['role'] = st.text_input(f"Role {i+1}", value=work.get('role', ''))
                c1, c2 = st.columns(2)
                work['start_date'] = c1.text_input(f"Start Date {i+1}", value=work.get('start_date', ''))
                work['end_date'] = c2.text_input(f"End Date {i+1}", value=work.get('end_date', ''))
                work['description'] = st.text_area(f"Description {i+1}", value=work.get('description', ''), height=100)

        st.markdown("---")
        st.subheader("Education")
        education = profile.get('education', [])
        while len(education) < 2:
            education.append({})
            
        for i, edu in enumerate(education):
            with st.expander(f"Education {i+1}", expanded=False):
                edu['institution'] = st.text_input(f"Institution {i+1}", value=edu.get('institution', ''))
                edu['degree'] = st.text_input(f"Degree {i+1}", value=edu.get('degree', ''))
                edu['year'] = st.text_input(f"Year {i+1}", value=edu.get('year', ''))

        st.markdown("---")
        st.subheader("Skills & Certifications")
        skills_certs = st.text_area("List your skills and certifications here", value=profile.get('skills_certs', ''), height=150)
        
        if st.form_submit_button("Save Profile"):
            # Reconstruct profile object
            new_profile = {
                "personal_info": {
                    "name": name, "email": email, "phone": phone,
                    "location": location, "linkedin": linkedin, "github": github
                },
                # Filter out empty entries
                "work_history": [w for w in work_history if w.get('company')],
                "education": [e for e in education if e.get('institution')],
                "skills_certs": skills_certs
            }
            if profile_manager.save_profile(new_profile):
                st.success("Profile saved successfully!")
            else:
                st.error("Failed to save profile.")

def render_tailor_cv(api_key):
    st.subheader("Tailor your CV")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("Job Description")
        job_description = st.text_area("Paste the job description here...", height=400)
        
    with col2:
        st.info("Your Resume Source")
        source_option = st.radio("Source", ["Upload File", "Use Saved Profile"])
        
        resume_content = ""
        
        if source_option == "Upload File":
            uploaded_file = st.file_uploader("Upload your CV (Markdown)", type=["md"])
            if uploaded_file:
                resume_content = uploaded_file.read().decode("utf-8")
                st.success(f"Loaded: {uploaded_file.name}")
        else:
            if st.button("Load from Profile"):
                prof = profile_manager.load_profile()
                resume_content = profile_manager.profile_to_markdown(prof)
                st.success("Profile loaded!")
                with st.expander("View Generated Resume"):
                    st.markdown(resume_content)
            else:
                # Attempt silent load if available to keep state
                prof = profile_manager.load_profile()
                resume_content = profile_manager.profile_to_markdown(prof)

    st.markdown("---")
    if st.button("✨ Tailor Resume"):
        if not job_description:
            st.error("Please provide a Job Description.")
        elif not resume_content:
            st.error("Please provide your Resume (Upload or Load Profile).")
        elif not api_key:
             st.error("Please provide an API Key.")
        else:
            with st.spinner("Analyzing and rewriting..."):
                tailored_resume = process_resume(resume_content, job_description, api_key)
                if tailored_resume.startswith("Error"):
                    st.error(tailored_resume)
                else:
                    st.success("Success!")
                    tab1, tab2 = st.tabs(["Preview", "Raw Markdown"])
                    with tab1: st.markdown(tailored_resume)
                    with tab2: st.code(tailored_resume, language='markdown')
                    st.download_button("⬇️ Download", tailored_resume, "tailored_resume.md", "text/markdown")

if __name__ == "__main__":
    main()
