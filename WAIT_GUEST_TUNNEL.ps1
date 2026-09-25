$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$urlFile = Join-Path $root 'data\guest_public_base_url.txt'
$logFile = Join-Path $root 'data\guest_tunnel.log'
for($i=0; $i -lt 45; $i++) {
    if(Test-Path $urlFile) {
        $u=(Get-Content $urlFile -Raw).Trim()
        if($u.StartsWith('https://')) {
            Write-Host "[OK] Mobile Guest Voice HTTPS ready: $u"
            exit 0
        }
    }
    Start-Sleep -Seconds 1
}
Write-Host "[WARNING] Trusted Guest Voice tunnel is not ready yet."
Write-Host "Check: $logFile"
exit 1
