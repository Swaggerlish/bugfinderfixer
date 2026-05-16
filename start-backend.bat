@echo off
echo ========================================
echo Starting Bug Finder Backend Server
echo ========================================
echo.

cd backend

echo Checking for virtual environment...
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo ========================================
echo Starting FastAPI Server...
echo ========================================
echo Backend will be available at: http://localhost:8000
echo API Documentation at: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

uvicorn main:app --reload --host 0.0.0.0 --port 8000

@REM Made with Bob
