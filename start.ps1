<#
.SYNOPSIS
Starts the Multi-Modal Evidence Review Enterprise Application (Backend + Frontend).

.DESCRIPTION
This script installs frontend dependencies and launches both the FastAPI backend and Next.js frontend concurrently.
#>

$ErrorActionPreference = "Stop"

Write-Host "🚀 Starting Multi-Modal Evidence Review Enterprise Application..." -ForegroundColor Cyan

# Install Python dependencies if needed
Write-Host "📦 Ensuring Python dependencies are installed..." -ForegroundColor Yellow
python -m pip install -r requirements.txt -q
python -m pip install python-multipart uvicorn -q

# Install Node dependencies if needed
Write-Host "📦 Ensuring Node dependencies are installed..." -ForegroundColor Yellow
Set-Location -Path "frontend"
npm install --silent
Set-Location -Path ".."

Write-Host "🌐 Launching FastAPI Backend (Port 8000)..." -ForegroundColor Green
$BackendProcess = Start-Process -FilePath "python" -ArgumentList "-m uvicorn backend.app.main:app --reload --port 8000" -PassThru -NoNewWindow

Write-Host "🎨 Launching Next.js Frontend (Port 3000)..." -ForegroundColor Magenta
Set-Location -Path "frontend"
$FrontendProcess = Start-Process -FilePath "npm" -ArgumentList "run dev" -PassThru -NoNewWindow
Set-Location -Path ".."

Write-Host "`n✅ Both servers are running!" -ForegroundColor Green
Write-Host "👉 Dashboard UI: http://localhost:3000" -ForegroundColor White
Write-Host "👉 API Docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host "`nPress Ctrl+C to stop both servers." -ForegroundColor Gray

try {
    while ($true) {
        Start-Sleep -Seconds 1
    }
}
finally {
    Write-Host "`n🛑 Stopping servers..." -ForegroundColor Red
    if (!($BackendProcess.HasExited)) { Stop-Process -Id $BackendProcess.Id -Force }
    if (!($FrontendProcess.HasExited)) { Stop-Process -Id $FrontendProcess.Id -Force }
}
