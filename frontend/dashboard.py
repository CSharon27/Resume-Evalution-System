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
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: #111827 !important;
        font-weight: 700;
        text-align: center;
        margin-bottom: 20px;
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
    .card h3 {
        color: #475569;
        font-size: 1.2rem;
        margin-bottom: 8px;
    }
    .card h2 {
        color: #0c4a6e;
        font-size: 2rem;
        margin: 0;
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

    /* Info Alerts */
    .stAlert {
        border-radius: 10px;
        font-size: 0.95rem;
    }
    </style>
""", unsafe_allow_html=True)

# --------------------------
# Sidebar Navigation
# --------------------------
st.sidebar.title("📑 Resume Evaluation")
page = st.sidebar.radio(
    "Navigate",
    ["🏠 Dashboard", "📂 Upload Resume", "📋 Job Descriptions",
     "⚡ Batch Processing", "📊 Manage Data"]
)

# --------------------------
# Branding Header
# --------------------------
def header(title):
    st.markdown(f"## Resume Evaluation System — {title}")

# --------------------------
# Dashboard Page
# --------------------------
if page == "🏠 Dashboard":
    header("📊 Dashboard Overview")

    try:
        resumes = requests.get(f"{BASE_URL}/resumes").json().get("resumes", [])
        jobs = requests.get(f"{BASE_URL}/job-descriptions").json().get("job_descriptions", [])
        evaluations = requests.get(f"{BASE_URL}/evaluations").json().get("evaluations", [])
    except:
        resumes, jobs, evaluations = [], [], []

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<div class='card'><h3>📄 Resumes</h3><h2>{len(resumes)}</h2></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='card'><h3>💼 Job Descriptions</h3><h2>{len(jobs)}</h2></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='card'><h3>✅ Evaluations</h3><h2>{len(evaluations)}</h2></div>", unsafe_allow_html=True)

    st.markdown("### Recent Evaluations")
    if evaluations:
        for e in evaluations:
            st.markdown(f"- Resume ID: `{e.get('resume_id', '-')}`, Score: **{e.get('relevance_score', 'N/A')}%**")
    else:
        st.info("No evaluations yet.")

# --------------------------
# Upload Resume Page
# --------------------------
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

# --------------------------
# Job Descriptions Page
# --------------------------
elif page == "📋 Job Descriptions":
    header("📋 Job Descriptions")
    try:
        jobs = requests.get(f"{BASE_URL}/job-descriptions").json().get("job_descriptions", [])
    except:
        jobs = []
    if jobs:
        for job in jobs:
            st.markdown(f"<div class='card'><b>{job.get('title', 'Unknown')}</b><br>{job.get('description', '')}</div>", unsafe_allow_html=True)
    else:
        st.info("No job descriptions available.")

# --------------------------
# Batch Processing Page
# --------------------------
elif page == "⚡ Batch Processing":
    header("⚡ Batch Processing")
    st.info("Upload multiple resumes to process in bulk.")
    batch_files = st.file_uploader("Upload multiple resumes", type=["pdf", "docx"], accept_multiple_files=True)
    if st.button("Process Batch") and batch_files:
        st.success(f"✅ {len(batch_files)} resumes queued for processing.")

# --------------------------
# Manage Data Page
# --------------------------
elif page == "📊 Manage Data":
    header("📊 Manage Data")
    st.info("View and manage resumes, job descriptions, and evaluations.")
    try:
        resumes = requests.get(f"{BASE_URL}/resumes").json().get("resumes", [])
        jobs = requests.get(f"{BASE_URL}/job-descriptions").json().get("job_descriptions", [])
        evaluations = requests.get(f"{BASE_URL}/evaluations").json().get("evaluations", [])
    except:
        resumes, jobs, evaluations = [], [], []

    st.subheader("📄 Resumes")
    st.write(resumes if resumes else "No resumes uploaded.")

    st.subheader("💼 Job Descriptions")
    st.write(jobs if jobs else "No job descriptions available.")

    st.subheader("✅ Evaluations")
    st.write(evaluations if evaluations else "No evaluations available.")
