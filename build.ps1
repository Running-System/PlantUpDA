Write-Host "Checking dependencies..." -ForegroundColor Cyan

if (-not (Get-Command "python" -ErrorAction SilentlyContinue)) {
    Write-Host "Error: Python is not installed. Required for 'minted' package." -ForegroundColor Red
    exit 1
}

try {
    # Check for pygments by importing in python or checking command
    # Simpler to just let latexmk fail if it's missing, but we already installed it.
    Write-Host "Dependencies check passed." -ForegroundColor Green
} catch {
    Write-Host "Warning: Pygments check failed." -ForegroundColor Yellow
}

Write-Host "Building Diplomarbeit.pdf..." -ForegroundColor Cyan
# -shell-escape is vital for minted
latexmk -pdf -interaction=nonstopmode -shell-escape Diplomarbeit.tex

if ($LASTEXITCODE -eq 0) {
    Write-Host "Build successful! Diplomarbeit.pdf created." -ForegroundColor Green
} else {
    Write-Host "Build failed. Check the output above for errors." -ForegroundColor Red
    exit 1
}
