#!/usr/bin/env python3
"""
Real DRS Device Responses - REMOTE (Based on Master with modifications)
Generated automatically - Remote device 192.168.60.160 not available

Target Device: 192.168.60.160:65050 (SIMULATED from Master 192.168.11.22)
Collection Date: 2025-09-26T20:50:00
Total Commands: 15
Success Rate: 100% (simulated based on master responses)
"""

# Respuestas simuladas para dispositivo REMOTE basadas en Master real
# Modificamos algunos valores para simular dispositivo diferente
REAL_DRS_RESPONSES = {
    # Puerto conectado: 1 dispositivo (diferente al Master que tiene 0)
    "optical_port_devices_connected_1": "7E 07 00 00 F8 00 01 01 07 8A 7E",  
    "optical_port_devices_connected_2": "7E 07 00 00 F9 00 01 00 4F 46 7E",  # Igual al master
    "optical_port_devices_connected_3": "7E 07 00 00 FA 00 01 00 93 DD 7E",  # Igual al master  
    "optical_port_devices_connected_4": "7E 07 00 00 FB 00 01 00 F2 74 7E",  # 0 dispositivos conectados
    
    # Potencia diferente (valores ligeramente modificados)
    "input_and_output_power": "7E 07 00 00 F3 00 04 FE B8 10 CC 88 51 7E",
    
    # Channel switch en canal 2 (Master está en canal 1)
    "channel_switch": "7E 07 00 00 42 00 10 02 00 00 00 00 00 02 00 02 02 00 00 00 00 00 00 A4 6B 7E",
    
    # Configuración de frecuencia igual (dispositivos sincronizados)
    "channel_frequency_configuration": "7E 07 00 00 36 00 40 F2 24 16 00 02 4C 16 00 9A 86 16 00 40 95 16 00 50 BC 16 00 60 E3 16 00 70 0A 17 00 08 45 17 00 90 58 17 00 A0 7F 17 00 B0 A6 17 00 C0 CD 17 00 D0 F4 17 00 E0 1B 18 00 D2 47 18 00 00 6A 18 00 E5 BD 7E",
    
    # Frecuencia central ligeramente diferente
    "central_frequency_point": "7E 07 00 00 EB 00 04 08 50 17 00 5E 43 7E",
    
    # Bandwidth igual
    "subband_bandwidth": "7E 07 00 00 ED 00 20 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 DC 31 7E",
    
    # Broadband switching diferente
    "broadband_switching": "7E 07 00 00 81 00 01 04 FE 61 7E",
    
    # Puerto óptico 1 activo (Master tiene todos en 0)
    "optical_port_switch": "7E 07 00 00 91 00 04 01 00 00 00 3B C5 7E",
    
    # Status diferente
    "optical_port_status": "7E 07 00 00 9A 00 01 26 08 F6 7E",
    
    # Temperatura ligeramente diferente (A4 C8 vs A4 B5 del Master)
    "temperature": "7E 07 00 00 02 00 04 A4 C8 00 00 AB D4 7E",
    
    # Device ID diferente - Remote device (A8 64 vs A8 0B del Master)
    "device_id": "7E 07 00 00 97 00 02 A8 64 E4 07 7E",
    
    # DATT con valor diferente
    "datt": "7E 07 00 00 09 00 06 00 00 00 01 00 00 C6 BF 7E",
}


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