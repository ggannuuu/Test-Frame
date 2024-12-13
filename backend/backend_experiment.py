import sys
import pandas as pd
import serial
import time

class Backend:
    def __init__(self):
        self.force = 0.0
        self.time = 0.0
        self.displacement = 0.0
        self.serial_port1 = "COM8"
        self.serial_port2 = "COM9"
        self.baudrate = 9600
        self.connection1 = None
        self.connection2 = None
        self.start_time = time.time()
        self.update_time = self.start_time

        # material variable
        self.material_name = ""
        self.specimen_type = ""
        self.width = 1.0
        self.thickness = 1.0
        self.gage_length = 1.0

        # mode variable
        self.step_size = 10
        self.elongation_rate = 10
        self.time_interval = 10
        self.mode = "continuous"

        # motor variable
        self.motor_initial_pos = 0
        self.motor_step_size = 20
        self.motor_vel = 50
        self.motor_time_interval = 30

    def connect_serial(self):
        """Initialize the serial connection."""
        try:
            self.connection1 = serial.Serial(self.serial_port1, self.baudrate, timeout=1)
            self.connection2 = serial.Serial(self.serial_port2, self.baudrate, timeout=1)
            print(f"Connected to {self.serial_port1} at {self.baudrate} baud.")
            print(f"Connected to {self.serial_port2} at {self.baudrate} baud.")
            time.sleep(2)
        except serial.SerialException as e:
            print(f"Error: Could not connect to serial port: {e}")
            time.sleep(2)
            sys.exit(1)

    def update_force(self):
        """Read force data from the serial connection."""
        if self.connection1 and self.connection1.in_waiting > 0:
            try:
                line = self.connection1.readline().decode('utf-8').strip()
                #print(f"Raw line from Force serial: {line}")  # Debugging raw data

                if line.startswith("Load_Cell:"):
                    self.force = float(line.split(":")[1].strip())
                    self.time = time.time() - self.start_time  # Update elapsed time
                    #print(f"Parsed force: {self.force}")  # Debugging parsed force value
                else:
                    print("Unrecognized data format.")
            except ValueError:
                print("Error: Failed to parse force value.")
        else:
            print("No data available from serial port (FORCE).")


    def update_position(self):
        if self.connection2:
            print(f"Bytes in buffer: {self.connection2.in_waiting}")  # Debugging: Check if data exists
            if self.connection2.in_waiting > 0:
                try:
                    line = self.connection2.readline().decode('utf-8').strip()
                    print(f"Received line: {line}")  # Debugging raw data

                    if line.startswith("POS:"):
                        self.displacement = float(line.split(":")[1].strip())
                        print(f"Parsed displacement: {self.displacement}")  # Debugging parsed value
                    elif line.startswith("LOG:"):
                        log_line = line.split(":")[1].strip()
                        print(f"Log message: {log_line}")
                    else:
                        print("Unrecognized data format.")
                except ValueError:
                    print("Error: Failed to parse displacement value.")
            else:
                print("No data available from serial port (POS).")
        else:
            print("Serial connection not established.")



    def motor_setPos(self, val):
        command = f"#P:{val}\n"
        print(f"Sending command: {command}")
        self.connection2.write(command.encode())

    def motor_setVel(self, val):
        command = f"#V:{val}\n"
        print(f"Sending command: {command}")
        self.connection2.write(command.encode())



    def motor_stop(self):
        command = f"#S:0\n"
        print(f"Sending command: {command}")
        self.connection2.write(command.encode())

    def motor_calibration(self):
        command = f"#C:0\n"
        print(f"Sending command: {command}")
        self.connection2.write(command.encode())


    def execute_experiment(self, dir):
        
        sign = 1 if dir == "right" else -1

        if (self.mode == "continuous"):
            self.motor_setVel(sign * self.elongation_rate)
        elif (self.mode == "manual"):
            self.motor_setPos(sign * self.step_size)
        elif (self.mode == "timer"):
            for _ in range(100):  
                self.motor_setPos(sign * self.step_size)
                time.sleep(self.time_interval)


    def get_time(self):
        return self.time
    
    def set_time(self):
        return self.time
    

    def get_force(self):
        return self.force
    
    def set_force(self, force):
        self.force = force

    def get_position(self):
        return self.displacement
    
    def set_position(self, displacement):
        self.displacement = displacement


    def set_motor_step_size(self, val):
        self.motor_step_size = val

    def set_motor_vel(self, val):
        self.motor_vel = val

    def set_motor_time_invterval(self, val):
        self.motor_time_interval = val


    def get_readings(self):
        return self.force*9.81, self.displacement
    
    def get_data(self):
        if time.time() - self.update_time > 0.2:
            self.update_position()
            self.update_force()
            self.update_time = time.time()
        return self.time, self.force * 9.81, self.displacement
