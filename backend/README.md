# Resume Evaluation System - Backend

This is the backend component of the Resume Evaluation System, built with FastAPI.

## Features

- **FastAPI REST API** - High-performance API server
- **Resume Parsing** - Extract text from PDF, DOCX, and TXT files
- **AI-Powered Evaluation** - Semantic matching using LLM and NLP
- **Database Management** - SQLite database for storing evaluations
- **File Upload Handling** - Secure file upload and processing
- **API Documentation** - Auto-generated OpenAPI/Swagger docs

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Download spaCy Model**
   ```bash
   python -m spacy download en_core_web_sm
   ```

3. **Start the Backend Server**
   ```bash
   python run_backend.py
   ```

4. **Access the API**
   - API Server: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Interactive API: http://localhost:8000/redoc

## API Endpoints

- `GET /` - Health check
- `POST /upload/resume` - Upload resume file
- `POST /upload/job-description` - Upload job description
- `POST /evaluate` - Evaluate resume against job description
- `GET /resumes` - Get all resumes
- `GET /job-descriptions` - Get all job descriptions

## Configuration

The backend uses environment variables for configuration:

- `OPENAI_API_KEY` - OpenAI API key for LLM features (required for AI features)
- `UPLOAD_DIR` - Directory for file uploads (default: data/uploads)
- `DATABASE_URL` - Database connection string

### Setting up OpenAI API Key

**For Local Development:**
```bash
# Create .env file
cp env.template .env
# Edit .env with your actual API key
```

**For GitHub Deployment:**
1. Go to your repository Settings
2. Navigate to "Secrets and variables" → "Actions"
3. Add `OPENAI_API_KEY` as a repository secret
4. See `GITHUB_DEPLOYMENT.md` for detailed instructions

**Security Note:** Never commit your actual API key to version control!

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database connection
│   ├── services/            # Business logic
│   ├── models/              # Database models
│   ├── parsers/             # File parsing utilities
│   └── evaluators/          # AI evaluation logic
├── requirements.txt         # Python dependencies
├── run_backend.py          # Backend launcher
└── README.md               # This file
```

## Development

To run in development mode with auto-reload:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Deployment

For production deployment, use Gunicorn:

```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Dependencies

- FastAPI - Web framework
- Uvicorn - ASGI server
- SQLAlchemy - Database ORM
- PyMuPDF - PDF processing
- spaCy - NLP processing
- LangChain - LLM integration
- OpenAI - AI model access
