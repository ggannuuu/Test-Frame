import serial
import time
import threading

# Attempt to connect to the Arduino on COM8
try:
    arduino = serial.Serial('COM8', 115200, timeout=1, writeTimeout=2)  # Use COM8 as identified
    time.sleep(2)  # Wait for the connection to establish
    if arduino.is_open:
        print("Successfully connected to Arduino on COM8.")
except serial.SerialException as e:
    print(f"Error: Could not connect to Arduino on COM8. {e}")

def read_serial_data():
    if arduino is None:
        print("Serial connection not established.")
        return

    print("Serial thread running...")  # To confirm the thread is active

    while True:
        try:
            if arduino.in_waiting > 0:
                line = arduino.readline().decode('utf-8', errors='ignore').strip()
                print(f"Raw Arduino output: {line}")  # Print clean, decoded data
            time.sleep(0.1)
        except Exception as e:
            print(f"Error reading from Arduino: {e}")
            break

# Start the serial data reading thread
serial_thread = threading.Thread(target=read_serial_data)
serial_thread.daemon = True
serial_thread.start()

# Main loop to enter commands directly
print("Enter commands to send to the Arduino. Format examples:")
print("p 150 - Set Position to 150")
print("v 50 - Set Velocity to 50")
print("P 0 - Set mode to Position Mode")
print("V 0 - Set mode to Velocity Mode")
print("S 0 - Emergency Stop")
print("C 0 - Calibrate")

while True:
    user_input = input("Enter command: ").strip().split()
    
    if not user_input:
        continue

    command = user_input[0]  # Command character
    value = user_input[1] if len(user_input) > 1 else "0"  # Default to "0" if no value is provided

    # Format the command for Arduino and send it
    command_str = f"{command} {value}\n"
    try:
        arduino.write(command_str.encode())
        print(f"Sent to Arduino: {command_str.strip()}")
    except Exception as e:
        print(f"Error sending command to Arduino: {e}")