@echo off
setlocal
cd /d "%~dp0"
echo Running Adam Acquisition v1.0.1 smoke tests...
python -m pytest -q tests
if errorlevel 1 (
  echo.
  echo Smoke tests FAILED.
  pause
  exit /b 1
)
echo.
echo Smoke tests PASSED.
pause
