import datetime
import itertools
import logging
import os
import smtplib
import threading
import time
import tkinter as tk
from email.message import EmailMessage
from tkinter import messagebox
from tkinter.ttk import Progressbar

from scripts.database.queries import DatabaseManager
from scripts.gui.helpers import create_treeview, create_pdf
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
        self.button_frame = None
        self.gpa_label = None
        self.year_frame = None
        self.gpa_frame = None
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
        self.generate_frame = tk.Frame(self.parent, padx=60)
        self.generate_frame.grid(row=0, column=1, columnspan=1, sticky="ew")

        # title
        self.title = tk.Label(self.generate_frame, text="Generate Report", font=('Helvetica', 14, 'bold'))
        self.title.configure(foreground='black')
        self.title.pack(padx=20, pady=20, fill='x', expand=True)

        # Year Selector Frame
        self.year_frame = tk.Frame(self.generate_frame)
        self.year_frame.pack(padx=60, pady=10, fill='x', expand=True)
        self.select_year = tk.Label(self.year_frame, text="Select Year:", font=('Helvetica', 12, 'normal'))
        self.select_year.pack(side='left', padx=10)
        current_year = datetime.datetime.now().year  # Get the current year
        self.year_selector = tk.Spinbox(self.year_frame, font=('Helvetica', 11, 'normal'), from_=2016, to=current_year,
                                        width=18)
        self.year_selector.pack(side='left', padx=10)

        # Optional Label
        tk.Label(self.generate_frame, text="OR", font=("Helvetica", 12, "bold"), foreground="#7a7a7a") \
            .pack(padx=80, pady=5, fill='x', expand=True)

        # GPA Entry Frame
        self.gpa_frame = tk.Frame(self.generate_frame)
        self.gpa_frame.pack(padx=60, pady=10, fill='x', expand=True)
        self.gpa_label = tk.Label(self.gpa_frame, text="Enter GPA:", font=('Helvetica', 12, 'normal'))
        self.gpa_label.pack(side='left', padx=10)
        self.gpa_entry = tk.Entry(self.gpa_frame, font=('Helvetica', 11, 'normal'), width=19)
        self.gpa_entry.pack(side='left', padx=18)

        # Submit Button
        self.button_frame = tk.Frame(self.generate_frame)
        self.button_frame.pack(padx=150, pady=30, fill='x', expand=True)
        submit_button = tk.Button(self.button_frame, text="Generate", command=self.submit)
        submit_button.configure(background='#0cb000', foreground='#FFFFFF', font=('Helvetica', 12, 'normal')),
        submit_button.pack(side='left', padx=10)

        # Back Button
        back_button = tk.Button(self.button_frame, text="Back", command=self.generate_frame.grid_forget)
        back_button.configure(font=('Helvetica', 12, 'normal')),
        back_button.pack(side='left', padx=10)

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

        # Show submitted message
        messagebox.showinfo("Summary", f"Requesting students from {year}\nwith a maximum GPA of {gpa}")

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
        tree = create_treeview(self.report_frame, columns, column_widths, 215, height=20)

        # Counter for the number of alerts to be sent
        self.alerts_to_send = 0

        # Get data
        data = [["Student ID", "Student Name", "GPA Semester 1", "GPA Semester 2", "Cumulative GPA"]]

        # Insert data in table
        for results in Prolog.calculate_cumulative_gpa():
            for student in results['Results']:
                student_id, name, email, school_code, programme_code, gpa1, gpa2, cumulative_gpa = student
                if not cumulative_gpa == "No GPA calculated" and cumulative_gpa <= gpa:
                    # Add student to the table
                    tree.insert("", "end", values=(student_id, name, gpa1, gpa2, cumulative_gpa))

                    # Add student to the data list
                    data.append([student_id, name, gpa1, gpa2, cumulative_gpa])

                    # Increment the counter
                    self.alerts_to_send += 1

                    # Get the advisor, director, and administrator for the student's programme and school
                    advisor = db_manager.get_student_advisor(student_id)
                    director = db_manager.get_programme_director(programme_code)
                    administrator = db_manager.get_school_administrator(school_code)

                    # Get the names of the school and programme
                    school = db_manager.get_school_name(school_code)
                    programme = db_manager.get_programme_name(programme_code)

                    # Create a thread for the send_alert function
                    t = threading.Thread(target=self.send_alert,
                                         args=(name, email, school, programme, cumulative_gpa, gpa, advisor,
                                               director, administrator))
                    t.start()

        # If there are alerts to send, show the label and progress bar
        if self.alerts_to_send > 0:
            # Label
            self.alert_var.set(f"Sending alerts")
            self.alert_label = tk.Label(self.report_frame, textvariable=self.alert_var)
            self.alert_label.place(relx=0.25, rely=0.97, anchor='s')

            # Progress bar
            self.progressbar = Progressbar(self.report_frame, mode='indeterminate')
            self.progressbar.place(relx=0.35, rely=0.97, anchor='s')
            self.progressbar.start(3)

        # Specify the directory where the report will be saved
        directory = "../../reports/"

        # Create a PDF with the data
        report_name = create_pdf(data, year, gpa, directory)

        # Check if the file was created successfully
        if os.path.exists(report_name):
            messagebox.showinfo("Success", "Report saved as a PDF successfully.")
        else:
            messagebox.showerror("Error", "Report could not be saved as a PDF.")

        close_button = tk.Button(self.report_frame, text="Close", command=self.report_frame.grid_forget)

        # Center the buttons at the bottom of the window
        close_button.place(relx=0.5, rely=0.98, anchor='s', width=100)

    def send_alert(self, name, email, school, programme, cumulative_gpa, gpa, advisor, director,
                   administrator):
        sender = 'academicprobationsystem2023@gmail.com'
        password = 'eulp fsbb dore qhza'

        # Get the advisor, director, and administrator for the student's programme and school
        _, advisor_name, advisor_email, _ = advisor
        _, director_name, director_email, _ = director
        _, administrator_name, administrator_email, _ = administrator

        student_body = f"""
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
        """

        advisor_body = f"""
            Email: {advisor_email}
            
            Dear {advisor_name},

            I hope this message finds you well. I am writing to inform you that one of your advisees, {name}, has 
            fallen below the required GPA threshold [{gpa}] for this academic term.

            As per our academic probation system, we kindly request your immediate attention to this matter. We 
            believe that your guidance and support can help {name} improve their academic performance.

            Please feel free to reach out if you need any additional information.

            Best regards,
            Academic Probation System
            University of Technology, Jamaica
        """

        director_body = f"""
            Email: {director_email}
        
            Dear {director_name},

            I hope this message finds you well. I am writing to bring to your attention that {name} in {programme}, 
            has fallen below the required GPA threshold [{gpa}] for this academic term.

            As per our academic probation system, we kindly request your immediate attention to this matter. Your 
            intervention and guidance can play a crucial role in helping {name} improve their academic performance.

            Please feel free to reach out if you need any additional information.

            Best regards,
            Academic Probation System
            University of Technology, Jamaica
        """

        administrator_body = f"""
            Email: {administrator_email}
            
            Dear {administrator_name},

            I hope this message finds you well. I am writing to inform you that {name} in {programme}, 
            has fallen below the required GPA threshold [{gpa}] for this academic term.

            As per our academic probation system, we kindly request your immediate attention to this matter. Your 
            administrative support can play a crucial role in helping {name} improve their academic performance.

            Please feel free to reach out if you need any additional information.

            Best regards,
            Academic Probation System
            University of Technology, Jamaica
        """

        # Student message
        student_message = EmailMessage()
        student_message['Subject'] = 'Alert: You are on Academic Probation'
        student_message['From'] = f'{sender}'
        student_message['To'] = f'{sender}'
        student_message.set_content(student_body)

        # Advisor message
        advisor_message = EmailMessage()
        advisor_message['Subject'] = 'Urgent: Student Academic Performance'
        advisor_message['From'] = f'{sender}'
        advisor_message['To'] = f'{sender}'
        advisor_message.set_content(advisor_body)

        # Director message
        director_message = EmailMessage()
        director_message['Subject'] = 'Concern Regarding Student Academic Performance'
        director_message['From'] = f'{sender}'
        director_message['To'] = f'{sender}'
        director_message.set_content(director_body)

        # Administrator message
        administrator_message = EmailMessage()
        administrator_message['Subject'] = 'Notification of Student Academic Performance'
        administrator_message['From'] = f'{sender}'
        administrator_message['To'] = f'{sender}'
        administrator_message.set_content(administrator_body)

        done = [False]
        t = threading.Thread(target=animate, args=(done,))
        t.start()

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender, password)
            server.send_message(student_message)
            server.send_message(advisor_message)
            server.send_message(director_message)
            server.send_message(administrator_message)
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
                # Update the label with a success message in green
                self.alert_var.set("Email alerts sent!")
                self.alert_label.config(fg='green')
                # Schedule the removal of the label
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
