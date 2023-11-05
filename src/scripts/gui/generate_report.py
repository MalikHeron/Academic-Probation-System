import datetime
import itertools
import logging
import smtplib
import threading
import time
import tkinter as tk
from email.message import EmailMessage
from tkinter import messagebox
from tkinter.ttk import Progressbar

from scripts.database.queries import DatabaseManager
from scripts.gui.helpers import create_treeview
from scripts.prolog_interface import PrologQueryHandler as Prolog

db_manager = DatabaseManager()  # create an instance of DatabaseManager


def animate(done):
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done[0]:
            break
        print('\rSending alert... ' + c, end='', flush=True)
        time.sleep(0.1)


class GenerateReportFrame:

    def __init__(self, parent):
        self.alert_label = None
        self.alerts_to_send = None
        self.progressbar = None
        self.select_year = None
        self.generate_frame = None
        self.title = None
        self.gpa_entry = None
        self.year_selector = None
        self.report_frame = None
        self.parent = parent
        self.alert_var = tk.StringVar()
        self.setup_components()

    def setup_components(self):
        # Create report frame
        self.generate_frame = tk.Frame(self.parent)
        self.generate_frame.grid(row=0, column=1, columnspan=1, sticky="ew")

        # title
        self.title = tk.Label(self.generate_frame, text="Generate Report", font=('Arial', 16, 'bold'))
        self.title.configure(foreground='black')
        self.title.pack(padx=20, pady=20, fill='x', expand=True)

        # Year Selector
        current_year = datetime.datetime.now().year  # Get the current year
        self.select_year = tk.Label(self.generate_frame, text="Select Year:", font=('Arial', 12, 'normal'))
        self.select_year.pack(padx=150, anchor="w")
        self.year_selector = tk.Spinbox(self.generate_frame, font=('Arial', 11, 'normal'), from_=2016, to=current_year)
        self.year_selector.pack(padx=150, pady=5, fill='x', expand=True)

        # Optional Label
        tk.Label(self.generate_frame, text="OR", font=("Helvetica", 12, "bold"), foreground="#7a7a7a") \
            .pack(padx=80, pady=5, fill='x', expand=True)

        # GPA Entry
        tk.Label(self.generate_frame, text="Enter GPA:", font=('Arial', 12, 'normal')).pack(padx=150, anchor="w")
        self.gpa_entry = tk.Entry(self.generate_frame, font=('Arial', 11, 'normal'))
        self.gpa_entry.pack(padx=150, pady=5, fill='x', expand=True)

        # spacing
        tk.Label(self.generate_frame, text="", font=('Arial', 12, 'normal')).pack()

        # Submit Button
        submit_button = tk.Button(self.generate_frame, text="Generate", command=self.submit)
        submit_button.configure(background='#0cb000', foreground='#FFFFFF', font=('Arial', 12, 'normal'))
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

        # Counter for the number of alerts to be sent
        self.alerts_to_send = 0

        # Insert data in table
        for results in Prolog.calculate_cumulative_gpa():
            for student in results['Results']:
                student_id, name, email, school, programme, gpa1, gpa2, cumulative_gpa = student
                if not cumulative_gpa == "No GPA calculated" and cumulative_gpa <= gpa:
                    tree.insert("", "end", values=(student_id, name, gpa1, gpa2, cumulative_gpa))
                    # Increment the counter
                    self.alerts_to_send += 1
                    # Create a thread for the send_alert function
                    t = threading.Thread(target=self.send_alert,
                                         args=(name, email, school, programme, cumulative_gpa, gpa))
                    t.start()

        if self.alerts_to_send > 0:
            # Label to show the number of alerts sent
            self.alert_var.set(f"Sending alerts")
            self.alert_label = tk.Label(self.report_frame, textvariable=self.alert_var)
            self.alert_label.place(relx=0.15, rely=0.96, anchor='s')

            # Progress bar
            self.progressbar = Progressbar(self.report_frame, mode='determinate')
            self.progressbar.place(relx=0.3, rely=0.96, anchor='s')
            self.progressbar.start(3)

        # Close button
        close_button = tk.Button(self.report_frame, text="Close", command=self.report_frame.grid_forget)
        close_button.place(relx=0.5, rely=0.97, anchor='s')

    def send_alert(self, name, email, school, programme, cumulative_gpa, gpa):
        sender = 'academicprobationsystem2023@gmail.com'
        password = 'eulp fsbb dore qhza'

        message = EmailMessage()
        message['Subject'] = 'Alert: You are on Academic Probation'
        message['From'] = f'{sender}'
        message['To'] = f'{sender}'
        message.set_content(f"""
            Email: {email}
            Programme: {programme}
            School: {school}
    
            Dear {name},
        
            We hope this message finds you well. This email is to inform you that your recent GPA [{cumulative_gpa}]
            has fallen below the required threshold [{gpa}] and you are now on academic probation.
        
            Academic probation is a serious matter. It is a signal that you may need to make significant changes to 
            meet the academic standards required to continue at our institution. However, it's important to remember 
            that this is not a permanent status, and many students have successfully returned to good standing after 
            a period of probation.
        
            Here are some steps you can take:
            
            1. Meet with your academic advisor: They can provide guidance on course selection, study strategies, 
            and connecting with campus resources. 
            
            2. Utilize campus resources: This includes tutoring centers, writing workshops, and counseling services. 
            
            3. Reflect on your habits: Consider if changes need to be made in your study habits, time management, 
            or course load.
            
            Remember, this is a time for action and improvement. It's important to take advantage of the resources 
            available to you and to communicate regularly with your advisor.
            
            Please do not hesitate to reach out if you have any questions or need further clarification about the 
            implications of being on academic probation.
            
            Best Regards,
            Academic Probation System
            University of Technology, Jamaica
        """)

        done = [False]
        t = threading.Thread(target=animate, args=(done,))
        t.start()

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender, password)
            server.send_message(message)
            server.quit()

            done[0] = True
            t.join()  # Wait for the animation thread to finish

            print(f'\rAlert sent to {email}', flush=True)
            logging.info(f'Alert sent to {email}')

            # Decrement the counter
            self.alerts_to_send -= 1

            # If all alerts have been sent, update the label and remove the progress bar
            if self.alerts_to_send == 0:
                # Destroy the progress bar
                self.progressbar.destroy()
                # Update the label
                self.alert_var.set("Email alerts sent!")
                # Change the color of the label to green
                self.alert_label.config(fg='green')
                # Schedule the removal of the label and progress bar
                self.report_frame.after(2000, self.remove_alerts)  # 2000 milliseconds = 2 seconds
        except Exception as e:
            logging.error(f'Error sending alert: {e}')
            # Destroy the progress bar
            self.progressbar.destroy()
            # Update the label with a failure message in red
            self.alert_var.set(f"Error sending email alerts!")
            self.alert_label.config(fg='red')

    def remove_alerts(self):
        # Remove the label
        self.alert_var.set("")
