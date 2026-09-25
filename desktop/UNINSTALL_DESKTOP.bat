@echo off
echo Close Adam Assistant before uninstalling.
echo This removes the current installation and its locally saved data.
powershell -NoProfile -ExecutionPolicy Bypass -Command "$x=Get-NetTCPConnection -LocalPort 8770 -State Listen -ErrorAction SilentlyContinue; $x | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }; Start-Sleep -Milliseconds 500; $r=Join-Path $env:LOCALAPPDATA 'KanaanSoft\AdamAssistant_current'; if(Test-Path $r){Remove-Item $r -Recurse -Force}; Remove-Item (Join-Path ([Environment]::GetFolderPath('Desktop')) 'Adam Personal AI Assistant v0.6.7.lnk') -Force -ErrorAction SilentlyContinue"
pause
