import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from datetime import datetime

API_BASE_URL = "https://resume-evalution-system-backend.onrender.com"  # Replace with your backend URL

# ------------------ Utility Functions ------------------ #
def make_api_request(endpoint, method="GET", data=None, files=None):
    url = f"{API_BASE_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, files=files, timeout=30)
        elif method == "DELETE":
            response = requests.delete(url, timeout=10)
        if response.status_code in [200, 201]:
            return response.json()
        return None
    except Exception as e:
        return None

def create_metric_card(title, value, icon, color):
    return f"""
    <div style="background: {color}; padding: 1rem; border-radius: 0.5rem; color: white; text-align: center; margin-bottom: 0.5rem;">
        <div style="font-size: 1.5rem;">{icon}</div>
        <div style="font-size: 1.2rem; font-weight: bold;">{value}</div>
        <div>{title}</div>
    </div>
    """

def display_evaluation_results(evaluation):
    """Display detailed evaluation charts and suggestions"""
    # Skill Gap
    st.markdown("#### 🎯 Skill Gap Analysis")
    matched_skills = evaluation.get('matched_skills', [])
    missing_skills = evaluation.get('missing_skills', [])
    all_skills = matched_skills + missing_skills

    categories = {'Technical Skills': [], 'Soft Skills': [], 'Tools & Technologies': []}
    for skill in all_skills:
        sl = skill.lower()
        if any(tech in sl for tech in ['python','java','javascript','react','angular','vue','node','sql','mongodb','postgresql','docker','aws','azure']):
            categories['Technical Skills'].append(skill)
        elif any(soft in sl for soft in ['communication','leadership','teamwork','problem solving','analytical','creative','management']):
            categories['Soft Skills'].append(skill)
        else:
            categories['Tools & Technologies'].append(skill)

    matched_counts = [len([s for s in v if s in matched_skills]) for v in categories.values()]
    missing_counts = [len([s for s in v if s in missing_skills]) for v in categories.values()]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=list(categories.keys()), y=matched_counts, name='Matched Skills', marker_color='#4ecdc4', text=matched_counts, textposition='auto'))
    fig.add_trace(go.Bar(x=list(categories.keys()), y=missing_counts, name='Missing Skills', marker_color='#ff6b6b', text=missing_counts, textposition='auto'))
    fig.update_layout(barmode='stack', title="Skill Gap Analysis by Category", height=400, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

    # Resume Quality
    st.markdown("#### 📋 Resume Quality Analysis")
    resume_data = evaluation.get('resume_data', {})
    has_skills = len(resume_data.get('skills', [])) > 0
    has_education = len(resume_data.get('education', [])) > 0
    has_experience = len(resume_data.get('experience', [])) > 0
    has_projects = len(resume_data.get('projects', [])) > 0
    has_certifications = len(resume_data.get('certifications', [])) > 0

    completeness_score = sum([has_skills, has_education, has_experience, has_projects, has_certifications]) * 20
    total_skills = len(resume_data.get('skills', []))
    relevance_score = (len(matched_skills) / max(total_skills, 1)) * 100
    experience_score = min(len(resume_data.get('experience', [])) * 2 * 10, 100)
    quality_score = (completeness_score + relevance_score + experience_score) / 3

    df = pd.DataFrame({
        'Metric': ['Content Completeness', 'Skill Relevance', 'Experience Level', 'Overall Quality'],
        'Score': [completeness_score, relevance_score, experience_score, quality_score]
    })

    fig2 = go.Figure(go.Scatterpolar(
        r=df['Score'], theta=df['Metric'], fill='toself',
        line_color='#667eea', fillcolor='rgba(102,126,234,0.3)', name='Resume Quality'
    ))
    fig2.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=True, height=400)
    st.plotly_chart(fig2, use_container_width=True)

    # AI Optimization
    st.markdown("#### 🤖 AI-Powered Optimization Suggestions")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("##### 🎯 Immediate Improvements")
        immediate_tips = []
        if missing_skills: immediate_tips.append(f"**Learn these skills:** {', '.join(missing_skills[:3])}")
        if 'Limited project portfolio' in evaluation.get('weaknesses', []): immediate_tips.append("**Add 2-3 detailed projects**")
        if 'No relevant certifications' in evaluation.get('weaknesses', []): immediate_tips.append("**Get certified** in key technologies")
        if not immediate_tips: immediate_tips.append("**Resume looks good!** Focus on interview preparation")
        for tip in immediate_tips: st.markdown(f"• {tip}")

    with col2:
        st.markdown("##### 🚀 Advanced Optimizations")
        for tip in ["**Quantify achievements**", "**Use action verbs**", "**Tailor keywords** to job descriptions", "**Add a professional summary**"]:
            st.markdown(f"• {tip}")

# ------------------ Pages ------------------ #
def dashboard_page():
    st.markdown("### 📊 Dashboard Overview")
    resumes_resp = make_api_request("/resumes/") or {"resumes": []}
    jobs_resp = make_api_request("/job-descriptions/") or {"job_descriptions": []}
    eval_resp = make_api_request("/evaluations/") or {"evaluations": []}

    num_resumes = len(resumes_resp.get("resumes", []))
    num_jobs = len(jobs_resp.get("job_descriptions", []))
    num_eval = len(eval_resp.get("evaluations", []))

    st.markdown("#### 📊 Quick Stats")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Resumes", num_resumes)
    col2.metric("Job Descriptions", num_jobs)
    col3.metric("Evaluations", num_eval)
    if num_eval > 0:
        avg_score = sum(e.get('relevance_score',0) for e in eval_resp.get("evaluations",[])) / num_eval
        col4.metric("Avg Score", f"{avg_score:.1f}")

def upload_resume_page():
    st.markdown("### 📄 Upload Resume")
    uploaded_files = st.file_uploader("Choose resume files", type=['pdf','docx'], accept_multiple_files=True)
    if uploaded_files:
        for file in uploaded_files:
            st.markdown(f"**Uploaded:** {file.name}")
            try:
                response = requests.post(f"{API_BASE_URL}/resumes/", files={"file": (file.name, file)}, timeout=20)
                if response.status_code in [200,201]:
                    st.success(f"{file.name} uploaded successfully!")
                else:
                    st.error(f"Failed to upload {file.name}")
            except Exception as e:
                st.error(f"Error uploading {file.name}: {e}")

def upload_job_description_page():
    st.markdown("### 💼 Upload Job Description")
    uploaded_files = st.file_uploader("Choose job description files", type=['pdf','docx'], accept_multiple_files=True)
    if uploaded_files:
        for file in uploaded_files:
            st.markdown(f"**Uploaded:** {file.name}")
            try:
                response = requests.post(f"{API_BASE_URL}/job-descriptions/", files={"file": (file.name, file)}, timeout=20)
                if response.status_code in [200,201]:
                    st.success(f"{file.name} uploaded successfully!")
                else:
                    st.error(f"Failed to upload {file.name}")
            except Exception as e:
                st.error(f"Error uploading {file.name}: {e}")

def evaluate_resume_page():
    st.markdown("### 🔍 Evaluate Resume")
    resumes_resp = make_api_request("/resumes/") or {"resumes":[]}
    jobs_resp = make_api_request("/job-descriptions/") or {"job_descriptions":[]}

    resume_options = [r["filename"] for r in resumes_resp.get("resumes",[])]
    job_options = [j["title"] for j in jobs_resp.get("job_descriptions",[])]

    selected_resume = st.selectbox("Select Resume", options=resume_options)
    selected_job = st.selectbox("Select Job Description", options=job_options)

    if st.button("Evaluate"):
        st.info("Evaluation in progress...")
        data = {"resume_name": selected_resume, "job_name": selected_job}
        result = make_api_request("/evaluations/", method="POST", data=data)
        if result:
            st.success("Evaluation completed!")
            display_evaluation_results(result)
        else:
            st.error("Evaluation failed or API unavailable.")

def view_evaluations_page():
    st.markdown("### 📋 View Evaluations")
    eval_resp = make_api_request("/evaluations/") or {"evaluations":[]}
    evaluations = eval_resp.get("evaluations",[])
    if not evaluations:
        st.info("No evaluations found.")
        return

    df = pd.DataFrame(evaluations)
    st.dataframe(df)

def batch_processing_page():
    st.markdown("### 📦 Batch Processing")
    st.info("Upload multiple resumes/job descriptions and evaluate in batch.")
    uploaded_resumes = st.file_uploader("Upload Resumes", type=['pdf','docx'], accept_multiple_files=True, key="batch_resumes")
    uploaded_jobs = st.file_uploader("Upload Job Descriptions", type=['pdf','docx'], accept_multiple_files=True, key="batch_jobs")
    if st.button("Run Batch Evaluation"):
        st.info("Batch evaluation started...")
        st.success("Batch processing feature will be implemented here.")

def manage_data_page():
    st.markdown("### 🗂️ Manage Data")
    st.info("View and delete resumes, job descriptions, and evaluations.")
    st.success("Manage Data feature will be implemented here.")

# ------------------ Main App ------------------ #
def main():
    if 'page' not in st.session_state:
        st.session_state.page = "Dashboard"

    st.sidebar.markdown("## 🗂 Navigation")
    pages = {
        "Dashboard": dashboard_page,
        "Upload Resume": upload_resume_page,
        "Upload Job Description": upload_job_description_page,
        "Evaluate Resume": evaluate_resume_page,
        "View Evaluations": view_evaluations_page,
        "Batch Processing": batch_processing_page,
        "Manage Data": manage_data_page
    }

    for name in pages:
        if st.sidebar.button(name):
            st.session_state.page = name
            st.experimental_rerun()

    st.markdown('<h1>📄 Resume Evaluation System</h1>', unsafe_allow_html=True)

    # Display selected page
    pages[st.session_state.page]()

if __name__ == "__main__":
    main()
