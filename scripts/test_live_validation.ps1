# Test live validation mode
Write-Host "Testing LIVE validation mode..." -ForegroundColor Green

# Create JSON body for live mode
$body = @{
    scenario_id = "dmu_basic_check"
    ip_address = "192.168.11.22" 
    hostname = "dmu"
    mode = "live"
} | ConvertTo-Json

Write-Host "Request body (LIVE mode): $body" -ForegroundColor Yellow

# Make the API call
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8080/api/validation/run" -Method POST -Body $body -ContentType "application/json" -UseBasicParsing
    Write-Host "Response Status: $($response.StatusCode)" -ForegroundColor Green
    Write-Host "Response Content (LIVE):" -ForegroundColor Green
    $response.Content | ConvertFrom-Json | ConvertTo-Json -Depth 10
} catch {
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n" -ForegroundColor White
Write-Host "Testing DRU scenario..." -ForegroundColor Green

# Test DRU scenario
$dru_body = @{
    scenario_id = "dru_remote_check"
    ip_address = "192.168.11.100"
    hostname = "dru34132"
    mode = "mock"
} | ConvertTo-Json

try {
    $response = Invoke-WebRequest -Uri "http://localhost:8080/api/validation/run" -Method POST -Body $dru_body -ContentType "application/json" -UseBasicParsing
    Write-Host "DRU Response Status: $($response.StatusCode)" -ForegroundColor Green
    Write-Host "DRU Response Content:" -ForegroundColor Green
    $response.Content | ConvertFrom-Json | ConvertTo-Json -Depth 10
} catch {
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
}