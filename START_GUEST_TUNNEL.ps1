$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$tools = Join-Path $root 'tools'
$data = Join-Path $root 'data'
$exe = Join-Path $tools 'cloudflared.exe'
$urlFile = Join-Path $data 'guest_public_base_url.txt'
$logFile = Join-Path $data 'guest_tunnel.log'
$statusFile = Join-Path $data 'guest_tunnel_status.json'
New-Item -ItemType Directory -Force -Path $tools,$data | Out-Null
Remove-Item $urlFile -Force -ErrorAction SilentlyContinue
Remove-Item $statusFile -Force -ErrorAction SilentlyContinue

function Write-Status([string]$state,[string]$message) {
    $obj = @{ state=$state; message=$message; updated_at=(Get-Date).ToString('s') }
    $obj | ConvertTo-Json -Compress | Set-Content -Encoding UTF8 $statusFile
}
function Log([string]$message) {
    $line = "[$(Get-Date -Format s)] $message"
    Write-Host $line
    $line | Add-Content -Encoding UTF8 $logFile
}

"" | Set-Content -Encoding UTF8 $logFile
Write-Status 'starting' 'Preparing trusted HTTPS tunnel...'
Log 'Adam Guest Voice HTTPS launcher v8.2.0.8'
Log 'Gateway target: http://127.0.0.1:8771'

# Prefer an already installed cloudflared.
$cmd = Get-Command cloudflared.exe -ErrorAction SilentlyContinue
if ($cmd) {
    $exe = $cmd.Source
    Log "Using installed cloudflared: $exe"
} elseif (-not (Test-Path $exe)) {
    $download = 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe'
    Write-Status 'downloading' 'Downloading Cloudflare tunnel helper...'
    Log 'cloudflared not found; downloading official Windows release.'
    $downloaded = $false
    try {
        $curl = Get-Command curl.exe -ErrorAction SilentlyContinue
        if ($curl) {
            & $curl.Source -L --fail --retry 2 --connect-timeout 15 -o $exe $download
            if ($LASTEXITCODE -eq 0 -and (Test-Path $exe)) { $downloaded = $true }
        }
    } catch { Log "curl download failed: $($_.Exception.Message)" }
    if (-not $downloaded) {
        try {
            [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
            Invoke-WebRequest -UseBasicParsing -Uri $download -OutFile $exe -TimeoutSec 120
            if (Test-Path $exe) { $downloaded = $true }
        } catch { Log "PowerShell download failed: $($_.Exception.Message)" }
    }
    if (-not $downloaded) {
        $msg='Could not download cloudflared. Check internet/Windows security, then restart Adam.'
        Log "ERROR: $msg"
        Write-Status 'error' $msg
        Read-Host 'Press Enter to close this tunnel window'
        exit 20
    }
}

try {
    $size=(Get-Item $exe).Length
    if ($size -lt 1000000) { throw "cloudflared.exe is incomplete ($size bytes)" }
    Log "cloudflared ready ($([math]::Round($size/1MB,1)) MB)."
} catch {
    $msg="Tunnel helper validation failed: $($_.Exception.Message)"
    Log "ERROR: $msg"
    Write-Status 'error' $msg
    Read-Host 'Press Enter to close this tunnel window'
    exit 22
}

# Confirm the private guest gateway is alive before exposing it.
Write-Status 'starting' 'Waiting for the Guest Voice gateway...'
$gatewayReady=$false
for($i=0;$i -lt 20;$i++) {
    try {
        $r=Invoke-WebRequest -UseBasicParsing -Uri 'http://127.0.0.1:8771/health' -TimeoutSec 2
        if($r.StatusCode -eq 200){$gatewayReady=$true;break}
    } catch {}
    Start-Sleep -Milliseconds 500
}
if(-not $gatewayReady){
    $msg='Guest Voice gateway on port 8771 did not become ready.'
    Log "ERROR: $msg"
    Write-Status 'error' $msg
    Read-Host 'Press Enter to close this tunnel window'
    exit 23
}
Log 'Guest Voice gateway is healthy.'
Write-Status 'starting' 'Creating trusted HTTPS address...'

try {
    $stdoutFile = Join-Path $data 'cloudflared_stdout.log'
    $stderrFile = Join-Path $data 'cloudflared_stderr.log'
    Remove-Item $stdoutFile,$stderrFile -Force -ErrorAction SilentlyContinue

    # cloudflared writes normal informational output to STDERR.  Do not pipe
    # native STDERR through PowerShell with ErrorActionPreference=Stop because
    # PowerShell 5.1 can promote those harmless INFO lines to NativeCommandError.
    $args = @('tunnel','--url','http://127.0.0.1:8771','--no-autoupdate','--loglevel','info')
    $proc = Start-Process -FilePath $exe -ArgumentList $args -PassThru -WindowStyle Hidden `
        -RedirectStandardOutput $stdoutFile -RedirectStandardError $stderrFile

    $deadline = (Get-Date).AddSeconds(45)
    $lastStdout = 0
    $lastStderr = 0
    $ready = $false
    while((Get-Date) -lt $deadline) {
        foreach($f in @($stdoutFile,$stderrFile)) {
            if(Test-Path $f) {
                $lines = Get-Content $f -ErrorAction SilentlyContinue
                foreach($line in $lines) {
                    if($line -match 'https://[^\s"'']+\.trycloudflare\.com') {
                        $u = $Matches[0].TrimEnd('.',',',';')
                        if(-not $ready) {
                            $u | Set-Content -Encoding ASCII $urlFile
                            Write-Status 'ready' "Trusted HTTPS ready: $u"
                            Log "Trusted HTTPS URL created: $u"
                            Write-Host ''
                            Write-Host '============================================================' -ForegroundColor Green
                            Write-Host "[OK] MOBILE GUEST VOICE HTTPS READY: $u" -ForegroundColor Green
                            Write-Host '============================================================' -ForegroundColor Green
                            $ready = $true
                        }
                    }
                }
            }
        }
        if($ready){ break }
        if($proc.HasExited){ break }
        Start-Sleep -Milliseconds 500
        $proc.Refresh()
    }

    if(-not $ready) {
        $tail = ''
        if(Test-Path $stderrFile) { $tail = ((Get-Content $stderrFile -Tail 12) -join ' | ') }
        if(-not $tail -and (Test-Path $stdoutFile)) { $tail = ((Get-Content $stdoutFile -Tail 12) -join ' | ') }
        if(-not $proc.HasExited) { try { Stop-Process -Id $proc.Id -Force -ErrorAction SilentlyContinue } catch {} }
        $msg='Cloudflare did not publish a trusted HTTPS URL within 45 seconds.'
        if($tail){ $msg += " Last tunnel output: $tail" }
        Log "ERROR: $msg"
        Write-Status 'error' $msg
        Read-Host 'Press Enter to close this tunnel window'
        exit 21
    }

    # Keep this launcher alive while the tunnel is running.
    while(-not $proc.HasExited) {
        Start-Sleep -Seconds 2
        $proc.Refresh()
    }
    $msg="Cloudflare tunnel stopped (exit code $($proc.ExitCode)). Restart Adam to create a new mobile HTTPS address."
    Log "ERROR: $msg"
    Write-Status 'error' $msg
    Read-Host 'Press Enter to close this tunnel window'
    exit 24
} catch {
    $msg="Tunnel launcher failed: $($_.Exception.Message)"
    Log "ERROR: $msg"
    Write-Status 'error' $msg
    Read-Host 'Press Enter to close this tunnel window'
    exit 21
}
