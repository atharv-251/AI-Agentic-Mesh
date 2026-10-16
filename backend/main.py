from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.database import engine, initialize_database
from backend.routers.workflow_runs import router as workflow_runs_router
from backend.routers.amplify import router as amplify_router
from backend.routers.amplify_jobs import router as amplify_jobs_router
from backend.routers.backend_plans import router as backend_plans_router
import backend.models  # Ensure all SQLAlchemy models are registered
from backend.logging_config import setup_logging, RealtimeRequestLoggingMiddleware
from backend.routers import transitions_router

# Setup real-time terminal logger (auto-detects -v for DEBUG)
logger = setup_logging()

# Initialize database schema
initialize_database()

app = FastAPI(
    title="KT Planner - Master Orchestration Platform",
    version="1.0.0",
    description="AI-powered Transition Planning & Knowledge Transfer Orchestration Platform",
)

# Real-time request logging middleware
app.add_middleware(RealtimeRequestLoggingMiddleware)

# CORS middleware for local frontend dev server & production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(transitions_router)
app.include_router(workflow_runs_router)
app.include_router(amplify_router)
app.include_router(amplify_jobs_router)
app.include_router(backend_plans_router)

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "KT Planner Master Backend",
        "version": "1.0.0",
        "authoritative_db": "SQL Server LocalDB" if engine.dialect.name == "mssql" else "SQLite kt_planner.db",
    }

# Single Deployable Service: Serve static frontend files if built
FRONTEND_DIST = Path(__file__).resolve().parent.parent / "frontend" / "dist"
if FRONTEND_DIST.exists():
    app.mount("/assets", StaticFiles(directory=FRONTEND_DIST / "assets"), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        if full_path == "api" or full_path.startswith("api/"):
            raise HTTPException(status_code=404, detail="API endpoint not available in the Amplify-first application")
        file_path = FRONTEND_DIST / full_path
        if file_path.exists() and file_path.is_file():
            return FileResponse(file_path)
        return FileResponse(FRONTEND_DIST / "index.html")
