import streamlit as st
import requests

# Backend API base URL
API_URL = "https://your-backend-url.onrender.com"

# --------------------------
# Utility Functions
# --------------------------
def check_api_status():
    """Check if backend API is alive."""
    try:
        resp = requests.get(f"{API_URL}/")
        if resp.status_code == 200:
            return True, resp.json().get("message", "OK")
        else:
            return False, f"Error {resp.status_code}"
    except Exception as e:
        return False, str(e)

def fetch_resumes():
    try:
        return requests.get(f"{API_URL}/resumes/").json().get("resumes", [])
    except:
        return []

def fetch_jobs():
    try:
        return requests.get(f"{API_URL}/job-descriptions/").json().get("job_descriptions", [])
    except:
        return []

def fetch_evaluations():
    try:
        return requests.get(f"{API_URL}/evaluations/").json().get("evaluations", [])
    except:
        return []

# --------------------------
# Sidebar Navigation
# --------------------------
st.sidebar.title("📂 Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "Resumes", "Job Descriptions", "Evaluations"])

# Show API status in sidebar
status, msg = check_api_status()
if status:
    st.sidebar.success(f"✅ API Online: {msg}")
else:
    st.sidebar.error(f"❌ API Offline: {msg}")

# --------------------------
# Dashboard
# --------------------------
if page == "Dashboard":
    st.title("📊 Resume Evaluation Dashboard")

    resumes = fetch_resumes()
    jobs = fetch_jobs()
    evaluations = fetch_evaluations()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📄 Total Resumes", len(resumes))
    with col2:
        st.metric("📝 Job Descriptions", len(jobs))
    with col3:
        st.metric("✅ Evaluations Done", len(evaluations))

    # Show average score if evaluations exist
    if evaluations:
        try:
            avg_score = sum(e.get("relevance_score", 0) for e in evaluations) / len(evaluations)
            st.markdown(f"### ⭐ Average Relevance Score: `{avg_score:.2f}`")
        except:
            st.warning("⚠️ Evaluations data format issue.")
    else:
        st.info("No evaluations yet.")

# --------------------------
# Resumes Page
# --------------------------
elif page == "Resumes":
    st.title("📄 Manage Resumes")

    uploaded = st.file_uploader("Upload a Resume", type=["pdf", "docx"])
    if uploaded:
        files = {"file": uploaded.getvalue()}
        resp = requests.post(f"{API_URL}/resumes/", files=files)
        if resp.status_code == 200:
            st.success(f"Uploaded {uploaded.name}")
        else:
            st.error("Upload failed!")

    st.markdown("### Existing Resumes")
    resumes = fetch_resumes()
    if resumes:
        for r in resumes:
            st.write(f"- {r}")
    else:
        st.info("No resumes uploaded.")

# --------------------------
# Job Descriptions Page
# --------------------------
elif page == "Job Descriptions":
    st.title("📝 Manage Job Descriptions")

    jd_text = st.text_area("Enter Job Description")
    if st.button("Save Job Description"):
        resp = requests.post(f"{API_URL}/job-descriptions/", json={"jd": jd_text})
        if resp.status_code == 200:
            st.success("Job description saved!")
        else:
            st.error("Failed to save job description.")

    st.markdown("### Existing Job Descriptions")
    jobs = fetch_jobs()
    if jobs:
        for j in jobs:
            st.write(f"- {j}")
    else:
        st.info("No job descriptions available.")

# --------------------------
# Evaluations Page
# --------------------------
elif page == "Evaluations":
    st.title("✅ Resume Evaluations")

    evaluations = fetch_evaluations()
    if evaluations:
        for e in evaluations:
            st.json(e)
    else:
        st.info("No evaluations yet.")
