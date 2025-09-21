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
# Enhanced Styling (Glassmorphism + Gradient)
# --------------------------
st.markdown("""
    <style>
    /* Main background */
    .main {
        background: linear-gradient(135deg, #e0eafc 0%, #cfdef3 100%);
        font-family: "Segoe UI", sans-serif;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.9);
        backdrop-filter: blur(12px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    .stSidebar .stRadio label {
        color: #e2e8f0 !important;
        font-weight: 500;
        padding: 8px 12px;
        border-radius: 8px;
        transition: background 0.2s;
    }
    .stSidebar .stRadio label:hover {
        background: rgba(59, 130, 246, 0.2);
    }

    /* Active Radio Button Highlight */
    div[role='radiogroup'] label[data-checked="true"] {
        background: linear-gradient(90deg, #2563eb, #3b82f6);
        color: white !important;
        font-weight: 600 !important;
    }

    /* Headings */
    h1, h2, h3 {
        font-family: "Segoe UI", sans-serif;
        font-weight: 600;
        color: #1e3a8a;
    }

    /* Glassmorphic Card */
    .card {
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(10px);
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
        text-align: center;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .card:hover {
        transform: translateY(-6px);
        box-shadow: 0 12px 24px rgba(0,0,0,0.2);
    }

    .card h3 {
        color: #475569;
        font-size: 1.1rem;
        margin-bottom: 6px;
    }
    .card h2 {
        color: #2563eb;
        font-size: 2.2rem;
        margin: 0;
    }

    /* Buttons */
    div.stButton > button {
        background: linear-gradient(90deg, #2563eb, #3b82f6);
        color: white;
        border-radius: 10px;
        padding: 0.7rem 1.3rem;
        border: none;
        font-weight: 600;
        transition: all 0.2s;
        box-shadow: 0 4px 10px rgba(37, 99, 235, 0.3);
    }
    div.stButton > button:hover {
        background: linear-gradient(90deg, #1d4ed8, #2563eb);
        transform: scale(1.05);
        box-shadow: 0 6px 14px rgba(37, 99, 235, 0.5);
    }

    /* Info messages */
    .stAlert {
        border-radius: 12px;
        font-size: 0.95rem;
        backdrop-filter: blur(8px);
    }

    /* Job Description & Evaluations Table */
    .data-card {
        background: rgba(255, 255, 255, 0.65);
        backdrop-filter: blur(8px);
        border-radius: 14px;
        padding: 16px;
        margin-bottom: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
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
    st.title("📊 Dashboard Overview")

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
            st.markdown(
                f"<div class='data-card'>Resume ID: <b>{e.get('resume_id', '-')}</b> <br> Score: "
                f"<span style='color:#2563eb;font-weight:600;'>{e.get('relevance_score', 'N/A')}%</span></div>",
                unsafe_allow_html=True
            )
    else:
        st.info("No evaluations yet.")

# --------------------------
# Upload Resume Page
# --------------------------
elif page == "📂 Upload Resume":
    st.title("📂 Upload Resume")
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
    st.title("📋 Job Descriptions")
    try:
        jobs = requests.get(f"{BASE_URL}/job-descriptions").json().get("job_descriptions", [])
    except:
        jobs = []
    if jobs:
        for job in jobs:
            st.markdown(
                f"<div class='data-card'><b>{job.get('title', 'Unknown')}</b><br>{job.get('description', '')}</div>",
                unsafe_allow_html=True
            )
    else:
        st.info("No job descriptions available.")

# --------------------------
# Batch Processing Page
# --------------------------
elif page == "⚡ Batch Processing":
    st.title("⚡ Batch Processing")
    st.info("Upload multiple resumes to process in bulk.")
    batch_files = st.file_uploader("Upload multiple resumes", type=["pdf", "docx"], accept_multiple_files=True)
    if st.button("Process Batch") and batch_files:
        st.success(f"✅ {len(batch_files)} resumes queued for processing.")

# --------------------------
# Manage Data Page
# --------------------------
elif page == "📊 Manage Data":
    st.title("📊 Manage Data")
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
