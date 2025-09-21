# Resume Evaluation System - Frontend

This is the frontend component of the Resume Evaluation System, built with Streamlit.

## Features

- **Interactive Dashboard** - Modern, responsive web interface
- **Resume Upload** - Drag-and-drop file upload with validation
- **Job Description Upload** - Support for file and text input
- **Real-time Evaluation** - Live progress tracking and results
- **Advanced Analytics** - Charts, graphs, and detailed reports
- **Professional UI** - Beautiful design with animations and effects
- **Export Functionality** - Download results as JSON/CSV

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the Backend First**
   ```bash
   # From the backend folder
   python run_backend.py
   ```

3. **Start the Frontend**
   ```bash
   python run_frontend.py
   ```

4. **Access the Dashboard**
   - Dashboard: http://localhost:8501
   - Backend API: http://localhost:8000

## Features Overview

### 📄 Resume Management
- Upload resumes in PDF, DOCX, or TXT format
- Student information management
- File validation and size limits
- Batch processing support

### 💼 Job Description Management
- Upload job descriptions from files or text
- Company and position details
- Location and requirements tracking
- Content extraction and validation

### 🔍 Evaluation Engine
- AI-powered resume evaluation
- Semantic matching with LLM
- Hard skill matching
- Detailed scoring and feedback

### 📊 Analytics Dashboard
- Real-time metrics and statistics
- Interactive charts and graphs
- Score distribution analysis
- Trend tracking over time

### 🎨 Professional UI
- Modern, responsive design
- Smooth animations and transitions
- Professional color scheme
- Mobile-friendly interface

## Project Structure

```
frontend/
├── dashboard.py             # Main Streamlit application
├── run_frontend.py         # Frontend launcher
├── demo.py                 # Demo and testing scripts
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Configuration

The frontend connects to the backend API at `http://localhost:8000` by default. This can be configured in the `dashboard.py` file:

```python
API_BASE_URL = "http://localhost:8000"
```

## Development

To run in development mode:

```bash
streamlit run dashboard.py --server.port 8501
```

## Customization

### Styling
The dashboard uses custom CSS for professional styling. You can modify the styles in the `dashboard.py` file.

### API Integration
The frontend communicates with the backend through REST API calls. All API interactions are handled in the `make_api_request()` function.

### Adding New Features
1. Add new functions to `dashboard.py`
2. Update the navigation menu
3. Add corresponding backend API endpoints
4. Test the integration

## Dependencies

- Streamlit - Web application framework
- Requests - HTTP client for API calls
- Pandas - Data manipulation
- Plotly - Interactive visualizations
- Python-multipart - File upload support

## Troubleshooting

### Backend Connection Issues
- Ensure the backend server is running on port 8000
- Check firewall settings
- Verify API_BASE_URL configuration

### File Upload Issues
- Check file size limits (10MB default)
- Verify file format support (PDF, DOCX, TXT)
- Ensure upload directory permissions

### Performance Issues
- Use smaller file sizes for testing
- Check system resources
- Monitor API response times
