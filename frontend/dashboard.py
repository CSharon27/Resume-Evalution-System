# frontend/dashboard.py
import streamlit as st
import requests

BASE_URL = "https://resume-evalution-system-backend.onrender.com"

st.set_page_config(
    page_title="Resume Evaluation System",
    page_icon="📑",
    layout="wide",
)

# --------------------------
# Custom Styling
# --------------------------
# Add this just after st.set_page_config(...)
st.markdown("""
    <style>
    /* General */
    .main {
        background-color: #f8fafc;
        font-family: 'Segoe UI', sans-serif;
    }
    h1, h2, h3, h4 {
        font-weight: 600 !important;
        color: #1e293b;
    }

    /* Gradient headers */
    h1 {
        background: linear-gradient(90deg, #1E3A8A, #2563EB);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.2rem !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1E3A8A, #2563EB);
        color: white;
    }
    section[data-testid="stSidebar"] .stMarkdown, 
    section[data-testid="stSidebar"] label, 
    section[data-testid="stSidebar"] div {
        color: white !important;
    }
    section[data-testid="stSidebar"] button {
        background: #2563EB !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        margin: 4px 0;
    }
    section[data-testid="stSidebar"] button:hover {
        background: #1E40AF !important;
    }

    /* Metric cards */
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 1rem;
        text-align: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.08);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.12);
    }

    /* Info box */
    .info-box {
        background: #EFF6FF;
        border-left: 5px solid #2563EB;
        padding: 12px 16px;
        border-radius: 8px;
        margin: 10px 0;
        color: #1e293b;
    }

    /* Progress bar */
    .progress-container {
        background: #e5e7eb;
        border-radius: 999px;
        overflow: hidden;
        height: 20px;
        margin: 10px 0;
    }
    .progress-bar {
        height: 20px;
        text-align: center;
        line-height: 20px;
        color: white;
        font-size: 0.8rem;
        font-weight: bold;
        border-radius: 999px;
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
# Dashboard Page
# --------------------------
if page == "🏠 Dashboard":
    st.markdown("<h1 style='color:#1E3A8A;'>📊 Dashboard Overview</h1>", unsafe_allow_html=True)

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

    st.markdown("### 📌 Recent Evaluations")
    if evaluations:
        for e in evaluations:
            st.markdown(
                f"<div class='info-box'>Resume ID: <b>{e.get('resume_id', '-')}</b> — "
                f"Score: <b style='color:#2563EB'>{e.get('relevance_score', 'N/A')}%</b></div>",
                unsafe_allow_html=True
            )
    else:
        st.info("No evaluations yet.")

# --------------------------
# Upload Resume Page
# --------------------------
elif page == "📂 Upload Resume":
    st.markdown("<h1 style='color:#1E3A8A;'>📂 Upload Resume</h1>", unsafe_allow_html=True)
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
    st.markdown("<h1 style='color:#1E3A8A;'>📋 Job Descriptions</h1>", unsafe_allow_html=True)
    try:
        jobs = requests.get(f"{BASE_URL}/job-descriptions").json().get("job_descriptions", [])
    except:
        jobs = []
    if jobs:
        for job in jobs:
            st.markdown(
                f"<div class='card'><b>{job.get('title', 'Unknown')}</b><br>{job.get('description', '')}</div>",
                unsafe_allow_html=True
            )
    else:
        st.info("No job descriptions available.")

# --------------------------
# Batch Processing Page
# --------------------------
elif page == "⚡ Batch Processing":
    st.markdown("<h1 style='color:#1E3A8A;'>⚡ Batch Processing</h1>", unsafe_allow_html=True)
    st.info("Upload multiple resumes to process in bulk.")
    batch_files = st.file_uploader("Upload multiple resumes", type=["pdf", "docx"], accept_multiple_files=True)
    if st.button("🚀 Process Batch") and batch_files:
        st.success(f"✅ {len(batch_files)} resumes queued for processing.")

# --------------------------
# Manage Data Page
# --------------------------
elif page == "📊 Manage Data":
    st.markdown("<h1 style='color:#1E3A8A;'>📊 Manage Data</h1>", unsafe_allow_html=True)
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


