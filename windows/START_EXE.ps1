$ErrorActionPreference = "Stop"

$exe = Join-Path $PSScriptRoot "NetworkEncyclopedia.exe"
if (-not (Test-Path $exe)) {
    Write-Error "NetworkEncyclopedia.exe was not found. Extract the complete Windows ZIP first."
    exit 2
}

if (-not $env:NETENC_TOKEN) {
    $secureToken = Read-Host "Enter a strong private sync token" -AsSecureString
    if ($secureToken.Length -eq 0) {
        Write-Error "NETENC_TOKEN must not be empty."
        exit 3
    }
    $bstr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureToken)
    try {
        $env:NETENC_TOKEN = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($bstr)
    } finally {
        [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr)
    }
}

$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"
if (-not $env:NETENC_HOST) { $env:NETENC_HOST = "0.0.0.0" }
if (-not $env:NETENC_PORT) { $env:NETENC_PORT = "5050" }
if (-not $env:NETENC_DEVICE) { $env:NETENC_DEVICE = $env:COMPUTERNAME }

$url = "http://127.0.0.1:$($env:NETENC_PORT)"
Write-Host ""
Write-Host "NetworkEncyclopedia - Engineer Jokar"
Write-Host "Local URL: $url"
Write-Host "Port: $($env:NETENC_PORT)"
Write-Host "Sync token: protected input; not printed"
Write-Host "Keep this window open while the server is running."
Write-Host "Use only trusted Private networks for LAN sync."
Write-Host ""

$proc = Start-Process -FilePath $exe -WorkingDirectory $PSScriptRoot -PassThru -NoNewWindow
$ready = $false
try {
    for ($i = 0; $i -lt 90; $i++) {
        $proc.Refresh()
        if ($proc.HasExited) {
            Write-Warning "The server process exited before the health check completed (exit $($proc.ExitCode))."
            break
        }
        try {
            $health = Invoke-RestMethod -Uri "$url/api/health" -TimeoutSec 2
            if ($health.ok) {
                $ready = $true
                break
            }
        } catch {
            # The service may still be initializing.
        }
        Start-Sleep -Seconds 1
    }

    if ($ready) {
        Write-Host "Server health check passed; opening the browser."
        Start-Process $url
    } else {
        Write-Warning "The server did not become healthy within 90 seconds. Review startup output."
        Write-Host "You can retry manually at $url after the service finishes starting."
    }

    if (-not $proc.HasExited) { Wait-Process -Id $proc.Id }
} finally {
    $env:NETENC_TOKEN = $null
}
