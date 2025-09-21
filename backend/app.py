import streamlit as st
import json
from app.evaluators.semantic_matcher import SemanticMatcher
from app.parsers.resume_parser import ResumeParser

st.set_page_config(page_title="Resume Evaluation System", layout="wide")
st.title("🚀 Resume Evaluation System")

# Initialize classes
matcher = SemanticMatcher()
parser = ResumeParser()  # optional for parsing uploaded resumes

# --- Upload Resume ---
uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])

if uploaded_file:
    st.success("File uploaded successfully!")

    # Parse resume (optional)
    resume_data = parser.parse_resume(uploaded_file)

    # Evaluate resume using SemanticMatcher
    evaluation_results = matcher.evaluate_resume(resume_data)

    # --- Display Results ---
    st.subheader("📊 Evaluation Results")
    st.json(evaluation_results)

    # Scores
    st.subheader("✅ Scores")
    st.metric("Relevance Score", evaluation_results["relevance_score"])
    st.metric("Hard Match Score", evaluation_results["hard_match_score"])
    st.metric("Semantic Match Score", evaluation_results["semantic_match_score"])

    # Missing elements
    st.subheader("🚫 Missing Skills")
    st.write(evaluation_results.get("missing_skills", []))

    st.subheader("🎓 Missing Certifications")
    st.write(evaluation_results.get("missing_certifications", []))

    st.subheader("📚 Suggested Projects")
    st.write(evaluation_results.get("missing_projects", []))

    st.subheader("💡 Strengths & Weaknesses")
    st.write("Strengths:", evaluation_results.get("strengths", []))
    st.write("Weaknesses:", evaluation_results.get("weaknesses", []))

    st.subheader("📝 Improvement Suggestions")
    st.write(evaluation_results.get("improvement_suggestions", []))

    st.subheader("🏆 Overall Feedback")
    st.write(evaluation_results.get("overall_feedback", "LLM analysis not available"))
