import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QWidget, QFrame, QDialog, QLineEdit, QMessageBox, QSplitter, QComboBox
from PyQt5.QtCore import Qt, QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

class ExperimentApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Experiment Page")
        self.setGeometry(100, 100, 1200, 800)
        
        # Main Widget
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        
        # Main Layout using QSplitter for better resizing behavior
        self.main_splitter = QSplitter(Qt.Horizontal, self.main_widget)
        self.main_layout = QHBoxLayout(self.main_widget)
        self.main_layout.addWidget(self.main_splitter)
        self.main_widget.setLayout(self.main_layout)
        
        # Left Side Buttons Frame
        self.side_frame = QFrame(self)
        self.side_frame.setFrameShape(QFrame.StyledPanel)
        self.side_layout = QVBoxLayout(self.side_frame)
        
        self.title_page_button = QPushButton("Material Setting")
        self.title_page_button.setFont(self.font(14))
        self.title_page_button.clicked.connect(self.open_material_setting_page)
        self.side_layout.addWidget(self.title_page_button)
        
        self.input_page_button = QPushButton("Experiment Mode Setting")
        self.input_page_button.setFont(self.font(14))
        self.input_page_button.clicked.connect(self.open_experimental_setting_page)
        self.side_layout.addWidget(self.input_page_button)

        self.calibration_page_button = QPushButton("Calibration")
        self.calibration_page_button.setFont(self.font(14))
        self.calibration_page_button.clicked.connect(self.open_calibration_page)
        self.side_layout.addWidget(self.calibration_page_button)

        self.save_data_page_button = QPushButton("Save Data")
        self.save_data_page_button.setFont(self.font(14))
        self.save_data_page_button.clicked.connect(self.open_save_data_page)
        self.side_layout.addWidget(self.save_data_page_button)

        self.input_page_button = QPushButton("Emergency Stop")
        self.input_page_button.setFont(self.font(14))
        self.input_page_button.setStyleSheet("background-color: red; color: white; font-weight: bold;")
        #self.input_page_button.clicked.connect(self.open_save_data_page)
        self.side_layout.addWidget(self.input_page_button)
        
        self.side_frame.setLayout(self.side_layout)
        self.main_splitter.addWidget(self.side_frame)
        
        # Splitter for Top Plot and Bottom Buttons
        self.right_splitter = QSplitter(Qt.Vertical)
        self.main_splitter.addWidget(self.right_splitter)
        
        # Top Plot Area
        self.top_widget = QWidget(self)
        self.top_layout = QVBoxLayout(self.top_widget)
        
                
        # Plot Area
        self.figure, self.ax = plt.subplots()
        self.ax.set_title("Stress vs Strain")
        self.ax.set_xlabel("Strain")
        self.ax.set_ylabel("Stress")
        self.line, = self.ax.plot([], [], 'r-')
        
        self.canvas = FigureCanvas(self.figure)
        self.top_layout.addWidget(self.canvas)
        
        self.top_widget.setLayout(self.top_layout)
        self.right_splitter.addWidget(self.top_widget)
        
        # Bottom Buttons Frame with Box
        self.bottom_frame = QFrame(self)
        self.bottom_frame.setFrameShape(QFrame.StyledPanel)
        self.bottom_layout = QHBoxLayout(self.bottom_frame)
        
        self.start_stop_button = QPushButton("Start/Stop")
        self.start_stop_button.setFont(self.font(14))
        self.start_stop_button.clicked.connect(self.start_stop_experiment)
        self.bottom_layout.addWidget(self.start_stop_button)
        
        # self.step_button = QPushButton("Step")
        # self.step_button.setFont(self.font(14))
        # self.step_button.clicked.connect(self.step_experiment)
        # self.bottom_layout.addWidget(self.step_button)
        
        self.continue_button = QPushButton("Change Plot")
        self.continue_button.setFont(self.font(14))
        self.continue_button.clicked.connect(self.open_plot_selection_page)
        self.bottom_layout.addWidget(self.continue_button)
        
        self.next_button = QPushButton("Quit")
        self.next_button.setFont(self.font(14))
        self.next_button.clicked.connect(self.open_save_data_page)
        self.bottom_layout.addWidget(self.next_button)
        
        self.bottom_frame.setLayout(self.bottom_layout)
        self.right_splitter.addWidget(self.bottom_frame)
        
        # Set initial splitter sizes to allocate better space for widgets
        self.right_splitter.setSizes([600, 200])
        self.main_splitter.setStretchFactor(1, 1)  # Give right side more resizing priority

    def font(self, size):
        from PyQt5.QtGui import QFont
        return QFont("Arial", size)

    def start_stop_experiment(self):
        QMessageBox.information(self, "Start/Stop", "Start/Stop button clicked.")

    def step_experiment(self):
        QMessageBox.information(self, "Step", "Step button clicked.")

    def continue_experiment(self):
        QMessageBox.information(self, "Continue", "Continue button clicked.")

    def open_plot_selection_page(self):
        plot_dialog = QDialog(self)
        plot_dialog.setWindowTitle("Select Plot")
        plot_dialog.setGeometry(100, 100, 400, 200)
        layout = QVBoxLayout(plot_dialog)
        
        label = QLabel("Select the type of plot you want to display:")
        label.setFont(self.font(14))
        layout.addWidget(label)
        
        plot_combo_box = QComboBox()
        plot_combo_box.addItems(["Stress vs Strain", "Force vs Time", "Force vs Displacement"])
        layout.addWidget(plot_combo_box)
        
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(lambda: self.change_plot(plot_combo_box.currentText(), plot_dialog))
        layout.addWidget(ok_button)
        
        plot_dialog.exec_()


    def change_plot(self, plot_type, dialog):
        # Load data based on selected plot type
        if plot_type == "Stress vs Strain":
            data = pd.read_csv("frontend/metal_stress_vs_strain.csv")
            x_label, y_label = "Strain", "Stress"
        elif plot_type == "Force vs Time":
            data = pd.read_csv("frontend/metal_force_vs_time.csv")
            x_label, y_label = "Time", "Force"
        elif plot_type == "Force vs Displacement":
            data = pd.read_csv("frontend/metal_force_vs_displacement.csv")
            x_label, y_label = "Displacement", "Force"
        else:
            QMessageBox.warning(self, "Invalid Selection", "Invalid plot type selected.")
            return
        
        # Update plot
        self.ax.clear()
        self.ax.plot(data.iloc[:, 0], data.iloc[:, 1], 'r-')
        self.ax.set_title(plot_type)
        self.ax.set_xlabel(x_label)
        self.ax.set_ylabel(y_label)
        self.canvas.draw()
        
        # Close the dialog
        dialog.accept()

    def open_material_setting_page(self):
        # This function remains the same
        pass

    def open_experimental_setting_page(self):
        # This function remains the same
        pass

    def open_calibration_page(self):
        # This function remains the same
        pass

    def open_save_data_page(self):
        # This function remains the same
        pass


    def open_title_page(self):
        title_dialog = QDialog(self)
        title_dialog.setWindowTitle("Title Page")
        title_dialog.setGeometry(100, 100, 400, 200)
        layout = QVBoxLayout(title_dialog)
        
        title_label = QLabel("Title Page")
        title_label.setFont(self.font(20))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        start_button = QPushButton("Start")
        start_button.clicked.connect(title_dialog.accept)
        layout.addWidget(start_button)
        
        title_dialog.exec_()

    def open_material_setting_page(self):
        input_dialog = QDialog(self)
        input_dialog.setWindowTitle("Material Setting")
        input_dialog.setGeometry(100, 100, 400, 300)
        layout = QVBoxLayout(input_dialog)
        
        input_label = QLabel("Material Setting")
        input_label.setFont(self.font(20))
        input_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(input_label)
        
        name_label = QLabel("Name:")
        layout.addWidget(name_label)
        name_entry = QLineEdit()
        layout.addWidget(name_entry)
        
        area_label = QLabel("Width:")
        layout.addWidget(area_label)
        area_entry = QLineEdit()
        layout.addWidget(area_entry)

        area_label = QLabel("Thickness:")
        layout.addWidget(area_label)
        area_entry = QLineEdit()
        layout.addWidget(area_entry)
        
        length_label = QLabel("Gage Length:")
        layout.addWidget(length_label)
        length_entry = QLineEdit()
        layout.addWidget(length_entry)
        
        next_button = QPushButton("Done")
        next_button.clicked.connect(input_dialog.accept)
        layout.addWidget(next_button)
        
        input_dialog.exec_()


    def open_experimental_setting_page(self):
        input_dialog = QDialog(self)
        input_dialog.setWindowTitle("Experiment Mode Setting")
        input_dialog.setGeometry(100, 100, 400, 300)
        layout = QVBoxLayout(input_dialog)
        
        input_label = QLabel("Experiment Mode Setting")
        input_label.setFont(self.font(20))
        input_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(input_label)

        # Buttons for "Material Testing Mode" and "3D Scanner Mode"
        button_layout = QHBoxLayout()
        material_button = QPushButton("Material Testing Mode")
        scanner_button = QPushButton("3D Scanner Mode")
        button_layout.addWidget(material_button)
        button_layout.addWidget(scanner_button)
        layout.addLayout(button_layout)
        
        length_label = QLabel("Time Interval:")
        layout.addWidget(length_label)
        length_entry = QLineEdit()
        layout.addWidget(length_entry)

        length_label = QLabel("Step Size:")
        layout.addWidget(length_label)
        length_entry = QLineEdit()
        layout.addWidget(length_entry)
        
        next_button = QPushButton("Done")
        next_button.clicked.connect(input_dialog.accept)
        layout.addWidget(next_button)
        
        input_dialog.exec_()


    def open_calibration_page(self):
        save_dialog = QDialog(self)
        save_dialog.setWindowTitle("Adjustment/Calibration")
        save_dialog.setGeometry(100, 100, 400, 200)
        layout = QVBoxLayout(save_dialog)
        
        save_label = QLabel("Adjustment/Calibration")
        save_label.setFont(self.font(20))
        save_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(save_label)
        
        # Add force reading section (if needed in the layout)
        self.force_value_label = QLabel("0.00")  # Placeholder for real-time force value
        self.force_value_label.setFont(self.font(16))
        layout.addWidget(QLabel("Force Load [N]:"))
        layout.addWidget(self.force_value_label)

        # Create buttons and layouts
        button_layout = QHBoxLayout()
        
        # Create buttons
        back_double_button = QPushButton("◀◀")
        back_button = QPushButton("◀")
        forward_button = QPushButton("▶")
        forward_double_button = QPushButton("▶▶")

        # Add buttons to horizontal layout
        button_layout.addWidget(back_double_button)
        button_layout.addWidget(back_button)
        button_layout.addWidget(forward_button)
        button_layout.addWidget(forward_double_button)

        # Add horizontal layout to main layout
        layout.addLayout(button_layout)

        # Add ZERO button
        zero_button = QPushButton("ZERO")
        zero_button.clicked.connect(save_dialog.accept)  # Corrected to use save_dialog
        layout.addWidget(zero_button)
        
        # Timer to update the force value (placeholder logic for demonstration)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_force_value)
        self.timer.start(100)  # Update every 100 ms
        
        save_dialog.exec_()


    def open_emergency_stop_page(self):
        save_dialog = QDialog(self)
        save_dialog.setWindowTitle("Save Data Page")
        save_dialog.setGeometry(100, 100, 400, 200)
        layout = QVBoxLayout(save_dialog)
        
        save_label = QLabel("Save Data Page")
        save_label.setFont(self.font(20))
        save_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(save_label)
        
        save_button = QPushButton("Save Data")
        save_button.clicked.connect(self.save_data)
        layout.addWidget(save_button)
        
        done_button = QPushButton("Done")
        done_button.clicked.connect(save_dialog.accept)
        layout.addWidget(done_button)
        
        save_dialog.exec_()

    def open_save_data_page(self):
        save_dialog = QDialog(self)
        save_dialog.setWindowTitle("Save Data Page")
        save_dialog.setGeometry(100, 100, 400, 200)
        layout = QVBoxLayout(save_dialog)
        
        save_label = QLabel("Save Data Page")
        save_label.setFont(self.font(20))
        save_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(save_label)
        
        save_button = QPushButton("Save Data")
        save_button.clicked.connect(self.save_data)
        layout.addWidget(save_button)
        
        done_button = QPushButton("Done")
        done_button.clicked.connect(save_dialog.accept)
        layout.addWidget(done_button)
        
        save_dialog.exec_()

    def update_force_value(self):
        """Update the force value label with data from the load cell."""
        try:
            # Placeholder: Replace with actual load cell reading logic
            force_value = 0.0  # Example value
            self.force_value_label.setText(f"{force_value:.2f}")
        except RuntimeError:
            # Catch any runtime errors, such as accessing a deleted QLabel
            self.timer.stop()


    def save_data(self):
        QMessageBox.information(self, "Save Data", "Data has been saved.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExperimentApp()
    window.show()
    sys.exit(app.exec_())
