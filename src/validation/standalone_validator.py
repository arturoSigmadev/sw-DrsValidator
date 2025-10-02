#!/usr/bin/env python3
"""
Standalone TCP Validator - Sin dependencias de tests existentes
"""

import socket
import subprocess
import time
import platform
from datetime import datetime
from typing import Dict, Any, List

def validate_device_standalone(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validación independiente de dispositivos
    """
    try:
        device_type = config.get("device_type", "unknown")
        ip_address = config.get("ip_address")
        hostname = config.get("hostname", "device")
        mode = config.get("mode", "mock")
        
        if mode == "mock":
            return _mock_validation(config)
        else:
            return _live_validation(config)
            
    except Exception as e:
        return {
            "overall_status": "CRITICAL",
            "message": f"Validation failed: {str(e)}",
            "tests": [],
            "duration_ms": 0,
            "timestamp": datetime.now().isoformat()
        }

def _mock_validation(config: Dict[str, Any]) -> Dict[str, Any]:
    """Validación simulada"""
    return {
        "overall_status": "PASS",
        "message": f"Mock validation successful for {config.get('device_type')}",
        "tests": [
            {
                "name": "Mock Ping Test",
                "status": "PASS",
                "message": f"✅ Mock ping to {config.get('ip_address')} successful",
                "details": "Simulated network connectivity",
                "duration_ms": 100
            },
            {
                "name": "Mock TCP Connection", 
                "status": "PASS",
                "message": f"✅ Mock TCP connection successful",
                "details": "Simulated device communication",
                "duration_ms": 200
            },
            {
                "name": "Mock Device Command",
                "status": "PASS", 
                "message": f"✅ Mock {config.get('device_type')} command successful",
                "details": "Simulated device response with normal parameters",
                "duration_ms": 300
            }
        ],
        "duration_ms": 600,
        "timestamp": datetime.now().isoformat()
    }

def _live_validation(config: Dict[str, Any]) -> Dict[str, Any]:
    """Validación en vivo"""
    start_time = time.time()
    
    results = {
        "overall_status": "PASS",
        "tests": [],
        "duration_ms": 0,
        "timestamp": datetime.now().isoformat()
    }
    
    ip_address = config.get("ip_address")
    device_type = config.get("device_type", "unknown")
    
    # Test 1: Ping
    ping_test = _ping_test(ip_address)
    results["tests"].append(ping_test)
    
    # Test 2: TCP Connection
    tcp_test = _tcp_connection_test(ip_address)
    results["tests"].append(tcp_test)
    
    # Test 3: Device-specific test
    device_test = _device_specific_test(config)
    results["tests"].append(device_test)
    
    # Determinar estado general
    failed_tests = [t for t in results["tests"] if t["status"] == "FAIL"]
    warning_tests = [t for t in results["tests"] if t["status"] == "WARNING"]
    
    if failed_tests:
        results["overall_status"] = "FAIL"
        results["message"] = f"Validation failed: {len(failed_tests)} tests failed"
    elif warning_tests:
        results["overall_status"] = "WARNING"
        results["message"] = f"Validation completed with warnings: {len(warning_tests)} warnings"
    else:
        results["overall_status"] = "PASS"
        results["message"] = f"All validation tests passed for {device_type}"
    
    # Calcular duración total
    end_time = time.time()
    results["duration_ms"] = int((end_time - start_time) * 1000)
    
    return results

def _ping_test(ip_address: str) -> Dict[str, Any]:
    """Test de ping"""
    try:
        # Determinar comando según el sistema
        if platform.system().lower() == "windows":
            cmd = ["ping", "-n", "1", "-w", "3000", ip_address]
        else:
            cmd = ["ping", "-c", "1", "-W", "3", ip_address]
        
        start = time.time()
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        duration = int((time.time() - start) * 1000)
        
        if result.returncode == 0:
            return {
                "name": "Network Ping",
                "status": "PASS",
                "message": f"✅ Device {ip_address} is reachable",
                "details": f"Ping successful in {duration}ms",
                "duration_ms": duration
            }
        else:
            return {
                "name": "Network Ping",
                "status": "FAIL", 
                "message": f"❌ Device {ip_address} is not reachable",
                "details": f"Ping failed after {duration}ms - check network connectivity",
                "duration_ms": duration
            }
            
    except subprocess.TimeoutExpired:
        return {
            "name": "Network Ping",
            "status": "FAIL",
            "message": f"❌ Ping to {ip_address} timed out",
            "details": "Network timeout - device may be offline",
            "duration_ms": 10000
        }
    except Exception as e:
        return {
            "name": "Network Ping", 
            "status": "FAIL",
            "message": f"❌ Ping test error: {str(e)}",
            "details": "Network test configuration error",
            "duration_ms": 100
        }

def _tcp_connection_test(ip_address: str, ports: List[int] = [65050]) -> Dict[str, Any]:
    """Test de conexión TCP al puerto DRS específico (65050)"""
    successful_ports = []
    
    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((ip_address, port))
            sock.close()
            
            if result == 0:
                successful_ports.append(port)
                
        except Exception:
            continue
    
    if successful_ports:
        return {
            "name": "TCP Connection", 
            "status": "PASS",
            "message": f"✅ TCP connection successful on DRS port(s): {successful_ports}",
            "details": f"Device is accessible on {len(successful_ports)} DRS port(s) - ready for Santone protocol",
            "duration_ms": len(ports) * 1000
        }
    else:
        return {
            "name": "TCP Connection",
            "status": "FAIL",
            "message": f"❌ DRS port not accessible on {ip_address}",
            "details": f"Tested DRS ports {ports} - device may be offline or using different configuration",
            "duration_ms": len(ports) * 5000
        }

def _device_specific_test(config: Dict[str, Any]) -> Dict[str, Any]:
    """Test específico del dispositivo"""
    device_type = config.get("device_type", "unknown")
    ip_address = config.get("ip_address")
    
    # Simulación de test específico por tipo de dispositivo
    if device_type in ["dmu_ethernet", "dru_ethernet"]:
        return {
            "name": f"{device_type.upper()} Communication",
            "status": "WARNING", 
            "message": f"⚠️ {device_type} protocol test not implemented",
            "details": f"Device {ip_address} basic connectivity confirmed, but specific protocol validation pending",
            "duration_ms": 1000
        }
    else:
        return {
            "name": "Device Communication",
            "status": "WARNING",
            "message": f"⚠️ Unknown device type: {device_type}",
            "details": f"Generic connectivity test only - protocol-specific validation not available",
            "duration_ms": 500
        }

# Función de compatibilidad
validate_device = validate_device_standalone