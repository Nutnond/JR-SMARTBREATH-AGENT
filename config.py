import os
from dotenv import load_dotenv

load_dotenv()
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3")
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
JWT_ISSUER = os.environ.get("JWT_ISSUER", "SecurityApi")
JWT_AUDIENCE = os.environ.get("JWT_AUDIENCE", "MotomanageService")
JWT_SECRET = os.environ.get("JWT_SECRET", "MotomanageSuperSecurityPrivateKeyCreateat2025")  
BASE_CORS_API_URL = os.environ.get("BASE_CORS_API_URL", "http://localhost:8080") 
OPEN_AI_API_KEY = os.environ.get("OPEN_AI_API_KEY", "")