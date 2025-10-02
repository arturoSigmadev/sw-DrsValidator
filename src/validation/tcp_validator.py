#!/usr/bin/env python3
"""
TCP Validator - Reutiliza lógica de tests existentes para validación de técnicos.
"""

import sys
import os
import logging
from pathlib import Path
from unittest.mock import patch, MagicMock
import subprocess
import socket
from typing import Dict, Any, Optional

# Path setup is simplified as this module is part of the 'src' package
project_root = Path(__file__).parent.parent.parent

# The following imports are removed as they are an anti-pattern.
# The code will rely on the subprocess fallback.
IMPORTS_AVAILABLE = False


class TechnicianTCPValidator:
    """
    Validador TCP para técnicos de campo.
    Reutiliza la lógica de tests existentes pero presenta resultados amigables.
    """
    
    def __init__(self):
        self.project_root = project_root
        self.check_eth_script = project_root / "plugins" / "check_eth.py"
    
    def validate_device_mock_mode(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validación en modo simulado usando patrones de test_tcp_transceiver.py
        """
        try:
            device_type = config.get("device_type")
            ip_address = config.get("ip_address")
            hostname = config.get("hostname", "test-device")
            
            # Definir respuestas mock para diferentes tipos de dispositivos
            mock_responses = self._get_mock_responses(device_type)
            
            results = {
                "overall_status": "PASS",
                "tests": [],
                "duration_ms": 0,
                "timestamp": self._get_timestamp()
            }
            
            # Test 1: Conectividad TCP básica
            tcp_test = self._mock_tcp_connectivity_test(ip_address, mock_responses)
            results["tests"].append(tcp_test)
            
            # Test 2: Comando de grupo (group_query)
            group_test = self._mock_group_query_test(device_type, mock_responses)
            results["tests"].append(group_test)
            
            # Test 3: Validación de thresholds
            threshold_test = self._mock_threshold_validation(config, mock_responses)
            results["tests"].append(threshold_test)
            
            # Determinar estado general
            failed_tests = [t for t in results["tests"] if t["status"] == "FAIL"]
            warning_tests = [t for t in results["tests"] if t["status"] == "WARNING"]
            
            if failed_tests:
                results["overall_status"] = "FAIL"
            elif warning_tests:
                results["overall_status"] = "WARNING"
                
            return results
            
        except Exception as e:
            return {
                "overall_status": "CRITICAL",
                "error": f"Mock validation failed: {str(e)}",
                "action": "Check validation configuration and try again",
                "tests": [],
                "duration_ms": 0,
                "timestamp": self._get_timestamp()
            }
    
    def validate_device_live_mode(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validación en modo en vivo usando patrones de test_check_eth_integration.py
        """
        try:
            device_type = config.get("device_type")
            ip_address = config.get("ip_address")
            hostname = config.get("hostname", "device")
            
            results = {
                "overall_status": "PASS",
                "tests": [],
                "duration_ms": 0,
                "timestamp": self._get_timestamp()
            }
            
            # Test 1: Ping básico
            ping_test = self._live_ping_test(ip_address)
            results["tests"].append(ping_test)
            
            # Si ping falla, no continuar con otros tests
            if ping_test["status"] == "FAIL":
                results["overall_status"] = "FAIL"
                return results
            
            # Test 2: Conexión TCP al puerto del dispositivo
            tcp_test = self._live_tcp_connection_test(ip_address)
            results["tests"].append(tcp_test)
            
            # Test 3: Comando check_eth real
            if IMPORTS_AVAILABLE:
                check_eth_test = self._live_check_eth_test(config)
                results["tests"].append(check_eth_test)
            else:
                # Fallback si no están disponibles los imports
                subprocess_test = self._live_subprocess_test(config)
                results["tests"].append(subprocess_test)
            
            # Determinar estado general
            failed_tests = [t for t in results["tests"] if t["status"] == "FAIL"]
            warning_tests = [t for t in results["tests"] if t["status"] == "WARNING"]
            
            if failed_tests:
                results["overall_status"] = "FAIL"
            elif warning_tests:
                results["overall_status"] = "WARNING"
                
            return results
            
        except Exception as e:
            return {
                "overall_status": "CRITICAL",
                "error": f"Live validation failed: {str(e)}",
                "action": "Check device connection and network configuration",
                "tests": [],
                "duration_ms": 0,
                "timestamp": self._get_timestamp()
            }
    
    # ==================== MÉTODOS AUXILIARES ====================
    
    def _get_mock_responses(self, device_type: str) -> Dict[str, Any]:
        """Generar respuestas mock según el tipo de dispositivo"""
        mock_data = {
            "dmu_ethernet": {
                "temperature": 42,
                "signal_strength": -35,
                "status": "OK",
                "uplink": -38,
                "downlink": -32
            },
            "dru_ethernet": {
                "temperature": 38,
                "signal_strength": -30,
                "status": "OK",
                "uplink": -35,
                "downlink": -28
            },
            "discovery_ethernet": {
                "devices_found": 2,
                "status": "OK",
                "scan_duration": 5.2
            }
        }
        return mock_data.get(device_type, mock_data["dmu_ethernet"])
    
    def _mock_tcp_connectivity_test(self, ip_address: str, mock_responses: Dict) -> Dict[str, Any]:
        """Simular test de conectividad TCP"""
        return {
            "name": "TCP Connectivity",
            "status": "PASS",
            "message": f"✅ TCP connection to {ip_address} simulated successfully",
            "details": f"Mock connection established on port 65050 (simulated)",
            "duration_ms": 50
        }
    
    def _mock_group_query_test(self, device_type: str, mock_responses: Dict) -> Dict[str, Any]:
        """Simular test de group query"""
        temp = mock_responses.get("temperature", 40)
        return {
            "name": "Group Query Command",
            "status": "PASS",
            "message": f"✅ Group query for {device_type} successful",
            "details": f"Mock response: temp={temp}°C, signal={mock_responses.get('signal_strength', -35)}dBm",
            "duration_ms": 100
        }
    
    def _mock_threshold_validation(self, config: Dict, mock_responses: Dict) -> Dict[str, Any]:
        """Simular validación de thresholds"""
        temp = mock_responses.get("temperature", 40)
        temp_warning = config.get("temp_warning", 45)
        
        if temp >= temp_warning:
            return {
                "name": "Threshold Validation",
                "status": "WARNING", 
                "message": f"⚠️ Temperature {temp}°C above warning threshold {temp_warning}°C",
                "details": "Device temperature is elevated but within operating range",
                "duration_ms": 25
            }
        else:
            return {
                "name": "Threshold Validation",
                "status": "PASS",
                "message": f"✅ All thresholds within normal range",
                "details": f"Temperature {temp}°C < warning {temp_warning}°C",
                "duration_ms": 25
            }
    
    def _live_ping_test(self, ip_address: str) -> Dict[str, Any]:
        """Test de ping real"""
        try:
            import platform
            ping_cmd = ["ping", "-n", "1"] if platform.system() == "Windows" else ["ping", "-c", "1"]
            ping_cmd.append(ip_address)
            
            result = subprocess.run(ping_cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                return {
                    "name": "Network Ping",
                    "status": "PASS",
                    "message": f"✅ Device {ip_address} is reachable",
                    "details": "Network connectivity confirmed",
                    "duration_ms": 500
                }
            else:
                return {
                    "name": "Network Ping", 
                    "status": "FAIL",
                    "message": f"❌ Device {ip_address} is not reachable",
                    "details": "Check network cable, device power, and IP configuration",
                    "duration_ms": 1000
                }
        except Exception as e:
            return {
                "name": "Network Ping",
                "status": "FAIL", 
                "message": f"❌ Ping test failed: {str(e)}",
                "details": "Network test error - check system configuration",
                "duration_ms": 100
            }
    
    def _live_tcp_connection_test(self, ip_address: str, port: int = 65050) -> Dict[str, Any]:
        """Test de conexión TCP real"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((ip_address, port))
            sock.close()
            
            if result == 0:
                return {
                    "name": "TCP Connection",
                    "status": "PASS",
                    "message": f"✅ TCP connection to {ip_address}:{port} successful",
                    "details": "Device TCP port is accessible",
                    "duration_ms": 200
                }
            else:
                return {
                    "name": "TCP Connection",
                    "status": "FAIL",
                    "message": f"❌ TCP connection to {ip_address}:{port} failed",
                    "details": "Device may be offline or port blocked",
                    "duration_ms": 5000
                }
        except Exception as e:
            return {
                "name": "TCP Connection",
                "status": "FAIL",
                "message": f"❌ TCP connection error: {str(e)}",
                "details": "Network connection issue",
                "duration_ms": 1000
            }
    
    def _live_check_eth_test(self, config: Dict) -> Dict[str, Any]:
        """Test usando check_eth real (cuando imports están disponibles)"""
        try:
            # Aquí iría la lógica real de check_eth cuando los imports estén disponibles
            return {
                "name": "Check Eth Command",
                "status": "PASS",
                "message": "✅ check_eth command executed successfully",
                "details": "Device communication and data parsing successful",
                "duration_ms": 2000
            }
        except Exception as e:
            return {
                "name": "Check Eth Command",
                "status": "FAIL",
                "message": f"❌ check_eth execution failed: {str(e)}",
                "details": "Device command execution error",
                "duration_ms": 1000
            }
    
    def _live_subprocess_test(self, config: Dict) -> Dict[str, Any]:
        """Test usando subprocess como fallback"""
        try:
            device_type = config.get("device_type")
            ip_address = config.get("ip_address")
            hostname = config.get("hostname", "device")
            
            cmd = [
                sys.executable, str(self.check_eth_script),
                '--address', ip_address,
                '--device', device_type,
                '--hostname', hostname,
            ]
            
            # Log del comando que se va a ejecutar
            logging.info(f"🔧 Ejecutando comando DRS: {' '.join(cmd)}")
            
            # Ejecutar con timeout
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            # Log de la respuesta
            logging.info(f"📥 Respuesta del comando - Código: {result.returncode}")
            if result.stdout:
                logging.info(f"📥 STDOUT: {result.stdout.strip()}")
            if result.stderr:
                logging.warning(f"📥 STDERR: {result.stderr.strip()}")
            
            if result.returncode == 0:
                return {
                    "name": "Device Command",
                    "status": "PASS", 
                    "message": f"✅ {device_type} command successful",
                    "details": f"Device at {ip_address} responded correctly",
                    "duration_ms": 3000
                }
            else:
                return {
                    "name": "Device Command",
                    "status": "FAIL",
                    "message": f"❌ {device_type} command failed",
                    "details": f"Error: {result.stderr or 'Unknown error'}",
                    "duration_ms": 5000
                }
                
        except subprocess.TimeoutExpired:
            return {
                "name": "Device Command",
                "status": "FAIL",
                "message": "❌ Device command timeout",
                "details": "Command took too long - device may be unresponsive",
                "duration_ms": 30000
            }
        except Exception as e:
            return {
                "name": "Device Command", 
                "status": "FAIL",
                "message": f"❌ Command execution error: {str(e)}",
                "details": "System error during command execution",
                "duration_ms": 1000
            }
    
    def _get_timestamp(self) -> str:
        """Obtener timestamp actual"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def ping_device(self, ip_address: str) -> Dict[str, Any]:
        """Test de ping público para técnicos"""
        return self._live_ping_test(ip_address)


# Función de conveniencia para usar desde la API
def validate_device(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Función principal para validar dispositivos.
    
    Args:
        config: Configuración del dispositivo con keys:
            - device_type: Tipo de dispositivo (dmu_ethernet, dru_ethernet, etc.)
            - ip_address: Dirección IP del dispositivo
            - hostname: Nombre del dispositivo
            - mode: Modo de validación ('mock' o 'live')
            
    Returns:
        Dict con resultado de la validación para técnicos
    """
    validator = TechnicianTCPValidator()
    mode = config.get('mode', 'mock')
    
    if mode == 'mock':
        return validator.validate_device_mock_mode(config)
    elif mode == 'live':
        return validator.validate_device_live_mode(config)
    else:
        return {
            'status': 'FAIL',
            'message': f'Invalid validation mode: {mode}',
            'valid_modes': ['mock', 'live']
        }
