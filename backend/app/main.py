# backend/app/main.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Resume Evaluation API")

# Allow CORS for frontend (adjust origin if needed)
origins = [
    os.getenv("FRONTEND_URL", "*")  # you can set FRONTEND_URL in Render
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Example route
@app.get("/")
async def root():
    return {"message": "Resume Evaluation API is running!"}

# Spacy model loading (download if not present)
try:
    import spacy
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import spacy.cli
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Include your routers here
# from .routers import router
# app.include_router(router)
