@echo off
powershell -NoProfile -ExecutionPolicy Bypass -Command "$x=Get-NetTCPConnection -LocalPort 8765,8766,8767,8768,8769,8770,8771 -State Listen -ErrorAction SilentlyContinue; $x | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }; Get-Process cloudflared -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue"
del /q "%~dp0data\guest_public_base_url.txt" >nul 2>nul
echo Adam Acquisition stopped, including Guest Voice gateway/tunnel.
pause
