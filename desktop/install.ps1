param([switch]$Update)
$ErrorActionPreference = 'Stop'
$Source = Split-Path -Parent $PSScriptRoot
$OldRoot = Join-Path $env:LOCALAPPDATA 'KanaanSoft\RamiAssistant'
$LegacyRoot = Join-Path $env:LOCALAPPDATA 'KanaanSoft\RamiAssistant_v060'
$OlderRoot = Join-Path $env:LOCALAPPDATA 'KanaanSoft\RamiAssistant_v062'
$PreviousRoot = Join-Path $env:LOCALAPPDATA 'KanaanSoft\RamiAssistant_v063'
$NewestRoot = Join-Path $env:LOCALAPPDATA 'KanaanSoft\RamiAssistant_current'
$InstallRoot = Join-Path $env:LOCALAPPDATA 'KanaanSoft\AdamAssistant_current'
Write-Host 'Installing Adam Personal AI Assistant v0.6.7 WhatsApp Conversation update on port 8770...'
if (-not (Get-Command python -ErrorAction SilentlyContinue)) { throw 'Python 3 is required. Install Python and select Add Python to PATH.' }
Write-Host 'Stopping previous assistant servers on ports 8765 through 8770...'
$Listeners = Get-NetTCPConnection -LocalPort 8765,8766,8767,8768,8769,8770 -State Listen -ErrorAction SilentlyContinue
foreach ($Listener in $Listeners) { if ($Listener.OwningProcess -and $Listener.OwningProcess -ne $PID) { Stop-Process -Id $Listener.OwningProcess -Force -ErrorAction SilentlyContinue } }
Start-Sleep -Milliseconds 800
New-Item -ItemType Directory -Force -Path $InstallRoot | Out-Null
Get-ChildItem $Source -Force | Where-Object { $_.Name -notin @('__pycache__','.venv','data','desktop','android') } | ForEach-Object { Copy-Item $_.FullName $InstallRoot -Recurse -Force }
$DesktopTarget = Join-Path $InstallRoot 'desktop'; New-Item -ItemType Directory -Force -Path $DesktopTarget | Out-Null
Get-ChildItem $PSScriptRoot -Force | ForEach-Object { Copy-Item $_.FullName $DesktopTarget -Recurse -Force }
$DataTarget = Join-Path $InstallRoot 'data'; New-Item -ItemType Directory -Force -Path $DataTarget | Out-Null
if (Test-Path (Join-Path $OldRoot 'data')) { Get-ChildItem (Join-Path $OldRoot 'data') -Force | ForEach-Object { Copy-Item $_.FullName $DataTarget -Recurse -Force } }
if (Test-Path (Join-Path $LegacyRoot 'data')) { Get-ChildItem (Join-Path $LegacyRoot 'data') -Force | ForEach-Object { Copy-Item $_.FullName $DataTarget -Recurse -Force } }
if (Test-Path (Join-Path $OlderRoot 'data')) { Get-ChildItem (Join-Path $OlderRoot 'data') -Force | ForEach-Object { Copy-Item $_.FullName $DataTarget -Recurse -Force } }
if (Test-Path (Join-Path $PreviousRoot 'data')) { Get-ChildItem (Join-Path $PreviousRoot 'data') -Force | ForEach-Object { Copy-Item $_.FullName $DataTarget -Recurse -Force } }
if (Test-Path (Join-Path $NewestRoot 'data')) { Get-ChildItem (Join-Path $NewestRoot 'data') -Force | ForEach-Object { Copy-Item $_.FullName $DataTarget -Recurse -Force } }
if (Test-Path (Join-Path $Source 'data')) { Get-ChildItem (Join-Path $Source 'data') -Force | ForEach-Object { if (-not (Test-Path (Join-Path $DataTarget $_.Name))) { Copy-Item $_.FullName $DataTarget -Recurse -Force } } }
if (-not (Test-Path (Join-Path $DataTarget 'contacts.json'))) { Set-Content -Path (Join-Path $DataTarget 'contacts.json') -Value '[]' }
if (Test-Path (Join-Path $OldRoot '.env')) { Copy-Item (Join-Path $OldRoot '.env') (Join-Path $InstallRoot '.env') -Force }
if (Test-Path (Join-Path $LegacyRoot '.env')) { Copy-Item (Join-Path $LegacyRoot '.env') (Join-Path $InstallRoot '.env') -Force }
if (Test-Path (Join-Path $OlderRoot '.env')) { Copy-Item (Join-Path $OlderRoot '.env') (Join-Path $InstallRoot '.env') -Force }
if (Test-Path (Join-Path $PreviousRoot '.env')) { Copy-Item (Join-Path $PreviousRoot '.env') (Join-Path $InstallRoot '.env') -Force }
if (Test-Path (Join-Path $NewestRoot '.env')) { Copy-Item (Join-Path $NewestRoot '.env') (Join-Path $InstallRoot '.env') -Force }
if (Test-Path (Join-Path $Source '.env')) { Copy-Item (Join-Path $Source '.env') (Join-Path $InstallRoot '.env') -Force }
$Venv = Join-Path $InstallRoot '.venv'
if (-not (Test-Path (Join-Path $Venv 'Scripts\python.exe'))) { python -m venv $Venv }
& (Join-Path $Venv 'Scripts\python.exe') -m pip install --disable-pip-version-check -r (Join-Path $InstallRoot 'requirements.txt')
$Shell = New-Object -ComObject WScript.Shell
$OldShortcuts = @('Adam Personal AI Assistant v0.6.1.lnk','Adam Personal AI Assistant v0.6.2.lnk','Adam Personal AI Assistant v0.6.3.lnk','Adam Personal AI Assistant v0.6.4.lnk','Adam Personal AI Assistant v0.6.5.lnk','Adam Personal AI Assistant v0.6.6.lnk')
foreach($Shortcut in $OldShortcuts){Remove-Item (Join-Path ([Environment]::GetFolderPath('Desktop')) $Shortcut) -Force -ErrorAction SilentlyContinue}
$DesktopShortcut = $Shell.CreateShortcut((Join-Path ([Environment]::GetFolderPath('Desktop')) 'Adam Personal AI Assistant v0.6.7.lnk'))
$DesktopShortcut.TargetPath='wscript.exe'; $DesktopShortcut.Arguments='"'+(Join-Path $InstallRoot 'desktop\launcher.vbs')+'"'; $DesktopShortcut.WorkingDirectory=$InstallRoot; $DesktopShortcut.Save()
$StartDir=Join-Path $env:APPDATA 'Microsoft\Windows\Start Menu\Programs\Kanaan Soft'; New-Item -ItemType Directory -Force -Path $StartDir | Out-Null
foreach($Shortcut in $OldShortcuts){Remove-Item (Join-Path $StartDir $Shortcut) -Force -ErrorAction SilentlyContinue}
$StartShortcut=$Shell.CreateShortcut((Join-Path $StartDir 'Adam Personal AI Assistant v0.6.7.lnk')); $StartShortcut.TargetPath=$DesktopShortcut.TargetPath; $StartShortcut.Arguments=$DesktopShortcut.Arguments; $StartShortcut.WorkingDirectory=$InstallRoot; $StartShortcut.Save()
Write-Host 'v0.6.7 installation completed. Existing data and .env were preserved.' -ForegroundColor Green
Start-Process 'wscript.exe' -ArgumentList ('"'+(Join-Path $InstallRoot 'desktop\launcher.vbs')+'"')
