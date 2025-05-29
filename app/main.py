import streamlit as st
import pandas as pd
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio
from utils import clean_text

# ✨ Streamlit Theme Setup
st.set_page_config(
    layout="wide",
    page_title="Cold Email Generator",
    page_icon="📬"
)

st.markdown("<h1 style='text-align: center; color: #4CAF50;'>💼 AI-Powered Cold Email Generator</h1>", unsafe_allow_html=True)
st.markdown("### 🚀 Reach Out With Confidence", unsafe_allow_html=True)
st.markdown("upload your portfolio csv following the example format , you details and the url of the job vacancy", unsafe_allow_html=True)
# Sidebar
with st.sidebar:
    st.header("🛠️ Setup")
    uploaded_file = st.file_uploader("📁 Upload Portfolio CSV", type="csv")
    with st.expander("📄 Portfolio CSV Format Guide"):
        st.markdown("""
        Your CSV should contain:
        - `Techstack`: A short description of the technologies or skills used.
        - `Links`: URL to your project (GitHub, portfolio, etc.)

        **Example:**
        ```
        Techstack,Links  
        React, Tailwind, Firebase,https://github.com/example/react-firebase-app  
        Python, FastAPI, PostgreSQL,https://github.com/example/api-project
        ```
        """)
    user_name = st.text_input("👤 Your Name")
    user_role = st.text_input("💼 Your Role")
    user_company = st.text_input("🏢 Previous Company or Experience")
    user_pitch = st.text_area("📝 A short personal summary or motivation")
    url_input = st.text_input("🌐 Job URL", value="")
    submit_button = st.button("🎯 Generate Email")
st.markdown("---")


# Main Content
col1, col2 = st.columns([1, 2])

if submit_button:
    if uploaded_file and user_name:
        with st.spinner("🔍 Scraping and analyzing job details..."):
            try:
                loader = WebBaseLoader([url_input])
                data = clean_text(loader.load().pop().page_content)
                portfolio = Portfolio(file_path=uploaded_file)
                portfolio.load_portfolio()
                chain = Chain()
                jobs = chain.extract_jobs(data)

                for i, job in enumerate(jobs):
                    st.markdown(f"### 📄 Job #{i+1}")
                    st.json(job)
                    skills = job.get('skills', [])
                    links = portfolio.query_links(skills)

                    st.markdown("#### ✨ Suggested Email:")
                    email = chain.write_mail(job, links, user_name, user_role, user_company, user_pitch)

                    st.code(email, language='markdown')
                    st.success("✅ Email generated!")

            except Exception as e:
                st.error(f"⚠️ Error: {e}")
    else:
        st.warning("⚠️ Please upload a CSV and enter your name.")

# Footer

st.markdown("---")
st.markdown("""
<center>
Made by <strong>Shashank</strong>  
<a href="www.linkedin.com/in/shashank-yadav-a75a54302" target="_blank">🔗 LinkedIn</a> |
<a href="https://github.com/iamshashankyadav" target="_blank">💻 GitHub</a>
</center>
""", unsafe_allow_html=True)
