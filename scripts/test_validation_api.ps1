# Test API validation endpoint
Write-Host "Testing validation API endpoint..." -ForegroundColor Green

# Create JSON body
$body = @{
    scenario_id = "dmu_basic_check"
    ip_address = "192.168.11.22"
    hostname = "dmu"
    mode = "mock"
} | ConvertTo-Json

Write-Host "Request body: $body" -ForegroundColor Yellow

# Make the API call
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8080/api/validation/run" -Method POST -Body $body -ContentType "application/json" -UseBasicParsing
    Write-Host "Response Status: $($response.StatusCode)" -ForegroundColor Green
    Write-Host "Response Content:" -ForegroundColor Green
    $response.Content | ConvertFrom-Json | ConvertTo-Json -Depth 10
} catch {
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
}