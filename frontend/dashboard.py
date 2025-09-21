import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from datetime import datetime

API_BASE_URL = "https://resume-evalution-system-backend.onrender.com"

# ------------------ Utility Functions ------------------ #
def make_api_request(endpoint, method="GET", data=None, files=None):
    url = f"{API_BASE_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "DELETE":
            response = requests.delete(url)
        else:  # POST
            if files:
                response = requests.post(url, files=files)
            else:
                response = requests.post(url, json=data)
        if response.status_code in [200, 201]:
            return response.json()
        return None
    except Exception as e:
        return None

def check_api_status():
    try:
        resp = requests.get(f"{API_BASE_URL}/")
        if resp.status_code == 200:
            return True, resp.json().get("message", "OK")
        else:
            return False, f"Error {resp.status_code}"
    except:
        return False, "Not reachable"

# ------------------ Main App ------------------ #
def main():
    if 'page' not in st.session_state:
        st.session_state.page = "Dashboard"

    st.markdown('<h1>📄 Resume Evaluation System</h1>', unsafe_allow_html=True)

    # ------------------ Sidebar ------------------ #
    with st.sidebar:
        nav_options = {
            "🏠 Dashboard": "Dashboard",
            "📄 Upload Resume": "Upload Resume",
            "💼 Job Descriptions": "Job Descriptions",
            "🔍 Evaluate Resume": "Evaluate Resume",
            "📋 View Evaluations": "View Evaluations",
            "📦 Batch Processing": "Batch Processing",
            "🗂️ Manage Data": "Manage Data"
        }
        for display, page in nav_options.items():
            if st.button(display, key=f"nav_{page}"):
                st.session_state.page = page
                st.rerun()

        # Sidebar Quick Stats
        st.markdown("### 📊 Quick Stats")
        resumes = make_api_request("/resumes/") or []
        job_descriptions = make_api_request("/job-descriptions/") or []
        evaluations = make_api_request("/evaluations/") or []

        st.metric("Resumes", len(resumes))
        st.metric("Job Descriptions", len(job_descriptions))
        st.metric("Evaluations", len(evaluations))
        if evaluations:
            avg_score = sum(e.get('relevance_score', 0) for e in evaluations) / len(evaluations)
            st.metric("Avg Score", f"{avg_score:.1f}")

        # API Status
        status, msg = check_api_status()
        if status:
            st.success(f"API Status: ✅ {msg}")
        else:
            st.error(f"API Status: ❌ {msg}")

    # ------------------ Page Logic ------------------ #
    page = st.session_state.page

    if page == "Dashboard":
        st.markdown("### 📊 Dashboard Overview")
        st.info("Welcome to the Resume Evaluation System! Navigate from the sidebar to start.")

    elif page == "Upload Resume":
        st.title("📄 Upload Resume")
        uploaded = st.file_uploader("Upload a Resume", type=["pdf", "docx"])
        if uploaded:
            files = {"file": uploaded.getvalue()}
            resp = make_api_request("/resumes/", method="POST", files=files)
            if resp:
                st.success(f"Uploaded {uploaded.name}")
            else:
                st.error("Upload failed!")

        st.markdown("### Existing Resumes")
        resumes = make_api_request("/resumes/") or []
        for r in resumes:
            st.write(f"- {r}")

    elif page == "Job Descriptions":
        st.title("💼 Manage Job Descriptions")

        st.markdown("#### 1️⃣ Upload JD Document")
        jd_file = st.file_uploader("Upload JD (PDF/DOCX)", type=["pdf", "docx"])
        if jd_file:
            files = {"file": jd_file.getvalue()}
            resp = make_api_request("/job-descriptions/", method="POST", files=files)
            if resp:
                st.success(f"Uploaded {jd_file.name}")
            else:
                st.error("Upload failed!")

        st.markdown("#### 2️⃣ Enter Job Description Manually")
        jd_text = st.text_area("Enter Job Description")
        if st.button("Save Job Description"):
            if jd_text.strip():
                resp = make_api_request("/job-descriptions/", method="POST", data={"jd": jd_text})
                if resp:
                    st.success("Job description saved!")
                else:
                    st.error("Failed to save job description.")
            else:
                st.warning("Please enter some text before saving.")

        st.markdown("### Existing Job Descriptions")
        jobs = make_api_request("/job-descriptions/") or []
        for j in jobs:
            st.write(f"- {j}")

    elif page == "Evaluate Resume":
        st.title("🔍 Evaluate Resume")
        st.info("Evaluation logic goes here.")

    elif page == "View Evaluations":
        st.title("📋 View Evaluations")
        evaluations = make_api_request("/evaluations/") or []
        if evaluations:
            for e in evaluations:
                st.json(e)
        else:
            st.info("No evaluations yet.")

    elif page == "Batch Processing":
        st.title("📦 Batch Processing")
        st.info("Batch processing logic goes here.")

    elif page == "Manage Data":
        st.title("🗂️ Manage Data")
        st.info("Data management logic goes here.")


if __name__ == "__main__":
    main()
