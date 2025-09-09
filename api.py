# api.py
import os
from fastapi import FastAPI, HTTPException, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader

import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig

# Import your existing agents and orchestrator
from agents.news_agent import NewsScoutAgent
from agents.github_agent import GithubScoutAgent
from agents.arxiv_agent import ArxivScoutAgent
from agents.synthesis_agent import SynthesisAgent
from agents.startup_finder_agent import StartupFinderAgent
from agents.verification_agent import VerificationAgent
from orchestrator import Orchestrator
from config import PROJECT_ID, LOCATION

# --- API & Security Setup ---

# This creates the main web application instance
app = FastAPI(
    title="VC Trend Analysis Agent API",
    description="An API to run a multi-agent system for discovering and verifying investment trends.",
    version="1.0.0"
)

# IMPORTANT: Configure CORS to allow your frontend to call the API
# In production, you should restrict this to your actual frontend's domain.
origins = [
    "http://localhost",
    "http://localhost:3000", # Common port for React/Next.js dev
    "http://localhost:5173", # Common port for Vite/SvelteKit dev
    # TODO: Add your deployed Firebase Hosting URL here!
    # e.g., "https://your-hackathon-project.web.app"
    "https://tum-cdtm25mun-8792.web.app" # <-- YOUR LIVE URL IS HERE
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For a hackathon, '*' is fine. For production, use the `origins` list.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple API Key Security
# In a real app, you'd use OAuth2, but this is secure and easy for a hackathon.
API_KEY = os.environ.get("API_KEY", "your-super-secret-key-for-dev") # Get key from environment
API_KEY_NAME = "X-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == API_KEY:
        return api_key
    else:
        raise HTTPException(status_code=403, detail="Could not validate credentials")

# --- Global Initialization ---

# Initialize the core model only once when the server starts
print("Initializing Vertex AI system...")
vertexai.init(project=PROJECT_ID, location=LOCATION)
gemini_model = GenerativeModel("gemini-2.5-pro")
print("Vertex AI system initialized.")

# Instantiate all agents once to be reused across requests
orchestrator = Orchestrator(
    news_scout=NewsScoutAgent(model=gemini_model),
    github_scout=GithubScoutAgent(model=gemini_model),
    arxiv_scout=ArxivScoutAgent(model=gemini_model),
    synthesis_agent=SynthesisAgent(model=gemini_model),
    startup_finder=StartupFinderAgent(model=gemini_model),
    verification_agent=VerificationAgent(model=gemini_model)
)

# --- API Endpoints ---

@app.get("/", tags=["Health Check"])
async def root():
    """A simple health check endpoint."""
    return {"status": "ok", "message": "Trend Analysis API is running!"}


@app.post("/analyze", tags=["Analysis"], dependencies=[Security(get_api_key)])
async def run_analysis():
    """
    Triggers the full, end-to-end trend analysis pipeline.
    This is the main endpoint your frontend will call.
    """
    try:
        print("Received request to /analyze. Starting orchestrator...")
        # The orchestrator's run method is synchronous, but FastAPI can run it
        # in an external threadpool to prevent blocking.
        final_report = orchestrator.run()
        return {"report": final_report}
    except Exception as e:
        print(f"An error occurred during analysis: {e}")
        # In a real app, you'd have more specific error handling.
        raise HTTPException(status_code=500, detail=str(e))