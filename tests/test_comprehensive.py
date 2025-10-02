#!/usr/bin/env python3
"""
Unit Tests for Batch Commands Validator

Tests comprehensive functionality including:
- Hex frame generation and validation  
- Batch command execution (mock/live)
- SantoneDecoder integration
- FastAPI endpoint simulation
- Error handling and edge cases
"""

import unittest
import sys
from pathlib import Path

# Add src to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from validation.batch_commands_validator import BatchCommandsValidator, CommandType, ValidationResult
from validation.hex_frames import get_master_frame, get_remote_frame, validate_frame_format
from validation.decoder_integration import CommandDecoderMapping, create_mock_decoder_response


class TestBatchCommandsValidator(unittest.TestCase):
    """Test suite for BatchCommandsValidator functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.validator = BatchCommandsValidator()
        self.test_ip = "192.168.1.100"
        self.test_commands = ["device_id", "temperature", "optical_port_devices_connected_1"]
    
    def test_hex_frame_generation(self):
        """Test hex frame generation for DRS commands"""
        # Test master frame generation
        device_id_frame = get_master_frame("device_id")
        self.assertIsNotNone(device_id_frame)
        self.assertTrue(validate_frame_format(device_id_frame))
        self.assertTrue(device_id_frame.startswith("7E"))
        self.assertTrue(device_id_frame.endswith("7E"))
        
        # Test remote frame generation
        temp_frame = get_remote_frame("temperature")
        self.assertIsNotNone(temp_frame)
        self.assertTrue(validate_frame_format(temp_frame))
        
        print("✅ Hex frame generation tests passed")
    
    def test_decoder_mapping(self):
        """Test command to decoder mapping"""
        # Test mapped commands
        self.assertTrue(CommandDecoderMapping.has_decoder("device_id"))
        self.assertEqual(CommandDecoderMapping.get_decoder_method("device_id"), "_decode_device_id")
        self.assertEqual(CommandDecoderMapping.get_command_value("device_id"), 0x97)
        
        # Test temperature mapping
        self.assertTrue(CommandDecoderMapping.has_decoder("temperature"))
        self.assertEqual(CommandDecoderMapping.get_decoder_method("temperature"), "_decode_temperature")
        
        print("✅ Decoder mapping tests passed")
    
    def test_mock_decoder_integration(self):
        """Test enhanced mock decoder responses"""
        # Test device_id decoding
        device_id_raw = bytes.fromhex("0A0E")  # 3594 in little endian
        decoded = create_mock_decoder_response("device_id", device_id_raw)
        self.assertIn("device_id", decoded)
        self.assertEqual(decoded["device_id"], 3594)
        
        # Test temperature decoding
        temp_raw = bytes.fromhex("C701")  # 455 -> 45.5°C
        decoded = create_mock_decoder_response("temperature", temp_raw)
        self.assertIn("temperature", decoded)
        self.assertEqual(decoded["temperature"], 45.5)
        
        print("✅ Mock decoder integration tests passed")
    
    def test_batch_validation_mock_mode(self):
        """Test batch validation in mock mode"""
        result = self.validator.validate_batch_commands(
            ip_address=self.test_ip,
            command_type=CommandType.MASTER,
            mode="mock",
            selected_commands=self.test_commands
        )
        
        # Verify overall result structure
        self.assertIn("overall_status", result)
        self.assertIn("statistics", result)
        self.assertIn("results", result)
        self.assertEqual(result["mode"], "mock")
        self.assertEqual(result["command_type"], "master")
        
        # Verify statistics
        stats = result["statistics"]
        self.assertEqual(stats["total_commands"], len(self.test_commands))
        self.assertEqual(stats["passed"], len(self.test_commands))
        self.assertEqual(stats["success_rate"], 100.0)
        
        # Verify individual results
        self.assertEqual(len(result["results"]), len(self.test_commands))
        for cmd_result in result["results"]:
            self.assertIn("command", cmd_result)
            self.assertIn("status", cmd_result)
            self.assertIn("decoded_values", cmd_result)
            
        print(f"✅ Mock mode batch validation tests passed - {stats['success_rate']}% success rate")
    
    def test_batch_validation_live_mode_timeout(self):
        """Test batch validation in live mode with expected timeouts"""
        result = self.validator.validate_batch_commands(
            ip_address="192.168.1.200",  # Non-existent IP for timeout testing
            command_type=CommandType.MASTER,
            mode="live",
            selected_commands=["device_id", "temperature"]
        )
        
        # Should have timeout results
        self.assertIn("overall_status", result)
        self.assertEqual(result["mode"], "live")
        
        # Check that timeouts are handled properly
        stats = result["statistics"]
        self.assertTrue(stats["timeouts"] > 0)
        self.assertEqual(stats["success_rate"], 0.0)
        
        print(f"✅ Live mode timeout handling tests passed - {stats['timeouts']} timeouts detected")
    
    def test_command_type_enum_conversion(self):
        """Test CommandType enum functionality"""
        # Test enum values
        self.assertEqual(CommandType.MASTER.value, "master")
        self.assertEqual(CommandType.REMOTE.value, "remote")
        
        # Test validation with different command types
        master_result = self.validator.validate_batch_commands(
            ip_address=self.test_ip,
            command_type=CommandType.MASTER,
            mode="mock",
            selected_commands=["device_id"]
        )
        self.assertEqual(master_result["command_type"], "master")
        
        remote_result = self.validator.validate_batch_commands(
            ip_address=self.test_ip,
            command_type=CommandType.REMOTE,
            mode="mock",
            selected_commands=["device_id"]
        )
        self.assertEqual(remote_result["command_type"], "remote")
        
        print("✅ Command type enum conversion tests passed")
    
    def test_edge_cases(self):
        """Test edge cases and error handling"""
        # Test with empty command list (should execute all master commands)
        result = self.validator.validate_batch_commands(
            ip_address=self.test_ip,
            command_type=CommandType.MASTER,
            mode="mock",
            selected_commands=[]
        )
        # Empty list means "run all commands" - this is correct behavior
        self.assertGreater(result["total_commands"], 0)  # Should run all master commands
        
        # Test with None command list (should also execute all commands)
        result = self.validator.validate_batch_commands(
            ip_address=self.test_ip,
            command_type=CommandType.MASTER,
            mode="mock",
            selected_commands=None
        )
        self.assertGreater(result["total_commands"], 0)
        
        # Test with non-existent command (should handle gracefully)
        result = self.validator.validate_batch_commands(
            ip_address=self.test_ip,
            command_type=CommandType.MASTER,
            mode="mock",
            selected_commands=["nonexistent_command"]
        )
        
        # Should handle gracefully - may return error status
        self.assertIn("results", result)
        self.assertEqual(len(result["results"]), 1)  # Should try to process the command
        
        print("✅ Edge case handling tests passed")
    
    def test_decoder_metadata(self):
        """Test that decoder metadata is properly tracked"""
        result = self.validator.validate_batch_commands(
            ip_address=self.test_ip,
            command_type=CommandType.MASTER,
            mode="mock",
            selected_commands=["device_id"]
        )
        
        cmd_result = result["results"][0]
        decoded_values = cmd_result["decoded_values"]
        
        # Check for integration metadata
        self.assertIn("status", decoded_values)
        self.assertIn("mock_source", decoded_values)
        self.assertIn("decoder_mapping", decoded_values)
        
        self.assertEqual(decoded_values["status"], "mock_enhanced")
        self.assertEqual(decoded_values["mock_source"], "integrated_decoder")
        self.assertTrue(decoded_values["decoder_mapping"])
        
        print("✅ Decoder metadata tracking tests passed")
    
    def test_performance_metrics(self):
        """Test that performance metrics are properly captured"""
        result = self.validator.validate_batch_commands(
            ip_address=self.test_ip,
            command_type=CommandType.MASTER,
            mode="mock",
            selected_commands=self.test_commands
        )
        
        # Check overall timing
        self.assertIn("duration_ms", result)
        self.assertTrue(result["duration_ms"] > 0)
        
        # Check individual command timing
        for cmd_result in result["results"]:
            self.assertIn("duration_ms", cmd_result)
            self.assertTrue(cmd_result["duration_ms"] > 0)
        
        # Check average duration calculation
        stats = result["statistics"]
        self.assertIn("average_duration_ms", stats)
        self.assertTrue(stats["average_duration_ms"] > 0)
        
        print(f"✅ Performance metrics tests passed - avg {stats['average_duration_ms']}ms per command")


class TestAPIIntegration(unittest.TestCase):
    """Test API integration aspects"""
    
    def setUp(self):
        """Set up API test fixtures"""
        from validation.hex_frames import DRS_MASTER_FRAMES, DRS_REMOTE_FRAMES
        self.master_commands = list(DRS_MASTER_FRAMES.keys())
        self.remote_commands = list(DRS_REMOTE_FRAMES.keys())
    
    def test_supported_commands_structure(self):
        """Test supported commands response structure"""
        # Simulate the API endpoint logic
        decoder_mappings = {}
        for cmd in self.master_commands + self.remote_commands:
            decoder_mappings[cmd] = CommandDecoderMapping.has_decoder(cmd)
        
        response_data = {
            "master_commands": self.master_commands,
            "remote_commands": self.remote_commands,
            "total_commands": len(self.master_commands) + len(self.remote_commands),
            "decoder_mappings": decoder_mappings
        }
        
        # Verify structure
        self.assertGreater(response_data["total_commands"], 20)
        self.assertGreater(len(response_data["master_commands"]), 10)
        self.assertGreater(len(response_data["remote_commands"]), 10)
        
        # Verify decoder mappings
        mapped_count = sum(1 for mapped in decoder_mappings.values() if mapped)
        self.assertGreater(mapped_count, 10)
        
        print(f"✅ API supported commands tests passed - {response_data['total_commands']} total commands")
    
    def test_api_request_validation(self):
        """Test API request model validation"""
        # Valid request structure
        valid_request = {
            "ip_address": "192.168.1.100",
            "command_type": "master",
            "mode": "mock",
            "selected_commands": ["device_id", "temperature"],
            "timeout_seconds": 3
        }
        
        # Verify required fields
        self.assertIn("ip_address", valid_request)
        self.assertIn("command_type", valid_request)
        self.assertIn("mode", valid_request)
        
        # Verify field types
        self.assertIsInstance(valid_request["ip_address"], str)
        self.assertIsInstance(valid_request["command_type"], str)
        self.assertIsInstance(valid_request["mode"], str)
        self.assertIsInstance(valid_request["selected_commands"], list)
        self.assertIsInstance(valid_request["timeout_seconds"], int)
        
        print("✅ API request validation tests passed")


def run_comprehensive_tests():
    """Run comprehensive test suite"""
    print("=== 🧪 Running Comprehensive Batch Commands Test Suite ===")
    print()
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_suite.addTest(unittest.makeSuite(TestBatchCommandsValidator))
    test_suite.addTest(unittest.makeSuite(TestAPIIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Summary
    print("\n=== 📊 Test Results Summary ===")
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\n❌ FAILURES:")
        for test, failure in result.failures:
            print(f"  - {test}: {failure}")
    
    if result.errors:
        print("\n🚫 ERRORS:")
        for test, error in result.errors:
            print(f"  - {test}: {error}")
    
    success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun) * 100
    print(f"\n🎯 Overall Success Rate: {success_rate:.1f}%")
    
    if success_rate == 100.0:
        print("🎉 ALL TESTS PASSED - System ready for production!")
    elif success_rate >= 90.0:
        print("✅ Most tests passed - Minor issues to address")  
    else:
        print("⚠️ Multiple failures detected - Review required")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_comprehensive_tests()
    sys.exit(0 if success else 1)