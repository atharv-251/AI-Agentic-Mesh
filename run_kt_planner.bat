@echo off
setlocal
cd /d "%~dp0"
echo ======================================================================
echo Starting KT Planner Platform (Single Deployable Service)
echo Uvicorn + FastAPI + React UI + selected local database
echo ======================================================================

python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 %*
pause
