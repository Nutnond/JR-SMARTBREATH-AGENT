import os
from dotenv import load_dotenv

load_dotenv()
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3")
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
JWT_ISSUER = os.environ.get("JWT_ISSUER", "SecurityApi")
JWT_AUDIENCE = os.environ.get("JWT_AUDIENCE", "MotomanageService")
JWT_SECREAT = os.environ.get("JWT_SECREAT", "MotomanageSuperSecurityPrivateKeyCreateat2025")  
BASE_CORS_API_URL = os.environ.get("BASE_CORS_API_URL", "https://localhost:5179/graphql/")  
VERIFY_HTTPS = os.environ.get("VERIFY_HTTPS", "False").lower() in ("true", "1", "yes")