import datetime
import threading
import tkinter as tk
from tkinter import messagebox

from src.scripts.alert import send_alert
from src.scripts.database.queries import DatabaseManager
from src.scripts.gui.helpers import create_treeview
from src.scripts.prolog_interface import PrologQueryHandler as Prolog

db_manager = DatabaseManager()  # create an instance of DatabaseManager


class GenerateReportFrame:

    def __init__(self, parent):
        self.select_year = None
        self.generate_frame = None
        self.title = None
        self.gpa_entry = None
        self.year_selector = None
        self.report_frame = None
        self.parent = parent

        self.setup_components()

    def setup_components(self):
        # Create report frame
        self.generate_frame = tk.Frame(self.parent)
        self.generate_frame.grid(row=0, column=1, columnspan=1, sticky="nsew")

        # title
        self.title = tk.Label(self.generate_frame, text="Generate Report", font=('Arial', 16, 'bold'))
        self.title.configure(foreground='black')
        self.title.pack(padx=20, pady=20, fill='x', expand=True)

        # Year Selector
        current_year = datetime.datetime.now().year  # Get the current year
        self.select_year = tk.Label(self.generate_frame, text="Select Year:", font=('Arial', 12, 'normal'))
        self.select_year.pack()
        self.year_selector = tk.Spinbox(self.generate_frame, font=('Arial', 11, 'normal'), from_=2016, to=current_year)
        self.year_selector.pack(padx=150, pady=5, fill='x', expand=True)

        # Optional Label
        tk.Label(self.generate_frame, text="OR", font=("Helvetica", 12, "bold")).pack(padx=80, pady=5, fill='x',
                                                                                      expand=True)
        # GPA Entry
        tk.Label(self.generate_frame, text="Enter GPA:", font=('Arial', 12, 'normal')).pack()
        self.gpa_entry = tk.Entry(self.generate_frame, font=('Arial', 11, 'normal'))
        self.gpa_entry.pack(padx=80, pady=5, fill='x', expand=True)

        # Submit Button
        submit_button = tk.Button(self.generate_frame, text="Generate Report", command=self.submit)
        submit_button.pack(padx=150, pady=5, fill='x', expand=True)

        # Back Button
        back_button = tk.Button(self.generate_frame, text="Back", command=self.generate_frame.grid_forget)
        back_button.pack(padx=150, pady=5, fill='x', expand=True)

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
        self.view_report(year, gpa)

    def view_report(self, year, gpa):
        # Create report frame
        self.report_frame = tk.Frame(self.parent)
        self.report_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

        # Labels
        tk.Label(self.report_frame, text="University of Technology", font=("Helvetica", 10, "bold")).pack()
        tk.Label(self.report_frame, text="Academic Probation Alert GPA Report").pack()
        tk.Label(self.report_frame, text=f"Year: {year}").pack()
        tk.Label(self.report_frame, text=f"GPA: {gpa}").pack(pady=5)

        # Define columns
        columns = ("Student ID", "Student Name", "GPA Semester 1", "GPA Semester 2", "Cumulative GPA")
        column_widths = [100, 200, 200, 200, 150]

        # Update knowledge base
        db_manager.update_knowledge_base(year)

        # Create Treeview
        tree = create_treeview(self.report_frame, columns, column_widths, 60, height=20)

        # Insert data in table
        for results in Prolog.calculate_cumulative_gpa():
            for student in results['Results']:
                student_id, name, email, school, programme, gpa1, gpa2, cumulative_gpa = student
                if not cumulative_gpa == "No GPA calculated" and cumulative_gpa <= gpa:
                    tree.insert("", "end", values=(student_id, name, gpa1, gpa2, cumulative_gpa))
                    # Create a thread for the send_alert function
                    t = threading.Thread(target=send_alert, args=(name, email, school, programme, cumulative_gpa, gpa))
                    t.start()

        close_button = tk.Button(self.report_frame, text="Close", command=self.report_frame.grid_forget)

        # Center the close button at the bottom of the window
        close_button.place(relx=0.5, rely=0.97, anchor='s')
