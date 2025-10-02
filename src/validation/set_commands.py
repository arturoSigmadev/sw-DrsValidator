#!/usr/bin/env python3
"""
DRS Validation Framework - Set Commands Module
Implementación de comandos de configuración para dispositivos DRS
Basado en la lógica extraída de set_eth.py
"""

import struct
from typing import List, Optional
from crccheck.crc import Crc16Xmodem


def calculate_crc16_ccitt(data: bytes) -> str:
    """
    Calcula CRC-16-CCITT usando el algoritmo correcto (XMODEM)
    Implementación que coincide exactamente con el código oficial de Santone
    """
    crc = Crc16Xmodem.calc(data)
    crc_hex = f"{crc:04X}"
    # Swap bytes como hace el código oficial
    checksum = crc_hex[2:4] + crc_hex[0:2]
    checksum = checksum.upper()
    # Escape de caracteres especiales
    checksum = checksum.replace("5E", "5E5D").replace("7E", "5E7D")
    return checksum


def frequency_to_hex(frequency_mhz: float) -> str:
    """
    Convierte frecuencia en MHz a formato hex de 8 caracteres (formato DRS)
    Compatible con la lógica del HostController.php
    
    frequency_mhz: Frecuencia en MHz (ej: 145.0)
    Returns: String hex de 8 caracteres con bytes invertidos
    """
    # Convertir MHz a unidades DRS (multiplicar por 10000)
    drs_units = int(frequency_mhz * 10000)
    
    # Convertir a hex de 8 caracteres
    hex_value = f"{drs_units:08X}"
    
    # Invertir bytes (formato DRS) - mismo algoritmo que PHP
    inverted = hex_value[6:8] + hex_value[4:6] + hex_value[2:4] + hex_value[0:2]
    
    return inverted.upper()


def build_santone_frame(cmd_name: int, cmd_data: str) -> bytes:
    """
    Construye trama Santone completa con CRC
    cmd_name: comando en decimal (ej: 0x80 = 128)
    cmd_data: datos en formato hex string (ej: "02")

    Formato: 7E [HEADER] [DATA] [CRC] 7E
    HEADER: 07 00 00 [CMD] 00 [LEN] [DATA]
    """
    # Header fijo según protocolo Santone
    module_function = "07"  # Siempre 07 para Digital Board
    module_address = "00"   # Dirección del módulo
    data_initiation = "00"  # DataType.DATA_INITIATION
    response_flag = "00"    # ResponseFlag.SUCCESS
    
    # Comando en hex de 2 dígitos
    cmd_hex = f"{cmd_name:02X}"

    # Longitud de datos (en bytes, no en hex chars)
    data_length = len(cmd_data) // 2  # Cada 2 chars = 1 byte
    len_hex = f"{data_length:02X}"

    # Construir trama sin CRC (exactamente como el código oficial)
    frame_data = f"{module_function}{module_address}{data_initiation}{cmd_hex}{response_flag}{len_hex}{cmd_data}"

    # Calcular CRC
    crc = calculate_crc16_ccitt(bytes.fromhex(frame_data))

    # Trama completa
    full_frame = f"7E{frame_data}{crc}7E"

    return bytes.fromhex(full_frame)


class SetCommands:
    """Comandos de configuración para dispositivos DRS"""

    @staticmethod
    def set_working_mode(wideband: bool = True) -> bytes:
        """
        Cambia entre WideBand (02) y Channel Mode (03)

        Args:
            wideband: True para WideBand, False para Channel Mode

        Returns:
            bytes: Trama Santone completa con CRC
        """
        cmd_name = 0x80
        mode_data = "02" if wideband else "03"
        return build_santone_frame(cmd_name, mode_data)

    @staticmethod
    def set_attenuation(uplink_db: int, downlink_db: int, device_type: str = "dmu") -> bytes:
        """
        Configura atenuaciones de uplink y downlink

        Args:
            uplink_db: Atenuación uplink en dB (0-30)
            downlink_db: Atenuación downlink en dB (0-40)
            device_type: "dmu" o "dru"

        Returns:
            bytes: Trama Santone completa con CRC

        Raises:
            ValueError: Si los valores están fuera de rango
        """
        if not (0 <= uplink_db <= 30):
            raise ValueError("uplink_db debe estar entre 0 y 30 dB")
        if not (0 <= downlink_db <= 40):
            raise ValueError("downlink_db debe estar entre 0 y 40 dB")

        cmd_name = 0xE7

        # Convertir a hex (multiplicar por 4 según lógica PHP)
        uplink_hex = f"{uplink_db * 4:02X}"
        downlink_hex = f"{downlink_db * 4:02X}"

        # Orden según dispositivo (basado en HostController.php)
        if device_type.lower() == "dmu":
            cmd_data = f"{downlink_hex}{uplink_hex}"
        else:
            cmd_data = f"{uplink_hex}{downlink_hex}"

        return build_santone_frame(cmd_name, cmd_data)

    @staticmethod
    def set_channel_activation(channels: List[bool]) -> bytes:
        """
        Activa/desactiva canales (hasta 16 canales)

        Args:
            channels: Lista de booleanos (True=ON, False=OFF)

        Returns:
            bytes: Trama Santone completa con CRC
        """
        cmd_name = 0x41

        cmd_data = ""
        for i, channel in enumerate(channels[:16]):  # Máximo 16 canales
            cmd_data += "00" if channel else "01"  # 00=ON, 01=OFF

        # Rellenar con OFF si menos de 16 canales
        while len(cmd_data) < 32:  # 16 bytes * 2 chars = 32
            cmd_data += "01"

        return build_santone_frame(cmd_name, cmd_data)

    @staticmethod
    def set_channel_frequencies(frequencies: List[str]) -> bytes:
        """
        Configura frecuencias de canales

        Args:
            frequencies: Lista de frecuencias en hex (8 chars cada una)

        Returns:
            bytes: Trama Santone completa con CRC
        """
        cmd_name = 0x35

        cmd_data = ""
        for freq in frequencies[:16]:  # Máximo 16 canales
            # Asegurar formato correcto (8 caracteres hex)
            freq_clean = freq.replace("0x", "").replace(" ", "").upper()
            cmd_data += freq_clean.zfill(8)

        # Rellenar con ceros si menos de 16 canales (128 chars total)
        while len(cmd_data) < 128:
            cmd_data += "00000000"

        return build_santone_frame(cmd_name, cmd_data)

    @staticmethod
    def set_single_channel_frequency(channel_index: int, frequency_hex: str) -> bytes:
        """
        Configura frecuencia de un canal específico

        Args:
            channel_index: Índice del canal (0-15)
            frequency_hex: Frecuencia en hex (8 caracteres)

        Returns:
            bytes: Trama Santone completa con CRC
        """
        if not (0 <= channel_index <= 15):
            raise ValueError("channel_index debe estar entre 0 y 15")

        # Crear lista con frecuencia solo en el canal especificado
        frequencies = ["00000000"] * 16
        freq_clean = frequency_hex.replace("0x", "").replace(" ", "").upper()
        frequencies[channel_index] = freq_clean.zfill(8)

        return SetCommands.set_channel_frequencies(frequencies)

    @staticmethod
    def generate_vhf_frequencies() -> List[str]:
        """Genera 16 frecuencias VHF espaciadas uniformemente (145-160 MHz, pasos de 0.0125 MHz)"""
        start_freq = 145.0
        end_freq = 160.0
        num_channels = 16
        
        step = (end_freq - start_freq) / (num_channels - 1)
        frequencies = [start_freq + i * step for i in range(num_channels)]
        
        return [frequency_to_hex(freq) for freq in frequencies]

    @staticmethod
    def generate_p25_frequencies() -> List[str]:
        """Genera 16 frecuencias P25 espaciadas uniformemente (851-869 MHz)"""
        start_freq = 851.0
        end_freq = 869.0
        num_channels = 16
        
        step = (end_freq - start_freq) / (num_channels - 1)
        frequencies = [start_freq + i * step for i in range(num_channels)]
        
        return [frequency_to_hex(freq) for freq in frequencies]

    @staticmethod
    def generate_tetra400_frequencies() -> List[str]:
        """Genera 16 frecuencias TETRA 400 espaciadas uniformemente (410-430 MHz)"""
        start_freq = 410.0
        end_freq = 430.0
        num_channels = 16
        
        step = (end_freq - start_freq) / (num_channels - 1)
        frequencies = [start_freq + i * step for i in range(num_channels)]
        
        return [frequency_to_hex(freq) for freq in frequencies]


def validate_set_command(command_name: str, params: dict) -> dict:
    """
    Valida y ejecuta comandos de seteo

    Args:
        command_name: Nombre del comando
        params: Parámetros del comando

    Returns:
        dict: Resultado de la ejecución
    """
    try:
        frame = None

        if command_name == "set_working_mode":
            frame = SetCommands.set_working_mode(params.get("wideband", True))

        elif command_name == "set_attenuation":
            frame = SetCommands.set_attenuation(
                params["uplink_db"],
                params["downlink_db"],
                params.get("device_type", "dmu")
            )

        elif command_name == "set_channel_activation":
            frame = SetCommands.set_channel_activation(params["channels"])

        elif command_name == "set_channel_frequencies":
            frame = SetCommands.set_channel_frequencies(params["frequencies"])

        elif command_name == "set_single_channel_frequency":
            frame = SetCommands.set_single_channel_frequency(
                params["channel_index"],
                params["frequency_hex"]
            )

        if frame:
            return {
                "status": "success",
                "command": command_name,
                "frame_hex": frame.hex().upper(),
                "frame_length": len(frame),
                "params": params
            }
        else:
            return {
                "status": "error",
                "command": command_name,
                "error": "Comando no reconocido"
            }

    except Exception as e:
        return {
            "status": "error",
            "command": command_name,
            "error": str(e),
            "params": params
        }


# Funciones de utilidad para testing
def test_crc_calculation():
    """Test del cálculo de CRC"""
    test_data = bytes.fromhex("07000080000102")
    crc = calculate_crc16_ccitt(test_data)
    print(f"CRC para {test_data.hex().upper()}: {crc:04X}")
    return crc


def test_frame_building():
    """Test de construcción de tramas"""
    # Test set working mode
    frame = SetCommands.set_working_mode(True)
    print(f"Set WideBand frame: {frame.hex().upper()}")

    # Test set attenuation
    frame = SetCommands.set_attenuation(10, 15, "dmu")
    print(f"Set attenuation frame: {frame.hex().upper()}")

    # Test channel activation
    channels = [True] * 8 + [False] * 8
    frame = SetCommands.set_channel_activation(channels)
    print(f"Set channels frame: {frame.hex().upper()}")


if __name__ == "__main__":
    print("DRS Set Commands Module - Testing")
    test_crc_calculation()
    test_frame_building()