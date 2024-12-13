import sys
import os
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QWidget, QFrame, QDialog, QLineEdit, QMessageBox, QSplitter, QComboBox, QGroupBox, QRadioButton, QLineEdit, QStackedWidget, QTextEdit
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from real_time_plot_table import RealTimePlot, RealTimeTable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.backend_experiment import Backend

import random

class BackendSimulator:
    """Simulates the backend providing force and displacement readings."""
    def __init__(self):
        self.force = 0.0
        self.displacement = 0.0
        self.time = 0

    def get_readings(self):
        # Simulate real-time values
        self.force = random.uniform(0, 100)  # Random force in N
        self.displacement = random.uniform(0, 50)  # Random displacement in mm
        return self.force, self.displacement
    
    def get_data(self):
        self.time += 1  # Simulate time increment
        self.force = random.uniform(0, 100)  # Simulate force in N
        self.displacement = random.uniform(0, 50)  # Simulate displacement in mm
        return self.time, self.force, self.displacement



class ExperimentApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Experiment Page")
        self.setGeometry(100, 100, 1200, 800)

        '''
        Backend Simulator
        '''
        self.backend = backend
        self.backend.connect_serial()


        
        # Main Widget
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        # Main Layout using QSplitter for better resizing behavior
        self.main_splitter = QSplitter(Qt.Horizontal, self.main_widget)
        self.main_layout = QHBoxLayout(self.main_widget)
        self.main_layout.addWidget(self.main_splitter)
        self.main_widget.setLayout(self.main_layout)

        # Setting and Input Section
        # Left Side of the Main Widget
        self.setting_frame = QFrame()
        self.setting_frame.setFrameShape(QFrame.StyledPanel)
        self.setting_layout = QVBoxLayout(self.setting_frame)
        #self.add_setting_contents()
        self.main_splitter.addWidget(self.setting_frame)

        # Right side widget
        self.second_splitter = QSplitter(Qt.Vertical)
        self.main_splitter.addWidget(self.second_splitter)


        # Right-Top side widget
        self.top_right_splitter = QSplitter(Qt.Horizontal)
        self.second_splitter.addWidget(self.top_right_splitter)

        # Graph Section
        # Right-Top-Left section
        self.graph_section_frame = QFrame()
        self.graph_section_frame.setFrameShape(QFrame.StyledPanel)
        self.graph_section_layout = QVBoxLayout(self.graph_section_frame)
        #self.add_graph_section_contents()
        self.top_right_splitter.addWidget(self.graph_section_frame)


        # Value Log Display
        # Right-Top-Right section
        self.log_panel_frame = QFrame()
        self.log_panel_frame.setFrameShape(QFrame.StyledPanel)
        self.log_panel_layout = QVBoxLayout(self.log_panel_frame)
        #self.add_log_panel_contents()
        self.top_right_splitter.addWidget(self.log_panel_frame)

        # Control Panel
        # Right-Bottom Side of the Main Widget
        self.control_panel_frame = QFrame()
        self.control_panel_frame.setFrameShape(QFrame.StyledPanel)
        self.control_panel_layout = QVBoxLayout(self.control_panel_frame)
        #self.add_control_panel_contents()
        self.second_splitter.addWidget(self.control_panel_frame)


        # Call the Contents functions
        self.add_setting_contents()
        self.add_graph_section_contents()
        self.add_log_panel_contents()
        self.add_control_panel_contents()


        # Default Size Adjustment
        self.main_splitter.setSizes([400, 800])  # Adjust Left (Settings) and Right
        self.second_splitter.setSizes([600, 200])  # Adjust Top-Right and Bottom
        self.top_right_splitter.setSizes([600, 200])  # Adjust Graph and Log





    # Function for Setting and Input Page
    # Section on the left
    def add_setting_contents(self):
        # Left Side Input Widget
        # Todo: Material Input, Mode Settings (Cont., Manual, Timer), Calib (Zero), Change plot, Save, Emergency Stop

        self.input_frame = QFrame(self)
        self.input_frame.setFrameShape(QFrame.StyledPanel)
        self.input_layout = QVBoxLayout(self.input_frame)

        ## Material Setting
        ## Blanks for Material name, Specimen type, width, gage length, and thickness
        self.material_fields = {}
        self.add_input_field("Material Name: ", "material_name")
        self.add_input_field("Specimen Type: ", "specimen_type")
        self.add_input_field("Width [mm]: ", "width")
        self.add_input_field("Thickness [mm]: ", "thickness")
        self.add_input_field("Gage Length [mm]: ", "gage_length")

        self.save_material_input_button = QPushButton("OK")
        self.save_material_input_button.clicked.connect(self.validate_and_save_material_settings)
        self.input_layout.addWidget(self.save_material_input_button)

        self.setting_layout.addWidget(self.input_frame)


        ## Mode Setting
        ## Offers Continuous, Manual, and Timer mode. Default as Continuous
        self.mode_setting_box = QGroupBox("Mode Selection")
        
        self.mode_layout = QVBoxLayout(self.mode_setting_box)

        ### Mode Buttons
        self.continuous_mode_button = QRadioButton("Continuous")
        self.manual_mode_button = QRadioButton("Manual")
        self.timer_mode_button = QRadioButton("Timer")

        self.continuous_mode_button.setChecked(True)

        self.mode_layout.addWidget(self.continuous_mode_button)
        self.mode_layout.addWidget(self.manual_mode_button)
        self.mode_layout.addWidget(self.timer_mode_button)

        self.dynamic_content = QStackedWidget()
        self.dynamic_content.setFrameShape(QFrame.StyledPanel)

        ### Mode functions
        self.add_continuous_mode_content()
        self.add_manual_mode_content()
        self.add_timer_mode_content()

        self.continuous_mode_button.toggled.connect(lambda: self.switch_mode(0))
        self.manual_mode_button.toggled.connect(lambda: self.switch_mode(1))
        self.timer_mode_button.toggled.connect(lambda: self.switch_mode(2))

        self.setting_layout.addWidget(self.mode_setting_box)
        #self.control_panel_layout.addWidget(self.dynamic_content)

        ## Zero
        ## Zeros the force and displacement
        self.calibration_button = QPushButton("Zero")
        self.calibration_button.setFont(self.font(14))
        self.calibration_button.clicked.connect(self.zero_force_displacement)
        self.setting_layout.addWidget(self.calibration_button)

        ## Plot Mode Setting
        ## Allows Force vs. Time and Force vs. Displacement plots


        ## Save
        ## Save the file in csv. Need to be done in backend
        self.save_button = QPushButton("Save")
        self.save_button.setFont(self.font(14))
        self.save_button.clicked.connect(self.save)
        self.setting_layout.addWidget(self.save_button)


        ## Emergency Stop
        ## Stops whatever everything right now
        self.emergency_stop_button = QPushButton("E-Stop")
        self.emergency_stop_button.clicked.connect(self.emergency_stop)
        self.emergency_stop_button.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: white;
                font-weight: bold;
                font-size: 30px;
                border: none;
                border-radius: 50px; /* Circular shape */
                width: 100px;       /* Fixed width */
                height: 100px;      /* Fixed height */
            }
            QPushButton:hover {
                background-color: darkred;
            }
        """)
        self.setting_layout.addWidget(self.emergency_stop_button)


    # Functions for the control Panel
    # It is on the right-bottom section
    # Offers Real-Time force and displacement reading, mode selection settings(It is from setting contents), Probe control, and start recording and stop recording buttons
    def add_control_panel_contents(self):


        ## Real Time Force and Displacement Reading
        self.real_time_force_label = QLabel("Force [N]: 0.00")
        self.real_time_force_label.setFont(self.font(18))
        self.control_panel_layout.addWidget(self.real_time_force_label)

        self.real_time_displacement_label = QLabel("Displacement [mm]: 0.00")
        self.real_time_displacement_label.setFont(self.font(18))
        self.control_panel_layout.addWidget(self.real_time_displacement_label)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_readings)
        self.timer.start(500)

        ## Probe Control

        self.probe_control_box = QGroupBox()
        self.probe_control_layout = QHBoxLayout(self.probe_control_box)

        self.move_left_button = QPushButton("◀")
        self.move_left_button.setFont(self.font(14))
        self.move_left_button.clicked.connect(self.move_left)

        self.move_right_button = QPushButton("▶")
        self.move_right_button.setFont(self.font(14))
        self.move_right_button.clicked.connect(self.move_right)

        self.probe_control_layout.addWidget(self.move_left_button)
        self.probe_control_layout.addWidget(self.move_right_button)

        self.control_panel_layout.addWidget(self.probe_control_box)


        ## Mode Input Widget
        self.control_panel_layout.addWidget(self.dynamic_content)


        ## Start / Stop Buttons
        self.start_stop_experiment_box = QGroupBox()
        self.start_stop_experiment_layout = QHBoxLayout(self.start_stop_experiment_box)

        self.start_experiment_button = QPushButton("Start")
        self.start_experiment_button.setFont(self.font(14))
        self.start_experiment_button.clicked.connect(self.start_experiment)

        self.stop_experiment_button = QPushButton("Stop")
        self.stop_experiment_button.setFont(self.font(14))
        self.stop_experiment_button.clicked.connect(self.stop_experiment)

        self.start_stop_experiment_layout.addWidget(self.start_experiment_button)
        self.start_stop_experiment_layout.addWidget(self.stop_experiment_button)

        self.control_panel_layout.addWidget(self.start_stop_experiment_box)




    def add_graph_section_contents(self):
        '''
        Real Time Plot
        '''
        self.real_time_plot = RealTimePlot(self)
        self.graph_section_layout.addWidget(self.real_time_plot)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start(500)



    def add_log_panel_contents(self):
        '''
        Real Time Table
        '''

        self.real_time_table = RealTimeTable(self)
        self.log_panel_layout.addWidget(self.real_time_table)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_table_data)
        self.timer.start(500)

        self.log_console = QTextEdit(self)
        self.log_console.setReadOnly(True)  # Make the log console read-only
        self.log_panel_layout.addWidget(self.log_console)

        # Example: Simulate backend logs being added to the terminal
        self.log_timer = QTimer(self)
        self.log_timer.timeout.connect(self.update_log_console)
        self.log_timer.start(500)  # Update logs every 500 ms
    


    # Global Functions

    ## Font
    ## set font

    def font(self, size):
        return QFont("Arial", size)

    ## Dummy function for display of real-time values
    




    # Material Setting Function  

    ## Creates the blanks for the inputs
    ## Format : "Label Text" // Blank
    def add_input_field(self, label_text, field_name):
        field_layout = QHBoxLayout()

        label = QLabel(label_text)
        label.setStyleSheet("font-size: 26px; font-family: Arial;")
        input_field = QLineEdit()
        input_field.setPlaceholderText("Enter")

        self.material_fields[field_name] = input_field

        field_layout.addWidget(label)
        field_layout.addWidget(input_field)

        self.input_layout.addLayout(field_layout)

    def validate_and_save_material_settings(self):
        for field_name, input_field in self.material_fields.items():
            if not input_field.text().strip():
                QMessageBox.warning(self, "Validation Error", f"Please fill in all fields.")
                return

        material_settings = {field_name: input_field.text() for field_name, input_field in self.material_fields.items()}
        self.backend.material_name = material_settings["material_name"]
        self.backend.specimen_type = material_settings["specimen_type"]
        self.backend.width = float(material_settings["width"])
        self.backend.thickness = float(material_settings["thickness"])
        self.backend.gage_length = float(material_settings["gage_length"])
        print("Material Settings Saved:", material_settings)

        QMessageBox.information(self, "Success", "Material settings have been saved!")

    # Mode Setting Function
    ## function for switch from one to another mode
    def switch_mode(self, index):
        self.dynamic_content.setCurrentIndex(index)

    ## Continuous mode selection
    ## Offers elongation rate field
    def add_continuous_mode_content(self):
        cont_widget = QWidget()
        layout = QVBoxLayout(cont_widget)

        elongation_rate_label = QLabel("Elongation Rate [mm/s] : ")
        elongation_rate_input = QLineEdit()
        elongation_rate_input.setPlaceholderText("Enter")

        layout.addWidget(elongation_rate_label)
        layout.addWidget(elongation_rate_input)

        self.save_continuous_mode_input_button = QPushButton("Enter")
        self.save_continuous_mode_input_button.clicked.connect(lambda: self.mode_value_enter("continuous"))
        self.input_layout.addWidget(self.save_continuous_mode_input_button)

        self.dynamic_content.addWidget(cont_widget)

    ## Manual mode selection
    ## Offers displacement values and allows to execute experiment only with adj

    def add_manual_mode_content(self):
        manual_widget = QWidget()
        layout = QVBoxLayout(manual_widget)

        manual_displacement_label = QLabel("Displacement(Step Size) [mm] : ")
        manual_displacement_input = QLineEdit()
        manual_displacement_input.setPlaceholderText("Enter")

        layout.addWidget(manual_displacement_label)
        layout.addWidget(manual_displacement_input)

        self.save_manual_mode_input_button = QPushButton("Enter")
        self.save_manual_mode_input_button.clicked.connect(lambda: self.mode_value_enter("manual"))
        self.input_layout.addWidget(self.save_manual_mode_input_button)
        
        self.dynamic_content.addWidget(manual_widget)

    ## Timer mode selection
    ## Offers time interval and displacement values input

    def add_timer_mode_content(self):
        timer_widget = QWidget()
        layout = QVBoxLayout(timer_widget)

        timer_displacement_label = QLabel("Displacement(Step Size) [mm] : ")
        timer_displacement_input = QLineEdit()
        timer_displacement_input.setPlaceholderText("Enter")

        timer_interval_label = QLabel("Time Interval [s] : ")
        timer_interval_input = QLineEdit()
        timer_interval_input.setPlaceholderText("Enter")

        layout.addWidget(timer_displacement_label)
        layout.addWidget(timer_displacement_input)

        layout.addWidget(timer_interval_label)
        layout.addWidget(timer_interval_input)

        self.save_timer_mode_input_button = QPushButton("Enter")
        self.save_timer_mode_input_button.clicked.connect(lambda: self.mode_value_enter("timer"))
        self.input_layout.addWidget(self.save_timer_mode_input_button)

        self.dynamic_content.addWidget(timer_widget)

    def mode_value_enter(self, mode):
        try:
            if mode == "continuous":
                elongation_rate = float(self.elongation_rate_input.text().strip())
                self.backend.elongation_rate = elongation_rate
                self.backend.mode = "continuous"
                QMessageBox.information(self, "Success", f"Continuous mode settings saved: Elongation Rate = {elongation_rate} mm/s")

            elif mode == "manual":
                manual_displacement = float(self.manual_displacement_input.text().strip())
                self.backend.step_size = manual_displacement
                self.backend.mode = "manual"
                QMessageBox.information(self, "Success", f"Manual mode settings saved: Displacement = {manual_displacement} mm")

            elif mode == "timer":
                timer_displacement = float(self.timer_displacement_input.text().strip())
                timer_interval = float(self.timer_interval_input.text().strip())
                self.backend.step_size = timer_displacement
                self.backend.time_interval = timer_interval
                self.backend.mode = "timer"
                QMessageBox.information(self, "Success", f"Timer mode settings saved: Displacement = {timer_displacement} mm, Interval = {timer_interval} s")

        except ValueError:
            QMessageBox.warning(self, "Validation Error", "Please enter valid numerical values.")
        except AttributeError as e:
            QMessageBox.critical(self, "Error", f"Backend does not support the required attributes: {e}")

        # For debugging, print the updated backend values
        print("Backend Updated:")
        print(f"Mode: {mode}")
        if mode == "continuous":
            print(f"Elongation Rate: {self.backend.elongation_rate}")
        elif mode == "manual":
            print(f"Manual Displacement: {self.backend.manual_displacement}")
        elif mode == "timer":
            print(f"Timer Displacement: {self.backend.timer_displacement}, Timer Interval: {self.backend.timer_interval}")

    # Calibration
    # Zeros the force and displacement
    def zero_force_displacement(self):
        self.backend.set_force(0.0)
        self.backend.set_position(0.0)
        return

    # Plot mode function
    # Changed from F vs t to F vs d or vice versa
    '''
    To be done
    '''
    def plot_format(self, index):
        return

    # Save
    # Save the records
    '''
    To be done
    '''
    def save(self):
        return
    

    # Emergency Stop
    # Stop the motor and whatever
    '''
    To be done
    '''
    def emergency_stop(self):
        self.backend.motor_stop()



    # Control Panel Functions

    ## Force and Reading Updates
    ## Dummy

    def update_readings(self):
        force, displacement = self.backend.get_readings()

        self.real_time_force_label.setText(f"Force [N]: {force:.2f}")
        self.real_time_displacement_label.setText(f"Displacement [mm]: {displacement:.2f}")

    ## Probe Control
    def move_left(self):
        self.backend.execute_experiment("left")
        return
    
    def move_right(self):
        self.backend.execute_experiment("right")
        return
    
    ## Start and Stop Experiment

    def start_experiment(self):
        return
    
    def stop_experiment(self):
        return
    


    # Graph Section Functions
    # Update the plot in real time

    def update_plot_data(self):
        """Fetch new data from the backend and update the plot."""
        time, force, displacement = self.backend.get_data()
        self.real_time_plot.update_plot(time, force, displacement)




    # Log Panel Section Functions
    # Update the Table in real time

    def update_table_data(self):
        """Fetch new data from the backend and update the table."""
        time, force, displacement = self.backend.get_data()
        self.real_time_table.update_table(time, force, displacement)

    def update_log_console(self):
        # Example log message; replace this with actual backend messages
        time, force, displacement = self.backend.get_data()
        log_message = f"Time: {time:.2f} s, Force: {force:.2f} N, Displacement: {displacement:.2f} mm\n"
        
        # Append the log message to the console
        self.log_console.append(log_message)
        
        # Automatically scroll to the bottom
        self.log_console.moveCursor(self.log_console.textCursor().End)


        

if __name__ == "__main__":
    backend = Backend()



    app = QApplication(sys.argv)
    default_font = QFont("Arial", 14)
    app.setFont(default_font)
    window = ExperimentApp()
    window.show()
    sys.exit(app.exec_())
