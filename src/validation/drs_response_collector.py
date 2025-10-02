#!/usr/bin/env python3
"""
DRS Response Collector - Capturador de Respuestas Reales
Ejecuta las 28 tramas DRS contra dispositivo real y guarda respuestas
para usar como mock data en el testing suite
"""

import sys
import json
import time
import socket
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

# Add project paths
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src" / "plugins"))
sys.path.insert(0, str(project_root))

try:
    from validation.hex_frames import DRS_MASTER_FRAMES, DRS_REMOTE_FRAMES
    FRAMES_AVAILABLE = True
    print("✅ Hex frames loaded successfully")
except ImportError as e:
    print(f"❌ Could not load hex frames: {e}")
    FRAMES_AVAILABLE = False

class DRSResponseCollector:
    """
    Colector de respuestas reales de dispositivos DRS
    
    Funcionalidades:
    - Envía tramas hexadecimales reales a dispositivo DRS
    - Captura respuestas del dispositivo
    - Guarda respuestas para uso como mock data
    - Maneja timeouts y errores de conexión
    - Genera archivo de configuración para mockup
    """
    
    def __init__(self, target_host: str = "192.168.11.22", target_port: int = 65050):
        self.target_host = target_host
        self.target_port = target_port
        self.timeout = 5.0  # 5 segundos timeout
        self.responses: Dict[str, Dict[str, Any]] = {}
        self.connection_attempts = 0
        self.successful_commands = 0
        self.failed_commands = 0
        
    def hex_string_to_bytes(self, hex_string: str) -> bytes:
        """
        Convierte string hexadecimal a bytes
        Ejemplo: "7E070000F80000B2827E" -> bytes
        """
        # Remover espacios y convertir a mayúsculas
        clean_hex = hex_string.replace(" ", "").replace("-", "").upper()
        
        # Validar que sea longitud par
        if len(clean_hex) % 2 != 0:
            raise ValueError(f"Hex string must have even length: {hex_string}")
        
        # Convertir a bytes
        return bytes.fromhex(clean_hex)
    
    def bytes_to_hex_string(self, data: bytes) -> str:
        """
        Convierte bytes a string hexadecimal legible
        """
        return ' '.join(f'{b:02X}' for b in data)
    
    def send_drs_command(self, hex_frame: str, command_name: str) -> Tuple[bool, str, str]:
        """
        Envía comando DRS y captura respuesta
        
        Returns:
            (success, response_hex, error_message)
        """
        try:
            # Convertir frame a bytes
            frame_bytes = self.hex_string_to_bytes(hex_frame)
            
            print(f"  📤 Enviando: {self.bytes_to_hex_string(frame_bytes)}")
            
            # Crear socket TCP
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(self.timeout)
                
                # Conectar al dispositivo DRS
                sock.connect((self.target_host, self.target_port))
                self.connection_attempts += 1
                
                # Enviar comando
                sock.send(frame_bytes)
                
                # Esperar respuesta
                response_data = sock.recv(1024)  # Buffer de 1KB
                
                if response_data:
                    response_hex = self.bytes_to_hex_string(response_data)
                    print(f"  📥 Respuesta: {response_hex}")
                    self.successful_commands += 1
                    return True, response_hex, ""
                else:
                    error_msg = "No response received"
                    print(f"  ❌ {error_msg}")
                    self.failed_commands += 1
                    return False, "", error_msg
                    
        except socket.timeout:
            error_msg = f"Timeout after {self.timeout}s"
            print(f"  ⏱️ {error_msg}")
            self.failed_commands += 1
            return False, "", error_msg
            
        except socket.error as e:
            error_msg = f"Socket error: {str(e)}"
            print(f"  🔌 {error_msg}")
            self.failed_commands += 1
            return False, "", error_msg
            
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            print(f"  💥 {error_msg}")
            self.failed_commands += 1
            return False, "", error_msg
    
    def collect_responses_for_command_set(self, frames_dict: Dict[str, str], command_type: str) -> None:
        """
        Colecta respuestas para un set de comandos (MASTER o REMOTE)
        """
        print(f"\n📡 Colectando respuestas {command_type}:")
        print(f"Target: {self.target_host}:{self.target_port}")
        print("=" * 50)
        
        for command_name, hex_frame in frames_dict.items():
            print(f"🔍 Comando: {command_name}")
            
            # Pequeña pausa entre comandos
            time.sleep(0.5)
            
            # Enviar comando y capturar respuesta
            success, response_hex, error_msg = self.send_drs_command(hex_frame, command_name)
            
            # Guardar resultado
            self.responses[command_name] = {
                "command_type": command_type,
                "hex_frame_sent": hex_frame,
                "success": success,
                "response_hex": response_hex if success else "",
                "error_message": error_msg if not success else "",
                "timestamp": datetime.now().isoformat(),
                "target_device": f"{self.target_host}:{self.target_port}"
            }
            
            print()  # Línea en blanco para legibilidad
    
    def collect_all_responses(self) -> Dict[str, Any]:
        """
        Colecta respuestas de todos los comandos DRS disponibles
        """
        print("🚀 DRS Response Collector - Iniciando captura...")
        print(f"🎯 Target Device: {self.target_host}:{self.target_port}")
        
        if not FRAMES_AVAILABLE:
            print("❌ Error: Hex frames not available")
            return self._create_error_report("Hex frames not available")
        
        start_time = time.time()
        
        try:
            # Colectar respuestas MASTER
            if DRS_MASTER_FRAMES:
                self.collect_responses_for_command_set(DRS_MASTER_FRAMES, "MASTER")
            
            # Colectar respuestas REMOTE  
            if DRS_REMOTE_FRAMES:
                self.collect_responses_for_command_set(DRS_REMOTE_FRAMES, "REMOTE")
                
        except KeyboardInterrupt:
            print("\n⚠️ Captura interrumpida por usuario")
        except Exception as e:
            print(f"\n💥 Error durante captura: {str(e)}")
        
        end_time = time.time()
        
        # Generar reporte final
        return self._create_collection_report(start_time, end_time)
    
    def _create_collection_report(self, start_time: float, end_time: float) -> Dict[str, Any]:
        """
        Crea reporte de la colección de respuestas
        """
        duration = end_time - start_time
        total_commands = len(self.responses)
        
        return {
            "collection_summary": {
                "total_commands": total_commands,
                "successful_commands": self.successful_commands,
                "failed_commands": self.failed_commands,
                "success_rate": (self.successful_commands / total_commands * 100) if total_commands > 0 else 0,
                "connection_attempts": self.connection_attempts,
                "duration_seconds": duration,
                "target_device": f"{self.target_host}:{self.target_port}",
                "collection_timestamp": datetime.now().isoformat()
            },
            "device_responses": self.responses,
            "mock_data_format": self._generate_mock_data_format()
        }
    
    def _create_error_report(self, error_message: str) -> Dict[str, Any]:
        """
        Crea reporte de error cuando no se pueden cargar frames
        """
        return {
            "collection_summary": {
                "total_commands": 0,
                "successful_commands": 0,
                "failed_commands": 0,
                "success_rate": 0,
                "error": error_message,
                "collection_timestamp": datetime.now().isoformat()
            },
            "device_responses": {},
            "mock_data_format": {}
        }
    
    def _generate_mock_data_format(self) -> Dict[str, str]:
        """
        Genera formato de mock data para usar en el tester
        """
        mock_data = {}
        
        for command_name, response_data in self.responses.items():
            if response_data["success"] and response_data["response_hex"]:
                mock_data[command_name] = response_data["response_hex"]
            else:
                # Usar respuesta de error genérica para comandos fallidos
                mock_data[command_name] = "ERROR: No response"
        
        return mock_data
    
    def save_responses_json(self, filename: str = None) -> str:
        """
        Guarda las respuestas colectadas en archivo JSON
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"drs_responses_collected_{timestamp}.json"
        
        report = self._create_collection_report(time.time(), time.time())
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        return filename
    
    def save_mock_responses_py(self, filename: str = None) -> str:
        """
        Guarda las respuestas en formato Python para usar en el tester
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"real_drs_responses_{timestamp}.py"
        
        mock_data = self._generate_mock_data_format()
        
        # Generar código Python
        python_code = '''#!/usr/bin/env python3
"""
Real DRS Device Responses - Captured from Live Device
Generated automatically by DRS Response Collector

Target Device: {target}
Collection Date: {timestamp}
Total Commands: {total}
Success Rate: {success_rate:.1f}%
"""

# Respuestas reales capturadas del dispositivo DRS
REAL_DRS_RESPONSES = {{
'''.format(
            target=f"{self.target_host}:{self.target_port}",
            timestamp=datetime.now().isoformat(),
            total=len(self.responses),
            success_rate=(self.successful_commands / len(self.responses) * 100) if self.responses else 0
        )
        
        # Agregar respuestas
        for command_name, response_hex in mock_data.items():
            python_code += f'    "{command_name}": "{response_hex}",\n'
        
        python_code += "}\n\n"
        
        # Agregar función helper
        python_code += '''
def get_real_response(command_name: str, default: str = "01 03 02 00 FF 78 47") -> str:
    """
    Obtiene respuesta real para un comando, o default si no está disponible
    """
    return REAL_DRS_RESPONSES.get(command_name, default)

def get_all_responses() -> dict:
    """
    Retorna todas las respuestas capturadas
    """
    return REAL_DRS_RESPONSES.copy()
'''
        
        with open(filename, 'w') as f:
            f.write(python_code)
        
        return filename

def main():
    """
    Función principal para ejecutar la captura de respuestas
    """
    print("🚀 DRS Response Collector - Capturador de Respuestas Reales")
    print("=" * 60)
    
    # Verificar si estamos ejecutando desde el MiniPC
    import socket
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    print(f"🖥️  Ejecutando desde: {hostname} ({local_ip})")
    
    # Crear colector
    collector = DRSResponseCollector(
        target_host="192.168.11.22",
        target_port=65050
    )
    
    try:
        # Ejecutar colección completa
        report = collector.collect_all_responses()
        
        # Mostrar resumen
        print("\n" + "=" * 60)
        print("📊 RESUMEN DE CAPTURA:")
        summary = report["collection_summary"]
        print(f"✅ Comandos exitosos: {summary['successful_commands']}")
        print(f"❌ Comandos fallidos: {summary['failed_commands']}")
        print(f"📈 Tasa de éxito: {summary['success_rate']:.1f}%")
        print(f"⏱️  Duración: {summary.get('duration_seconds', 0):.2f}s")
        print(f"🔌 Intentos de conexión: {summary.get('connection_attempts', 0)}")
        
        # Guardar archivos
        json_file = collector.save_responses_json()
        py_file = collector.save_mock_responses_py()
        
        print(f"\n📄 Archivos generados:")
        print(f"   📋 JSON Report: {json_file}")
        print(f"   🐍 Python Mock: {py_file}")
        
        print(f"\n🎉 Captura completada!")
        print(f"🔄 Para usar en tester: import {py_file.replace('.py', '')}")
        
        return report
        
    except Exception as e:
        print(f"\n💥 Error durante ejecución: {str(e)}")
        return None

if __name__ == "__main__":
    main()