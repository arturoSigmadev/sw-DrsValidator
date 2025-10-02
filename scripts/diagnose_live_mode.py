#!/usr/bin/env python3
"""
Script de diagnóstico para troubleshooting del modo live
"""

import requests
import json
import time
import sys
from typing import Dict, Any

class ValidationDiagnostics:
    def __init__(self, base_url: str = "http://192.168.60.140:8080"):
        self.base_url = base_url
        
    def test_health_endpoint(self) -> bool:
        """Test básico de conectividad"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=10)
            print(f"✅ Health check: {response.status_code}")
            print(f"   Response: {response.json()}")
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Health check failed: {e}")
            return False
    
    def test_mock_validation(self) -> bool:
        """Test validación en modo mock"""
        try:
            payload = {
                "scenario_id": "lna-santone",
                "ip_address": "192.168.11.22", 
                "hostname": "test_dmu",
                "mode": "mock"
            }
            
            response = requests.post(
                f"{self.base_url}/api/validation/run",
                json=payload,
                timeout=30
            )
            
            print(f"✅ Mock validation: {response.status_code}")
            response_data = response.json()
            result = response_data.get('result', {})
            print(f"   Overall Status: {result.get('overall_status', 'unknown')}")
            print(f"   Tests: {len(result.get('tests', []))}")
            
            return response.status_code == 200 and result.get('overall_status') in ['PASS', 'WARNING']
            
        except Exception as e:
            print(f"❌ Mock validation failed: {e}")
            return False
    
    def test_live_validation(self, ip_address: str = "192.168.11.22") -> Dict[str, Any]:
        """Test validación en modo live"""
        try:
            payload = {
                "scenario_id": "lna-santone",
                "ip_address": ip_address,
                "hostname": "live_test_dmu", 
                "mode": "live"
            }
            
            print(f"🔬 Testing live validation with IP: {ip_address}")
            start_time = time.time()
            
            response = requests.post(
                f"{self.base_url}/api/validation/run",
                json=payload,
                timeout=60
            )
            
            duration = time.time() - start_time
            response_data = response.json()
            result = response_data.get('result', {})
            
            print(f"⏱️  Duration: {duration:.2f}s")
            print(f"📊 Response status: {response.status_code}")
            print(f"📈 Validation status: {result.get('overall_status', 'unknown')}")
            
            # Analizar tests individuales
            tests = result.get('tests', [])
            print(f"\n🧪 Individual tests ({len(tests)}):")
            for i, test in enumerate(tests, 1):
                status_emoji = "✅" if test['status'] == 'PASS' else ("⚠️" if test['status'] == 'WARNING' else "❌")
                print(f"   {i}. {status_emoji} {test['name']}: {test['message']}")
            
            return response_data
            
        except requests.exceptions.Timeout:
            print(f"⏰ Live validation timed out after 60s")
            return {"error": "timeout", "duration": 60}
        except Exception as e:
            print(f"❌ Live validation failed: {e}")
            return {"error": str(e)}
    
    def test_different_ips(self) -> None:
        """Probar con diferentes IPs"""
        test_ips = [
            "192.168.11.22",   # IP por defecto DMU
            "192.168.11.100",  # IP por defecto DRU
            "127.0.0.1",       # Localhost
            "8.8.8.8"          # Google DNS (para test de conectividad)
        ]
        
        print("\n🌐 Testing different IP addresses:")
        for ip in test_ips:
            print(f"\n--- Testing IP: {ip} ---")
            result = self.test_live_validation(ip)
            
            # Pequeña pausa entre tests
            time.sleep(2)
    
    def check_container_logs(self) -> None:
        """Revisar logs del contenedor (requiere SSH)"""
        try:
            import subprocess
            
            print("\n📋 Recent container logs:")
            result = subprocess.run([
                "ssh", "root@192.168.60.140", 
                "docker logs --tail 10 drs-validation-framework-service"
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                print(result.stdout)
            else:
                print(f"❌ Could not fetch logs: {result.stderr}")
                
        except Exception as e:
            print(f"❌ Log check failed: {e}")
    
    def run_full_diagnostics(self) -> None:
        """Ejecutar diagnóstico completo"""
        print("🔍 DRS Validation Framework - Diagnostics")
        print("=" * 50)
        
        # 1. Test básico de salud
        print("\n1️⃣ Health Check")
        health_ok = self.test_health_endpoint()
        
        # 2. Test modo mock
        print("\n2️⃣ Mock Mode Test")
        mock_ok = self.test_mock_validation()
        
        # 3. Test modo live con IP específica
        print("\n3️⃣ Live Mode Test")
        live_result = self.test_live_validation()
        
        # 4. Test con diferentes IPs
        print("\n4️⃣ Multiple IP Tests")
        self.test_different_ips()
        
        # 5. Check logs
        print("\n5️⃣ Container Logs")
        self.check_container_logs()
        
        # Resumen
        print("\n" + "=" * 50)
        print("📊 DIAGNOSTIC SUMMARY")
        print(f"   Health Check: {'✅ OK' if health_ok else '❌ FAIL'}")
        print(f"   Mock Mode: {'✅ OK' if mock_ok else '❌ FAIL'}")
        print(f"   Live Mode: {'✅ OK' if 'error' not in live_result else '❌ FAIL'}")

def main():
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = "http://192.168.60.140:8080"
    
    print(f"🎯 Target URL: {base_url}")
    
    diagnostics = ValidationDiagnostics(base_url)
    diagnostics.run_full_diagnostics()

if __name__ == "__main__":
    main()