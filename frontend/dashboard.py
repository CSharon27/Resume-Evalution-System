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

        # Sidebar Quick Stats
        st.markdown("### 📊 Quick Stats")
        resumes = make_api_request("/resumes/")
        job_descriptions = make_api_request("/job-descriptions/")
        evaluations = make_api_request("/evaluations/")

        st.metric("Resumes", len(resumes) if resumes else 0)
        st.metric("Job Descriptions", len(job_descriptions) if job_descriptions else 0)
        st.metric("Evaluations", len(evaluations) if evaluations else 0)
        if evaluations:
            avg_score = sum(e['relevance_score'] for e in evaluations) / len(evaluations)
            st.metric("Avg Score", f"{avg_score:.1f}")

        # API Status
        api_status = make_api_request("/")
        if api_status:
            st.success("API Online ✅")
        else:
            st.error("API Offline ❌")

    # ----------------- Main Content ----------------- #
    page = st.session_state.page

    if page == "Dashboard":
        st.markdown("### 📊 Dashboard Overview")
        st.info("Welcome to the Resume Evaluation System! Navigate from the sidebar to start.")

    elif page == "Upload Resume":
        st.markdown("### 📄 Upload Resume")
        resume_file = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf", "docx"])
        if resume_file:
            files = {"file": resume_file.getvalue()}
            resp = requests.post(f"{API_BASE_URL}/resumes/", files=files)
            if resp.status_code in [200, 201]:
                st.success(f"Uploaded {resume_file.name}")
            else:
                st.error("Upload failed!")

    elif page == "Job Descriptions":
        st.title("💼 Manage Job Descriptions")

        st.markdown("#### 1️⃣ Upload Job Description Document")
        jd_file = st.file_uploader("Upload JD (PDF/DOCX)", type=["pdf", "docx"])
        if jd_file:
            files = {"file": jd_file.getvalue()}
            resp = requests.post(f"{API_BASE_URL}/job-descriptions/", files=files)
            if resp.status_code in [200, 201]:
                st.success(f"Uploaded {jd_file.name}")
            else:
                st.error("Upload failed!")

        st.markdown("#### 2️⃣ Enter Job Description Manually")
        jd_text = st.text_area("Enter Job Description")
        if st.button("Save Job Description"):
            if jd_text.strip():
                resp = requests.post(f"{API_BASE_URL}/job-descriptions/", json={"jd": jd_text})
                if resp.status_code in [200, 201]:
                    st.success("Job description saved!")
                else:
                    st.error("Failed to save job description.")
            else:
                st.warning("Please enter some text before saving.")

        st.markdown("### Existing Job Descriptions")
        jobs = make_api_request("/job-descriptions/")
        if jobs:
            for j in jobs:
                st.write(f"- {j}")
        else:
            st.info("No job descriptions available.")

    elif page == "Evaluate Resume":
        st.markdown("### 🔍 Evaluate Resume")
        # Evaluation interface logic here

    elif page == "View Evaluations":
        view_evaluations()

    elif page == "Batch Processing":
        st.markdown("### 📦 Batch Processing")
        # Add batch processing logic here

    elif page == "Manage Data":
        st.markdown("### 🗂️ Manage Data")
        # Add manage data logic here

if __name__ == "__main__":
    main()

