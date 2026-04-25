@echo off
cd /d %~dp0

echo AI Test Software Starting...
echo.

python -c "import flask" 2>nul
if errorlevel 1 (
    echo Installing dependencies...
    pip install Flask Flask-CORS requests
)

if not exist "results" mkdir results
if not exist "static" mkdir static

echo Starting server at http://127.0.0.1:5000
echo Press Ctrl+C to stop
echo.

python app.py
pause