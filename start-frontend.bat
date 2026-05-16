@echo off
echo ========================================
echo Starting Bug Finder Frontend
echo ========================================
echo.

cd frontend

echo Checking for node_modules...
if not exist "node_modules" (
    echo Installing dependencies...
    call npm install
) else (
    echo Dependencies already installed.
)

echo.
echo ========================================
echo Starting React Development Server...
echo ========================================
echo Frontend will be available at: http://localhost:3000
echo.
echo The browser will open automatically.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

call npm start

@REM Made with Bob
