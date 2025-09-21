# GitHub Deployment Guide for Resume Evaluation System

This guide will help you deploy your Resume Evaluation System to GitHub with secure OpenAI API key handling.

## 🔐 Security Setup

### 1. GitHub Secrets Configuration

To keep your OpenAI API key secure, you'll use GitHub Secrets:

1. **Go to your GitHub repository**
2. **Click on "Settings" tab**
3. **In the left sidebar, click "Secrets and variables" → "Actions"**
4. **Click "New repository secret"**
5. **Add the following secrets:**

| Secret Name | Value | Description |
|-------------|-------|-------------|
| `OPENAI_API_KEY` | `your_actual_openai_api_key` | Your OpenAI API key from https://platform.openai.com/api-keys |
| `DATABASE_URL` | `sqlite:///./resume_evaluation.db` | Database connection string |
| `PORT` | `8000` | Port for the backend server |

### 2. Environment Variables for Local Development

For local development, create a `.env` file in the `backend` folder:

```bash
# Copy the template
cp backend/env.template backend/.env

# Edit the .env file with your actual values
OPENAI_API_KEY=your_actual_openai_api_key_here
DATABASE_URL=sqlite:///./resume_evaluation.db
DEBUG=true
HOST=0.0.0.0
PORT=8000
```

**⚠️ Important:** Never commit the `.env` file to version control!

## 🚀 Deployment Options

### Option 1: GitHub Pages (Frontend Only)

For the frontend dashboard:

1. **Go to repository Settings**
2. **Scroll down to "Pages" section**
3. **Select "Deploy from a branch"**
4. **Choose "main" branch and "/ (root)" folder**
5. **Save**

### Option 2: Railway (Full Stack)

1. **Go to [Railway.app](https://railway.app)**
2. **Connect your GitHub account**
3. **Import your repository**
4. **Add environment variables:**
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `PORT`: 8000
5. **Deploy**

### Option 3: Render (Full Stack)

1. **Go to [Render.com](https://render.com)**
2. **Connect your GitHub account**
3. **Create a new Web Service**
4. **Select your repository**
5. **Configure:**
   - **Build Command:** `cd backend && pip install -r requirements.txt`
   - **Start Command:** `cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Environment Variables:**
     - `OPENAI_API_KEY`: Your OpenAI API key
     - `PORT`: 8000

### Option 4: Heroku (Full Stack)

1. **Install Heroku CLI**
2. **Create Heroku app:**
   ```bash
   heroku create your-app-name
   ```
3. **Set environment variables:**
   ```bash
   heroku config:set OPENAI_API_KEY=your_actual_api_key
   heroku config:set PORT=8000
   ```
4. **Deploy:**
   ```bash
   git push heroku main
   ```

## 📁 Project Structure for Deployment

```
your-repo/
├── backend/                 # Backend API
│   ├── app/                # FastAPI application
│   ├── requirements.txt    # Python dependencies
│   ├── Procfile           # Heroku deployment config
│   ├── env.template       # Environment variables template
│   └── run_backend.py     # Backend launcher
├── frontend/               # Frontend dashboard
│   ├── dashboard.py       # Streamlit application
│   ├── requirements.txt   # Frontend dependencies
│   └── run_frontend.py    # Frontend launcher
├── data/                   # Shared data directory
├── .gitignore             # Git ignore file
├── README.md              # Project documentation
└── GITHUB_DEPLOYMENT.md   # This file
```

## 🔧 Configuration Files

### .gitignore
Make sure your `.gitignore` includes:
```
# Environment variables
.env
.env.local
.env.production

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/

# Database
*.db
*.sqlite

# Uploads
data/uploads/*
!data/uploads/.gitkeep

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

### Procfile (for Heroku)
Create `backend/Procfile`:
```
web: cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## 🧪 Testing Your Deployment

### Local Testing
```bash
# Test backend
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000

# Test frontend
cd frontend
streamlit run dashboard.py --server.port 8501
```

### Production Testing
1. **Check API endpoints:**
   - `https://your-app.herokuapp.com/` (Health check)
   - `https://your-app.herokuapp.com/docs` (API documentation)

2. **Test OpenAI integration:**
   - Upload a resume
   - Upload a job description
   - Run evaluation
   - Verify AI feedback is generated

## 🔍 Troubleshooting

### Common Issues

1. **"No module named 'app'" error:**
   - Make sure you're running from the correct directory
   - Check that all dependencies are installed

2. **OpenAI API key not working:**
   - Verify the API key is correct
   - Check that you have credits in your OpenAI account
   - Ensure the environment variable is set correctly

3. **Database connection issues:**
   - Check DATABASE_URL configuration
   - Ensure database file permissions are correct

4. **Port binding issues:**
   - Use `$PORT` environment variable for production
   - Check that the port is not already in use

### Debug Mode
Enable debug mode by setting `DEBUG=true` in your environment variables.

## 📚 Additional Resources

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [FastAPI Deployment Guide](https://fastapi.tiangolo.com/deployment/)
- [Streamlit Deployment Guide](https://docs.streamlit.io/streamlit-community-cloud)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

## 🆘 Support

If you encounter issues:
1. Check the logs in your deployment platform
2. Verify all environment variables are set correctly
3. Test locally first before deploying
4. Check the API documentation at `/docs` endpoint

---

**Remember:** Keep your API keys secure and never commit them to version control!
