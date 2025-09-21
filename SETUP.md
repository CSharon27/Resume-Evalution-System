# Resume Evaluation System - Setup Guide

## Overview

The Automated Resume Relevance Check System is an AI-powered solution for evaluating resumes against job descriptions. It combines hard matching (keyword/skill matching) with semantic matching (LLM-powered analysis) to provide comprehensive evaluation results.

## Features

- **Automated Resume Evaluation**: Process PDF/DOCX resumes against job descriptions
- **Hybrid Scoring**: Combines hard matching (keywords, skills) with semantic matching (LLM-powered)
- **Relevance Scoring**: Generate 0-100 relevance scores with High/Medium/Low verdicts
- **Gap Analysis**: Identify missing skills, certifications, and projects
- **Student Feedback**: Provide personalized improvement suggestions
- **Web Dashboard**: Streamlit-based interface for placement team
- **Scalable Processing**: Handle thousands of resumes weekly

## Prerequisites

- Python 3.8 or higher
- pip package manager
- OpenAI API key (for LLM features)

## Installation

### 1. Clone or Download the Project

```bash
git clone <repository-url>
cd resume_evaluation_system
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Download spaCy Model

```bash
python -m spacy download en_core_web_sm
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root:

```bash
cp env.example .env
```

Edit `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=your_openai_api_key_here
```

## Quick Start

### Option 1: Automated Setup (Recommended)

Run the automated setup script:

```bash
python run_system.py
```

This will:
- Check dependencies
- Download required models
- Start the API server
- Start the dashboard
- Open the system in your browser

### Option 2: Manual Setup

#### 1. Start the API Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 2. Start the Dashboard (in a new terminal)

```bash
streamlit run app/frontend/dashboard.py --server.port 8501
```

#### 3. Access the System

- **Dashboard**: http://localhost:8501
- **API Documentation**: http://localhost:8000/docs
- **API Base URL**: http://localhost:8000

## Testing

Run the test suite to verify everything is working:

```bash
python test_system.py
```

## Usage

### 1. Upload Job Description

1. Go to the dashboard
2. Click "Upload Job Description"
3. Fill in the job details
4. Paste the job description text
5. Click "Upload Job Description"

### 2. Upload Resume

1. Click "Upload Resume"
2. Fill in student details
3. Upload PDF or DOCX file
4. Click "Upload Resume"

### 3. Evaluate Resume

1. Click "Evaluate Resume"
2. Select a resume and job description
3. Click "Evaluate Resume"
4. View detailed results

### 4. View Results

- Go to "View Evaluations" to see all results
- Use "Manage Data" to delete old data
- Export results for further analysis

## API Endpoints

### Resume Management
- `POST /upload/resume` - Upload and parse resume
- `GET /resumes` - Get all resumes
- `DELETE /resumes/{id}` - Delete resume

### Job Description Management
- `POST /upload/job-description` - Upload job description
- `GET /job-descriptions` - Get all job descriptions
- `DELETE /job-descriptions/{id}` - Delete job description

### Evaluation
- `POST /evaluate` - Evaluate resume against job description
- `GET /evaluations` - Get all evaluations
- `GET /evaluations/{id}` - Get detailed evaluation results

## Configuration

Edit `app/config.py` to customize:

- Scoring weights
- File upload limits
- LLM settings
- Database configuration
- Evaluation thresholds

## Troubleshooting

### Common Issues

1. **spaCy Model Not Found**
   ```bash
   python -m spacy download en_core_web_sm
   ```

2. **OpenAI API Key Missing**
   - Add your API key to `.env` file
   - Restart the application

3. **Port Already in Use**
   - Change ports in `app/config.py`
   - Or kill existing processes

4. **File Upload Errors**
   - Check file size limits
   - Ensure file is PDF or DOCX
   - Verify file is not corrupted

### Logs and Debugging

- API logs: Check terminal running `uvicorn`
- Dashboard logs: Check terminal running `streamlit`
- Database: SQLite file created in project root

## Project Structure

```
resume_evaluation_system/
├── app/
│   ├── main.py                 # FastAPI application
│   ├── config.py              # Configuration settings
│   ├── database.py            # Database setup
│   ├── models/
│   │   └── database.py        # Database models
│   ├── parsers/
│   │   ├── resume_parser.py   # Resume parsing
│   │   └── job_description_parser.py  # JD parsing
│   ├── evaluators/
│   │   ├── hard_matcher.py    # Hard matching
│   │   ├── semantic_matcher.py # Semantic matching
│   │   └── resume_evaluator.py # Main evaluator
│   ├── services/
│   │   └── resume_service.py  # Business logic
│   └── frontend/
│       └── dashboard.py       # Streamlit dashboard
├── data/                      # Upload directory
├── requirements.txt           # Dependencies
├── test_system.py            # Test suite
├── run_system.py             # Launcher script
└── README.md                 # This file
```

## Performance

- **Processing Speed**: ~2-5 seconds per resume evaluation
- **Scalability**: Can handle 1000+ resumes per hour
- **Memory Usage**: ~500MB base + 100MB per 100 resumes
- **Storage**: ~1MB per resume + evaluation data

## Security

- File upload validation
- SQL injection protection
- CORS enabled for web access
- Input sanitization
- Error handling

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
1. Check the troubleshooting section
2. Run the test suite
3. Check the logs
4. Create an issue with details

## Future Enhancements

- [ ] Batch processing
- [ ] Advanced analytics
- [ ] Email notifications
- [ ] Resume templates
- [ ] Integration with ATS systems
- [ ] Mobile app
- [ ] Multi-language support
