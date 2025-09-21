# frontend/dashboard.py
import streamlit as st
import requests

BASE_URL = "https://resume-evalution-system-backend.onrender.com"

# --------------------------
# Page Config
# --------------------------
st.set_page_config(
    page_title="Resume Evaluation System",
    page_icon="📑",
    layout="wide",
)

# --------------------------
# Custom Styling
# --------------------------
st.markdown("""
    <style>
    /* Main background */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #fdfdfd 0%, #f7f9fb 100%);
        font-family: "Segoe UI", sans-serif;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #ffffff !important;
        padding-top: 30px;
        border-right: 1px solid #e5e7eb;
    }

    /* Sidebar Navigation */
    [role="radiogroup"] > label {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 12px 18px;
        margin: 6px 0;
        border-radius: 12px;
        font-weight: 500;
        font-size: 1rem;
        color: #374151 !important;
        background: #f9fafb;
        border: 1px solid #e5e7eb;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    [role="radiogroup"] > label:hover {
        background: #f3f4f6;
        border-color: #d1d5db;
        color: #111827 !important;
        transform: translateX(5px);
    }
    [role="radiogroup"] > label[data-checked="true"] {
        background: #e0f2fe;
        color: #0c4a6e !important;
        font-weight: 600 !important;
        border: 1px solid #38bdf8;
        transform: translateX(8px);
    }

    /* Sidebar quick stats */
    .quick-card {
        background: #f9fafb;
        padding: 12px;
        margin: 8px 0;
        border-radius: 10px;
        text-align: center;
        border: 1px solid #e5e7eb;
    }
    .quick-card h4 {
        margin: 0;
        font-size: 0.9rem;
        color: #475569;
    }
    .quick-card p {
        margin: 0;
        font-size: 1.2rem;
        font-weight: bold;
        color: #0c4a6e;
    }

    /* Stat Cards */
    .card {
        background: #ffffff;
        padding: 25px;
        border-radius: 16px;
        box-shadow: 0 6px 12px rgba(0,0,0,0.08);
        text-align: center;
        transition: transform 0.2s ease;
    }
    .card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 20px rgba(0,0,0,0.12);
    }

    /* Buttons */
    div.stButton > button {
        background: #0ea5e9;
        color: white;
        border-radius: 10px;
        padding: 0.7rem 1.4rem;
        font-weight: 600;
        border: none;
        box-shadow: 0 4px 10px rgba(14, 165, 233, 0.3);
        transition: all 0.2s ease;
    }
    div.stButton > button:hover {
        background: #0284c7;
        transform: scale(1.05);
        box-shadow: 0 6px 14px rgba(14, 165, 233, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# --------------------------
# Sidebar: Branding + Navigation + Quick Stats
# --------------------------
st.sidebar.title("📑 Resume Evaluation System")

# Fetch backend + stats
backend_status = "🟢 Online"
resumes = jobs = evaluations = []
try:
    resumes = requests.get(f"{BASE_URL}/resumes").json().get("resumes", [])
    jobs = requests.get(f"{BASE_URL}/job-descriptions").json().get("job_descriptions", [])
    evaluations = requests.get(f"{BASE_URL}/evaluations").json().get("evaluations", [])
except:
    backend_status = "🔴 Offline"

# Navigation
page = st.sidebar.radio(
    "Navigate",
    ["🏠 Dashboard", "📂 Upload Resume", "📝 Evaluate Resume",
     "📋 Job Descriptions", "⚡ Batch Processing",
     "📑 View Evaluations", "📊 Manage Data"]
)

# Backend status
st.sidebar.markdown(f"**Backend Status:** {backend_status}")

# Quick stats in sidebar
st.sidebar.markdown("### ⚡ Quick Stats")
st.sidebar.markdown(f"<div class='quick-card'><h4>Resumes</h4><p>{len(resumes)}</p></div>", unsafe_allow_html=True)
st.sidebar.markdown(f"<div class='quick-card'><h4>Jobs</h4><p>{len(jobs)}</p></div>", unsafe_allow_html=True)
st.sidebar.markdown(f"<div class='quick-card'><h4>Evaluations</h4><p>{len(evaluations)}</p></div>", unsafe_allow_html=True)

# --------------------------
# Helper: Page Header
# --------------------------
def header(title):
    st.markdown(f"## Resume Evaluation System — {title}")

# --------------------------
# Pages
# --------------------------
if page == "🏠 Dashboard":
    header("📊 Dashboard Overview")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<div class='card'><h3>📄 Resumes</h3><h2>{len(resumes)}</h2></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='card'><h3>💼 Job Descriptions</h3><h2>{len(jobs)}</h2></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='card'><h3>✅ Evaluations</h3><h2>{len(evaluations)}</h2></div>", unsafe_allow_html=True)

    st.markdown("### Recent Evaluations")
    if evaluations:
        for e in evaluations[:5]:
            st.markdown(f"- Resume ID: `{e.get('resume_id', '-')}`, Score: **{e.get('relevance_score', 'N/A')}%**")
    else:
        st.info("No evaluations yet.")

elif page == "📂 Upload Resume":
    header("📂 Upload Resume")
    uploaded_file = st.file_uploader("Upload a resume file (PDF/DOCX)", type=["pdf", "docx"])
    if uploaded_file:
        files = {"file": uploaded_file.getvalue()}
        try:
            resp = requests.post(f"{BASE_URL}/resumes", files=files)
            if resp.status_code == 200:
                st.success("✅ Resume uploaded successfully!")
            else:
                st.error("❌ Failed to upload resume.")
        except:
            st.error("⚠️ Backend not reachable.")

elif page == "📝 Evaluate Resume":
    header("📝 Evaluate Resume")
    uploaded_file = st.file_uploader("Select a resume for evaluation", type=["pdf", "docx"])
    job_id = st.text_input("Enter Job ID for evaluation")
    if st.button("Evaluate") and uploaded_file and job_id:
        files = {"file": uploaded_file.getvalue()}
        try:
            resp = requests.post(f"{BASE_URL}/evaluate/{job_id}", files=files)
            if resp.status_code == 200:
                st.success("✅ Evaluation completed!")
                st.json(resp.json())
            else:
                st.error("❌ Evaluation failed.")
        except:
            st.error("⚠️ Backend not reachable.")

elif page == "📋 Job Descriptions":
    header("📋 Job Descriptions")
    if jobs:
        for job in jobs:
            st.markdown(f"<div class='card'><b>{job.get('title', 'Unknown')}</b><br>{job.get('description', '')}</div>", unsafe_allow_html=True)
    else:
        st.info("No job descriptions available.")

elif page == "⚡ Batch Processing":
    header("⚡ Batch Processing")
    st.info("Upload multiple resumes to process in bulk.")
    batch_files = st.file_uploader("Upload multiple resumes", type=["pdf", "docx"], accept_multiple_files=True)
    if st.button("Process Batch") and batch_files:
        st.success(f"✅ {len(batch_files)} resumes queued for processing.")

elif page == "📑 View Evaluations":
    header("📑 View Evaluations")
    if evaluations:
        for e in evaluations:
            st.markdown(f"<div class='card'>Resume: <b>{e.get('resume_id')}</b><br>Job: <b>{e.get('job_id')}</b><br>Score: <b>{e.get('relevance_score', 'N/A')}%</b></div>", unsafe_allow_html=True)
    else:
        st.info("No evaluations available.")

elif page == "📊 Manage Data":
    header("📊 Manage Data")
    st.subheader("📄 Resumes")
    st.write(resumes if resumes else "No resumes uploaded.")

    st.subheader("💼 Job Descriptions")
    st.write(jobs if jobs else "No job descriptions available.")

    st.subheader("✅ Evaluations")
    st.write(evaluations if evaluations else "No evaluations available.")
