# GRECE
Automated Hydroponics NFT System

This project is an automated hydroponic Nutrient Film Technique (NFT) system that uses Raspberry Pi and Arduino to maintain optimal growing conditions for plants. Leveraging IoT and a Django REST API, it allows for real-time monitoring, data logging, and remote control, all designed to maximize growth efficiency in a low-maintenance setup.

Features
Automated Control: Uses a Raspberry Pi and Arduino to manage water flow, lighting, and nutrient dosing, ensuring plants receive precisely what they need at the right time.
Real-Time Monitoring: Sensor data (pH, EC, temperature, humidity) is continuously monitored, sent to the Raspberry Pi, and displayed via the Django REST framework for easy tracking.
Remote Access: Access the system remotely through the Django REST API to view live data, adjust settings, and receive alerts if any parameters deviate from optimal ranges.
Data Logging: Sensor data is stored in a database for historical tracking and optimization of plant growth conditions.
Customizable Triggers: Set thresholds for environmental variables, with automatic notifications if conditions fall outside set ranges.
Hardware
Raspberry Pi: Acts as the main controller, running control scripts, managing data storage, and interfacing with the web API.
Arduino: Controls pumps, LED lights, and nutrient dosing through relays, communicating with the Raspberry Pi via serial communication.
Sensors: pH, EC, temperature, humidity, and light sensors track environmental conditions, feeding data to the Raspberry Pi for processing.
Software
Python: Handles data processing and control logic on the Raspberry Pi.
Arduino C++: Manages hardware control for relays and sensors on the Arduino.
Django REST Framework: Provides a REST API for real-time monitoring, remote control, and data visualization.
SQLite/MySQL: Stores sensor data for long-term tracking and analysis.
Future Plans
Machine Learning Integration: Develop predictive models using historical data to suggest optimal conditions and automate future growth cycles.
Mobile App: Create a mobile app to offer seamless access to live monitoring and control via the REST API.
Getting Started
Clone the repository, set up hardware as per the wiring diagram, and follow the setup instructions in the repository to install dependencies and configure the environment.

License
This project is licensed under the MIT License. Contributions are welcome!