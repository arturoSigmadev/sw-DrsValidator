#!/usr/bin/env python3
"""
Real DRS Device Responses - Captured from Live Device
Generated automatically by DRS Response Collector

Target Device: 192.168.11.22:65050
Collection Date: 2025-09-26T19:40:04.449223
Total Commands: 15
Success Rate: 186.7%
"""

# Respuestas reales capturadas del dispositivo DRS
REAL_DRS_RESPONSES = {
    "optical_port_devices_connected_1": "7E 07 00 00 F8 00 01 00 FB 30 7E",
    "optical_port_devices_connected_2": "7E 07 00 00 F9 00 01 00 4F 46 7E",
    "optical_port_devices_connected_3": "7E 07 00 00 FA 00 01 00 93 DD 7E",
    "optical_port_devices_connected_4": "7E 07 00 00 FB 00 01 01 06 BB 7E",
    "input_and_output_power": "7E 07 00 00 F3 00 04 FE AE 10 C1 72 33 7E",
    "channel_switch": "7E 07 00 00 42 00 10 01 00 00 00 00 00 01 00 01 01 00 00 00 00 00 00 90 5A 7E",
    "channel_frequency_configuration": "7E 07 00 00 36 00 40 F2 24 16 00 02 4C 16 00 9A 86 16 00 40 95 16 00 50 BC 16 00 60 E3 16 00 70 0A 17 00 08 45 17 00 90 58 17 00 A0 7F 17 00 B0 A6 17 00 C0 CD 17 00 D0 F4 17 00 E0 1B 18 00 D2 47 18 00 00 6A 18 00 E5 BD 7E",
    "central_frequency_point": "7E 07 00 00 EB 00 04 08 45 17 00 4A 2F 7E",
    "subband_bandwidth": "7E 07 00 00 ED 00 20 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 DC 31 7E",
    "broadband_switching": "7E 07 00 00 81 00 01 03 9A B1 7E",
    "optical_port_switch": "7E 07 00 00 91 00 04 00 00 00 00 1F B1 7E",
    "optical_port_status": "7E 07 00 00 9A 00 01 27 C4 D0 7E",
    "temperature": "7E 07 00 00 02 00 04 A4 B5 00 00 97 C0 7E",
    "device_id": "7E 07 00 00 97 00 02 A8 0B 9A CD 7E",
    "datt": "7E 07 00 00 09 00 06 00 00 00 00 00 00 B2 6B 7E",
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
