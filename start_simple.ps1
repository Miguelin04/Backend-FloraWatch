# FloraWatch - Script de Inicio Simple
Write-Host "INICIANDO FLORAWATCH BACKEND..." -ForegroundColor Green

# Activar entorno virtual
Write-Host "Activando entorno virtual..." -ForegroundColor Yellow
& ".\virtual_311\Scripts\Activate.ps1"

# Configurar GDAL
Write-Host "Configurando GDAL..." -ForegroundColor Yellow
$currentPath = Get-Location
$env:GDAL_LIBRARY_PATH = "$currentPath\virtual_311\Lib\site-packages\osgeo\gdal.dll"
$env:GDAL_DATA = "$currentPath\virtual_311\Lib\site-packages\osgeo\data"
$env:DB_PORT = "5433"

Write-Host "GDAL configurado correctamente" -ForegroundColor Green

# Mostrar URLs importantes
Write-Host ""
Write-Host "SERVIDOR DJANGO INICIANDO..." -ForegroundColor Green
Write-Host "URL Principal: http://localhost:8000/" -ForegroundColor Cyan
Write-Host "Admin Panel: http://localhost:8000/admin/" -ForegroundColor Cyan
Write-Host "API Status: http://localhost:8000/api/status/" -ForegroundColor Cyan
Write-Host ""
Write-Host "Presiona Ctrl+C para detener el servidor" -ForegroundColor Yellow
Write-Host ""

# Iniciar servidor Django
python manage.py runserver