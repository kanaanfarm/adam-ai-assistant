@echo off
setlocal
cd /d "%~dp0"
title Adam Acquisition Diagnostics

echo ============================================================
echo Adam Acquisition v1.0.1 - Diagnostics
echo ============================================================
echo.
where python >nul 2>nul
if errorlevel 1 (
  echo Python: NOT FOUND
) else (
  echo Python:
  python --version
)
echo.
echo Package checks:
python -c "import flask; print('Flask: OK', flask.__version__ if hasattr(flask,'__version__') else '')" 2>nul || echo Flask: MISSING
python -c "import dotenv; print('python-dotenv: OK')" 2>nul || echo python-dotenv: MISSING
python -c "import requests; print('requests: OK')" 2>nul || echo requests: MISSING
python -c "import msal; print('MSAL: OK')" 2>nul || echo MSAL: MISSING/OPTIONAL

echo.
echo Port 8770 status:
netstat -ano | findstr ":8770" || echo Port 8770 is not currently listening.

echo.
echo If Adam is running, open:
echo http://127.0.0.1:8770/api/health
pause
