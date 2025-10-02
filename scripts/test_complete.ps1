# DRS Validation Framework - Test Suite Completo
Write-Host "===== DRS VALIDATION FRAMEWORK - SUITE DE PRUEBAS =====" -ForegroundColor Cyan
Write-Host ""

$baseUrl = "http://localhost:8080"
$success = 0
$failures = 0

function Test-Endpoint($name, $url, $method = "GET", $body = $null) {
    Write-Host "Probando: $name" -NoNewline
    try {
        if ($method -eq "POST" -and $body) {
            $response = Invoke-RestMethod -Uri "$baseUrl$url" -Method $method -Body $body -ContentType "application/json"
        } else {
            $response = Invoke-RestMethod -Uri "$baseUrl$url" -Method $method
        }
        Write-Host " ✅ EXITOSO" -ForegroundColor Green
        return $response
    } catch {
        Write-Host " ❌ FALLÓ: $($_.Exception.Message)" -ForegroundColor Red
        return $null
    }
}

Write-Host "1. Probando Health Check..."
$health = Test-Endpoint "Health Check" "/health"
if ($health) { 
    Write-Host "   Estado: $($health.status)" -ForegroundColor Yellow
    $success++
} else { 
    $failures++ 
}

Write-Host ""
Write-Host "2. Probando Scenarios..."
$scenarios = Test-Endpoint "Scenarios" "/api/validation/scenarios"
if ($scenarios) {
    Write-Host "   Escenarios disponibles: $($scenarios.scenarios.Count)" -ForegroundColor Yellow
    foreach ($scenario in $scenarios.scenarios) {
        Write-Host "   - $($scenario.name) ($($scenario.id))" -ForegroundColor Gray
    }
    $success++
} else { 
    $failures++ 
}

Write-Host ""
Write-Host "3. Probando Validación Mock..."
$mockBody = @{
    scenario_id = "dmu_basic_check"
    ip_address = "192.168.11.22"  
    hostname = "dmu"
    mode = "mock"
} | ConvertTo-Json

$mockResult = Test-Endpoint "Validación Mock" "/api/validation/run" "POST" $mockBody
if ($mockResult) {
    Write-Host "   Estado: $($mockResult.result.overall_status)" -ForegroundColor Yellow
    Write-Host "   Pruebas ejecutadas: $($mockResult.result.tests.Count)" -ForegroundColor Yellow
    $success++
} else { 
    $failures++ 
}

Write-Host ""
Write-Host "4. Probando Validación Live..."
$liveBody = @{
    scenario_id = "dru_remote_check"
    ip_address = "192.168.11.100"
    hostname = "dru34132"
    mode = "live"
} | ConvertTo-Json

$liveResult = Test-Endpoint "Validación Live" "/api/validation/run" "POST" $liveBody
if ($liveResult) {
    Write-Host "   Estado: $($liveResult.result.overall_status)" -ForegroundColor Yellow
    Write-Host "   Modo: $($liveResult.mode)" -ForegroundColor Yellow
    $success++
} else { 
    $failures++ 
}

Write-Host ""
Write-Host "5. Probando Ping..."
$pingResult = Test-Endpoint "Ping Test" "/api/validation/ping/8.8.8.8" "POST"
if ($pingResult) {
    Write-Host "   Estado Ping: $($pingResult.status)" -ForegroundColor Yellow
    $success++
} else { 
    $failures++ 
}

Write-Host ""
Write-Host "================= RESUMEN =================" -ForegroundColor Cyan
Write-Host "Pruebas exitosas: $success" -ForegroundColor Green  
Write-Host "Pruebas fallidas: $failures" -ForegroundColor Red
$total = $success + $failures
$percentage = [math]::Round(($success / $total) * 100, 1)
Write-Host "Porcentaje de éxito: $percentage%" -ForegroundColor Yellow

if ($failures -eq 0) {
    Write-Host ""
    Write-Host "🎉 ¡TODAS LAS PRUEBAS PASARON! El framework está funcionando correctamente." -ForegroundColor Green
    Write-Host "🌐 Interfaz web disponible en: $baseUrl" -ForegroundColor Cyan
} else {
    Write-Host ""
    Write-Host "⚠️  Hay $failures prueba(s) fallida(s). Revisar logs para más detalles." -ForegroundColor Yellow
}