import asyncio
import struct
import random
import sys

# Check if running on Windows
IS_WINDOWS = sys.platform.startswith('win')

if IS_WINDOWS:
    try:
        from bleak import BleakServer
        from bleak import __version__ as bleak_version
        SERVER_AVAILABLE = True
    except ImportError:
        SERVER_AVAILABLE = False
else:
    # On non-Windows platforms, server functionality is limited
    SERVER_AVAILABLE = False

# Heart Rate Service UUID
HEART_RATE_SERVICE_UUID = "0000180d-0000-1000-8000-00805f9b34fb"
# Heart Rate Measurement Characteristic UUID
HEART_RATE_MEASUREMENT_UUID = "00002a37-0000-1000-8000-00805f9b34fb"

class HeartRateServer:
    def __init__(self):
        self.is_running = True
        
    def create_heart_rate_data(self, bpm):
        """
        Create heart rate measurement data according to Bluetooth specification
        Format: Flags (1 byte) + Heart Rate (1-2 bytes)
        - Flags: 0x01 = uint8, no contact detected
        - Heart Rate: uint8 value
        """
        # Flags: 0x01 (uint8, no contact detection)
        flags = 0x01
        # Heart rate value as uint8
        hr_measurement = struct.pack('<BB', flags, bpm)
        return hr_measurement
    
    async def send_heart_rates(self, server):
        """Send random heart rates between 80-120 every 15 seconds"""
        while self.is_running:
            # Generate random heart rate between 80 and 120
            heart_rate = random.randint(80, 120)
            
            print(f"Preparing to send heart rate: {heart_rate} BPM")
            
            try:
                # Look for the heart rate measurement characteristic
                hr_measurement_char = None
                for service in server.services:
                    if service.uuid == HEART_RATE_SERVICE_UUID:
                        for char in service.characteristics:
                            if char.uuid == HEART_RATE_MEASUREMENT_UUID:
                                hr_measurement_char = char
                                break
                        break
                
                if hr_measurement_char:
                    # Create the heart rate data
                    data = self.create_heart_rate_data(heart_rate)
                    
                    # Notify all subscribed clients
                    await server.notify(hr_measurement_char.handle, data)
                    print(f"✓ Sent heart rate: {heart_rate} BPM")
                else:
                    print("✗ Heart rate characteristic not found")
            except Exception as e:
                print(f"✗ Error sending heart rate: {e}")
            
            await asyncio.sleep(15)  # Wait 15 seconds before next measurement
    
    async def start_server(self):
        """Start the heart rate monitor server (Windows only)"""
        if not SERVER_AVAILABLE:
            print("❌ BLE server functionality is not available on this platform.")
            print("💡 This application is designed for Windows with Bluetooth 4.0+ adapter.")
            print("💡 Please run this on a Windows machine with proper Bluetooth support.")
            return
        
        print("Starting Bluetooth heart rate monitor server...")
        print(f"Bleak version: {bleak_version}")
        print("Advertising as 'HeartRateMonitor'")
        print("Service UUID:", HEART_RATE_SERVICE_UUID)
        print("Looking for devices to connect...")
        print("Press Ctrl+C to stop")
        
        # Define the service and characteristic configuration
        try:
            # Create the server with heart rate service
            server = BleakServer(
                services=[
                    (HEART_RATE_SERVICE_UUID, [
                        (HEART_RATE_MEASUREMENT_UUID, ["notify"])
                    ])
                ],
                name="HeartRateMonitor"
            )
            
            await server.start()
            print(f"✓ Server started with address: {server.address}")
            
            # Start sending heart rate measurements in the background
            notification_task = asyncio.create_task(self.send_heart_rates(server))
            
            # Keep the server running until interrupted
            try:
                while self.is_running:
                    await asyncio.sleep(1)
            except KeyboardInterrupt:
                print("\n🛑 Shutting down server...")
            finally:
                notification_task.cancel()
                try:
                    await notification_task
                except asyncio.CancelledError:
                    pass
                await server.stop()
                print("Server stopped")
                
        except Exception as e:
            print(f"❌ Server failed to start: {e}")
            print("💡 Make sure you're running as Administrator on Windows")
            print("💡 Also ensure Bluetooth is enabled and no other apps are using it")

def check_platform_compatibility():
    """Check if the current platform supports BLE server functionality"""
    print(f"Platform: {sys.platform}")
    if IS_WINDOWS:
        print("✓ Windows platform detected - BLE server should be supported")
        if SERVER_AVAILABLE:
            print("✓ Bleak library with server support loaded successfully")
        else:
            print("❌ Bleak server component not available - please install with server support")
    else:
        print("⚠️  Non-Windows platform detected - BLE server functionality may be limited")
        print("💡 This application is optimized for Windows with Bluetooth 4.0+ adapter")

async def main():
    server = HeartRateServer()
    
    # Check platform compatibility
    check_platform_compatibility()
    
    # Start the server
    await server.start_server()

if __name__ == "__main__":
    asyncio.run(main())