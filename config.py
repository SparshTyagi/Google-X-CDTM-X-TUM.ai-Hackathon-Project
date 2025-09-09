# config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Google Cloud Project Configuration
PROJECT_ID = "tum-cdtm25mun-8789"
LOCATION = "global"

# API Keys
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# --- Agent-Specific Configurations ---

# VC Persona for News and ArXiv agents
VC_PERSONA = """
Early-stage, deep-tech venture capital firm. We invest in foundational technologies
that can create new markets or radically disrupt existing ones. We are comfortable
with technical risk and long development cycles. We look for defensible 'moats'
built on novel science or engineering. We are particularly interested in the
intersections of software (AI/ML), biology, and advanced materials.
"""

# Technical Area of Interest for GitHub agent
GITHUB_INTEREST_AREA = "The emerging stack for building and deploying autonomous AI Agents"