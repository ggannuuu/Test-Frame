import tkinter as tk
from tkinter import messagebox

class ExperimentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Experiment Software")
        self.pages = {}

        # Initialize each page
        self.create_page1()
        self.create_page2()
        self.create_page3()
        self.create_page4()
        self.create_page5()
        self.create_page6()

        # Display the first page initially
        self.show_page("page1")

    def show_page(self, page_name):
        for page in self.pages.values():
            page.pack_forget()
        self.pages[page_name].pack()

    def create_page1(self):
        page = tk.Frame(self.root)
        tk.Label(page, text="Test Frame", font=("Arial", 24)).pack(pady=10)
        tk.Label(page, text="Tensile Test Software", font=("Arial", 18)).pack(pady=10)
        tk.Button(page, text="Tensile Test", command=lambda: self.show_page("page2")).pack(pady=5)
        tk.Button(page, text="Indentation Test", command=lambda: self.show_page("page2")).pack(pady=5)
        self.pages["page1"] = page

    def create_page2(self):
        page = tk.Frame(self.root)
        tk.Label(page, text="Enter Experiment Details", font=("Arial", 18)).pack(pady=10)

        tk.Label(page, text="Specimen Type:").pack(anchor="w")
        self.specimen_var = tk.StringVar()
        tk.OptionMenu(page, self.specimen_var, "ASTM D638 Type IV", "ASTM D638 Type V", "Other").pack(anchor="w")

        tk.Label(page, text="Width (mm):").pack(anchor="w")
        self.width_entry = tk.Entry(page)
        self.width_entry.pack(anchor="w")

        tk.Label(page, text="Thickness (mm):").pack(anchor="w")
        self.thinkness_entry = tk.Entry(page)
        self.thinkness_entry.pack(anchor="w")

        tk.Label(page, text="Gage Length (mm):").pack(anchor="w")
        self.length_entry = tk.Entry(page)
        self.length_entry.pack(anchor="w")

        self.selected_mode = None
        tk.Button(page, text="Material Tensile Test Mode", command=lambda: self.select_mode("tensile")).pack()
        tk.Button(page, text="3D Scanner Mode", command=lambda: self.select_mode("scanner")).pack()

        tk.Button(page, text="Next", command=self.validate_input).pack(pady=10)
        self.pages["page2"] = page

    def select_mode(self, mode):
        self.selected_mode = mode
        messagebox.showinfo("Mode Selected", f"{mode} mode selected")

    def validate_input(self):
        if not self.width_entry.get() or not self.thinkness_entry.get() or not self.length_entry.get() or not self.selected_mode:
            messagebox.showwarning("Validation Error", "Please fill all fields and select an experiment mode.")
        else:
            self.show_page("page3")

    def create_page3(self):
        page = tk.Frame(self.root)
        tk.Label(page, text="Adjustment/Calibration", font=("Arial", 18)).pack(pady=10)

        tk.Label(page, text="Force[N]: ").pack(anchor="w")
        tk.Label(page, text="Position[mm]: ").pack(anchor="w")

        tk.Button(page, text="◀◀", command=lambda: self.initial_position("coarseCCW")).pack(side="left")
        tk.Button(page, text="◀", command=lambda: self.initial_position("fineCCW")).pack(side="left")
        tk.Button(page, text="▶", command=lambda: self.initial_position("fineCW")).pack(side="left")
        tk.Button(page, text="▶▶", command=lambda: self.initial_position("coarseCW")).pack(side="left")
        tk.Button(page, text="Zero", command=self.calibrate).pack(pady=10)
        
        self.pages["page3"] = page

    def initial_position(self, adj_type):
        print(f"Adjusting position: {adj_type}")

    def calibrate(self):
        print("Calibration started")

    def create_page4(self):
        page = tk.Frame(self.root)
        tk.Label(page, text="Experiment", font=("Arial", 18)).pack(pady=10)

        # Placeholder for plot
        tk.Label(page, text="Plot goes here (Placeholder)").pack(pady=10)

        tk.Button(page, text="Start Recording", command=self.start_stop_experiment).pack(pady=5)
        tk.Button(page, text="Step", command=self.step_experiment).pack(pady=5)
        tk.Button(page, text="Continue", command=self.continue_experiment).pack(pady=5)
        tk.Button(page, text="Clear", command=self.clear_data).pack(pady=5)
        tk.Button(page, text="Finish", command=lambda: self.show_page("page5")).pack(pady=5)

        self.pages["page4"] = page

    def start_stop_experiment(self):
        print("Experiment started/stopped")

    def step_experiment(self):
        print("Step experiment")

    def continue_experiment(self):
        print("Continue experiment")

    def clear_data(self):
        print("Data cleared")

    def create_page5(self):
        page = tk.Frame(self.root)
        tk.Label(page, text="Save Experiment Data", font=("Arial", 18)).pack(pady=10)
        tk.Label(page, text="Would you like to save the experiment data?").pack(pady=10)
        tk.Button(page, text="Save", command=self.save_data).pack(pady=5)
        tk.Button(page, text="Done", command=lambda: self.show_page("page6")).pack(pady=5)

        self.pages["page5"] = page

    def save_data(self):
        print("Data saved")

    def create_page6(self):
        page = tk.Frame(self.root)
        tk.Label(page, text="Thank you for using our software!", font=("Arial", 24)).pack(pady=10)
        self.pages["page6"] = page


if __name__ == "__main__":
    root = tk.Tk()
    app = ExperimentApp(root)
    root.mainloop()
