$ErrorActionPreference = 'SilentlyContinue'
$healthUrl = 'http://127.0.0.1:8770/api/health'
$appUrl = 'http://127.0.0.1:8770/'

for ($i = 0; $i -lt 60; $i++) {
    try {
        $response = Invoke-WebRequest -Uri $healthUrl -UseBasicParsing -TimeoutSec 1
        if ($response.StatusCode -eq 200) {
            Start-Process $appUrl
            exit 0
        }
    } catch {
        # Adam is still starting. Try again shortly.
    }
    Start-Sleep -Milliseconds 500
}

# Fallback: open the page even if the health probe was blocked locally.
Start-Process $appUrl
exit 0
