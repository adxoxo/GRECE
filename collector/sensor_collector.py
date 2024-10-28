import serial
import time
from typing import Tuple, Optional

class SensorReader:
    def __init__(self, port: str = '/dev/ttyUSB0', baudrate: int = 9600):
        """Initialize the sensor reader with the specified port and baudrate."""
        self.serial = serial.Serial(port, baudrate, timeout=1.0)
        time.sleep(2)  # Wait for serial connection to stabilize
        
    def read_sensors(self) -> Tuple[Optional[float], Optional[float]]:
        """Read PH and EC values from the Arduino.
        
        Returns:
            Tuple of (ph_value, ec_value). Values will be None if there's an error.
        """
        if self.serial.in_waiting:
            try:
                line = self.serial.readline().decode('utf-8').strip()
                # Parse the line format "PH:value,EC:value"
                readings = dict(item.split(':') for item in line.split(','))
                
                ph_value = float(readings['PH']) if readings['PH'] != 'ERROR' else None
                ec_value = float(readings['EC']) if readings['EC'] != 'ERROR' else None
                
                return ph_value, ec_value
                
            except (ValueError, KeyError, IndexError) as e:
                print(f"Error parsing sensor data: {e}")
                return None, None
        return None, None
    
    def close(self):
        """Close the serial connection."""
        self.serial.close()

def main():
    # Create sensor reader instance
    try:
        reader = SensorReader()
        print("Starting sensor readings...")
        
        while True:
            ph, ec = reader.read_sensors()
            
            if ph is not None and ec is not None:
                print(f"PH: {ph:.2f}, EC: {ec:.2f}")
            else:
                print("Waiting for valid sensor readings...")
                
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nStopping sensor readings...")
    finally:
        reader.close()

if __name__ == "__main__":
    main()