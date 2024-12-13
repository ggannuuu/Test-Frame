<h1>ME 470 TEST FRAME APPLICATION MANUAL</h1>



# Experiment Software

## Overview
The team has developed software to streamline the experiment process. This software is designed to:
- Aid users in analyzing data
- Control test frames efficiently
- Manage a series of experiments conveniently

The software architecture consists of three components:
1. **Front-end:** Written in Python using PyQt5 for its fast response and user-friendly interface.
2. **Back-end:** Written in Python for handling data and calculations.
3. **Arduino Control Code:** Written in C++ using the Arduino IDE for direct hardware interaction.


This software requires the following libraries in python. Make sure to install before the usage.

1. **PyQt5**
2. **panda**
3. **matplotlib**
4. **serial**


---

## Features

### 1. **Material Input Section**
Users can input details about their materials and specimen dimensions, including:
- Material Name
- Specimen Type
- Width
- Thickness
- Gage Length

These details are used in the back-end to calculate stress and strain. Saved data files are named based on the entered material and specimen information.

### 2. **Mode Selection Section**
The software offers three operational modes:

#### Continuous Mode
- The test frame operates until specimen failure or maximum displacement.
- Users can specify the elongation rate on the control panel.

#### Manual Mode
- Users specify the displacement per step.
- The probe moves by the defined displacement when the ◄ or ► buttons are clicked.

#### Timer Mode
- Designed for use with 3D scanners.
- Automates elongation at user-defined time intervals and step sizes for hands-free operation.

### 3. **Control Panel**
- Buttons for movement and real-time readings of displacement and force.
- Input fields for elongation rates or step sizes, depending on the selected mode.

### 4. **Data Visualization**
- **Real-Time Force-Time Plot:** Displays the force-time curve dynamically during the experiment.
- **Detailed Terminal Output:** Shows recent data points and detailed readings that may not be apparent from the plot.

### 5. **Special Functions**
- **Zero:** Calibrates force and displacement for normalized results.
- **Save:** Exports experiment data as a `.csv` file for post-processing.
- **E-Stop:** Emergency stop button for safely terminating experiments to prevent damage to the specimen or test frame.

---

## User Interface Overview
### Figures
1. Material Input Section
2. Mode Selection Section
3. Control Panel
4. Real-Time Force-Time Plot
5. Recent Data Points and Terminal

The UI is designed for simplicity and clarity, ensuring first-time users can navigate it effectively.

---

## Key Benefits
- **Real-Time Performance:** Ensures low latency for data visualization and control.
- **User-Friendly Design:** Intuitive interface for seamless operation.
- **Versatile Modes:** Supports various experimental needs with flexible operation modes.
- **Comprehensive Data Handling:** Offers both visual and detailed data outputs for thorough analysis.

---

## Getting Started
1. Install required software: Python (with PyQt5), Arduino IDE.
2. Load the Arduino control code onto the Arduino board.
3. Run the front-end and back-end Python scripts.
4. Use the UI to input material details, select mode, and start experiments.

For more details, refer to the user manual provided with the software.

---

## Support
If you encounter any issues or have suggestions, please contact the development team at [support@example.com](mailto:support@example.com).

