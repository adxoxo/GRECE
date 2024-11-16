from bluepy.btle import DefaultDelegate
from bluepy.thingy52 import Thingy52
import serial
import time
import json
import requests
from datetime import datetime
import threading
from queue import Queue

class SensorData:
    
    def __init__(self):
        self.temperature = None
        self.humidity = None
        self.ec_level = None
        self.ph_level = None
        self.water_level = None
        self.lock = threading.Lock()

    def is_complete(self):
        # Always return True since missing data will default to 0
        return True

    def to_dict(self, system_id):
        
        return {
            "System": system_id,
            "Water_level": self.water_level if self.water_level is not None else 0,
            "EC": self.ec_level if self.ec_level is not None else 0,
            "PH": self.ph_level if self.ph_level is not None else 0,
            "Temp": self.temperature if self.temperature is not None else 0,
            "Humid": self.humidity if self.humidity is not None else 0,
        }

class SensorDelegate(DefaultDelegate):
    def __init__(self, sensor_data):
        DefaultDelegate.__init__(self)
        self.sensor_data = sensor_data

    def handleNotification(self, cHandle, data):
        with self.sensor_data.lock:
            if cHandle == self.thingy.environment.temperature_char.getHandle():
                # Temperature is encoded as sint8 + uint8
                integer = data[0]
                decimal = data[1]
                temp = integer + decimal/100.0
                self.sensor_data.temperature = temp
                print(f"Temperature: {temp:.2f}°C")
                
            elif cHandle == self.thingy.environment.humidity_char.getHandle():
                # Humidity is encoded as uint8
                humidity = data[0]
                self.sensor_data.humidity = humidity
                print(f"Humidity: {humidity}%")

def read_arduino_data(serial_port, sensor_data):
    """Thread function to read Arduino serial data"""
    while True:
        try:
            if serial_port.in_waiting:
                line = serial_port.readline().decode('utf-8').strip()
                # Assuming Arduino sends data in format: "EC:123,pH:7.0,Water:80"
                readings = dict(item.split(":") for item in line.split(","))
                
                with sensor_data.lock:
                    if "EC" in readings:
                        sensor_data.ec_value = float(readings["EC"])
                        print(f"EC Level: {sensor_data.ec_level}")
                    if "pH" in readings:
                        sensor_data.ph_value = float(readings["PH"])
                        print(f"PH Level: {sensor_data.ph_level}")
                    if "Water" in readings:
                        sensor_data.water_level = float(readings["Water"])
                        print(f"Water Level: {sensor_data.water_level}%")
                
            time.sleep(0.1)  # Small delay to prevent CPU overload
        except Exception as e:
            print(f"Error reading Arduino data: {e}")
            time.sleep(1)  # Longer delay on error

def send_data_to_server(data, server_url):
    """Send sensor data to server via HTTP POST"""
    try:
        response = requests.post(server_url, json=data)
        print(f"Data sent to server. Response: {response.status_code}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error sending data to server: {e}")
        return False

def main():
    # Configuration
    THINGY_MAC = "F2:B2:02:9A:36:67"  # Replace with your Thingy52 MAC address
    ARDUINO_PORT = "/dev/ttyACM0"  # Replace with your Arduino serial port
    ARDUINO_BAUD = 9600
    SERVER_URL = "http://your-server.com/api/data"  # Replace with your server URL
    SYSTEM_ID = 1
    
    sensor_data = SensorData()
    
    # Initialize Arduino serial connection
    try:
        arduino = serial.Serial(ARDUINO_PORT, ARDUINO_BAUD)
        print(f"Connected to Arduino on {ARDUINO_PORT}")
    except Exception as e:
        print(f"Error connecting to Arduino: {e}")
        return

    # Start Arduino reading thread
    arduino_thread = threading.Thread(target=read_arduino_data, 
                                    args=(arduino, sensor_data),
                                    daemon=True)
    arduino_thread.start()

    # Connect to Thingy52
    print(f"Connecting to Thingy52 ({THINGY_MAC})...")
    try:
        thingy = Thingy52(THINGY_MAC)
        delegate = SensorDelegate(sensor_data)
        delegate.thingy = thingy
        thingy.setDelegate(delegate)

        # Enable notifications
        thingy.environment.enable()
        thingy.environment.configure(temp_int=1000, humid_int=1000)
        thingy.environment.set_temperature_notification(True)
        thingy.environment.set_humidity_notification(True)

        print("Connected! Monitoring all sensors...")
        
        last_send_time = 0
        SEND_INTERVAL = 5  # Send data every 5 seconds

        try:
            while True:
                thingy.waitForNotifications(1.0)
                
                # Check if we have all sensor data and if it's time to send
                current_time = time.time()
                if (current_time - last_send_time >= SEND_INTERVAL and 
                    sensor_data.is_complete()):
                    
                    # Get data with lock to ensure consistency
                    with sensor_data.lock:
                        data_to_send = sensor_data.to_dict(SYSTEM_ID)
                    
                    # Send data to server
                    send_data_to_server(data_to_send, SERVER_URL)
                    last_send_time = current_time
                
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print("\nStopping...")
            
        finally:
            # Cleanup
            thingy.environment.set_temperature_notification(False)
            thingy.environment.set_humidity_notification(False)
            thingy.disconnect()
            arduino.close()
            print("Disconnected from all devices")
            
    except Exception as e:
        print(f"Error: {e}")
        arduino.close()

if __name__ == "__main__":
    main()