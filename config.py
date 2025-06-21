# config.py
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
COMPOSIO_API_KEY = os.getenv("COMPOSIO_API_KEY")
GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
CALLBACK_URL = os.getenv("CALLBACK_URL", "http://localhost:8000/callback")

