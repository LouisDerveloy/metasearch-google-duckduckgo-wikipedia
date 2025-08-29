# MetaSearch Engine - Launcher invisible
Add-Type -AssemblyName System.Windows.Forms

# Build si dist n'existe pas
if (!(Test-Path "./dist")) {
    Write-Host "Build frontend..." -ForegroundColor Yellow
    Start-Process "npm" -ArgumentList "run", "build" -Wait -WindowStyle Hidden
}

# Lancer frontend comme processus indépendant
$frontendProcess = Start-Process powershell -ArgumentList @(
    "-WindowStyle", "Hidden",
    "-Command", "Set-Location '$PWD'; `$Host.UI.RawUI.WindowTitle = 'MetaSearch-Frontend'; npm run preview"
) -PassThru

# Lancer API comme processus indépendant
$apiProcess = Start-Process powershell -ArgumentList @(
    "-WindowStyle", "Hidden",
    "-Command", "Set-Location '$PWD'; cd api; & '.\venv\Scripts\Activate.ps1'; `$Host.UI.RawUI.WindowTitle = 'MetaSearch-API'; python main.py"
) -PassThru

exit 0
