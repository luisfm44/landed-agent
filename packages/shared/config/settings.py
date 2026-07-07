import os

from dotenv import load_dotenv

load_dotenv()

LANDED_API_BASE_URL = os.getenv("LANDED_API_BASE_URL", "http://localhost:3001")
LANDED_API_TIMEOUT_SECONDS = float(os.getenv("LANDED_API_TIMEOUT_SECONDS", "60"))
LANDED_API_MAX_RETRIES = int(os.getenv("LANDED_API_MAX_RETRIES", "2"))
LANDED_API_BACKOFF_SECONDS = float(os.getenv("LANDED_API_BACKOFF_SECONDS", "1"))

ORCHESTRATOR_MODEL = os.getenv("ORCHESTRATOR_MODEL", "gemini-2.5-flash-lite")
FAST_AGENT_MODEL = os.getenv("FAST_AGENT_MODEL", "gemini-2.5-flash-lite")
REASONING_AGENT_MODEL = os.getenv("REASONING_AGENT_MODEL", "gemini-2.5-flash-lite")

MAX_TOOL_CALLS_PER_REQUEST = int(os.getenv("MAX_TOOL_CALLS_PER_REQUEST", "12"))

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_GROUNDING_MODEL = os.getenv("OLLAMA_GROUNDING_MODEL", "llama3.1")
