from flask import Flask, request, jsonify, render_template
import serial
import time
import threading

app = Flask(__name__, static_folder="../frontend/static", template_folder="../frontend")

import serial.tools.list_ports

ports = serial.tools.list_ports.comports()
for port in ports:
    print(port.device)

# Attempt to connect to the Arduino on COM7
try:
    arduino = serial.Serial('COM8', 115200, timeout=1, writeTimeout=2)  # Use COM7 as identified
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



@app.route('/')
def index():
    return render_template('index.html')

serial_thread = threading.Thread(target=read_serial_data)
serial_thread.daemon = True
serial_thread.start()

###Dynamixel Control Functions
#Arduino Dynamixel Commands
# Format: 'char int'
# p : set position
# v : set velocity
# P : set mode to position
# V : set mode to velocity
# S : emergency stop
# C : calibrate
def setPose(val):
    command = f'p {val}\n'
    arduino.write(command.encode())
    print(f"Sent to Arduino: {command.strip()}")  # Log sent command for debugging
    #arduino.write(f'p,{val}\n'.encode())

    return
def setVel(val):
    arduino.write(f'v {val}\n'.encode())
    return
def setPoseMode():
    arduino.write(f'P 0\n'.encode())
    return
def setVelMode():
    arduino.write(f'V 0\n'.encode())
    return
def emergencyStop():
    arduino.write(f'S 0\n'.encode())
    return
def calibrate():
    arduino.write(f'C 0\n'.encode())
    return
###Loadcell Functions


###Communication Functions

#page3
@app.route('/initial_adjust', methods=['POST'])
def initial_adjust():
    data = request.json
    adj_type = data.get("adjType")

    if adj_type == 'coarseCCW':
        setPose(100)
    elif adj_type == 'fineCCW':
        setPose(10)
    elif adj_type == 'fineCW':
        setPose(-10)
    elif adj_type == 'coarseCW':
        setPose(-100)
    

    time.sleep(0.1)

    return jsonify({"status": "success", "message": f"{adj_type} command sent to Arduino"})


# @app.route('/read_data', methods=['GET'])

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)




# @app.route('/move', methods=['POST'])
# def move_motor():
#     direction = request.json['direction']
#     if direction == 'up':
#         arduino.write(b'U')  # Send 'U' to move the motor up
#     elif direction == 'down':
#         arduino.write(b'D')  # Send 'D' to move the motor down
#     return jsonify({'status': 'Motor moved'}), 200

# @app.route('/start_experiment', methods=['POST'])
# def start_experiment():
#     arduino.write(b'S')  # Send 'S' to start the experiment
#     return jsonify({'status': 'Experiment started'}), 200

# @app.route('/stop_experiment', methods=['POST'])
# def stop_experiment():
#     arduino.write(b'X')  # Send 'X' to stop the experiment
#     return jsonify({'status': 'Experiment stopped'}), 200

# @app.route('/read_data', methods=['GET'])
# def read_data():
#     if arduino.in_waiting > 0:
#         data = arduino.readline().decode('utf-8').strip()
#         return jsonify({'data': data}), 200
#     return jsonify({'data': 'No data available'}), 200