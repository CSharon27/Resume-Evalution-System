import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from datetime import datetime

API_BASE_URL = "https://resume-evalution-system-backend.onrender.com"  # Replace with your API

# ------------------ Utility Functions ------------------ #
def make_api_request(endpoint, method="GET", data=None, files=None):
    url = f"{API_BASE_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "DELETE":
            response = requests.delete(url)
        elif files:
            response = requests.post(url, files=files)
        else:
            response = requests.post(url, json=data)

        if response.status_code in [200, 201]:
            return response.json()
        return None
    except Exception as e:
        st.error(f"API request failed: {e}")
        return None

def create_metric_card(title, value, icon, color):
    return f"""
    <div style="background: {color}; padding: 1rem; border-radius: 0.5rem; color: white; text-align: center;">
        <div style="font-size: 1.5rem;">{icon}</div>
        <div style="font-size: 1.2rem; font-weight: bold;">{value}</div>
        <div>{title}</div>
    </div>
    """

# ------------------ Pages ------------------ #
def page_dashboard():
    st.markdown("### 📊 Dashboard Overview")

    resumes = make_api_request("/resumes/") or []
    job_descriptions = make_api_request("/job-descriptions/") or []
    evaluations = make_api_request("/evaluations/") or []

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(create_metric_card("Resumes", len(resumes), "📄", "#1f77b4"), unsafe_allow_html=True)
    with col2:
        st.markdown(create_metric_card("Job Descriptions", len(job_descriptions), "💼", "#28a745"), unsafe_allow_html=True)
    with col3:
        st.markdown(create_metric_card("Evaluations", len(evaluations), "📊", "#ffc107"), unsafe_allow_html=True)
    with col4:
        valid_scores = [e.get('relevance_score') for e in evaluations if isinstance(e, dict) and 'relevance_score' in e]
        avg = f"{sum(valid_scores)/len(valid_scores):.1f}" if valid_scores else "0.0"
        st.markdown(create_metric_card("Avg Score", avg, "⭐", "#6c757d"), unsafe_allow_html=True)

    # Charts
    if evaluations:
        st.markdown("#### 📈 Evaluation Insights")
        df = pd.DataFrame(evaluations)

        col1, col2 = st.columns(2)
        with col1:
            verdict_counts = df['verdict'].value_counts()
            fig = px.pie(
                names=verdict_counts.index, values=verdict_counts.values,
                title="Verdict Distribution",
                color_discrete_map={'High': '#28a745', 'Medium': '#ffc107', 'Low': '#dc3545'}
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = px.histogram(df, x='relevance_score', nbins=20, title="Score Distribution", color_discrete_sequence=['#1f77b4'])
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No evaluations yet.")

def page_upload_resume():
    st.markdown("### 📄 Upload Resume")
    uploaded_file = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf", "docx"])
    if uploaded_file and st.button("Upload"):
        files = {"file": uploaded_file.getvalue()}
        result = make_api_request("/resumes/", method="POST", files={"file": uploaded_file})
        if result:
            st.success("✅ Resume uploaded successfully!")
        else:
            st.error("❌ Upload failed.")

def page_upload_job_description():
    st.markdown("### 💼 Upload Job Description")
    jd_text = st.text_area("Paste Job Description here:")
    if st.button("Submit JD"):
        if jd_text.strip():
            result = make_api_request("/job-descriptions/", method="POST", data={"description": jd_text})
            if result:
                st.success("✅ Job description uploaded!")
            else:
                st.error("❌ Failed to upload job description.")
        else:
            st.warning("Please enter some text.")

def page_evaluate_resume():
    st.markdown("### 🔍 Evaluate Resume")
    resumes = make_api_request("/resumes/") or []
    job_descriptions = make_api_request("/job-descriptions/") or []

    if not resumes or not job_descriptions:
        st.warning("Upload at least one resume and one job description first.")
        return

    resume = st.selectbox("Choose Resume", [r.get("id") for r in resumes])
    jd = st.selectbox("Choose Job Description", [j.get("id") for j in job_descriptions])

    if st.button("Run Evaluation"):
        result = make_api_request("/evaluate/", method="POST", data={"resume_id": resume, "jd_id": jd})
        if result:
            st.success("✅ Evaluation completed!")
            st.json(result)
        else:
            st.error("❌ Evaluation failed.")

def page_view_evaluations():
    st.markdown("### 📋 All Evaluations")
    evaluations = make_api_request("/evaluations/") or []
    if not evaluations:
        st.info("No evaluations yet.")
        return

    df = pd.DataFrame(evaluations)
    st.dataframe(df)

def page_batch_processing():
    st.markdown("### 📦 Batch Processing")
    uploaded_files = st.file_uploader("Upload multiple resumes", type=["pdf", "docx"], accept_multiple_files=True)
    if uploaded_files and st.button("Upload Batch"):
        for f in uploaded_files:
            make_api_request("/resumes/", method="POST", files={"file": f})
        st.success(f"✅ Uploaded {len(uploaded_files)} resumes.")

def page_manage_data():
    st.markdown("### 🗂️ Manage Data")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Clear Resumes"):
            make_api_request("/resumes/", method="DELETE")
            st.success("Resumes cleared.")
    with col2:
        if st.button("Clear Job Descriptions"):
            make_api_request("/job-descriptions/", method="DELETE")
            st.success("Job descriptions cleared.")
    with col3:
        if st.button("Clear Evaluations"):
            make_api_request("/evaluations/", method="DELETE")
            st.success("Evaluations cleared.")

# ------------------ Main App ------------------ #
def main():
    if 'page' not in st.session_state: 
        st.session_state.page = "Dashboard"

    st.markdown('<h1>📄 Resume Evaluation System</h1>', unsafe_allow_html=True)

    with st.sidebar:
        nav_options = {
            "🏠 Dashboard": "Dashboard",
            "📄 Upload Resume": "Upload Resume",
            "💼 Upload Job Description": "Upload Job Description",
            "🔍 Evaluate Resume": "Evaluate Resume",
            "📋 View Evaluations": "View Evaluations",
            "📦 Batch Processing": "Batch Processing",
            "🗂️ Manage Data": "Manage Data"
        }
        for display, page in nav_options.items():
            if st.button(display, key=f"nav_{page}"):
                st.session_state.page = page
                st.rerun()

    if st.session_state.page == "Dashboard":
        page_dashboard()
    elif st.session_state.page == "Upload Resume":
        page_upload_resume()
    elif st.session_state.page == "Upload Job Description":
        page_upload_job_description()
    elif st.session_state.page == "Evaluate Resume":
        page_evaluate_resume()
    elif st.session_state.page == "View Evaluations":
        page_view_evaluations()
    elif st.session_state.page == "Batch Processing":
        page_batch_processing()
    elif st.session_state.page == "Manage Data":
        page_manage_data()

if __name__ == "__main__":
    main()
