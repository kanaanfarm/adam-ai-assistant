@echo off
setlocal
cd /d "%~dp0"
title Adam Acquisition v8.4.0.2

echo ============================================================
echo Adam Acquisition v8.4.0.2 - AUTONOMOUS MEETING ATTENDANCE + REPRESENTATIVE
echo ============================================================
where python >nul 2>nul
if errorlevel 1 (
  echo [ERROR] Python was not found in PATH.
  pause
  exit /b 1
)
python -c "import flask,dotenv,requests" >nul 2>nul
if errorlevel 1 (
  echo [ERROR] Required Python packages are missing.
  echo Run INSTALL_REQUIREMENTS.bat once, then start Adam again.
  pause
  exit /b 1
)

echo [OK] Python and core dependencies detected.
set "ADAM_LOCAL_HTTPS=false"

powershell -NoProfile -Command "$x=Get-NetTCPConnection -LocalPort 8770,8771 -State Listen -ErrorAction SilentlyContinue; if($x){exit 9}else{exit 0}"
if errorlevel 9 (
  echo [ERROR] Adam owner or Guest Voice port is already in use. Run STOP_ASSISTANT.bat first.
  pause
  exit /b 9
)

echo [INFO] Owner Adam: http://127.0.0.1:8770
echo [INFO] Autonomous meeting scheduler starts automatically with Adam.
echo [INFO] Starting Guest Voice-only gateway on 127.0.0.1:8771 ...
start "Adam Guest Gateway v8.4.0.2" /min python "%~dp0guest_gateway.py"

echo [INFO] Waiting for Guest Voice gateway health...
powershell -NoProfile -Command "$ok=$false; 1..20 | ForEach-Object { try { $r=Invoke-WebRequest -UseBasicParsing -Uri 'http://127.0.0.1:8771/health' -TimeoutSec 1; if($r.StatusCode -eq 200){$ok=$true; return} } catch {}; Start-Sleep -Milliseconds 500 }; if(-not $ok){exit 23}"
if errorlevel 23 (
  echo [ERROR] Guest Voice gateway failed to start on port 8771.
  echo [INFO] A visible gateway window is opened for diagnosis.
  start "Adam Guest Gateway Diagnostic v8.4.0.2" cmd /k "cd /d ""%~dp0"" ^& python guest_gateway.py"
  pause
  exit /b 23
)
echo [OK] Guest Voice gateway healthy on http://127.0.0.1:8771/health
echo [INFO] Starting trusted mobile Guest Voice HTTPS tunnel ...
start "Adam Guest HTTPS Tunnel v8.4.0.2" powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0START_GUEST_TUNNEL.ps1"
start "Adam Browser Watcher" /min powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0OPEN_ADAM_WHEN_READY.ps1"

python app.py

echo.
echo Adam has stopped. Guest tunnel helper windows can now be closed.
pause
