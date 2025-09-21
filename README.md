# Resume Evaluation System

An AI-powered resume evaluation system that helps placement teams analyze and evaluate student resumes against job descriptions using advanced NLP and machine learning techniques.

## 🏗️ Project Structure

The project is now organized into separate frontend and backend components:

```
Resume-Evaluation-System/
├── backend/                 # FastAPI Backend Server
│   ├── app/                # Main application code
│   │   ├── main.py         # FastAPI application
│   │   ├── config.py       # Configuration
│   │   ├── database.py     # Database setup
│   │   ├── services/       # Business logic
│   │   ├── models/         # Database models
│   │   ├── parsers/        # File parsing
│   │   └── evaluators/     # AI evaluation
│   ├── requirements.txt    # Backend dependencies
│   ├── run_backend.py      # Backend launcher
│   └── README.md           # Backend documentation
├── frontend/               # Streamlit Frontend Dashboard
│   ├── dashboard.py        # Main dashboard
│   ├── requirements.txt    # Frontend dependencies
│   ├── run_frontend.py     # Frontend launcher
│   └── README.md           # Frontend documentation
├── data/                   # Shared data directory
│   ├── uploads/           # File uploads
│   └── sample_*           # Sample files
├── run_system.py          # Main system launcher
└── README.md              # This file
```

## 🚀 Quick Start

### Option 1: Run Complete System
```bash
# Start both frontend and backend
python run_system.py
```

### Option 2: Run Components Separately

#### Start Backend First
```bash
cd backend
pip install -r requirements.txt
python run_backend.py
```

#### Start Frontend (in new terminal)
```bash
cd frontend
pip install -r requirements.txt
python run_frontend.py
```

## 🌐 Access Points

- **Frontend Dashboard**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Interactive API**: http://localhost:8000/redoc

## ✨ Features

### 🤖 AI-Powered Evaluation
- **Semantic Matching**: Advanced NLP for understanding context
- **Hard Skill Matching**: Keyword and skill-based matching
- **LLM Integration**: OpenAI GPT for detailed feedback
- **Multi-format Support**: PDF, DOCX, and TXT file processing

### 📊 Interactive Dashboard
- **Modern UI**: Professional design with animations
- **Real-time Processing**: Live progress tracking
- **Advanced Analytics**: Charts, graphs, and detailed reports
- **Export Functionality**: Download results as JSON/CSV

### 🔧 Backend API
- **RESTful API**: FastAPI-based high-performance server
- **File Upload**: Secure file handling and validation
- **Database Management**: SQLite for data persistence
- **Auto Documentation**: OpenAPI/Swagger integration

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern, fast web framework
- **SQLAlchemy** - Database ORM
- **spaCy** - Natural language processing
- **LangChain** - LLM integration
- **OpenAI** - AI model access
- **PyMuPDF** - PDF processing

### Frontend
- **Streamlit** - Interactive web applications
- **Plotly** - Interactive visualizations
- **Pandas** - Data manipulation
- **Requests** - HTTP client

## 📋 Prerequisites

- Python 3.8+
- OpenAI API key (for LLM features)
- 4GB+ RAM recommended
- 1GB+ disk space

## 🔧 Configuration

### Environment Variables

**For Local Development:**
Create a `.env` file in the backend directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
UPLOAD_DIR=data/uploads
DATABASE_URL=sqlite:///./resume_evaluation.db
```

**For GitHub Deployment:**
Use GitHub Secrets to securely store your API key:
1. Go to repository Settings → Secrets and variables → Actions
2. Add `OPENAI_API_KEY` as a repository secret
3. See [GITHUB_DEPLOYMENT.md](GITHUB_DEPLOYMENT.md) for detailed instructions

### API Key Setup
1. Get an OpenAI API key from https://platform.openai.com/
2. For local development: `python backend/setup_llm.py`
3. For deployment: Use GitHub Secrets (recommended)

**🔐 Security Note:** Never commit your actual API key to version control!

## 🚀 Deployment

### GitHub Deployment
For secure deployment with GitHub Secrets:
- See [GITHUB_DEPLOYMENT.md](GITHUB_DEPLOYMENT.md) for complete instructions
- Supports Railway, Render, Heroku, and other platforms
- Secure API key handling with GitHub Secrets

### Quick Deploy Options
- **Railway**: Connect GitHub repo → Add secrets → Deploy
- **Render**: Import repo → Set environment variables → Deploy  
- **Heroku**: Use Heroku CLI with environment variables

## 📚 Documentation

- [Backend Documentation](backend/README.md)
- [Frontend Documentation](frontend/README.md)
- [GitHub Deployment Guide](GITHUB_DEPLOYMENT.md)
- [API Documentation](http://localhost:8000/docs) (when running)

### Development
```bash
python run_system.py
```

### Production
```bash
# Backend
cd backend
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker

# Frontend
cd frontend
streamlit run dashboard.py --server.port 8501
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Check the documentation in each component folder
- Review the API documentation at http://localhost:8000/docs
- Open an issue on GitHub

## 🎯 Use Cases

- **Placement Teams**: Evaluate student resumes against job requirements
- **HR Departments**: Streamline resume screening process
- **Career Centers**: Help students improve their resumes
- **Recruitment Agencies**: Match candidates to job openings
- **Educational Institutions**: Assess student readiness for placements

---

**Built with ❤️ for the placement community**