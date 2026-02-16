# PowerShell script to start MySQL and MongoDB services
# Run this script as Administrator

Write-Host "=== Starting Database Services ===" -ForegroundColor Cyan
Write-Host ""

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "[WARNING] This script should be run as Administrator" -ForegroundColor Yellow
    Write-Host "Right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    Write-Host ""
}

# Start MySQL
Write-Host "Starting MySQL..." -ForegroundColor Yellow
try {
    $mysqlService = Get-Service -Name "MySQL" -ErrorAction SilentlyContinue
    if ($mysqlService) {
        if ($mysqlService.Status -eq 'Running') {
            Write-Host "[OK] MySQL is already running" -ForegroundColor Green
        } else {
            Start-Service -Name "MySQL" -ErrorAction Stop
            Write-Host "[OK] MySQL started successfully" -ForegroundColor Green
        }
    } else {
        Write-Host "[X] MySQL service not found. Please check if MySQL is installed." -ForegroundColor Red
        Write-Host "    Try: Get-Service | Where-Object {`$_.DisplayName -like '*MySQL*'}" -ForegroundColor Gray
    }
} catch {
    Write-Host "[X] Error starting MySQL: $_" -ForegroundColor Red
}

Write-Host ""

# Start MongoDB
Write-Host "Starting MongoDB..." -ForegroundColor Yellow
try {
    $mongoService = Get-Service -Name "MongoDB" -ErrorAction SilentlyContinue
    if ($mongoService) {
        if ($mongoService.Status -eq 'Running') {
            Write-Host "[OK] MongoDB is already running" -ForegroundColor Green
        } else {
            Start-Service -Name "MongoDB" -ErrorAction Stop
            Write-Host "[OK] MongoDB started successfully" -ForegroundColor Green
        }
    } else {
        Write-Host "[X] MongoDB service not found. Please check if MongoDB is installed." -ForegroundColor Red
        Write-Host "    Try: Get-Service | Where-Object {`$_.DisplayName -like '*Mongo*'}" -ForegroundColor Gray
    }
} catch {
    Write-Host "[X] Error starting MongoDB: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "=== Service Status ===" -ForegroundColor Cyan
Get-Service MySQL, MongoDB -ErrorAction SilentlyContinue | Format-Table Name, Status, DisplayName

Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Run: python check_databases.py" -ForegroundColor White
Write-Host "2. Run: python setup_databases.py" -ForegroundColor White
Write-Host "3. Run: python seed_data.py (optional)" -ForegroundColor White
Write-Host "4. Run: python app.py" -ForegroundColor White
