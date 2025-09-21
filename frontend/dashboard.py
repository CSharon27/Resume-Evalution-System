import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from datetime import datetime

API_BASE_URL = "https://resume-evalution-system-backend.onrender.com"  # Replace with your API

# ------------------ Utility Functions ------------------ #
def make_api_request(endpoint, method="GET", data=None):
    url = f"{API_BASE_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "DELETE":
            response = requests.delete(url)
        else:
            response = requests.post(url, json=data)
        if response.status_code in [200, 201]:
            return response.json()
        return None
    except Exception:
        return None

def create_metric_card(title, value, icon, color):
    return f"""
    <div style="background: {color}; padding: 1rem; border-radius: 0.5rem; color: white; text-align: center;">
        <div style="font-size: 1.5rem;">{icon}</div>
        <div style="font-size: 1.2rem; font-weight: bold;">{value}</div>
        <div>{title}</div>
    </div>
    """

def get_verdict_icon(verdict):
    return {"High": "🟢", "Medium": "🟡", "Low": "🔴"}.get(verdict, "⚪")

# ------------------ Visualization Functions ------------------ #
def create_resume_quality_score(evaluation):
    st.markdown("#### 📋 Resume Quality Analysis")
    resume_data = evaluation.get('resume_data', {})
    has_skills = len(resume_data.get('skills', [])) > 0
    has_education = len(resume_data.get('education', [])) > 0
    has_experience = len(resume_data.get('experience', [])) > 0
    has_projects = len(resume_data.get('projects', [])) > 0
    has_certifications = len(resume_data.get('certifications', [])) > 0

    completeness_score = sum([has_skills, has_education, has_experience, has_projects, has_certifications]) * 20
    matched_skills = evaluation.get('matched_skills', [])
    total_skills = len(resume_data.get('skills', []))
    relevance_score = (len(matched_skills) / max(total_skills, 1)) * 100
    experience_score = min(len(resume_data.get('experience', [])) * 2 * 10, 100)
    quality_score = (completeness_score + relevance_score + experience_score) / 3

    df = pd.DataFrame({
        'Metric': ['Content Completeness', 'Skill Relevance', 'Experience Level', 'Overall Quality'],
        'Score': [completeness_score, relevance_score, experience_score, quality_score]
    })

    fig = go.Figure(go.Scatterpolar(
        r=df['Score'], theta=df['Metric'], fill='toself',
        line_color='#667eea', fillcolor='rgba(102,126,234,0.3)', name='Resume Quality'
    ))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=True, height=400)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("##### 💡 Quality Improvement Tips")
    for rec in (["Add more detailed sections (projects, certifications)"] if completeness_score < 80 else []) + \
               (["Focus on skills relevant to target positions"] if relevance_score < 70 else []) + \
               (["Include more detailed work experience"] if experience_score < 60 else []):
        st.markdown(f"• {rec}")
    if completeness_score >= 80 and relevance_score >= 70 and experience_score >= 60:
        st.success("✅ Resume quality is excellent!")

def create_skill_gap_analysis(evaluation):
    st.markdown("#### 🎯 Skill Gap Analysis")
    missing_skills = evaluation.get('missing_skills', [])
    matched_skills = evaluation.get('matched_skills', [])
    all_skills = missing_skills + matched_skills

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

def create_ai_optimization_suggestions(evaluation):
    st.markdown("#### 🤖 AI-Powered Optimization Suggestions")
    missing_skills, weaknesses = evaluation.get('missing_skills', []), evaluation.get('weaknesses', [])
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("##### 🎯 Immediate Improvements")
        immediate_tips = []
        if missing_skills: immediate_tips.append(f"**Learn these skills:** {', '.join(missing_skills[:3])}")
        if 'Limited project portfolio' in weaknesses: immediate_tips.append("**Add 2-3 detailed projects**")
        if 'No relevant certifications' in weaknesses: immediate_tips.append("**Get certified** in key technologies")
        if not immediate_tips: immediate_tips.append("**Resume looks good!** Focus on interview preparation")
        for tip in immediate_tips: st.markdown(f"• {tip}")

    with col2:
        st.markdown("##### 🚀 Advanced Optimizations")
        for tip in ["**Quantify achievements**", "**Use action verbs**", "**Tailor keywords** to job descriptions", "**Add a professional summary**"]: 
            st.markdown(f"• {tip}")

    optimization_score = max(100 - len(missing_skills) * 10, 0)
    st.markdown(f"##### 📊 Optimization Score: {optimization_score}/100")
    progress_color = "#4ecdc4" if optimization_score >= 70 else "#ff6b6b" if optimization_score >= 40 else "#ffa726"
    st.markdown(f"<div class='progress-container'><div class='progress-bar' style='width: {optimization_score}%; background: {progress_color};'>{optimization_score}%</div></div>", unsafe_allow_html=True)

def display_evaluation_results(evaluation):
    st.markdown("---")
    create_skill_gap_analysis(evaluation)
    st.markdown("---")
    create_resume_quality_score(evaluation)
    st.markdown("---")
    create_ai_optimization_suggestions(evaluation)
    st.markdown("---")

# ------------------ Main Pages ------------------ #
def view_evaluations():
    st.markdown("### 📋 All Evaluations")
    evaluations = make_api_request("/evaluations/")
    if not evaluations:
        st.info("ℹ️ No evaluations found. Please evaluate some resumes first.")
        return

    # ensure evaluations is a list of dicts
    if isinstance(evaluations, dict):
        evaluations = [evaluations]

    df = pd.DataFrame(evaluations)

    # Summary Cards
    st.markdown("#### 📊 Summary Statistics")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(create_metric_card("Average Score", f"{df['relevance_score'].mean():.1f}", "📊", "#1f77b4"), unsafe_allow_html=True)
    with col2:
        st.markdown(create_metric_card("High Suitability", str(len(df[df['verdict'] == 'High'])), "🟢", "#28a745"), unsafe_allow_html=True)
    with col3:
        st.markdown(create_metric_card("Medium Suitability", str(len(df[df['verdict'] == 'Medium'])), "🟡", "#ffc107"), unsafe_allow_html=True)
    with col4:
        st.markdown(create_metric_card("Total Evaluations", str(len(df)), "📋", "#6c757d"), unsafe_allow_html=True)

    # Charts
    st.markdown("#### 📈 Analytics Dashboard")
    col1, col2 = st.columns(2)
    with col1:
        verdict_counts = df['verdict'].value_counts()
        fig = px.pie(
            names=verdict_counts.index, values=verdict_counts.values,
            title="Verdict Distribution",
            color_discrete_map={'High': '#28a745', 'Medium': '#ffc107', 'Low': '#dc3545'}
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.histogram(df, x='relevance_score', nbins=20, title="Score Distribution", color_discrete_sequence=['#1f77b4'])
        fig.update_layout(xaxis_title="Relevance Score", yaxis_title="Count")
        st.plotly_chart(fig, use_container_width=True)

# ------------------ Main App ------------------ #
def main():
    if 'page' not in st.session_state: 
        st.session_state.page = "Dashboard"

    st.markdown('<h1>📄 Resume Evaluation System</h1>', unsafe_allow_html=True)

    # Sidebar
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

        # Sidebar Quick Stats
        st.markdown("### 📊 Quick Stats")
        resumes = make_api_request("/resumes/") or []
        job_descriptions = make_api_request("/job-descriptions/") or []
        evaluations = make_api_request("/evaluations/") or []

        st.metric("Resumes", len(resumes))
        st.metric("Job Descriptions", len(job_descriptions))
        st.metric("Evaluations", len(evaluations))

        # compute avg score safely
        valid_scores = [e.get('relevance_score') for e in evaluations if isinstance(e, dict) and 'relevance_score' in e]
        if valid_scores:
            avg_score = sum(valid_scores) / len(valid_scores)
            st.metric("Avg Score", f"{avg_score:.1f}")

    # Main content
    if st.session_state.page == "Dashboard":
        st.markdown("### 📊 Dashboard Overview")
        st.info("Welcome to the Resume Evaluation System! Navigate from the sidebar to start.")
    elif st.session_state.page == "Evaluate Resume":
        st.markdown("### 🔍 Evaluate Resume")
    elif st.session_state.page == "View Evaluations":
        view_evaluations()
    elif st.session_state.page == "Batch Processing":
        st.markdown("### 📦 Batch Processing")
    elif st.session_state.page == "Manage Data":
        st.markdown("### 🗂️ Manage Data")

if __name__ == "__main__":
    main()
