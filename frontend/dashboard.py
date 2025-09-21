"""Streamlit dashboard for Resume Evaluation System."""

import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from typing import Dict, List, Any
import time
import base64
from io import BytesIO

# Configure page
st.set_page_config(
    page_title="Resume Evaluation System",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/your-repo',
        'Report a bug': "https://github.com/your-repo/issues",
        'About': "# Resume Evaluation System\nAI-powered resume analysis for placement teams!"
    }
)

# API Configuration
API_BASE_URL = "https://resume-evalution-system-backend.onrender.com"

# Custom CSS - Professional Design
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Main header styling */
    .main-header {
        font-family: 'Inter', sans-serif;
        font-size: 3.5rem;
        font-weight: 700;
        color: #1a365d;
        text-align: center;
        margin-bottom: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -0.02em;
    }
    
    .sub-header {
        font-family: 'Inter', sans-serif;
        font-size: 1.2rem;
        color: #4a5568;
        text-align: center;
        margin-bottom: 3rem;
        font-weight: 400;
    }
    
    /* Professional metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        margin: 1rem 0;
        color: white;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .metric-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.4);
    }
    
    .metric-card h3 {
        font-family: 'Inter', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .metric-card p {
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        font-weight: 500;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    
    /* Professional message styling */
    .success-message {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        color: #155724;
        font-weight: 600;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #28a745;
        box-shadow: 0 4px 15px rgba(40, 167, 69, 0.2);
        font-family: 'Inter', sans-serif;
    }
    
    .error-message {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        color: #721c24;
        font-weight: 600;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #dc3545;
        box-shadow: 0 4px 15px rgba(220, 53, 69, 0.2);
        font-family: 'Inter', sans-serif;
    }
    
    .warning-message {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        color: #856404;
        font-weight: 600;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #ffc107;
        box-shadow: 0 4px 15px rgba(255, 193, 7, 0.2);
        font-family: 'Inter', sans-serif;
    }
    
    .info-message {
        background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
        color: #0c5460;
        font-weight: 600;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #17a2b8;
        box-shadow: 0 4px 15px rgba(23, 162, 184, 0.2);
        font-family: 'Inter', sans-serif;
    }
    
    /* Professional card styling */
    .evaluation-card {
        background: #ffffff;
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
        margin: 1.5rem 0;
        border: 1px solid #e2e8f0;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .evaluation-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
    }
    
    .evaluation-card:hover {
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.12);
        transform: translateY(-4px);
    }
    
    /* Professional progress bars */
    .progress-container {
        background: #f7fafc;
        border-radius: 15px;
        padding: 4px;
        margin: 15px 0;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .progress-bar {
        height: 24px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
    }
    
    /* Professional button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        text-transform: none;
        letter-spacing: 0.025em;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Professional sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        box-shadow: 2px 0 20px rgba(0, 0, 0, 0.1);
    }
    
    .sidebar .sidebar-content {
        background: transparent;
    }
    
    /* Professional file upload styling */
    .uploadedFile {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border: 2px dashed #6c757d;
        border-radius: 15px;
        padding: 2.5rem;
        text-align: center;
        margin: 1.5rem 0;
        transition: all 0.3s ease;
    }
    
    .uploadedFile:hover {
        border-color: #667eea;
        background: linear-gradient(135deg, #f0f4ff 0%, #e6f3ff 100%);
    }
    
    /* Professional animations */
    @keyframes fadeInUp {
        from { 
            opacity: 0; 
            transform: translateY(30px); 
        }
        to { 
            opacity: 1; 
            transform: translateY(0); 
        }
    }
    
    .fade-in {
        animation: fadeInUp 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    /* Professional score indicators */
    .score-high {
        color: #28a745;
        font-weight: 700;
        font-size: 1.3rem;
        text-shadow: 0 1px 2px rgba(40, 167, 69, 0.3);
    }
    
    .score-medium {
        color: #ffc107;
        font-weight: 700;
        font-size: 1.3rem;
        text-shadow: 0 1px 2px rgba(255, 193, 7, 0.3);
    }
    
    .score-low {
        color: #dc3545;
        font-weight: 700;
        font-size: 1.3rem;
        text-shadow: 0 1px 2px rgba(220, 53, 69, 0.3);
    }
    
    /* Professional loading spinner */
    .loading-spinner {
        display: inline-block;
        width: 24px;
        height: 24px;
        border: 3px solid #f3f4f6;
        border-top: 3px solid #667eea;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Professional table styling */
    .dataframe {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    /* Professional form styling */
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 2px solid #e2e8f0;
        padding: 0.75rem;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    .stTextArea > div > div > textarea {
        border-radius: 8px;
        border: 2px solid #e2e8f0;
        padding: 0.75rem;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Professional selectbox styling */
    .stSelectbox > div > div > div {
        border-radius: 8px;
        border: 2px solid #e2e8f0;
        font-family: 'Inter', sans-serif;
    }
    
    /* Professional tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
    }
    
    /* Professional radio button styling */
    .stRadio > div {
        gap: 1rem;
    }
    
    .stRadio > div > label {
        font-family: 'Inter', sans-serif;
        font-weight: 500;
    }
    
    /* Professional checkbox styling */
    .stCheckbox > label {
        font-family: 'Inter', sans-serif;
        font-weight: 500;
    }
    
    /* Professional file uploader styling */
    .stFileUploader > div {
        border-radius: 12px;
        border: 2px dashed #6c757d;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        transition: all 0.3s ease;
    }
    
    .stFileUploader > div:hover {
        border-color: #667eea;
        background: linear-gradient(135deg, #f0f4ff 0%, #e6f3ff 100%);
    }
    
    /* Professional metric styling */
    .metric-container {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        border: 1px solid #e2e8f0;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .metric-container:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
    }
    
    /* Professional footer styling */
    .footer {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem 0;
        text-align: center;
        margin-top: 3rem;
        border-radius: 20px 20px 0 0;
    }
    
    .footer h4 {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .footer p {
        font-family: 'Inter', sans-serif;
        margin: 0.25rem 0;
        opacity: 0.9;
    }
    
    /* Advanced Styling for Unique Features */
    .feature-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        margin: 1rem 0;
        color: white;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .feature-card:hover::before {
        left: 100%;
    }
    
    .feature-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.4);
    }
    
    .timeline-item {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #667eea;
        transition: all 0.3s ease;
    }
    
    .timeline-item:hover {
        transform: translateX(10px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    }
    
    .skill-tag {
        display: inline-block;
        background: linear-gradient(135deg, #4ecdc4, #44a08d);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        margin: 0.25rem;
        font-size: 0.9rem;
        font-weight: 500;
        box-shadow: 0 2px 10px rgba(78, 205, 196, 0.3);
        transition: all 0.3s ease;
    }
    
    .skill-tag:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(78, 205, 196, 0.4);
    }
    
    .missing-skill-tag {
        display: inline-block;
        background: linear-gradient(135deg, #ff6b6b, #ee5a52);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        margin: 0.25rem;
        font-size: 0.9rem;
        font-weight: 500;
        box-shadow: 0 2px 10px rgba(255, 107, 107, 0.3);
        transition: all 0.3s ease;
    }
    
    .missing-skill-tag:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.4);
    }
    
    .pulse-animation {
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .floating-animation {
        animation: floating 3s ease-in-out infinite;
    }
    
    @keyframes floating {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    
    .gradient-text {
        background: linear-gradient(135deg, #667eea, #764ba2, #f093fb);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
    }
    
    .glass-effect {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .neon-glow {
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.5);
        border: 1px solid rgba(102, 126, 234, 0.3);
    }
    
    .neon-glow:hover {
        box-shadow: 0 0 30px rgba(102, 126, 234, 0.8);
    }
    
    .data-visualization {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    }
    
    .interactive-element {
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .interactive-element:hover {
        transform: scale(1.05);
        filter: brightness(1.1);
    }
    
    .progress-ring {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        background: conic-gradient(#667eea 0deg, #764ba2 180deg, #f093fb 360deg);
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
    }
    
    .progress-ring::before {
        content: '';
        width: 80px;
        height: 80px;
        border-radius: 50%;
        background: white;
        position: absolute;
    }
    
    .progress-ring-text {
        position: relative;
        z-index: 1;
        font-weight: 700;
        font-size: 1.2rem;
        color: #333;
    }
</style>
""", unsafe_allow_html=True)

def make_api_request(endpoint: str, method: str = "GET", data: Dict = None, files: Dict = None) -> Dict:
    """Make API request to backend."""
    try:
        url = f"{API_BASE_URL}{endpoint}"
        
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            if files:
                response = requests.post(url, files=files, data=data, timeout=30)
            else:
                response = requests.post(url, json=data, timeout=10)
        elif method == "DELETE":
            response = requests.delete(url, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return {}
    except requests.exceptions.Timeout:
        st.error("Request timed out. Please try again.")
        return {}
    except Exception as e:
        st.error(f"Connection Error: {str(e)}")
        return {}

def show_loading_spinner(message: str = "Processing..."):
    """Show loading spinner with message."""
    with st.spinner(message):
        time.sleep(0.5)

def create_progress_bar(score: float, label: str) -> str:
    """Create a custom progress bar HTML."""
    color = "#28a745" if score >= 80 else "#ffc107" if score >= 60 else "#dc3545"
    return f"""
    <div class="progress-container">
        <div class="progress-bar" style="width: {score}%; background: {color};">
            {score:.1f}%
        </div>
    </div>
    <p style="text-align: center; margin-top: 5px; font-weight: bold;">{label}</p>
    """

def create_metric_card(title: str, value: str, icon: str = "📊", color: str = "#1f77b4") -> str:
    """Create a custom metric card HTML."""
    return f"""
    <div class="metric-card" style="background: linear-gradient(135deg, {color} 0%, {color}88 100%);">
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <div>
                <h3 style="margin: 0; font-size: 1.5rem;">{value}</h3>
                <p style="margin: 5px 0 0 0; opacity: 0.9;">{title}</p>
            </div>
            <div style="font-size: 2rem;">{icon}</div>
        </div>
    </div>
    """

def get_score_color(score: float) -> str:
    """Get color based on score."""
    if score >= 80:
        return "#28a745"
    elif score >= 60:
        return "#ffc107"
    else:
        return "#dc3545"

def get_verdict_icon(verdict: str) -> str:
    """Get icon based on verdict."""
    if verdict.lower() == "high":
        return "🟢"
    elif verdict.lower() == "medium":
        return "🟡"
    else:
        return "🔴"

def upload_resume():
    """Upload resume form with enhanced UI."""
    st.markdown("### 📄 Upload Resume")
    
    # Create two columns for better layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.container():
            st.markdown('<div class="evaluation-card">', unsafe_allow_html=True)
            
            with st.form("upload_resume_form", clear_on_submit=True):
                # Student information
                st.markdown("#### 👤 Student Information")
                col_name, col_email = st.columns(2)
                
                with col_name:
                    student_name = st.text_input(
                        "Student Name", 
                        placeholder="Enter student name",
                        help="Full name of the student"
                    )
                
                with col_email:
                    student_email = st.text_input(
                        "Student Email", 
                        placeholder="Enter student email",
                        help="Valid email address"
                    )
                
                st.markdown("---")
                
                # File upload
                st.markdown("#### 📁 Resume File")
                resume_file = st.file_uploader(
                    "Choose Resume File", 
                    type=['pdf', 'docx', 'txt'],
                    help="Upload PDF, DOCX, or TXT resume file (max 10MB)"
                )
                
                # File preview
                if resume_file:
                    file_size = len(resume_file.getvalue()) / 1024 / 1024  # MB
                    st.info(f"📄 **File:** {resume_file.name} ({file_size:.2f} MB)")
                    
                    if file_size > 10:
                        st.error("⚠️ File size exceeds 10MB limit")
                    else:
                        st.success("✅ File size is within limits")
                
                st.markdown("---")
                
                # Submit button
                col_submit, col_clear = st.columns([1, 1])
                with col_submit:
                    submitted = st.form_submit_button(
                        "🚀 Upload Resume", 
                        use_container_width=True,
                        type="primary"
                    )
                with col_clear:
                    if st.form_submit_button("🗑️ Clear Form", use_container_width=True):
                        st.rerun()
                
                if submitted:
                    if not student_name or not student_email or not resume_file:
                        st.error("❌ Please fill in all fields and upload a file")
                        return
                    
                    if file_size > 10:
                        st.error("❌ File size exceeds 10MB limit")
                        return
                    
                    # Show progress
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    try:
                        # Prepare file for upload
                        files = {"file": (resume_file.name, resume_file.getvalue(), resume_file.type)}
                        data = {
                            "student_name": student_name,
                            "student_email": student_email
                        }
                        
                        # Simulate progress
                        progress_bar.progress(25)
                        status_text.text("📤 Uploading file...")
                        
                        response = requests.post(f"{API_BASE_URL}/resume", files=files, data=data, timeout=30)
                        
                        progress_bar.progress(75)
                        status_text.text("🔍 Processing resume...")
                        
                        if response.status_code == 200:
                            result = response.json()
                            progress_bar.progress(100)
                            status_text.text("✅ Upload complete!")
                            
                            # Success message with animation
                            st.markdown(f"""
                            <div class="success-message fade-in">
                                <h4>🎉 Resume Uploaded Successfully!</h4>
                                <p><strong>Resume ID:</strong> {result['resume_id']}</p>
                                <p><strong>Student:</strong> {result['student_name']}</p>
                                <p><strong>Email:</strong> {result['student_email']}</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            time.sleep(2)
                            st.rerun()
                        else:
                            st.error(f"❌ Upload failed: {response.text}")
                            
                    except requests.exceptions.Timeout:
                        st.error("⏰ Upload timed out. Please try again.")
                    except Exception as e:
                        st.error(f"❌ Upload error: {str(e)}")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Help section
        st.markdown("### 💡 Help")
        st.markdown("""
        **Supported Formats:**
        - PDF (.pdf)
        - Word (.docx)
        - Text (.txt)
        
        **File Requirements:**
        - Maximum size: 10MB
        - Clear, readable text
        - Standard resume format
        
        **Tips for Better Results:**
        - Use clear section headers
        - Include relevant skills
        - Mention projects and experience
        - Keep formatting simple
        """)
        
        # Recent uploads
        st.markdown("### 📋 Recent Uploads")
        resumes = make_api_request("/resumes/")
        if resumes:
            for resume in resumes[-3:]:  # Show last 3
                st.markdown(f"• **{resume['student_name']}** - {resume['filename']}")
        else:
            st.info("No resumes uploaded yet")

def upload_job_description():
    """Upload job description form with file upload support."""
    st.markdown("### 💼 Upload Job Description")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.container():
            st.markdown('<div class="evaluation-card">', unsafe_allow_html=True)
            
            # Upload method selection
            st.markdown("#### 📋 Choose Upload Method")
            upload_method = st.radio(
                "How would you like to upload the job description?",
                ["📁 Upload File (PDF/DOCX/TXT)", "✏️ Enter Text Manually"],
                horizontal=True
            )
            
            st.markdown("---")
            
            with st.form("upload_jd_form", clear_on_submit=True):
                # Job information
                st.markdown("#### 🏢 Job Information")
                col_title, col_company = st.columns(2)
                
                with col_title:
                    title = st.text_input(
                        "Job Title", 
                        placeholder="e.g., Software Engineer",
                        help="Position title"
                    )
                
                with col_company:
                    company = st.text_input(
                        "Company", 
                        placeholder="e.g., Tech Corp",
                        help="Company name"
                    )
                
                location = st.text_input(
                    "Location", 
                    placeholder="e.g., Hyderabad, Bangalore, Pune, Delhi",
                    help="Job location"
                )
                
                st.markdown("---")
                
                # Job description content
                st.markdown("#### 📝 Job Description")
                content = ""
                
                if upload_method == "📁 Upload File (PDF/DOCX/TXT)":
                    # File upload
                    jd_file = st.file_uploader(
                        "Choose Job Description File", 
                        type=['pdf', 'docx', 'txt'],
                        help="Upload PDF, DOCX, or TXT job description file (max 10MB)"
                    )
                    
                    if jd_file:
                        file_size = len(jd_file.getvalue()) / 1024 / 1024  # MB
                        st.info(f"📄 **File:** {jd_file.name} ({file_size:.2f} MB)")
                        
                        if file_size > 10:
                            st.error("⚠️ File size exceeds 10MB limit")
                        else:
                            st.success("✅ File size is within limits")
                            
                            # Extract text from file
                            try:
                                if jd_file.name.lower().endswith('.pdf'):
                                    import fitz
                                    doc = fitz.open(stream=jd_file.getvalue(), filetype="pdf")
                                    content = ""
                                    for page in doc:
                                        content += page.get_text()
                                    doc.close()
                                elif jd_file.name.lower().endswith('.docx'):
                                    import docx2txt
                                    content = docx2txt.process(BytesIO(jd_file.getvalue()))
                                elif jd_file.name.lower().endswith('.txt'):
                                    content = jd_file.getvalue().decode('utf-8')
                                
                                # Show extracted content preview
                                if content:
                                    st.markdown("#### 📖 Extracted Content Preview")
                                    with st.expander("View extracted text", expanded=False):
                                        st.text_area("Extracted Text", content, height=200, disabled=True)
                                    
                                    char_count = len(content)
                                    st.caption(f"Character count: {char_count}")
                                    if char_count < 100:
                                        st.warning("⚠️ Extracted text seems too short. Please check the file.")
                                    elif char_count > 5000:
                                        st.warning("⚠️ Extracted text is very long. Consider using a shorter file.")
                                else:
                                    st.error("❌ Could not extract text from file. Please try a different file.")
                                    
                            except Exception as e:
                                st.error(f"❌ Error extracting text from file: {str(e)}")
                                content = ""
                
                else:  # Manual text input
                    content = st.text_area(
                        "Job Description", 
                        placeholder="Paste the complete job description here...\n\nInclude:\n- Required skills\n- Qualifications\n- Responsibilities\n- Experience requirements",
                        height=300,
                        help="Paste the complete job description with all requirements"
                    )
                    
                    # Character count for manual input
                    if content:
                        char_count = len(content)
                        st.caption(f"Character count: {char_count}")
                        if char_count < 100:
                            st.warning("⚠️ Job description seems too short. Please provide more details.")
                        elif char_count > 5000:
                            st.warning("⚠️ Job description is very long. Consider summarizing.")
                
                st.markdown("---")
                
                # Submit button
                col_submit, col_clear = st.columns([1, 1])
                with col_submit:
                    submitted = st.form_submit_button(
                        "🚀 Upload Job Description", 
                        use_container_width=True,
                        type="primary"
                    )
                with col_clear:
                    if st.form_submit_button("🗑️ Clear Form", use_container_width=True):
                        st.rerun()
                
                if submitted:
                    if not title or not company or not content:
                        st.error("❌ Please fill in all required fields and provide job description content")
                        return
                    
                    if len(content) < 50:
                        st.error("❌ Job description is too short. Please provide more details.")
                        return
                    
                    # Show progress
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    try:
                        data = {
                            "title": title,
                            "company": company,
                            "location": location,
                            "content": content
                        }
                        
                        progress_bar.progress(25)
                        status_text.text("📤 Uploading job description...")
                        
                        result = make_api_request("/job-description/", "POST", data)
                        
                        progress_bar.progress(75)
                        status_text.text("🔍 Processing requirements...")
                        
                        if result:
                            progress_bar.progress(100)
                            status_text.text("✅ Upload complete!")
                            
                            st.markdown(f"""
                            <div class="success-message fade-in">
                                <h4>🎉 Job Description Uploaded Successfully!</h4>
                                <p><strong>Job ID:</strong> {result['job_description_id']}</p>
                                <p><strong>Position:</strong> {result['title']}</p>
                                <p><strong>Company:</strong> {result['company']}</p>
                                <p><strong>Location:</strong> {result['location']}</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            time.sleep(2)
                            st.rerun()
                        else:
                            st.error("❌ Upload failed. Please try again.")
                            
                    except Exception as e:
                        st.error(f"❌ Upload error: {str(e)}")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Help section
        st.markdown("### 💡 Help")
        st.markdown("""
        **Upload Methods:**
        - **File Upload**: Upload PDF, DOCX, or TXT files
        - **Manual Entry**: Paste text directly
        
        **Supported File Formats:**
        - PDF documents (.pdf)
        - Word documents (.docx)
        - Text files (.txt)
        - Maximum size: 10MB
        
        **Job Description Tips:**
        - Include specific skills required
        - Mention experience level needed
        - List key responsibilities
        - Add educational requirements
        - Include location details
        
        **Better Results:**
        - Be specific about technologies
        - Mention soft skills
        - Include company culture
        - Add growth opportunities
        """)
        
        # Recent job descriptions
        st.markdown("### 📋 Recent Job Descriptions")
        job_descriptions = make_api_request("/job-descriptions/")
        if job_descriptions:
            for jd in job_descriptions[-3:]:  # Show last 3
                st.markdown(f"• **{jd['title']}** at {jd['company']}")
        else:
            st.info("No job descriptions uploaded yet")

def evaluate_resume():
    """Evaluate resume against job description with enhanced UI."""
    st.markdown("### 🔍 Evaluate Resume")
    
    # Get resumes and job descriptions
    resumes = make_api_request("/resumes/")
    job_descriptions = make_api_request("/job-descriptions/")
    
    if not resumes or not job_descriptions:
        st.markdown("""
        <div class="warning-message">
            <h4>⚠️ No Data Available</h4>
            <p>Please upload resumes and job descriptions first before evaluating.</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.container():
            st.markdown('<div class="evaluation-card">', unsafe_allow_html=True)
            
            with st.form("evaluate_form"):
                st.markdown("#### 📋 Select Resume and Job Description")
                
                # Resume selection
                col_resume, col_jd = st.columns(2)
                
                with col_resume:
                    st.markdown("**Resume Selection**")
                    resume_options = {f"{r['student_name']} ({r['filename']})": r for r in resumes}
                    selected_resume_key = st.selectbox(
                        "Choose Resume", 
                        list(resume_options.keys()),
                        help="Select a resume to evaluate"
                    )
                    
                    if selected_resume_key:
                        selected_resume = resume_options[selected_resume_key]
                        st.info(f"📄 **Selected:** {selected_resume['student_name']}")
                        st.caption(f"Email: {selected_resume['student_email']}")
                
                with col_jd:
                    st.markdown("**Job Description Selection**")
                    jd_options = {f"{jd['title']} at {jd['company']}": jd for jd in job_descriptions}
                    selected_jd_key = st.selectbox(
                        "Choose Job Description", 
                        list(jd_options.keys()),
                        help="Select a job description to evaluate against"
                    )
                    
                    if selected_jd_key:
                        selected_jd = jd_options[selected_jd_key]
                        st.info(f"💼 **Selected:** {selected_jd['title']}")
                        st.caption(f"Company: {selected_jd['company']} | Location: {selected_jd['location']}")
                
                st.markdown("---")
                
                # Evaluation options
                st.markdown("#### ⚙️ Evaluation Options")
                col_options1, col_options2 = st.columns(2)
                
                with col_options1:
                    include_llm_analysis = st.checkbox("🤖 Include AI Analysis", value=True, help="Use LLM for detailed feedback")
                    show_detailed_scores = st.checkbox("📊 Show Detailed Scores", value=True, help="Display breakdown of scoring")
                
                with col_options2:
                    generate_suggestions = st.checkbox("💡 Generate Suggestions", value=True, help="Provide improvement suggestions")
                    export_results = st.checkbox("📤 Export Results", value=False, help="Download evaluation results")
                
                st.markdown("---")
                
                # Submit button
                col_submit, col_clear = st.columns([1, 1])
                with col_submit:
                    submitted = st.form_submit_button(
                        "🚀 Start Evaluation", 
                        use_container_width=True,
                        type="primary"
                    )
                with col_clear:
                    if st.form_submit_button("🗑️ Clear Selection", use_container_width=True):
                        st.rerun()
                
                if submitted:
                    if not selected_resume_key or not selected_jd_key:
                        st.error("❌ Please select both resume and job description")
                        return
                    
                    # Show evaluation progress
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    try:
                        data = {
                            "resume_id": selected_resume['id'],
                            "job_description_id": selected_jd['id']
                        }
                        
                        # Simulate progress steps
                        progress_bar.progress(10)
                        status_text.text("🔍 Analyzing resume content...")
                        time.sleep(1)
                        
                        progress_bar.progress(30)
                        status_text.text("🔍 Parsing job requirements...")
                        time.sleep(1)
                        
                        progress_bar.progress(50)
                        status_text.text("⚖️ Performing hard matching...")
                        time.sleep(1)
                        
                        progress_bar.progress(70)
                        status_text.text("🧠 Running semantic analysis...")
                        time.sleep(1)
                        
                        progress_bar.progress(90)
                        status_text.text("📝 Generating feedback...")
                        
                        result = make_api_request("/evaluate/", "POST", data)
                        
                        progress_bar.progress(100)
                        status_text.text("✅ Evaluation complete!")
                        
                        if result:
                            st.markdown("""
                            <div class="success-message fade-in">
                                <h4>🎉 Evaluation Completed Successfully!</h4>
                                <p>Resume has been evaluated against the job description.</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Store result in session state to display outside form
                            st.session_state.evaluation_result = result
                            st.session_state.show_detailed_scores = show_detailed_scores
                            st.session_state.generate_suggestions = generate_suggestions
                            st.session_state.export_results = export_results
                            
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("❌ Evaluation failed. Please try again.")
                            
                    except Exception as e:
                        st.error(f"❌ Evaluation error: {str(e)}")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Display evaluation results if available (outside form context)
    if 'evaluation_result' in st.session_state:
        st.markdown("---")
        display_evaluation_results(
            st.session_state.evaluation_result, 
            st.session_state.show_detailed_scores, 
            st.session_state.generate_suggestions, 
            st.session_state.export_results
        )
        # Clear the evaluation result from session state
        del st.session_state.evaluation_result
        del st.session_state.show_detailed_scores
        del st.session_state.generate_suggestions
        del st.session_state.export_results
    
    with col2:
        # Quick stats
        st.markdown("### 📊 Quick Stats")
        
        # Resume stats
        st.markdown("#### 📄 Resumes")
        st.markdown(create_metric_card("Total Resumes", str(len(resumes)), "📄", "#1f77b4"), unsafe_allow_html=True)
        
        # Job description stats
        st.markdown("#### 💼 Job Descriptions")
        st.markdown(create_metric_card("Total Jobs", str(len(job_descriptions)), "💼", "#ff7f0e"), unsafe_allow_html=True)
        
        # Recent evaluations
        st.markdown("#### 🔍 Recent Evaluations")
        evaluations = make_api_request("/evaluations/")
        if evaluations:
            for eval in evaluations[-3:]:  # Show last 3
                verdict_icon = get_verdict_icon(eval['verdict'])
                st.markdown(f"• {verdict_icon} **{eval['verdict']}** - Score: {eval['relevance_score']:.1f}")
        else:
            st.info("No evaluations yet")
        
        # Tips
        st.markdown("#### 💡 Tips")
        st.markdown("""
        **For Better Results:**
        - Use detailed job descriptions
        - Include specific skills in resumes
        - Mention relevant projects
        - Add certifications and education
        
        **Understanding Scores:**
        - **80+**: Excellent match
        - **60-79**: Good match
        - **Below 60**: Needs improvement
        """)

def display_evaluation_results(evaluation: Dict[str, Any], show_detailed_scores: bool = True, 
                             generate_suggestions: bool = True, export_results: bool = False):
    """Display evaluation results with enhanced UI."""
    st.markdown("### 📊 Evaluation Results")
    
    # Main score display with visual progress bars
    st.markdown('<div class="evaluation-card">', unsafe_allow_html=True)
    
    # Overall score with large display
    relevance_score = evaluation['relevance_score']
    verdict = evaluation['verdict']
    verdict_icon = get_verdict_icon(verdict)
    score_color = get_score_color(relevance_score)
    
    st.markdown(f"""
    <div style="text-align: center; margin: 2rem 0;">
        <h1 style="color: {score_color}; font-size: 4rem; margin: 0;">{relevance_score:.1f}</h1>
        <h2 style="margin: 0;">{verdict_icon} {verdict} Suitability</h2>
        <p style="color: #666; font-size: 1.2rem;">Overall Relevance Score</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress bar for overall score
    st.markdown(create_progress_bar(relevance_score, "Overall Relevance"), unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Detailed scores in tabs
    if show_detailed_scores:
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Scores", "❌ Missing Elements", "✅ Strengths & Weaknesses", "💡 Feedback", "🎯 Advanced Analysis"])
        
        with tab1:
            st.markdown("#### Detailed Score Breakdown")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(create_progress_bar(evaluation['hard_match_score'], "Hard Match Score"), unsafe_allow_html=True)
                st.caption("Keyword and skill matching")
            
            with col2:
                st.markdown(create_progress_bar(evaluation['semantic_match_score'], "Semantic Match Score"), unsafe_allow_html=True)
                st.caption("AI-powered semantic analysis")
            
            with col3:
                st.markdown(f"""
                <div style="text-align: center; padding: 1rem; background: #f8f9fa; border-radius: 10px;">
                    <h3 style="margin: 0; color: {score_color};">{verdict}</h3>
                    <p style="margin: 5px 0 0 0; color: #666;">Final Verdict</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Score comparison chart
            scores_data = {
                'Score Type': ['Hard Match', 'Semantic Match', 'Overall'],
                'Score': [evaluation['hard_match_score'], evaluation['semantic_match_score'], evaluation['relevance_score']]
            }
            
            df_scores = pd.DataFrame(scores_data)
            fig = px.bar(df_scores, x='Score Type', y='Score', 
                        color='Score', color_continuous_scale='RdYlGn',
                        title="Score Breakdown")
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            st.markdown("#### Missing Elements Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("##### 🚫 Missing Skills")
                if evaluation['missing_skills']:
                    for skill in evaluation['missing_skills']:
                        st.markdown(f"• ❌ {skill}")
                else:
                    st.success("✅ No missing skills identified!")
                
                st.markdown("##### 🎓 Missing Certifications")
                if evaluation['missing_certifications']:
                    for cert in evaluation['missing_certifications']:
                        st.markdown(f"• ❌ {cert}")
                else:
                    st.success("✅ No missing certifications identified!")
            
            with col2:
                st.markdown("##### 📚 Suggested Projects")
                if evaluation['missing_projects']:
                    for project in evaluation['missing_projects']:
                        st.markdown(f"• 💡 {project}")
                else:
                    st.info("ℹ️ No specific projects suggested")
                
                st.markdown("##### 🎯 Missing Qualifications")
                missing_qualifications = evaluation.get('missing_qualifications', [])
                if missing_qualifications:
                    for qual in missing_qualifications:
                        st.markdown(f"• ❌ {qual}")
                else:
                    st.success("✅ No missing qualifications identified!")
        
        with tab3:
            st.markdown("#### Strengths & Weaknesses Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("##### ✅ Strengths")
                if evaluation['strengths']:
                    for i, strength in enumerate(evaluation['strengths'], 1):
                        st.markdown(f"**{i}.** ✅ {strength}")
                else:
                    st.info("ℹ️ No specific strengths identified")
            
            with col2:
                st.markdown("##### ⚠️ Weaknesses")
                if evaluation['weaknesses']:
                    for i, weakness in enumerate(evaluation['weaknesses'], 1):
                        st.markdown(f"**{i}.** ⚠️ {weakness}")
                else:
                    st.info("ℹ️ No specific weaknesses identified")
        
        with tab4:
            st.markdown("#### AI-Generated Feedback")
            
            if generate_suggestions and evaluation['improvement_suggestions']:
                st.markdown("##### 💡 Improvement Suggestions")
                st.markdown(f"""
                <div style="background: #e8f5e8; padding: 1rem; border-radius: 10px; border-left: 4px solid #28a745;">
                    {evaluation['improvement_suggestions']}
                </div>
                """, unsafe_allow_html=True)
            
            if evaluation['overall_feedback']:
                st.markdown("##### 📝 Overall Assessment")
                st.markdown(f"""
                <div style="background: #f8f9fa; padding: 1rem; border-radius: 10px; border-left: 4px solid #17a2b8;">
                    {evaluation['overall_feedback']}
                </div>
                """, unsafe_allow_html=True)
        
        with tab5:
            st.markdown("#### 🎯 Advanced Analysis")
            
            # Resume vs Job Comparison
            create_resume_job_comparison_chart(evaluation)
            
            st.markdown("---")
            
            # Skill Gap Analysis
            create_skill_gap_analysis(evaluation)
            
            st.markdown("---")
            
            # Resume Quality Score
            create_resume_quality_score(evaluation)
            
            st.markdown("---")
            
            # Resume Timeline
            create_resume_timeline(evaluation)
            
            st.markdown("---")
            
            # AI Optimization Suggestions
            create_ai_optimization_suggestions(evaluation)
    
    # Export functionality
    if export_results:
        st.markdown("---")
        st.markdown("#### 📤 Export Results")
        
        # Create downloadable data
        export_data = {
            'relevance_score': evaluation['relevance_score'],
            'hard_match_score': evaluation['hard_match_score'],
            'semantic_match_score': evaluation['semantic_match_score'],
            'verdict': evaluation['verdict'],
            'missing_skills': evaluation['missing_skills'],
            'strengths': evaluation['strengths'],
            'weaknesses': evaluation['weaknesses'],
            'improvement_suggestions': evaluation['improvement_suggestions'],
            'overall_feedback': evaluation['overall_feedback']
        }
        
        # Convert to JSON
        json_data = json.dumps(export_data, indent=2)
        
        # Create download button
        st.download_button(
            label="📥 Download Results as JSON",
            data=json_data,
            file_name=f"evaluation_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    
    # Quick action buttons
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Evaluate Another Resume", use_container_width=True):
            st.rerun()
    
    with col2:
        if st.button("📊 View All Evaluations", use_container_width=True):
            st.session_state.page = "View Evaluations"
            st.rerun()
    
    with col3:
        if st.button("🏠 Back to Dashboard", use_container_width=True):
            st.session_state.page = "Dashboard"
            st.rerun()

def view_evaluations():
    """View all evaluations with enhanced UI."""
    st.markdown("### 📋 All Evaluations")
    
    # Get evaluations
    evaluations = make_api_request("/evaluations/")
    
    if not evaluations:
        st.markdown("""
        <div class="info-message">
            <h4>ℹ️ No Evaluations Found</h4>
            <p>Please evaluate some resumes first to see results here.</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Create DataFrame
    df = pd.DataFrame(evaluations)
    
    # Summary statistics with enhanced cards
    st.markdown("#### 📊 Summary Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_score = df['relevance_score'].mean()
        st.markdown(create_metric_card("Average Score", f"{avg_score:.1f}", "📊", "#1f77b4"), unsafe_allow_html=True)
    
    with col2:
        high_count = len(df[df['verdict'] == 'High'])
        st.markdown(create_metric_card("High Suitability", str(high_count), "🟢", "#28a745"), unsafe_allow_html=True)
    
    with col3:
        medium_count = len(df[df['verdict'] == 'Medium'])
        st.markdown(create_metric_card("Medium Suitability", str(medium_count), "🟡", "#ffc107"), unsafe_allow_html=True)
    
    with col4:
        total_count = len(df)
        st.markdown(create_metric_card("Total Evaluations", str(total_count), "📋", "#6c757d"), unsafe_allow_html=True)
    
    # Charts section
    st.markdown("#### 📈 Analytics Dashboard")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Verdict distribution
        verdict_counts = df['verdict'].value_counts()
        fig = px.pie(values=verdict_counts.values, names=verdict_counts.index, 
                     title="Verdict Distribution",
                     color_discrete_map={'High': '#28a745', 'Medium': '#ffc107', 'Low': '#dc3545'})
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Score distribution
        fig = px.histogram(df, x='relevance_score', nbins=20, 
                          title="Score Distribution",
                          color_discrete_sequence=['#1f77b4'])
        fig.update_layout(xaxis_title="Relevance Score", yaxis_title="Count")
        st.plotly_chart(fig, use_container_width=True)
    
    # Score trends over time
    if 'created_at' in df.columns:
        df['created_at'] = pd.to_datetime(df['created_at'])
        df_sorted = df.sort_values('created_at')
        
        fig = px.line(df_sorted, x='created_at', y='relevance_score',
                     title="Score Trends Over Time",
                     color_discrete_sequence=['#ff7f0e'])
        fig.update_layout(xaxis_title="Date", yaxis_title="Relevance Score")
        st.plotly_chart(fig, use_container_width=True)
    
    # Filtering and search
    st.markdown("#### 🔍 Filter & Search")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        verdict_filter = st.selectbox("Filter by Verdict", ["All", "High", "Medium", "Low"])
    
    with col2:
        score_range = st.slider("Score Range", 0, 100, (0, 100))
    
    with col3:
        search_term = st.text_input("Search", placeholder="Search by ID or other fields")
    
    # Apply filters
    filtered_df = df.copy()
    
    if verdict_filter != "All":
        filtered_df = filtered_df[filtered_df['verdict'] == verdict_filter]
    
    filtered_df = filtered_df[
        (filtered_df['relevance_score'] >= score_range[0]) & 
        (filtered_df['relevance_score'] <= score_range[1])
    ]
    
    if search_term:
        filtered_df = filtered_df[filtered_df.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)]
    
    # Results table with enhanced display
    st.markdown(f"#### 📋 Evaluation Results ({len(filtered_df)} found)")
    
    if len(filtered_df) > 0:
        # Add color coding for verdicts
        def color_verdict(val):
            if val == 'High':
                return 'background-color: #d4edda; color: #155724'
            elif val == 'Medium':
                return 'background-color: #fff3cd; color: #856404'
            elif val == 'Low':
                return 'background-color: #f8d7da; color: #721c24'
            return ''
        
        # Display table with styling
        styled_df = filtered_df.style.applymap(color_verdict, subset=['verdict'])
        st.dataframe(styled_df, use_container_width=True)
        
        # Action buttons for each row
        st.markdown("#### ⚡ Quick Actions")
        
        if st.button("📥 Export Filtered Results", use_container_width=True):
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"evaluations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.rerun()
    else:
        st.info("No evaluations match the current filters.")
    
    # Detailed view option
    if len(filtered_df) > 0:
        st.markdown("#### 🔍 Detailed View")
        
        selected_eval_id = st.selectbox(
            "Select evaluation to view details:",
            options=filtered_df['id'].tolist(),
            format_func=lambda x: f"ID {x} - Score: {filtered_df[filtered_df['id']==x]['relevance_score'].iloc[0]:.1f} - {filtered_df[filtered_df['id']==x]['verdict'].iloc[0]}"
        )
        
        if selected_eval_id:
            # Get detailed evaluation
            detailed_eval = make_api_request(f"/evaluations/{selected_eval_id}")
            if detailed_eval:
                with st.expander("View Detailed Results", expanded=True):
                    display_evaluation_results(detailed_eval, show_detailed_scores=True, generate_suggestions=True, export_results=True)

def manage_data():
    """Manage resumes and job descriptions."""
    st.subheader("🗂️ Data Management")
    
    tab1, tab2 = st.tabs(["Resumes", "Job Descriptions"])
    
    with tab1:
        st.write("**Resumes**")
        resumes = make_api_request("/resumes")
        
        if resumes:
            for resume in resumes:
                with st.expander(f"{resume['student_name']} - {resume['filename']}"):
                    st.write(f"**Email:** {resume['student_email']}")
                    st.write(f"**Uploaded:** {resume['created_at']}")
                    
                    if st.button(f"Delete {resume['filename']}", key=f"delete_resume_{resume['id']}"):
                        result = make_api_request(f"/resumes/{resume['id']}", "DELETE")
                        if result:
                            st.success("Resume deleted successfully")
                            st.rerun()
        else:
            st.info("No resumes found")
    
    with tab2:/
        st.write("**Job Descriptions**")
        job_descriptions = make_api_request("/job-descriptions/")
        
        if job_descriptions:
            for jd in job_descriptions:
                with st.expander(f"{jd['title']} at {jd['company']}"):
                    st.write(f"**Location:** {jd['location']}")
                    st.write(f"**Uploaded:** {jd['created_at']}")
                    
                    if st.button(f"Delete {jd['title']}", key=f"delete_jd_{jd['id']}"):
                        result = make_api_request(f"/job-descriptions/{jd['id']}", "DELETE")
                        if result:
                            st.success("Job description deleted successfully")
                            st.rerun()
        else:
            st.info("No job descriptions found")

def create_resume_job_comparison_chart(evaluation):
    """Create a visual comparison chart between resume and job requirements."""
    # Extract data for comparison
    resume_skills = evaluation.get('resume_skills', [])
    job_skills = evaluation.get('job_skills', [])
    matched_skills = evaluation.get('matched_skills', [])
    missing_skills = evaluation.get('missing_skills', [])
    
    # Create comparison data
    comparison_data = {
        'Category': ['Resume Skills', 'Job Requirements', 'Matched Skills', 'Missing Skills'],
        'Count': [len(resume_skills), len(job_skills), len(matched_skills), len(missing_skills)],
        'Color': ['#4ecdc4', '#ff6b6b', '#45b7d1', '#ffa726']
    }
    
    df = pd.DataFrame(comparison_data)
    
    # Create horizontal bar chart
    fig = px.bar(
        df, 
        x='Count', 
        y='Category',
        color='Color',
        orientation='h',
        title="Resume vs Job Requirements Comparison",
        color_discrete_map={'#4ecdc4': '#4ecdc4', '#ff6b6b': '#ff6b6b', '#45b7d1': '#45b7d1', '#ffa726': '#ffa726'}
    )
    
    fig.update_layout(
        height=300,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        font=dict(size=12)
    )
    
    st.plotly_chart(fig, use_container_width=True)

def create_skill_gap_analysis(evaluation):
    """Create an interactive skill gap analysis with progress tracking."""
    missing_skills = evaluation.get('missing_skills', [])
    matched_skills = evaluation.get('matched_skills', [])
    
    if not missing_skills and not matched_skills:
        st.info("No skill analysis data available")
        return
    
    st.markdown("#### 🎯 Skill Gap Analysis")
    
    # Create skill categories
    technical_skills = []
    soft_skills = []
    tools_skills = []
    
    all_skills = missing_skills + matched_skills
    for skill in all_skills:
        skill_lower = skill.lower()
        if any(tech in skill_lower for tech in ['python', 'java', 'javascript', 'react', 'angular', 'vue', 'node', 'sql', 'mongodb', 'postgresql', 'docker', 'aws', 'azure']):
            technical_skills.append(skill)
        elif any(soft in skill_lower for soft in ['communication', 'leadership', 'teamwork', 'problem solving', 'analytical', 'creative', 'management']):
            soft_skills.append(skill)
        else:
            tools_skills.append(skill)
    
    # Create skill gap visualization
    categories = ['Technical Skills', 'Soft Skills', 'Tools & Technologies']
    matched_counts = [
        len([s for s in technical_skills if s in matched_skills]),
        len([s for s in soft_skills if s in matched_skills]),
        len([s for s in tools_skills if s in matched_skills])
    ]
    missing_counts = [
        len([s for s in technical_skills if s in missing_skills]),
        len([s for s in soft_skills if s in missing_skills]),
        len([s for s in tools_skills if s in missing_skills])
    ]
    
    # Create stacked bar chart
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Matched Skills',
        x=categories,
        y=matched_counts,
        marker_color='#4ecdc4',
        text=matched_counts,
        textposition='auto'
    ))
    
    fig.add_trace(go.Bar(
        name='Missing Skills',
        x=categories,
        y=missing_counts,
        marker_color='#ff6b6b',
        text=missing_counts,
        textposition='auto'
    ))
    
    fig.update_layout(
        barmode='stack',
        title="Skill Gap Analysis by Category",
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def create_resume_quality_score(evaluation):
    """Create a detailed resume quality score breakdown."""
    st.markdown("#### 📋 Resume Quality Analysis")
    
    # Calculate quality metrics
    resume_data = evaluation.get('resume_data', {})
    
    # Content completeness
    has_skills = len(resume_data.get('skills', [])) > 0
    has_education = len(resume_data.get('education', [])) > 0
    has_experience = len(resume_data.get('experience', [])) > 0
    has_projects = len(resume_data.get('projects', [])) > 0
    has_certifications = len(resume_data.get('certifications', [])) > 0
    
    completeness_score = sum([has_skills, has_education, has_experience, has_projects, has_certifications]) * 20
    
    # Skill relevance
    matched_skills = evaluation.get('matched_skills', [])
    total_skills = len(resume_data.get('skills', []))
    relevance_score = (len(matched_skills) / max(total_skills, 1)) * 100
    
    # Experience level
    experience_years = len(resume_data.get('experience', [])) * 2  # Rough estimate
    experience_score = min(experience_years * 10, 100)
    
    # Overall quality score
    quality_score = (completeness_score + relevance_score + experience_score) / 3
    
    # Create quality breakdown
    quality_data = {
        'Metric': ['Content Completeness', 'Skill Relevance', 'Experience Level', 'Overall Quality'],
        'Score': [completeness_score, relevance_score, experience_score, quality_score],
        'Color': ['#ff6b6b', '#4ecdc4', '#45b7d1', '#2ecc71']
    }
    
    df = pd.DataFrame(quality_data)
    
    # Create radar chart
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=df['Score'],
        theta=df['Metric'],
        fill='toself',
        name='Resume Quality',
        line_color='#667eea',
        fillcolor='rgba(102, 126, 234, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        title="Resume Quality Breakdown",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Quality recommendations
    st.markdown("##### 💡 Quality Improvement Tips")
    recommendations = []
    
    if completeness_score < 80:
        recommendations.append("Add more detailed sections (projects, certifications)")
    if relevance_score < 70:
        recommendations.append("Focus on skills relevant to target positions")
    if experience_score < 60:
        recommendations.append("Include more detailed work experience")
    
    if recommendations:
        for rec in recommendations:
            st.markdown(f"• {rec}")
    else:
        st.success("✅ Resume quality is excellent!")

def create_resume_timeline(evaluation):
    """Create an interactive resume timeline visualization."""
    st.markdown("#### ⏰ Resume Timeline")
    
    resume_data = evaluation.get('resume_data', {})
    education = resume_data.get('education', [])
    experience = resume_data.get('experience', [])
    
    if not education and not experience:
        st.info("No timeline data available")
        return
    
    # Create timeline data
    timeline_data = []
    
    # Add education entries
    for edu in education:
        timeline_data.append({
            'Type': 'Education',
            'Title': edu.get('degree', 'Education'),
            'Institution': edu.get('institution', 'Unknown'),
            'Year': edu.get('year', 'Unknown'),
            'Color': '#4ecdc4'
        })
    
    # Add experience entries
    for exp in experience:
        timeline_data.append({
            'Type': 'Experience',
            'Title': exp.get('position', 'Position'),
            'Institution': exp.get('company', 'Company'),
            'Year': exp.get('duration', 'Unknown'),
            'Color': '#ff6b6b'
        })
    
    if not timeline_data:
        st.info("No timeline data available")
        return
    
    # Create timeline visualization
    df = pd.DataFrame(timeline_data)
    
    fig = px.scatter(
        df,
        x='Year',
        y='Type',
        color='Type',
        size=[20] * len(df),
        hover_data=['Title', 'Institution'],
        title="Resume Timeline",
        color_discrete_map={'Education': '#4ecdc4', 'Experience': '#ff6b6b'}
    )
    
    fig.update_layout(
        height=300,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def create_ai_optimization_suggestions(evaluation):
    """Create AI-powered resume optimization suggestions."""
    st.markdown("#### 🤖 AI-Powered Optimization Suggestions")
    
    # Get evaluation data
    missing_skills = evaluation.get('missing_skills', [])
    strengths = evaluation.get('strengths', [])
    weaknesses = evaluation.get('weaknesses', [])
    
    # Create optimization categories
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### 🎯 Immediate Improvements")
        immediate_tips = []
        
        if missing_skills:
            immediate_tips.append(f"**Learn these skills:** {', '.join(missing_skills[:3])}")
        
        if 'Limited project portfolio' in weaknesses:
            immediate_tips.append("**Add 2-3 detailed projects** with technologies used")
        
        if 'No relevant certifications' in weaknesses:
            immediate_tips.append("**Get certified** in key technologies")
        
        if not immediate_tips:
            immediate_tips.append("**Resume looks good!** Focus on interview preparation")
        
        for tip in immediate_tips:
            st.markdown(f"• {tip}")
    
    with col2:
        st.markdown("##### 🚀 Advanced Optimizations")
        advanced_tips = []
        
        advanced_tips.append("**Quantify achievements** with specific numbers")
        advanced_tips.append("**Use action verbs** (developed, implemented, optimized)")
        advanced_tips.append("**Tailor keywords** to job descriptions")
        advanced_tips.append("**Add a professional summary** highlighting key strengths")
        
        for tip in advanced_tips:
            st.markdown(f"• {tip}")
    
    # Create optimization score
    optimization_score = 100 - len(missing_skills) * 10
    optimization_score = max(optimization_score, 0)
    
    st.markdown(f"##### 📊 Optimization Score: {optimization_score}/100")
    
    # Progress bar for optimization
    progress_color = "#4ecdc4" if optimization_score >= 70 else "#ff6b6b" if optimization_score >= 40 else "#ffa726"
    
    st.markdown(f"""
    <div class="progress-container">
        <div class="progress-bar" style="width: {optimization_score}%; background: {progress_color};">
            {optimization_score}%
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_batch_processing_interface():
    """Create interface for batch resume processing."""
    st.markdown("#### 📦 Batch Resume Processing")
    
    # File upload for multiple resumes
    uploaded_files = st.file_uploader(
        "Upload Multiple Resumes",
        type=['pdf', 'docx', 'txt'],
        accept_multiple_files=True,
        help="Select multiple resume files for batch processing"
    )
    
    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} files selected for processing")
        
        # Process button
        if st.button("🚀 Process All Resumes", type="primary"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            results = []
            
            for i, file in enumerate(uploaded_files):
                status_text.text(f"Processing {file.name}...")
                
                # Simulate processing
                time.sleep(1)
                
                # Mock result
                result = {
                    'filename': file.name,
                    'score': 75 + (i * 5) % 25,  # Mock score
                    'status': 'Processed'
                }
                results.append(result)
                
                progress_bar.progress((i + 1) / len(uploaded_files))
            
            status_text.text("✅ Batch processing complete!")
            
            # Display results
            results_df = pd.DataFrame(results)
            st.dataframe(results_df, use_container_width=True)
            
            # Download results
            csv = results_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Batch Results",
                data=csv,
                file_name=f"batch_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

def main():
    """Main dashboard function with enhanced UI and session state management."""
    # Initialize session state
    if 'page' not in st.session_state:
        st.session_state.page = "Dashboard"
    
    # Professional header
    st.markdown('<h1 class="main-header">📄 Resume Evaluation System</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI-powered resume analysis for placement teams</p>', unsafe_allow_html=True)
    
    # Sidebar navigation with enhanced styling
    with st.sidebar:
        st.markdown("### 🧭 Navigation")
        
        # Navigation buttons
        nav_options = {
            "🏠 Dashboard": "Dashboard",
            "📄 Upload Resume": "Upload Resume",
            "💼 Upload Job Description": "Upload Job Description",
            "🔍 Evaluate Resume": "Evaluate Resume",
            "📋 View Evaluations": "View Evaluations",
            "📦 Batch Processing": "Batch Processing",
            "🗂️ Manage Data": "Manage Data"
        }
        
        for display_name, page_name in nav_options.items():
            if st.button(display_name, use_container_width=True, key=f"nav_{page_name}"):
                st.session_state.page = page_name
                st.rerun()
        
        st.markdown("---")
        
        # System status
        st.markdown("### 🔧 System Status")
        
        # Check API connection
        try:
            response = requests.get(f"{API_BASE_URL}/", timeout=5)
            if response.status_code == 200:
                st.success("🟢 API Connected")
            else:
                st.error("🔴 API Error")
        except:
            st.error("🔴 API Offline")
        
        # Quick stats in sidebar
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
        
        st.markdown("---")
        
        # Help section
        st.markdown("### 💡 Help")
        st.markdown("""
        **Getting Started:**
        1. Upload job descriptions
        2. Upload student resumes
        3. Evaluate resumes
        4. View results
        
        **Need Help?**
        - Check the help sections
        - Review the tips
        - Contact support
        """)
    
    # Main content area
    if st.session_state.page == "Dashboard":
        st.markdown("### 📊 Dashboard Overview")
        
        # Welcome message
        st.markdown("""
        <div class="info-message">
            <h4>🎉 Welcome to the Resume Evaluation System!</h4>
            <p>Use the navigation menu to get started with uploading resumes and job descriptions, then evaluate them using our AI-powered system.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Enhanced metrics display
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(create_metric_card("Total Resumes", str(len(resumes) if resumes else 0), "📄", "#1f77b4"), unsafe_allow_html=True)
        
        with col2:
            st.markdown(create_metric_card("Total Job Descriptions", str(len(job_descriptions) if job_descriptions else 0), "💼", "#ff7f0e"), unsafe_allow_html=True)
        
        with col3:
            st.markdown(create_metric_card("Total Evaluations", str(len(evaluations) if evaluations else 0), "🔍", "#28a745"), unsafe_allow_html=True)
        
        with col4:
            if evaluations:
                avg_score = sum(e['relevance_score'] for e in evaluations) / len(evaluations)
                st.markdown(create_metric_card("Average Score", f"{avg_score:.1f}", "📊", "#6c757d"), unsafe_allow_html=True)
            else:
                st.markdown(create_metric_card("Average Score", "N/A", "📊", "#6c757d"), unsafe_allow_html=True)
        
        # Quick actions with enhanced buttons
        st.markdown("### 🚀 Quick Actions")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📄 Upload New Resume", use_container_width=True, type="primary"):
                st.session_state.page = "Upload Resume"
                st.rerun()
        
        with col2:
            if st.button("💼 Upload Job Description", use_container_width=True, type="primary"):
                st.session_state.page = "Upload Job Description"
                st.rerun()
        
        with col3:
            if st.button("🔍 Evaluate Resume", use_container_width=True, type="primary"):
                st.session_state.page = "Evaluate Resume"
                st.rerun()
        
        # Recent activity
        if evaluations:
            st.markdown("### 📈 Recent Activity")
            
            recent_evaluations = evaluations[-5:]  # Last 5 evaluations
            
            for eval in recent_evaluations:
                verdict_icon = get_verdict_icon(eval['verdict'])
                st.markdown(f"""
                <div class="evaluation-card" style="margin: 0.5rem 0;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <strong>Evaluation #{eval['id']}</strong>
                            <p style="margin: 0; color: #666;">Score: {eval['relevance_score']:.1f}</p>
                        </div>
                        <div style="font-size: 1.5rem;">{verdict_icon}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # System information
        st.markdown("### ℹ️ System Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Features:**
            - AI-powered resume analysis
            - Semantic matching with LLM
            - Detailed feedback generation
            - Export and reporting
            - Real-time evaluation
            """)
        
        with col2:
            st.markdown("""
            **Supported Formats:**
            - **Resumes**: PDF, DOCX, TXT
            - **Job Descriptions**: PDF, DOCX, TXT
            - **File Upload**: Both resume and JD uploads
            - **Maximum file size**: 10MB
            """)
    
    elif st.session_state.page == "Upload Resume":
        upload_resume()
    
    elif st.session_state.page == "Upload Job Description":
        upload_job_description()
    
    elif st.session_state.page == "Evaluate Resume":
        evaluate_resume()
    
    elif st.session_state.page == "View Evaluations":
        view_evaluations()
    
    elif st.session_state.page == "Batch Processing":
        create_batch_processing_interface()
    
    elif st.session_state.page == "Analytics":
        create_advanced_analytics()
    
    elif st.session_state.page == "Manage Data":
        manage_data()
    
    # Professional footer
    st.markdown("""
    <div class="footer">
        <h4>📄 Resume Evaluation System</h4>
        <p>Powered by AI and Machine Learning | Built for Innomatics Research Labs</p>
        <p style="font-size: 0.9rem; opacity: 0.8;">© 2024 - All rights reserved</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()


