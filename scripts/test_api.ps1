# Test API endpoints
$body = @{
    scenario_id = "dmu_basic_check"
    ip_address = "192.168.11.22"
    hostname = "dmu"
    mode = "mock"
} | ConvertTo-Json

Write-Host "Testing validation endpoint..."
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8080/api/validation/run" -Method POST -Body $body -ContentType "application/json"
    Write-Host "SUCCESS: $($response | ConvertTo-Json -Depth 5)"
} catch {
    Write-Host "ERROR: $($_.Exception.Message)"
    Write-Host "Response: $($_.Exception.Response | Out-String)"
}