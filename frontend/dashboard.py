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


# --------------------------
# Job Descriptions Page
# --------------------------
elif page == "Job Descriptions":
    st.title("📝 Manage Job Descriptions")

    st.markdown("#### 1️⃣ Upload Job Description Document")
    jd_file = st.file_uploader("Upload JD (PDF/DOCX)", type=["pdf", "docx"])
    if jd_file:
        files = {"file": jd_file.getvalue()}
        resp = requests.post(f"{API_URL}/job-descriptions/", files=files)
        if resp.status_code in [200, 201]:
            st.success(f"Uploaded {jd_file.name}")
        else:
            st.error("Upload failed!")

    st.markdown("#### 2️⃣ Enter Job Description Manually")
    jd_text = st.text_area("Enter Job Description")
    if st.button("Save Job Description"):
        if jd_text.strip():
            resp = requests.post(f"{API_URL}/job-descriptions/", json={"jd": jd_text})
            if resp.status_code in [200, 201]:
                st.success("Job description saved!")
            else:
                st.error("Failed to save job description.")
        else:
            st.warning("Please enter some text before saving.")

    st.markdown("### Existing Job Descriptions")
    jobs = fetch_jobs()
    if jobs:
        for j in jobs:
            st.write(f"- {j}")
    else:
        st.info("No job descriptions available.")
# ------------------ Main App ------------------ #
def main():
    if 'page' not in st.session_state: st.session_state.page = "Dashboard"

    st.markdown('<h1>📄 Resume Evaluation System</h1>', unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        nav_options = {
            "🏠 Dashboard": "Dashboard",
            "📄 Upload Resume": "Upload Resume",
            "💼 Upload Job Description": "Job Descriptions",
            "🔍 Evaluate Resume": "Evaluate Resume",
            "📋 View Evaluations": "View Evaluations",
            "📦 Batch Processing": "Batch Processing",
            "🗂️ Manage Data": "Manage Data"
        }
        for display, page in nav_options.items():
            if st.button(display, key=f"nav_{page}"):
                st.session_state.page = page
                st.rerun()

        # Sidebar Quick Stats & API status
        st.markdown("### 📊 Quick Stats")
        resumes = make_api_request("/resumes/")
        job_descriptions = make_api_request("/job-descriptions/")
        evaluations = make_api_request("/evaluations/")
        st.metric("Resumes", len(resumes) if resumes else 0)
        st.metric("Job Descriptions", len(job_descriptions) if job_descriptions else 0)
        st.metric("Evaluations", len(evaluations) if evaluations else 0)
        if evaluations:
            avg_score = sum(e.get('relevance_score', 0) for e in evaluations) / len(evaluations)
            st.metric("Avg Score", f"{avg_score:.1f}")

        # API Status
        try:
            status = requests.get(f"{API_BASE_URL}/").json().get("message", "Unknown")
            st.success(f"API Status: ✅ {status}")
        except:
            st.error("API Status: ❌ Not reachable")

    # ------------------ Page Contents ------------------ #
    page = st.session_state.page

    if page == "Dashboard":
        st.markdown("### 📊 Dashboard Overview")
        st.info("Welcome to the Resume Evaluation System! Navigate from the sidebar to start.")

    elif page == "Upload Resume":
        st.markdown("### 📄 Upload Resume")
        # Keep your existing upload logic here

    elif page == "Job Descriptions":
        st.title("💼 Manage Job Descriptions")

        # 1️⃣ Upload JD Document
        jd_file = st.file_uploader("Upload JD (PDF/DOCX)", type=["pdf", "docx"])
        if jd_file:
            files = {"file": jd_file.getvalue()}
            resp = requests.post(f"{API_BASE_URL}/job-descriptions/", files=files)
            if resp.status_code in [200, 201]:
                st.success(f"Uploaded {jd_file.name}")
            else:
                st.error("Upload failed!")

        # 2️⃣ Manual JD entry
        jd_text = st.text_area("Or Enter Job Description Manually")
        if st.button("Save Job Description"):
            if jd_text.strip():
                resp = requests.post(f"{API_BASE_URL}/job-descriptions/", json={"jd": jd_text})
                if resp.status_code in [200, 201]:
                    st.success("Job description saved!")
                else:
                    st.error("Failed to save job description.")
            else:
                st.warning("Please enter some text before saving.")

        # Display existing JDs
        st.markdown("### Existing Job Descriptions")
        jobs = make_api_request("/job-descriptions/")
        if jobs:
            for j in jobs:
                st.write(f"- {j}")
        else:
            st.info("No job descriptions available.")

    elif page == "Evaluate Resume":
        st.markdown("### 🔍 Evaluate Resume")
        # Keep your evaluation logic here

    elif page == "View Evaluations":
        view_evaluations()

    elif page == "Batch Processing":
        st.markdown("### 📦 Batch Processing")
        # Keep your batch logic here

    elif page == "Manage Data":
        st.markdown("### 🗂️ Manage Data")
        # Keep your data management logic here

if __name__ == "__main__":
    main()

