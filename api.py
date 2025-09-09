# api.py (Corrected)
import os
from fastapi import FastAPI, HTTPException, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
from google.cloud import firestore
import vertexai
from vertexai.generative_models import GenerativeModel

# Import the agents you ACTUALLY use in the final orchestrator
from agents.news_agent import NewsScoutAgent
from agents.github_agent import GithubScoutAgent
from agents.arxiv_agent import ArxivScoutAgent
from agents.final_report_agent import FinalReportAgent # <-- IMPORTANT
from orchestrator import Orchestrator
from config import PROJECT_ID, LOCATION

# --- API & Security Setup ---

app = FastAPI(
    title="VC Trend Analysis Agent API",
    description="An API to run a multi-agent system for discovering and verifying investment trends.",
    version="1.0.0"
)

# CORS configuration
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173",
    "https://tum-cdtm25mun-8792.web.app" # Your live URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # Use the specific list for better security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Key Security
API_KEY = os.environ.get("API_KEY", "your-super-secret-key-for-dev")
API_KEY_NAME = "X-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == API_KEY:
        return api_key
    else:
        raise HTTPException(status_code=403, detail="Could not validate credentials")

# --- Global Initialization ---

print("Initializing Vertex AI system...")
vertexai.init(project=PROJECT_ID, location=LOCATION)
gemini_model = GenerativeModel("gemini-1.5-pro-001") # Use 1.5 Pro for best results
print("Vertex AI system initialized.")
# Add the Firestore client
db = firestore.Client() 
print("Systems initialized.")

# Instantiate all agents once to be reused across requests
# THIS IS THE CORRECTED BLOCK
orchestrator = Orchestrator(
    news_scout=NewsScoutAgent(model=gemini_model),
    github_scout=GithubScoutAgent(model=gemini_model),
    arxiv_scout=ArxivScoutAgent(model=gemini_model),
    # The key change: Pass the FinalReportAgent with the correct keyword 'final_report_agent'
    final_report_agent=FinalReportAgent(model=gemini_model)
)

# --- API Endpoints ---

@app.get("/", tags=["Health Check"])
async def root():
    return {"status": "ok", "message": "Trend Analysis API is running!"}


@app.post("/analyze", tags=["Analysis"], dependencies=[Security(get_api_key)])
async def run_analysis():
    """
    Triggers the full, end-to-end trend analysis pipeline.
    """
    try:
        print("Received request to /analyze. Starting orchestrator...")
        final_report = orchestrator.run()
        # The report is already a JSON string, so we return it directly
        return {"report": final_report}
    except Exception as e:
        print(f"An error occurred during analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ADD THIS NEW ENDPOINT FOR THE SCHEDULER
@app.post("/run-scheduled-analysis", tags=["Scheduled Tasks"])
async def run_scheduled_analysis(api_key: str = Security(get_api_key)):
    """
    A secure endpoint for Cloud Scheduler to trigger.
    Runs the full analysis and saves the result to Firestore.
    """
    try:
        print("Received scheduled task. Starting orchestrator...")
        final_report_json_str = orchestrator.run()
        
        print("Saving report to Firestore...")
        # Get a reference to the document where we'll store the report
        # Using a fixed ID 'latest' makes it easy for the frontend to find
        doc_ref = db.collection("reports").document("latest")

        # The report is a string, so we store it in a field.
        # We also add a timestamp.
        doc_ref.set({
            "report_json": final_report_json_str,
            "last_updated": firestore.SERVER_TIMESTAMP
        })
        print("Successfully saved report to Firestore.")
        
        return {"status": "ok", "message": "Report updated in Firestore."}

    except Exception as e:
        print(f"An error occurred during scheduled analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))