pip install matplotlib

import tkinter as tk
from tkinter import messagebox
import serial
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import os
from datetime import datetime

# Serial communication setup (Adjust this to your port and settings)
SERIAL_PORT = 'COM3'  # Change this to your actual port
BAUDRATE = 115200

class DynamixelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dynamixel Servo Control")
        self.serial_conn = None
        self.connect_serial()

        # Configure layout with grid, which allows resizing
        self.root.geometry('1800x1000')
        self.root.rowconfigure(0, weight=1)  # Row 0 expands vertically
        self.root.columnconfigure(1, weight=1)  # Column 1 (plot) expands horizontally

        # Create a frame for the control panel on the left
        control_frame = tk.Frame(root)
        control_frame.grid(row=0, column=0, padx=20, pady=20, sticky='nsew')  # Left side

        # Control frame does not resize
        control_frame.rowconfigure(7, weight=1)  # Push buttons upwards

        # Label for encoder position
        self.label = tk.Label(control_frame, text="Enter Encoder Position:", font=("Arial", 18))
        self.label.pack()

        # Entry for encoder position
        self.encoder_value = tk.IntVar(value=0)
        self.encoder_input = tk.Entry(control_frame, textvariable=self.encoder_value, font=("Arial", 18), width=10)
        self.encoder_input.pack()

        # + and - buttons for adjusting encoder value
        button_frame = tk.Frame(control_frame)
        button_frame.pack(pady=10)

        self.increment_button = tk.Button(button_frame, text="+", font=("Arial", 18), command=self.increment_value)
        self.increment_button.pack(side=tk.LEFT, padx=10)

        self.decrement_button = tk.Button(button_frame, text="-", font=("Arial", 18), command=self.decrement_value)
        self.decrement_button.pack(side=tk.LEFT, padx=10)

        # Buttons for sending position and controlling rotation
        self.send_button = tk.Button(control_frame, text="Send Position", font=("Arial", 18), command=self.send_position)
        self.send_button.pack(pady=10)

        self.clockwise_button = tk.Button(control_frame, text="Rotate CW", font=("Arial", 18), command=self.rotate_clockwise)
        self.clockwise_button.pack(pady=10)

        self.counterclockwise_button = tk.Button(control_frame, text="Rotate CCW", font=("Arial", 18), command=self.rotate_counterclockwise)
        self.counterclockwise_button.pack(pady=10)

        # Start and Stop buttons for real-time plotting
        self.start_button = tk.Button(control_frame, text="Start", font=("Arial", 18), command=self.start_plotting)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(control_frame, text="Stop", font=("Arial", 18), command=self.stop_plotting)
        self.stop_button.pack(pady=10)

        # Save data button (saves data only)
        self.save_data_button = tk.Button(control_frame, text="Save Data", font=("Arial", 18), command=self.save_data)
        self.save_data_button.pack(pady=10)

        # Clear button to reset everything
        self.clear_button = tk.Button(control_frame, text="Clear", font=("Arial", 18), command=self.clear_data)
        self.clear_button.pack(pady=10)

        # Setup for plotting on the right, which should resize with the window
        plot_frame = tk.Frame(root)
        plot_frame.grid(row=0, column=1, sticky='nsew', padx=20, pady=20)

        # Allow the plot frame to expand
        plot_frame.rowconfigure(0, weight=1)
        plot_frame.columnconfigure(0, weight=1)

        self.figure, self.ax = plt.subplots(figsize=(10, 7))
        self.ax.set_xlabel('Encoder Value', fontsize=18)
        self.ax.set_ylabel('Force Sensor Value', fontsize=18)
        self.canvas = FigureCanvasTkAgg(self.figure, master=plot_frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew')

        # Initial plot data
        self.encoder_values = []
        self.force_values = []
        self.plotting_active = False  # Control flag for starting/stopping plot updates
        self.data_log = []  # Store data to save later

        # Create folders if they don't exist
        if not os.path.exists('data'):
            os.makedirs('data')
        if not os.path.exists('plot'):
            os.makedirs('plot')

        # Close the program when the window is closed
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def connect_serial(self):
        try:
            self.serial_conn = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)
            time.sleep(2)  # Allow time for connection to establish
            print("Connected to STM32 via FT232RL.")
        except serial.SerialException as e:
            messagebox.showerror("Connection Error", f"Error connecting to STM32: {e}")
            self.serial_conn = None

    def increment_value(self):
        current_value = self.encoder_value.get()
        self.encoder_value.set(current_value + 1)

    def decrement_value(self):
        current_value = self.encoder_value.get()
        self.encoder_value.set(current_value - 1)

    def send_position(self):
        if self.serial_conn:
            try:
                position = self.encoder_input.get()
                command = f'P{position}\n'  # Example format
                self.serial_conn.write(command.encode())
                print(f"Sent position: {position}")
            except Exception as e:
                messagebox.showerror("Error", f"Error sending position: {e}")
        else:
            messagebox.showwarning("Connection Error", "Serial connection not established.")

    def rotate_clockwise(self):
        if self.serial_conn:
            try:
                self.serial_conn.write(b'C\n')  # Example command for clockwise rotation
                print("Rotating clockwise.")
            except Exception as e:
                messagebox.showerror("Error", f"Error rotating clockwise: {e}")

    def rotate_counterclockwise(self):
        if self.serial_conn:
            try:
                self.serial_conn.write(b'CC\n')  # Example command for counterclockwise rotation
                print("Rotating counterclockwise.")
            except Exception as e:
                messagebox.showerror("Error", f"Error rotating counterclockwise: {e}")

    def start_plotting(self):
        self.plotting_active = True
        self.update_plot()

    def stop_plotting(self):
        self.plotting_active = False

    def update_plot(self):
        if not self.plotting_active:
            return

        # Simulate data, replace this with real data from STM32
        new_encoder_value = random.randint(0, 100)
        new_force_value = random.uniform(0, 10)

        self.encoder_values.append(new_encoder_value)
        self.force_values.append(new_force_value)

        # Save data to log for later saving to file
        self.data_log.append((new_encoder_value, new_force_value))

        # Limit to the last 50 points for a cleaner plot
        self.encoder_values = self.encoder_values[-50:]
        self.force_values = self.force_values[-50:]

        # Clear the plot and redraw it
        self.ax.clear()
        self.ax.plot(self.encoder_values, self.force_values, marker='o')
        self.ax.set_xlabel('Encoder Value', fontsize=18)
        self.ax.set_ylabel('Force Sensor Value', fontsize=18)
        self.canvas.draw()

        # Call this function again after 10 ms for 100 Hz update
        self.root.after(10, self.update_plot)

    def save_data(self):
        # Get the current date and time for naming
        current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

        # Save the logged data to a .txt file in the "data" folder
        with open(f'data/{current_time}.txt', 'w') as f:
            for encoder_val, force_val in self.data_log:
                f.write(f"Encoder Value: {encoder_val}, Force Value: {force_val}\n")

        messagebox.showinfo("Data Saved", "Data has been saved.")

    def clear_data(self):
        """Clears all data and resets the plot."""
        self.encoder_values.clear()
        self.force_values.clear()
        self.data_log.clear()
        self.ax.clear()
        self.ax.set_xlabel('Encoder Value', fontsize=18)
        self.ax.set_ylabel('Force Sensor Value', fontsize=18)
        self.canvas.draw()
        self.encoder_value.set(0)  # Reset encoder input
        print("All data cleared.")

    def on_closing(self):
        # Stop plotting and close the program
        self.stop_plotting()
        self.root.quit()  # Terminate the program when the window is closed
        self.root.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    app = DynamixelApp(root)
    root.mainloop()
