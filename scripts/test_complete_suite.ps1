# Comprehensive Test Suite for DRS Validation Framework
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  DRS VALIDATION FRAMEWORK TEST SUITE" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

$testsPassed = 0
$testsFailed = 0

# Test 1: Health Check
Write-Host "`n1. Testing Health Check..." -ForegroundColor Yellow
try {
    $healthResponse = Invoke-WebRequest -Uri "http://localhost:8080/health" -UseBasicParsing
    $healthData = $healthResponse.Content | ConvertFrom-Json
    if ($healthData.status -eq "healthy") {
        Write-Host "   ✅ PASS - Health Check: $($healthData.status)" -ForegroundColor Green
        $testsPassed++
    } else {
        Write-Host "   ❌ FAIL - Health Check" -ForegroundColor Red
        $testsFailed++
    }
} catch {
    Write-Host "   ❌ FAIL - Health Check Error: $($_.Exception.Message)" -ForegroundColor Red
    $testsFailed++
}

# Test 2: Scenarios API
Write-Host "`n2. Testing Scenarios API..." -ForegroundColor Yellow
try {
    $scenariosResponse = Invoke-WebRequest -Uri "http://localhost:8080/api/validation/scenarios" -UseBasicParsing
    $scenariosData = $scenariosResponse.Content | ConvertFrom-Json
    $scenarioCount = $scenariosData.scenarios.Count
    if ($scenarioCount -gt 0) {
        Write-Host "   ✅ PASS - Scenarios API: $scenarioCount scenarios available" -ForegroundColor Green
        foreach ($scenario in $scenariosData.scenarios) {
            Write-Host "      • $($scenario.name) ($($scenario.id))" -ForegroundColor Gray
        }
        $testsPassed++
    } else {
        Write-Host "   ❌ FAIL - No scenarios found" -ForegroundColor Red
        $testsFailed++
    }
} catch {
    Write-Host "   ❌ FAIL - Scenarios API Error: $($_.Exception.Message)" -ForegroundColor Red
    $testsFailed++
}

# Test 3: DMU Mock Validation
Write-Host "`n3. Testing DMU Mock Validation..." -ForegroundColor Yellow
try {
    $dmuBody = @{
        scenario_id = "dmu_basic_check"
        ip_address = "192.168.11.22"
        hostname = "dmu"
        mode = "mock"
    } | ConvertTo-Json
    
    $dmuResponse = Invoke-WebRequest -Uri "http://localhost:8080/api/validation/run" -Method POST -Body $dmuBody -ContentType "application/json" -UseBasicParsing
    $dmuData = $dmuResponse.Content | ConvertFrom-Json
    
    if ($dmuData.status -eq "success" -and $dmuData.result.overall_status -eq "PASS") {
        Write-Host "   ✅ PASS - DMU Mock Validation: $($dmuData.result.overall_status)" -ForegroundColor Green
        Write-Host "      • Tests executed: $($dmuData.result.tests.Count)" -ForegroundColor Gray
        $testsPassed++
    } else {
        Write-Host "   ❌ FAIL - DMU Mock Validation: $($dmuData.result.overall_status)" -ForegroundColor Red
        $testsFailed++
    }
} catch {
    Write-Host "   ❌ FAIL - DMU Mock Validation Error: $($_.Exception.Message)" -ForegroundColor Red
    $testsFailed++
}

# Test 4: DRU Mock Validation  
Write-Host "`n4. Testing DRU Mock Validation..." -ForegroundColor Yellow
try {
    $druBody = @{
        scenario_id = "dru_remote_check"
        ip_address = "192.168.11.100"
        hostname = "dru34132"
        mode = "mock"
    } | ConvertTo-Json
    
    $druResponse = Invoke-WebRequest -Uri "http://localhost:8080/api/validation/run" -Method POST -Body $druBody -ContentType "application/json" -UseBasicParsing
    $druData = $druResponse.Content | ConvertFrom-Json
    
    if ($druData.status -eq "success" -and $druData.result.overall_status -eq "PASS") {
        Write-Host "   ✅ PASS - DRU Mock Validation: $($druData.result.overall_status)" -ForegroundColor Green
        Write-Host "      • Tests executed: $($druData.result.tests.Count)" -ForegroundColor Gray
        $testsPassed++
    } else {
        Write-Host "   ❌ FAIL - DRU Mock Validation: $($druData.result.overall_status)" -ForegroundColor Red
        $testsFailed++
    }
} catch {
    Write-Host "   ❌ FAIL - DRU Mock Validation Error: $($_.Exception.Message)" -ForegroundColor Red
    $testsFailed++
}

# Test 5: API Documentation
Write-Host "`n5. Testing API Documentation..." -ForegroundColor Yellow
try {
    $docsResponse = Invoke-WebRequest -Uri "http://localhost:8080/api/docs" -UseBasicParsing
    if ($docsResponse.StatusCode -eq 200) {
        Write-Host "   ✅ PASS - API Documentation accessible" -ForegroundColor Green
        $testsPassed++
    } else {
        Write-Host "   ❌ FAIL - API Documentation not accessible" -ForegroundColor Red
        $testsFailed++
    }
} catch {
    Write-Host "   ❌ FAIL - API Documentation Error: $($_.Exception.Message)" -ForegroundColor Red
    $testsFailed++
}

# Test 6: Web Interface
Write-Host "`n6. Testing Web Interface..." -ForegroundColor Yellow
try {
    $webResponse = Invoke-WebRequest -Uri "http://localhost:8080" -UseBasicParsing
    if ($webResponse.StatusCode -eq 200 -and $webResponse.Content -match "DRS.*Validation") {
        Write-Host "   ✅ PASS - Web Interface accessible" -ForegroundColor Green
        $testsPassed++
    } else {
        Write-Host "   ❌ FAIL - Web Interface not properly configured" -ForegroundColor Red
        $testsFailed++
    }
} catch {
    Write-Host "   ❌ FAIL - Web Interface Error: $($_.Exception.Message)" -ForegroundColor Red
    $testsFailed++
}

# Summary
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "               TEST SUMMARY" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Tests Passed: $testsPassed" -ForegroundColor Green
Write-Host "Tests Failed: $testsFailed" -ForegroundColor Red
$totalTests = $testsPassed + $testsFailed
$successRate = [math]::Round(($testsPassed / $totalTests * 100), 2)
Write-Host "Success Rate: $successRate%" -ForegroundColor Cyan

if ($testsFailed -eq 0) {
    Write-Host "`n🎉 ALL TESTS PASSED! Framework is fully functional." -ForegroundColor Green
    Write-Host "🌐 Web Interface: http://localhost:8080" -ForegroundColor Cyan
    Write-Host "📚 API Documentation: http://localhost:8080/api/docs" -ForegroundColor Cyan
} else {
    Write-Host "`n⚠️ Some tests failed. Please check the implementation." -ForegroundColor Yellow
}

Write-Host "========================================" -ForegroundColor Cyan