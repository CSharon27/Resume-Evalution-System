# HireLens - Automated Resume Relevance Check System

**HireLens** is an AI-powered recruitment automation tool that evaluates resume-job description relevance using hybrid NLP techniques. The system uses pretrained models, stores all data in structured JSON files, and provides comprehensive feedback including skill gap analysis and personalized course recommendations.

## 🚀 Key Features

- **Hybrid NLP Evaluation**: Combines TF-IDF, fuzzy matching, and sentence embeddings for accurate matching
- **JSON-Based Architecture**: No SQL databases required - fully JSON-driven
- **Modular Design**: 6 independent functional modules for easy maintenance
- **Automated Feedback**: Generates strengths, weaknesses, and learning roadmaps
- **Course Recommendations**: Maps skill gaps to 200+ trending courses with clickable links
- **Batch Processing**: Evaluate multiple resumes against job descriptions simultaneously
- **Interactive Dashboard**: Streamlit-based visualization with charts and insights
- **FastAPI Backend**: RESTful API for easy integration

## 📋 System Requirements

- Python 3.9+
- 4GB RAM minimum (8GB recommended for batch processing)
- Internet connection (first-time model downloads only)

## 🛠️ Installation

### 1. Clone or Navigate to Project

```bash
cd HireLens
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Download spaCy Model

```bash
python -m spacy download en_core_web_sm
```

### 5. Initialize Data Directory

```bash
# Data directory will be auto-created on first run
# Or manually create it:
mkdir data
```

## 🎯 Quick Start

### Option 1: Frontend Dashboard (Recommended)

```bash
streamlit run frontend/app.py
```

Navigate to `http://localhost:8501` in your browser.

### Option 2: Backend API

```bash
uvicorn backend.main:app --reload
```

API documentation available at `http://localhost:8000/docs`

## 📚 Usage Guide

### Single Resume Evaluation

1. Launch the Streamlit dashboard
2. Navigate to **Single Evaluation** page
3. Upload resume (PDF/DOCX)
4. Paste job description
5. Click **Evaluate**
6. View comprehensive results with:
   - Relevance score and classification
   - Matched vs missing skills
   - Skill gap analysis
   - Course recommendations
   - Personalized feedback and learning roadmap

### Batch Evaluation

1. Navigate to **Batch Evaluation** page
2. Upload multiple resumes
3. Provide job description
4. View comparative results table
5. Export results or view detailed reports

### API Usage

```python
import requests

# Evaluate resume against job
response = requests.post(
    "http://localhost:8000/evaluate",
    json={
        "resume_file": "path/to/resume.pdf",
        "job_description": "We are looking for a Python developer..."
    }
)

result = response.json()
print(f"Score: {result['score']}")
print(f"Classification: {result['classification']}")
print(f"Skill Gaps: {result['skill_gaps']}")
```

## 🏗️ System Architecture

```
┌─────────────────┐
│  Streamlit UI   │
└────────┬────────┘
         │
    ┌────▼────────────────────────┐
    │    FastAPI Backend          │
    └────┬────────────────────────┘
         │
    ┌────▼────────────────────────┐
    │  Processing Modules         │
    ├─────────────────────────────┤
    │ 1. Resume Parser            │
    │ 2. Job Analyzer             │
    │ 3. Evaluation Engine        │
    │ 4. Skill Gap Analyzer       │
    │ 5. Course Recommender       │
    │ 6. Feedback Generator       │
    └────┬────────────────────────┘
         │
    ┌────▼────────────────────────┐
    │   JSON Data Storage         │
    └─────────────────────────────┘
```

## 📁 Project Structure

```
HireLens/
├── backend/                  # FastAPI backend
│   ├── main.py              # Main application
│   ├── routes.py            # API endpoints
│   └── utils.py             # Backend utilities
├── frontend/                # Streamlit dashboard
│   ├── app.py               # Main dashboard
│   └── components/          # UI components
├── modules/                 # Core processing modules
│   ├── resume_parser.py     # Resume parsing
│   ├── job_analyzer.py      # Job description analysis
│   ├── evaluation_engine.py # Hybrid NLP evaluation
│   ├── skill_gap_analyzer.py# Skill gap detection
│   ├── course_recommender.py# Course recommendations
│   └── feedback_generator.py# Feedback generation
├── config/                  # Configuration
│   ├── config.py            # System settings
│   └── models.py            # Data models
├── data/                    # JSON storage
│   └── courses_dataset.json # Course database
├── utils/                   # Utilities
│   ├── json_handler.py      # JSON operations
│   ├── nlp_utils.py         # NLP helpers
│   └── logger.py            # Logging
├── requirements.txt         # Dependencies
└── README.md               # This file
```

## 🔧 Configuration

Edit `config/config.py` to customize:

- **Scoring Weights**: Adjust TF-IDF, fuzzy, and embedding weights
- **Thresholds**: Modify High/Medium/Low classification thresholds
- **NLP Models**: Change spaCy or Sentence Transformer models
- **File Paths**: Configure JSON storage locations

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/upload-resume` | POST | Upload and parse resume |
| `/analyze-job` | POST | Analyze job description |
| `/evaluate` | POST | Full evaluation pipeline |
| `/batch-evaluate` | POST | Evaluate multiple resumes |
| `/get-evaluation/{id}` | GET | Retrieve results by ID |
| `/health` | GET | Health check |

Full API documentation: `http://localhost:8000/docs`

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_resume_parser.py -v

# Run with coverage
pytest --cov=modules tests/
```

## 🎓 NLP Models Used

- **spaCy**: `en_core_web_sm` for Named Entity Recognition
- **Sentence Transformers**: `all-MiniLM-L6-v2` for semantic similarity
- **scikit-learn**: TF-IDF vectorization and cosine similarity
- **RapidFuzz**: Fuzzy string matching for skill comparison

## 📈 Evaluation Methodology

**Hybrid Score = (0.3 × TF-IDF) + (0.3 × Fuzzy Match) + (0.4 × Embedding Similarity)**

- **TF-IDF**: Term frequency-inverse document frequency for keyword matching
- **Fuzzy Match**: Partial string matching for variant skill names
- **Embedding Similarity**: Semantic similarity using sentence embeddings

**Classification Thresholds:**
- High Relevance: ≥75
- Medium Relevance: 50-74
- Low Relevance: <50

## 🌟 Course Database

The system includes 200+ courses from:
- Coursera
- Udemy
- edX
- AWS Training
- Google Cloud Training
- Microsoft Learn
- Linux Foundation

Covering 50+ skills including Python, AWS, Kubernetes, Docker, Machine Learning, and more.

## 🤝 Contributing

This is a modular system designed for easy extension:

1. **Add New Skills**: Update `data/courses_dataset.json`
2. **Add New Modules**: Create new files in `modules/` directory
3. **Customize Evaluation**: Modify weights in `config/config.py`
4. **Add UI Components**: Create components in `frontend/components/`

## 📝 License

This project is licensed under the MIT License.

## 💡 Tips

- For best results, ensure resume and job description are detailed
- Use standard section headers in resumes (Skills, Experience, Education)
- Job descriptions should clearly specify required vs. preferred skills
- The system performs better with technical roles containing specific skill keywords

## 🐛 Troubleshooting

**Issue**: Module not found errors
- **Solution**: Ensure virtual environment is activated and dependencies installed

**Issue**: spaCy model not found
- **Solution**: Run `python -m spacy download en_core_web_sm`

**Issue**: Slow evaluation
- **Solution**: First-time model downloads may be slow. Subsequent evaluations will be faster.

**Issue**: Low scores for good matches
- **Solution**: Adjust scoring weights in `config/config.py` or ensure resume contains keywords from job description

## 📧 Support

For issues and questions, please check the documentation or create an issue in the repository.

---

**Built with ❤️ using Python, FastAPI, Streamlit, and modern NLP techniques**
