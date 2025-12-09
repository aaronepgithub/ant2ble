# Bluetooth Heart Rate Monitor Server

This application emulates a Bluetooth heart rate monitor that broadcasts random heart rate values between 80-120 BPM every 15 seconds. It's designed to work with Wahoo bike computers and other Bluetooth heart rate monitor compatible devices.

## Prerequisites

This application is designed for Windows and requires:
- Python 3.7 or higher (compatible with Python 3.13)
- Compatible Bluetooth adapter
- Administrator privileges to run the application

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application as Administrator:
```bash
python heart_rate_server.py
```

## How It Works

- The application advertises itself as a "HeartRateMonitor" 
- It broadcasts heart rate measurements using the standard Bluetooth Heart Rate Service (UUID: 0000180d-0000-1000-8000-00805f9b34fb)
- Heart rate values are sent in the standard format via the Heart Rate Measurement characteristic (UUID: 00002a37-0000-1000-8000-00805f9b34fb)
- Random heart rate values between 80-120 BPM are sent every 15 seconds

## Troubleshooting

- Make sure Bluetooth is enabled on your Windows PC
- Run the application as Administrator to ensure proper Bluetooth permissions
- Ensure no other applications are using the Bluetooth adapter exclusively
- Note: This implementation uses RFCOMM/SPP which may have compatibility limitations with some devices that expect true BLE heart rate service
- Your Wahoo bike computer should be able to detect and connect to "HeartRateMonitor" as a heart rate sensor

## Notes

- This implementation uses the PyBluez library for Bluetooth functionality
- Server functionality has limitations on Windows for true BLE advertising
- This implementation uses RFCOMM/SPP which may not be compatible with all devices expecting true BLE
- On non-Windows platforms, BLE server capabilities may be limited