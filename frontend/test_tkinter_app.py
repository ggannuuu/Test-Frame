import tkinter as tk
from tkinter import simpledialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

class ExperimentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Experiment Page")
        self.root.geometry("1200x800")
        
        # Bind the resize event to adjust the widget sizes dynamically
        self.root.bind("<Configure>", self.on_resize)
        
        # Main Page: Experiment Page
        self.setup_experiment_page()

    def setup_experiment_page(self):
        # Create a frame on the left side to hold some buttons, with a border
        self.side_frame = tk.Frame(self.root, bd=2, relief=tk.SUNKEN)
        self.side_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        # Buttons in the side frame
        self.start_stop_button = tk.Button(self.side_frame, text="Start/Stop", command=self.start_stop_experiment, font=("Arial", 18))
        self.start_stop_button.pack(pady=10, padx=10, fill=tk.X)
        
        self.step_button = tk.Button(self.side_frame, text="Step", command=self.step_experiment, font=("Arial", 18))
        self.step_button.pack(pady=10, padx=10, fill=tk.X)
        
        self.continue_button = tk.Button(self.side_frame, text="Continue", command=self.continue_experiment, font=("Arial", 18))
        self.continue_button.pack(pady=10, padx=10, fill=tk.X)
        
        self.next_button = tk.Button(self.side_frame, text="Next", command=self.open_save_data_page, font=("Arial", 18))
        self.next_button.pack(pady=10, padx=10, fill=tk.X)
        
        # Title Label
        self.title_label = tk.Label(self.root, text="Real-Time Stress vs Strain Plot", font=("Arial", 28))
        self.title_label.pack(pady=10)
        
        # Plot Area
        self.figure, self.ax = plt.subplots(figsize=(8, 5))
        self.ax.set_title("Stress vs Strain")
        self.ax.set_xlabel("Strain")
        self.ax.set_ylabel("Stress")
        self.line, = self.ax.plot([], [], 'r-')
        
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        # Buttons to open pop-up windows for other pages
        self.navigation_frame = tk.Frame(self.root)
        self.navigation_frame.pack(pady=10)
        
        self.title_page_button = tk.Button(self.navigation_frame, text="Open Title Page", command=self.open_title_page, font=("Arial", 18))
        self.title_page_button.grid(row=0, column=0, padx=20, pady=10)
        
        self.input_page_button = tk.Button(self.navigation_frame, text="Open Input Page", command=self.open_input_page, font=("Arial", 18))
        self.input_page_button.grid(row=0, column=1, padx=20, pady=10)

    def on_resize(self, event):
        # Get the new width and height of the window
        new_width = event.width
        new_height = event.height
        
        # Adjust font size based on window size
        font_size = max(14, int(new_height / 30))
        self.title_label.config(font=("Arial", font_size))
        
        # Adjust button sizes and padding
        for widget in self.side_frame.winfo_children() + self.navigation_frame.winfo_children():
            widget.config(font=("Arial", font_size))

    def start_stop_experiment(self):
        messagebox.showinfo("Start/Stop", "Start/Stop button clicked.")

    def step_experiment(self):
        messagebox.showinfo("Step", "Step button clicked.")

    def continue_experiment(self):
        messagebox.showinfo("Continue", "Continue button clicked.")

    def open_title_page(self):
        # Title Page
        title_popup = tk.Toplevel(self.root)
        title_popup.title("Title Page")
        title_popup.geometry("400x200")
        title_label = tk.Label(title_popup, text="Title Page", font=("Arial", 28))
        title_label.pack(pady=10)
        start_button = tk.Button(title_popup, text="Start", command=title_popup.destroy)
        start_button.pack(pady=5)

    def open_input_page(self):
        # Input Page
        input_popup = tk.Toplevel(self.root)
        input_popup.title("Input Page")
        input_popup.geometry("400x300")
        input_label = tk.Label(input_popup, text="Input Page", font=("Arial", 28))
        input_label.pack(pady=10)
        
        name_label = tk.Label(input_popup, text="Name:")
        name_label.pack()
        name_entry = tk.Entry(input_popup)
        name_entry.pack(pady=5)
        
        area_label = tk.Label(input_popup, text="Cross-sectional Area:")
        area_label.pack()
        area_entry = tk.Entry(input_popup)
        area_entry.pack(pady=5)
        
        length_label = tk.Label(input_popup, text="Length:")
        length_label.pack()
        length_entry = tk.Entry(input_popup)
        length_entry.pack(pady=5)
        
        next_button = tk.Button(input_popup, text="Next", command=input_popup.destroy)
        next_button.pack(pady=5)

    def open_save_data_page(self):
        # Data Save Page
        save_popup = tk.Toplevel(self.root)
        save_popup.title("Save Data Page")
        save_popup.geometry("400x200")
        save_label = tk.Label(save_popup, text="Save Data Page", font=("Arial", 28))
        save_label.pack(pady=10)
        
        save_button = tk.Button(save_popup, text="Save Data", command=self.save_data)
        save_button.pack(pady=5)
        
        done_button = tk.Button(save_popup, text="Done", command=save_popup.destroy)
        done_button.pack(pady=5)

    def save_data(self):
        messagebox.showinfo("Save Data", "Data has been saved.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExperimentApp(root)
    root.mainloop()
