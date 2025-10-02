# Test ping endpoint with path parameter
Write-Host "Testing ping endpoint..."
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8080/api/validation/ping/192.168.11.22" -Method POST -ContentType "application/json"
    Write-Host "SUCCESS: $($response | ConvertTo-Json -Depth 3)"
} catch {
    Write-Host "ERROR: $($_.Exception.Message)"
}