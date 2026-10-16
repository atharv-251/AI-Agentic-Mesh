from pathlib import Path
import os
import json
from dotenv import load_dotenv
from agentic_blueprint import get_llm, init_blueprint

# Load environment variables
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "kt_planner.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"
DATABASE_SELECTION_PATH = BASE_DIR / ".kt-database.json"
if DATABASE_SELECTION_PATH.exists():
    from backend.sqlserver import localdb_url
    selection = json.loads(DATABASE_SELECTION_PATH.read_text(encoding="utf-8"))
    if set(selection) != {"provider", "database"} or selection["provider"] != "sqlserver-localdb":
        raise ValueError("Unsupported local database selection; fix .kt-database.json before starting")
    DATABASE_URL = localdb_url(selection["database"])

HOLIDAYS_JSON_PATH = BASE_DIR / "holidays.json"
SAMPLE_EXTRACT_PATH = BASE_DIR / "KT_Extract-1789932244532.json"
UPLOADS_DIR = BASE_DIR / "uploads"
EXPORTS_DIR = BASE_DIR / "exports"

UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

# External Extraction API URL (read from .env)
EXTERNAL_API_URL = os.getenv("EXTERNAL_API_URL", "")
EXTERNAL_API_URL1 = os.getenv("EXTERNAL_API_URL1", "")

# Initialize Agentic Blueprint LLM Client
init_blueprint()
try:
    llm = get_llm(model="gpt-4o-mini", temperature=0.1)
except Exception as e:
    llm = None
