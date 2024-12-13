import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
from frontend.frontend_pyqt import ExperimentApp
from frontend.real_time_plot_table import RealTimePlot, RealTimeTable
from backend.backend_experiment import Backend


def main():
    # Initialize the backend
    backend = Backend()
    backend.connect_serial()

    # Initialize the application
    app = QApplication(sys.argv)
    default_font = QFont("Arial", 14)
    app.setFont(default_font)

    # Launch the main application window
    window = ExperimentApp(backend)
    window.show()

    # Execute the application loop
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
