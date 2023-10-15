import datetime
import tkinter as tk
from src.scripts.prolog_interface import PrologQueryHandler as Prolog
from tkinter import messagebox
from tkinter import ttk


class AcademicProbationSystem:
    def __init__(self):
        self.year_selector = None
        self.gpa_entry = None
        self.root = tk.Tk()
        self.root.title('Academic Probation System')
        self.setup_window()
        self.setup_components()

    def setup_window(self):
        # Set window size
        window_width = 500
        window_height = 200

        # Get screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate position
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)

        # Set window size and position
        self.root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

    def setup_components(self):
        # Year Selector
        current_year = datetime.datetime.now().year  # Get the current year
        tk.Label(self.root, text="Select Year:").pack()
        self.year_selector = tk.Spinbox(self.root, from_=2000, to=current_year)
        self.year_selector.pack(pady=5)

        # Optional Label
        tk.Label(self.root, text="OR", font=("Helvetica", 10, "bold")).pack(pady=5)

        # GPA Entry
        tk.Label(self.root, text="Enter GPA:").pack()
        self.gpa_entry = tk.Entry(self.root)
        self.gpa_entry.pack(pady=5)

        # Submit Button
        submit_button = tk.Button(self.root, text="Submit", command=self.submit)
        submit_button.pack(pady=5)

    def submit(self):
        # Get data
        year = self.year_selector.get()
        gpa = self.gpa_entry.get()

        if gpa != "":
            # Validate GPA
            try:
                gpa = float(gpa)
                if not 0.0 <= gpa <= 4.0:
                    raise ValueError("GPA must be between 0.0 and 4.0")
                else:
                    Prolog.update_gpa(gpa)  # update default GPA
            except ValueError as e:
                messagebox.showerror("Invalid Input", str(e))
                return
        else:
            gpa = Prolog.get_default_gpa()  # get default gpa

        messagebox.showinfo("Submitted", f"Year: {year}, GPA: {gpa}")
        self.report(year, gpa)

    def report(self, year, gpa):
        # Create new window
        new_window = tk.Toplevel(self.root)

        # Create a style
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))

        # Labels
        tk.Label(new_window, text="University of Technology", font=("Helvetica", 10, "bold")).pack()
        tk.Label(new_window, text="Academic Probation Alert GPA Report").pack()
        tk.Label(new_window, text=f"Year: {year}").pack()
        tk.Label(new_window, text=f"GPA: {gpa}").pack(pady=5)

        # Create Treeview in new window
        tree = ttk.Treeview(new_window, show='headings', style="Treeview")  # Apply the style

        # Define columns
        columns = ("Student ID", "Student Name", "GPA Semester 1", "GPA Semester 2", "Cumulative GPA")
        tree["columns"] = columns

        # Format columns
        for col in columns:
            tree.column(col, width=len(col) * 10)
            tree.heading(col, text=col)

        # Insert data
        tree.insert("", "end", values=("1", "John Doe", "3.5", "3.7", "3.6"))
        tree.pack()

        close_button = tk.Button(new_window, text="Close", command=new_window.destroy)
        close_button.pack(pady=5)

    def run(self):
        self.root.mainloop()


# Create and run the application
app = AcademicProbationSystem()
app.run()
