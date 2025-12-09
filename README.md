# Bluetooth Heart Rate Monitor Server

This application emulates a Bluetooth Low Energy (BLE) heart rate monitor that broadcasts random heart rate values between 80-120 BPM every 15 seconds. It's designed to work with Wahoo bike computers and other BLE heart rate monitor compatible devices.

## Prerequisites

This application is designed for Windows and requires:
- Python 3.7 or higher
- Compatible Bluetooth 4.0+ adapter
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
- Your Wahoo bike computer should be able to detect and connect to "HeartRateMonitor" as a heart rate sensor

## Notes

- This implementation uses the Bleak library which provides cross-platform BLE support
- Server functionality is primarily supported on Windows and macOS
- On Linux, BLE server functionality may be limited or require additional setup