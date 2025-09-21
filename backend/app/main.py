# backend/app/main.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI instance
app = FastAPI(title="Resume Evaluation API")

# Enable CORS for frontend
origins = [
    os.getenv("FRONTEND_URL", "*")  # Replace with your frontend URL if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Example root endpoint
@app.get("/")
async def root():
    return {"message": "Resume Evaluation API is running!"}

# Spacy model setup
try:
    import spacy
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import spacy.cli
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# TODO: Add your routers here
# from .routers import router
# app.include_router(router)
