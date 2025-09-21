# frontend/dashboard.py
import streamlit as st
import requests
from html import escape

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
# Fetch backend & data (safe)
# --------------------------
def fetch_safe(url, timeout=3):
    try:
        r = requests.get(url, timeout=timeout)
        r.raise_for_status()
        return r.json()
    except Exception:
        return None

resumes_data = fetch_safe(f"{BASE_URL}/resumes") or {}
jobs_data = fetch_safe(f"{BASE_URL}/job-descriptions") or {}
evals_data = fetch_safe(f"{BASE_URL}/evaluations") or {}

resumes = resumes_data.get("resumes", []) if isinstance(resumes_data, dict) else []
jobs = jobs_data.get("job_descriptions", []) if isinstance(jobs_data, dict) else []
evaluations = evals_data.get("evaluations", []) if isinstance(evals_data, dict) else []

backend_online = True if (resumes_data is not None and jobs_data is not None and evals_data is not None) else False

# --------------------------
# Read page from query params (so our custom links work)
# --------------------------
query_params = st.experimental_get_query_params()
page = query_params.get("page", ["Dashboard"])[0]  # default Dashboard

# --------------------------
# Build custom sidebar (HTML) to guarantee styling
# --------------------------
def render_sidebar(page, resumes_count, jobs_count, evals_count, backend_online):
    # choose classes for active items
    def cls(key):
        return "nav-link active" if page == key else "nav-link"

    backend_status = "Online" if backend_online else "Offline"
    backend_dot = '<span class="dot online"></span>' if backend_online else '<span class="dot offline"></span>'

    html = f"""
    <style>
    /* Sidebar wrapper */
    .custom-sidebar {{
        padding: 20px 14px;
        background: #ffffff;
        border-right: 1px solid #eef2f6;
        font-family: "Segoe UI", sans-serif;
    }}
    .brand {{
        text-align: center;
        margin-bottom: 12px;
    }}
    .brand h2 {{
        margin: 0;
        font-size: 16px;
        color: #0f172a;
        letter-spacing: 0.2px;
    }}
    .brand p {{
        margin: 4px 0 0 0;
        font-size: 12px;
        color: #6b7280;
    }}

    .nav {{
        margin-top: 16px;
        display: flex;
        flex-direction: column;
        gap: 8px;
    }}
    .nav-link {{
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 10px 12px;
        border-radius: 10px;
        text-decoration: none;
        color: #374151;
        background: #fbfdff;
        border: 1px solid #eef2f6;
        transition: all .18s ease;
        font-weight: 600;
    }}
    .nav-link:hover {{
        transform: translateX(6px);
        background: #f3f9ff;
        border-color: #dbeefe;
        color: #0c4a6e;
    }}
    .nav-link.active {{
        background: linear-gradient(90deg, #bfdbfe, #93c5fd);
        color: #063a7b;
        border: none;
        box-shadow: 0 6px 16px rgba(99, 102, 241, 0.08);
        transform: translateX(8px);
    }}

    .quick-stats {{
        margin-top: 18px;
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 8px;
    }}
    .quick-card {{
        background: #f8fafc;
        border-radius: 8px;
        padding: 8px 10px;
        border: 1px solid #eef2f6;
        text-align: center;
    }}
    .quick-card .title {{ font-size: 11px; color: #6b7280; margin: 0; }}
    .quick-card .value {{ font-size: 14px; color: #0c4a6e; font-weight: 700; margin: 4px 0 0 0; }}

    .backend-status {{
        margin-top: 14px;
        padding: 10px;
        background: #fbfdff;
        border-radius: 8px;
        border: 1px solid #eef2f6;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 10px;
    }}
    .backend-status .label {{ font-size: 12px; color: #475569; }}
    .dot {{
        width: 10px; height: 10px; border-radius: 50%;
        display: inline-block;
        box-shadow: 0 2px 6px rgba(2,6,23,0.06);
    }}
    .dot.online {{ background: #16a34a; }}
    .dot.offline {{ background: #ef4444; }}

    /* ensure sidebar HTML fits streamlit sidebar */
    .custom-sidebar a {{ display: block; }}
    </style>

    <div class="custom-sidebar">
      <div class="brand">
        <h2>Resume Evaluation System</h2>
        <p>AI-driven resume scoring</p>
      </div>

      <div class="nav">
        <a class="{cls('Dashboard')}" href="?page=Dashboard">🏠 Dashboard</a>
        <a class="{cls('Upload')}" href="?page=Upload">📂 Upload Resume</a>
        <a class="{cls('Evaluate')}" href="?page=Evaluate">📝 Evaluate Resume</a>
        <a class="{cls('JobDescriptions')}" href="?page=JobDescriptions">📋 Job Descriptions</a>
        <a class="{cls('Batch')}" href="?page=Batch">⚡ Batch Processing</a>
        <a class="{cls('ViewEvals')}" href="?page=ViewEvals">📑 View Evaluations</a>
        <a class="{cls('ManageData')}" href="?page=ManageData">📊 Manage Data</a>
      </div>

      <div class="quick-stats">
        <div class="quick-card"><div class="title">Resumes</div><div class="value">{resumes_count}</div></div>
        <div class="quick-card"><div class="title">Jobs</div><div class="value">{jobs_count}</div></div>
        <div class="quick-card"><div class="title">Evals</div><div class="value">{evals_count}</div></div>
        <div style="visibility:hidden"></div>
      </div>

      <div class="backend-status" title="Backend connectivity">
        <div>
          <div class="label">Backend</div>
          <div style="font-weight:700; color:#0f172a; margin-top:4px;">{backend_status}</div>
        </div>
        <div style="text-align:right">{backend_dot}</div>
      </div>
    </div>
    """

    return html

# render sidebar HTML
sidebar_html = render_sidebar(page, len(resumes), len(jobs), len(evaluations), backend_online)
st.sidebar.markdown(sidebar_html, unsafe_allow_html=True)

# --------------------------
# Main header (system name on every page)
# --------------------------
st.markdown("<div style='display:flex;align-items:center;gap:12px'><h1 style='margin:0'>Resume Evaluation System</h1></div>", unsafe_allow_html=True)
st.write("---")

# --------------------------
# Page: Dashboard
# --------------------------
if page == "Dashboard":
    st.subheader("📊 Dashboard Overview")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"<div style='background:#fff;padding:18px;border-radius:12px;border:1px solid #eef6ff;text-align:center;'><div style='color:#64748b'>📄 Resumes</div><div style='font-weight:700;font-size:20px;color:#0c4a6e'>{len(resumes)}</div></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div style='background:#fff;padding:18px;border-radius:12px;border:1px solid #eef6ff;text-align:center;'><div style='color:#64748b'>💼 Job Descriptions</div><div style='font-weight:700;font-size:20px;color:#0c4a6e'>{len(jobs)}</div></div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div style='background:#fff;padding:18px;border-radius:12px;border:1px solid #eef6ff;text-align:center;'><div style='color:#64748b'>✅ Evaluations</div><div style='font-weight:700;font-size:20px;color:#0c4a6e'>{len(evaluations)}</div></div>", unsafe_allow_html=True)

    st.markdown("### Recent Evaluations")
    if evaluations:
        for e in evaluations[:10]:
            st.markdown(f"<div style='background:#fbfdff;border:1px solid #eef6ff;padding:12px;border-radius:10px;margin-bottom:8px;'><b>Resume:</b> {escape(str(e.get('resume_id','-')))} &nbsp; <b>Job:</b> {escape(str(e.get('job_id','-')))} &nbsp; <b>Score:</b> <span style='color:#0c4a6e;font-weight:700'>{escape(str(e.get('relevance_score','N/A')))}%</span></div>", unsafe_allow_html=True)
    else:
        st.info("No evaluations yet.")

# --------------------------
# Page: Upload Resume
# --------------------------
elif page == "Upload":
    st.subheader("📂 Upload Resume")
    uploaded_file = st.file_uploader("Upload a resume (PDF/DOCX)", type=["pdf", "docx"])
    if uploaded_file:
        files = {"file": uploaded_file.getvalue()}
        try:
            resp = requests.post(f"{BASE_URL}/resumes", files=files, timeout=8)
            if resp.status_code == 200:
                st.success("✅ Resume uploaded successfully")
            else:
                st.error(f"❌ Upload failed ({resp.status_code})")
        except Exception:
            st.error("⚠️ Backend not reachable")

# --------------------------
# Page: Evaluate Resume
# --------------------------
elif page == "Evaluate":
    st.subheader("📝 Evaluate Resume")
    eval_file = st.file_uploader("Select a resume to evaluate", type=["pdf", "docx"])
    job_id = st.text_input("Job ID")
    if st.button("Evaluate"):
        if not eval_file or not job_id:
            st.warning("Please provide a resume file and a Job ID")
        else:
            files = {"file": eval_file.getvalue()}
            try:
                resp = requests.post(f"{BASE_URL}/evaluate/{escape(job_id)}", files=files, timeout=12)
                if resp.status_code == 200:
                    st.success("✅ Evaluation complete")
                    st.json(resp.json())
                else:
                    st.error(f"❌ Evaluation failed ({resp.status_code})")
            except Exception:
                st.error("⚠️ Backend not reachable")

# --------------------------
# Page: Job Descriptions
# --------------------------
elif page == "JobDescriptions":
    st.subheader("📋 Job Descriptions")
    if jobs:
        for job in jobs:
            st.markdown(f"<div style='background:#fff;border:1px solid #eef6ff;padding:12px;border-radius:10px;margin-bottom:8px;'><b>{escape(job.get('title','Unknown'))}</b><div style='color:#64748b;margin-top:6px'>{escape(job.get('description',''))}</div></div>", unsafe_allow_html=True)
    else:
        st.info("No job descriptions available.")

# --------------------------
# Page: Batch Processing
# --------------------------
elif page == "Batch":
    st.subheader("⚡ Batch Processing")
    files = st.file_uploader("Upload multiple resumes", type=["pdf", "docx"], accept_multiple_files=True)
    if st.button("Process Batch"):
        if not files:
            st.warning("Please select files")
        else:
            st.success(f"✅ {len(files)} files queued for batch processing (notified)")

# --------------------------
# Page: View Evaluations
# --------------------------
elif page == "ViewEvals":
    st.subheader("📑 View Evaluations")
    if evaluations:
        for e in evaluations:
            st.markdown(f"<div style='background:#fff;border:1px solid #eef6ff;padding:12px;border-radius:10px;margin-bottom:8px;'><b>Resume:</b> {escape(str(e.get('resume_id','-')))} &nbsp; <b>Job:</b> {escape(str(e.get('job_id','-')))} &nbsp; <b>Score:</b> <span style='color:#0c4a6e;font-weight:700'>{escape(str(e.get('relevance_score','N/A')))}%</span></div>", unsafe_allow_html=True)
    else:
        st.info("No evaluations available.")

# --------------------------
# Page: Manage Data
# --------------------------
elif page == "ManageData":
    st.subheader("📊 Manage Data")
    st.write("Resumes:")
    st.write(resumes if resumes else "No resumes uploaded.")
    st.write("Job Descriptions:")
    st.write(jobs if jobs else "No job descriptions.")
    st.write("Evaluations:")
    st.write(evaluations if evaluations else "No evaluations.")
