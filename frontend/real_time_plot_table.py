from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class RealTimePlot(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Matplotlib Figure
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)

        # Initial Plot Settings
        self.ax.set_title("Real-Time Plot", fontsize = 30)
        self.ax.set_xlabel("Time [s]", fontsize = 20)
        self.ax.set_ylabel("Force [N]", fontsize = 20)
        self.ax.grid()

        # Data Storage
        self.time_data = []
        self.force_data = []
  

        # Plot Lines
        self.force_line, = self.ax.plot([], [], label="Force [N]", color="red")

        self.ax.legend()

        # Layout
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.canvas)

    def update_plot(self, time, force, displacement):
        """Update the plot with new data."""
        # Append new data
        self.time_data.append(time)
        self.force_data.append(force)
  

        # Update plot data
        self.force_line.set_data(self.time_data, self.force_data)


        # Adjust plot limits dynamically
        self.ax.set_xlim(0, max(10, time))  # Ensure at least 10 seconds visible
        if self.force_data:
            min_force = min(self.force_data)
            max_force = max(self.force_data)
            range_padding = (max_force - min_force) * 0.2 if max_force != min_force else 1.0  # Add padding
            self.ax.set_ylim(min_force - range_padding, max_force + range_padding)

        # Redraw the canvas
        self.canvas.draw()

# class RealTimePlot(QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)

#         # Matplotlib Figure
#         self.figure = Figure()
#         self.canvas = FigureCanvas(self.figure)
#         self.ax = self.figure.add_subplot(111)

#         # Initial Plot Settings
#         self.ax.set_title("Real-Time Plot")
#         self.ax.set_xlabel("Time [s]")
#         self.ax.set_ylabel("Force [N] / Displacement [mm]")
#         self.ax.grid()

#         # Data Storage
#         self.time_data = []
#         self.force_data = []
#         self.displacement_data = []

#         # Plot Lines
#         self.force_line, = self.ax.plot([], [], label="Force [N]", color="red")
#         self.displacement_line, = self.ax.plot([], [], label="Displacement [mm]", color="blue")
#         self.ax.legend()

#         # Layout
#         self.layout = QVBoxLayout(self)
#         self.layout.addWidget(self.canvas)

#     def update_plot(self, time, force, displacement):
#         """Update the plot with new data."""
#         # Append new data
#         self.time_data.append(time)
#         self.force_data.append(force)
#         self.displacement_data.append(displacement)

#         # Update plot data
#         self.force_line.set_data(self.time_data, self.force_data)
#         self.displacement_line.set_data(self.time_data, self.displacement_data)

#         # Adjust plot limits dynamically
#         self.ax.set_xlim(0, max(10, time))  # Ensure at least 10 seconds visible
#         self.ax.set_ylim(0, max(max(self.force_data), max(self.displacement_data)) * 1.1)

#         # Redraw the canvas
#         self.canvas.draw()



class RealTimeTable(QWidget):
    """Widget displaying a table of the recent 5 values."""
    def __init__(self, parent=None):
        super().__init__(parent)

        # Table setup
        self.table = QTableWidget(5, 3)  # 5 rows, 3 columns (time, force, displacement)
        self.table.setHorizontalHeaderLabels(["Time [s]", "Force [N]", "Displacement [mm]"])
        self.table.verticalHeader().setVisible(False)  # Hide row numbers

        # Layout
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.table)

        # Data Storage
        self.data = []

    def update_table(self, time, force, displacement):
        """Update the table with new data."""
        # Add new data to the list
        self.data.append((time, force, displacement))

        # Keep only the last 5 entries
        if len(self.data) > 5:
            self.data.pop(0)

        # Update the table
        for row, (time, force, displacement) in enumerate(self.data):
            self.table.setItem(row, 0, QTableWidgetItem(f"{time}"))
            self.table.setItem(row, 1, QTableWidgetItem(f"{force:.2f}"))
            self.table.setItem(row, 2, QTableWidgetItem(f"{displacement:.2f}"))

        # Clear unused rows
        for row in range(len(self.data), 5):
            self.table.setItem(row, 0, QTableWidgetItem(""))
            self.table.setItem(row, 1, QTableWidgetItem(""))
            self.table.setItem(row, 2, QTableWidgetItem(""))