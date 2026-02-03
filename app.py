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

def main():
    st.title("📄 AI Resume Matcher")
    st.markdown("### Tailor your CV to any job description instantly.")
    st.markdown("---")

    # Sidebar
    with st.sidebar:
        st.header("Configuration")
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            api_key = st.text_input("Enter Gemini API Key", type="password", help="Get your key from Google AI Studio")
            if not api_key:
                st.warning("⚠️ API Key is required to proceed.")
        
        st.markdown("---")
        st.markdown("### How it works")
        st.info("1. Upload your Resume (Markdown format)\n2. Paste the Job Description\n3. Click 'Tailor Resume'\n4. Download your new custom CV!")
        st.markdown("---")
        st.caption("Powered by Google Gemini 3 Flash")

    # Main Content
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Job Description")
        job_description = st.text_area("Paste the job description here...", height=400, placeholder="e.g. We are looking for a Senior Python Developer...")

    with col2:
        st.subheader("Your Resume")
        uploaded_file = st.file_uploader("Upload your CV (Markdown)", type=["md"])
        resume_content = ""
        if uploaded_file is not None:
            resume_content = uploaded_file.read().decode("utf-8")
            st.success(f"Loaded: {uploaded_file.name}")
            with st.expander("Preview Original Resume"):
                st.markdown(resume_content)

    # Action
    if st.button("✨ Tailor Resume"):
        if not job_description:
            st.error("Please provide a Job Description.")
        elif not resume_content:
            st.error("Please upload your Resume.")
        elif not api_key:
             st.error("Please provide an API Key.")
        else:
            with st.spinner("Analyzing and rewriting... This may take a moment."):
                tailored_resume = process_resume(resume_content, job_description, api_key)
                
                if tailored_resume.startswith("Error"):
                    st.error(tailored_resume)
                else:
                    st.success("Resume tailored successfully!")
                    
                    # Results Tabs
                    tab1, tab2 = st.tabs(["Preview", "Raw Markdown"])
                    
                    with tab1:
                        st.markdown(tailored_resume)
                    
                    with tab2:
                        st.code(tailored_resume, language='markdown')
                    
                    # Download Button
                    st.download_button(
                        label="⬇️ Download Tailored Resume",
                        data=tailored_resume,
                        file_name="tailored_resume.md",
                        mime="text/markdown"
                    )

if __name__ == "__main__":
    main()
