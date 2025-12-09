import struct
import random
import time
import threading
import sys

# Check if running on Windows
IS_WINDOWS = sys.platform.startswith('win')

try:
    import bluetooth  # PyBluez library
    PYBLUEZ_AVAILABLE = True
except ImportError:
    PYBLUEZ_AVAILABLE = False

# Heart Rate Service UUID
HEART_RATE_SERVICE_UUID = "0000180d-0000-1000-8000-00805f9b34fb"
# Heart Rate Measurement Characteristic UUID
HEART_RATE_MEASUREMENT_UUID = "00002a37-0000-1000-8000-00805f9b34fb"

class HeartRateServer:
    def __init__(self):
        self.is_running = True
        self.server_sock = None
        
    def create_heart_rate_data(self, bpm):
        """
        Create heart rate measurement data according to Bluetooth specification
        Format: Flags (1 byte) + Heart Rate (1-2 bytes)
        - Flags: 0x06 = uint8, sensor contact detected, energy expended present
        - Heart Rate: uint8 value
        """
        # Flags: 0x06 (uint8, sensor contact detected, energy expended present)
        flags = 0x06
        # Heart rate value as uint8
        hr_measurement = struct.pack('<BB', flags, bpm)
        return hr_measurement
    
    def send_heart_rates(self):
        """Send random heart rates between 80-120 every 15 seconds"""
        while self.is_running:
            # Generate random heart rate between 80 and 120
            heart_rate = random.randint(80, 120)
            
            print(f"Heart rate: {heart_rate} BPM")
            
            # In a true implementation, we would broadcast this via BLE
            # Since PyBluez has limitations for BLE advertising on Windows,
            # we'll simulate the broadcast by just printing the values
            
            time.sleep(15)  # Wait 15 seconds before next measurement
    
    def start_server(self):
        """Start the heart rate monitor server (Windows with PyBluez)"""
        if not IS_WINDOWS:
            print("❌ This application is designed for Windows.")
            print("💡 PyBluez has limited BLE server capabilities on non-Windows platforms.")
            return
        
        if not PYBLUEZ_AVAILABLE:
            print("❌ PyBluez library is not available.")
            print("💡 Please install PyBluez using: pip install pybluez")
            return
        
        print("Starting Bluetooth heart rate monitor server...")
        print("Advertising as 'HeartRateMonitor'")
        print("Service UUID:", HEART_RATE_SERVICE_UUID)
        print("Looking for devices to connect...")
        print("Press Ctrl+C to stop")
        
        # Start the heart rate generation in a separate thread
        hr_thread = threading.Thread(target=self.send_heart_rates)
        hr_thread.daemon = True
        hr_thread.start()
        
        try:
            # Set up Bluetooth RFCOMM socket (basic approach)
            self.server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            self.server_sock.bind(("", bluetooth.PORT_ANY))
            self.server_sock.listen(1)
            
            port = self.server_sock.getsockname()[1]
            
            # Advertise service - note: this is SPP/RFCOMM, not true BLE
            bluetooth.advertise_service(
                self.server_sock,
                "HeartRateMonitor",
                service_id=HEART_RATE_SERVICE_UUID,
                service_classes=[HEART_RATE_SERVICE_UUID],
                profiles=[bluetooth.SERIAL_PORT_PROFILE],
                protocols=[bluetooth.RFCommProtocol]
            )
            
            print(f"✓ Server listening on RFCOMM channel {port}")
            
            # Keep the server running until interrupted
            try:
                while self.is_running:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n🛑 Shutting down server...")
                
        except bluetooth.BluetoothError as e:
            print(f"❌ Bluetooth error: {e}")
            print("💡 Make sure you're running as Administrator on Windows")
            print("💡 Also ensure Bluetooth is enabled and no other apps are using it")
        except Exception as e:
            print(f"❌ Server failed to start: {e}")
            print("💡 This may be due to PyBluez limitations on Windows")
        finally:
            if self.server_sock:
                self.server_sock.close()
            print("Server stopped")

def check_platform_compatibility():
    """Check if the current platform supports our implementation"""
    print(f"Platform: {sys.platform}")
    if IS_WINDOWS:
        print("✓ Windows platform detected")
        if PYBLUEZ_AVAILABLE:
            print("✓ PyBluez library available")
            print("⚠️  Note: PyBluez has limitations for BLE advertising on Windows")
            print("💡 Alternative implementations may be needed for full compatibility")
        else:
            print("❌ PyBluez library not available - please install with: pip install pybluez")
    else:
        print("⚠️  Non-Windows platform detected")
        print("💡 PyBluez has limited BLE server capabilities on non-Windows platforms")

def main():
    server = HeartRateServer()
    
    # Check platform compatibility
    check_platform_compatibility()
    
    if not PYBLUEZ_AVAILABLE:
        return
    
    # Start the server
    server.start_server()

if __name__ == "__main__":
    main()