"""
Command-to-Decoder mapping for DRS Santone protocol integration.

This module provides mapping between DRS command types and their corresponding
decoder functions in SantoneDecoder, ensuring proper response parsing.
"""

from typing import Dict, Callable, Any
from enum import IntEnum

# Import path mappings - these will be updated when integrating with main codebase
# For now, we'll create interfaces that match the expected signatures

class CommandDecoderMapping:
    """Maps DRS commands to their corresponding SantoneDecoder methods."""
    
    # Command name to decoder method mapping
    DECODER_MAP: Dict[str, str] = {
        # DRSMasterCommand mappings
        "optical_port_devices_connected_1": "_decode_optical_port_devices_connected_1",
        "optical_port_devices_connected_2": "_decode_optical_port_devices_connected_2", 
        "optical_port_devices_connected_3": "_decode_optical_port_devices_connected_3",
        "optical_port_devices_connected_4": "_decode_optical_port_devices_connected_4",
        "input_and_output_power": "_decode_input_and_output_power",
        "channel_switch": "_decode_channel_switch",
        "channel_frequency_configuration": "_decode_channel_frequency_configuration",
        "central_frequency_point": "_decode_central_frequency_point",
        "broadband_switching": "_decode_broadband_switching",
        "optical_port_switch": "_decode_optical_port_switch",
        "optical_port_status": "_decode_optical_port_status",
        "subband_bandwidth": "_decode_subband_bandwidth",
        "temperature": "_decode_temperature",
        "device_id": "_decode_device_id",
        "datt": "_decode_datt",
        
        # DRSRemoteCommand mappings (some overlap with master)
        # Temperature, device_id, etc. use same decoders as master
        # optical_port_devices_connected_1/2 are available for remote as well
    }
    
    # Command hex values to IntEnum mapping for decoder.decode() method
    COMMAND_VALUE_MAP: Dict[str, int] = {
        "optical_port_devices_connected_1": 0xf8,
        "optical_port_devices_connected_2": 0xf9,
        "optical_port_devices_connected_3": 0xfa,
        "optical_port_devices_connected_4": 0xfb,
        "input_and_output_power": 0xf3,
        "channel_switch": 0x42,
        "channel_frequency_configuration": 0x36,
        "central_frequency_point": 0xeb,
        "broadband_switching": 0x81,
        "optical_port_switch": 0x91,
        "optical_port_status": 0x9a,
        "subband_bandwidth": 0xed,
        "temperature": 0x02,
        "device_id": 0x97,
        "datt": 0x09,
    }
    
    @staticmethod
    def get_decoder_method(command_name: str) -> str:
        """Get decoder method name for a command."""
        return CommandDecoderMapping.DECODER_MAP.get(command_name, "_decode_generic")
    
    @staticmethod
    def get_command_value(command_name: str) -> int:
        """Get command hex value for decoder.decode() method."""
        return CommandDecoderMapping.COMMAND_VALUE_MAP.get(command_name, 0x00)
    
    @staticmethod
    def has_decoder(command_name: str) -> bool:
        """Check if command has a specific decoder."""
        return command_name in CommandDecoderMapping.DECODER_MAP

# Interface classes for type hints
class DecoderInterface:
    """Interface for decoder compatibility."""
    
    @staticmethod
    def decode(command_number: IntEnum, command_body: bytearray) -> Dict[str, Any]:
        """Generic decode method interface."""
        pass
    
    @staticmethod
    def _decode_device_id(data: bytearray) -> Dict[str, int]:
        """Device ID decoder interface."""
        pass
    
    @staticmethod
    def _decode_temperature(data: bytearray) -> Dict[str, float]:
        """Temperature decoder interface."""
        pass
    
    @staticmethod
    def power_convert(data: bytearray) -> float:
        """Power conversion utility."""
        pass

# Mock IntEnum for command types (will be replaced with actual imports)
class MockCommandType(IntEnum):
    """Mock command type for testing until real imports are available."""
    device_id = 0x97
    temperature = 0x02
    optical_port_devices_connected_1 = 0xf8

def create_mock_decoder_response(command_name: str, raw_data: bytes) -> Dict[str, Any]:
    """
    Create mock decoder response for testing integration.
    This will be replaced with actual SantoneDecoder calls.
    """
    if command_name == "device_id":
        # Mock device ID decoding (16-bit little endian)
        if len(raw_data) >= 2:
            device_id = int(raw_data[1] << 8 | raw_data[0])
            return {"device_id": device_id}
    
    elif command_name == "temperature":
        # Mock temperature decoding (signed 16-bit, scale 0.1)
        if len(raw_data) >= 2:
            value = raw_data[0] | (raw_data[1] << 8)
            if value & 0x8000:
                value = -(value & 0x7fff)
            temperature = round(value * 0.1, 2)
            return {"temperature": temperature}
    
    elif "optical_port_devices_connected" in command_name:
        # Mock device count
        if len(raw_data) >= 1:
            return {command_name: raw_data[0]}
    
    elif command_name == "central_frequency_point":
        # Mock frequency point (32-bit little endian, scale 0.0001)
        if len(raw_data) >= 4:
            value = int.from_bytes(raw_data[:4], byteorder='little')
            frequency = str(value / 10000)
            return {"central_frequency_point": frequency}
    
    elif "power" in command_name:
        # Mock power decoding (signed 16-bit, scale 1/256 dBm)
        if len(raw_data) >= 2:
            value = raw_data[0] | (raw_data[1] << 8)
            value = -(value & 0x8000) | (value & 0x7fff)
            power = round(value / 256, 2)
            return {command_name.replace("_", "_"): power}
    
    # Generic fallback
    return {command_name: f"raw_hex_{raw_data.hex() if raw_data else '00'}"}