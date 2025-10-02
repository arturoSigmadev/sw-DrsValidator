# Test ping endpoint
$body = @{
    host = "192.168.11.22"
} | ConvertTo-Json

Write-Host "Testing ping endpoint..."
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8080/api/validation/ping" -Method POST -Body $body -ContentType "application/json"
    Write-Host "SUCCESS: $($response | ConvertTo-Json -Depth 3)"
} catch {
    Write-Host "ERROR: $($_.Exception.Message)"
}