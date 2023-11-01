import datetime
import threading
import tkinter as tk
from tkinter import ttk, messagebox

from main_menu import sort_column
from scripts.alert import send_alert
from scripts.prolog_interface import PrologQueryHandler as Prolog


class GenerateReportFrame:
    def __init__(self, parent, title):
        self.parent = parent
        self.title = title
        self.frame = tk.Frame(self.parent)
        self.frame.pack()

        self.label = tk.Label(self.frame, text=self.title)
        self.label.pack()

        self.button = tk.Button(self.frame, text="Generate Report", command=self.generate_report)
        self.button.pack()

    def setup_components(self):
        # Create main frame
        self.main_frame = tk.Frame(self.window)
        self.main_frame.pack(fill='both', expand=True)

        # Year Selector
        current_year = datetime.datetime.now().year  # Get the current year
        tk.Label(self.main_frame, text="Select Year:").pack()
        self.year_selector = tk.Spinbox(self.main_frame, from_=2016, to=current_year)
        self.year_selector.pack(pady=5)

        # Optional Label
        tk.Label(self.main_frame, text="OR", font=("Helvetica", 10, "bold")).pack(pady=5)

        # GPA Entry
        tk.Label(self.main_frame, text="Enter GPA:").pack()
        self.gpa_entry = tk.Entry(self.main_frame)
        self.gpa_entry.pack(pady=5)

        # Submit Button
        submit_button = tk.Button(self.main_frame, text="Submit", command=self.submit)
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

        # Hide main frame and show report frame
        self.main_frame.pack_forget()
        self.report(year, gpa)

    def generate_report(self, year, gpa):
        # Create report frame
        self.report_frame = tk.Frame(self.window)
        self.report_frame.pack(fill='both', expand=True)

        # Create a style
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))

        # Labels
        tk.Label(self.report_frame, text="University of Technology", font=("Helvetica", 10, "bold")).pack()
        tk.Label(self.report_frame, text="Academic Probation Alert GPA Report").pack()
        tk.Label(self.report_frame, text=f"Year: {year}").pack()
        tk.Label(self.report_frame, text=f"GPA: {gpa}").pack(pady=5)

        # Create Canvas in new window
        canvas = tk.Canvas(self.report_frame)
        canvas.pack(side=tk.LEFT, fill='both', expand=True)

        # Add a Scrollbar to the Canvas
        scrollbar = ttk.Scrollbar(self.report_frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill='y')

        # Configure the canvas
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Create another frame inside the canvas
        second_frame = tk.Frame(canvas)

        # Add that new frame to a new window on the canvas
        canvas.create_window((0, 0), window=second_frame, anchor="nw")

        # Create Treeview in second frame
        tree = ttk.Treeview(second_frame, show='headings', style="Treeview")  # Apply the style

        # Define columns
        columns = ("Student ID", "Student Name", "GPA Semester 1", "GPA Semester 2", "Cumulative GPA")
        tree["columns"] = columns

        # Format columns
        for col in columns:
            tree.column(col, width=len(col) * 12)
            tree.heading(col, text=col, command=lambda _col=col: sort_column(tree, _col, False))

        # Insert data in table
        for results in Prolog.calculate_cumulative_gpa(year):
            for student in results['Results']:
                student_id, name, email, school, programme, gpa1, gpa2, cumulative_gpa = student
                if not cumulative_gpa == "No GPA calculated" and cumulative_gpa <= gpa:
                    tree.insert("", "end", values=(student_id, name, gpa1, gpa2, cumulative_gpa))
                    # Create a thread for the send_alert function
                    t = threading.Thread(target=send_alert, args=(name, email, school, programme, cumulative_gpa, gpa))
                    t.start()

        tree.pack()

        close_button = tk.Button(self.report_frame, text="Close", command=self.close_report)

        # Center the close button at the bottom of the window
        close_button.place(relx=0.5, rely=0.97, anchor='s')

    def close_report(self):
        # Hide report frame and show main frame
        self.report_frame.pack_forget()
        self.main_frame.pack(fill='both', expand=True)
