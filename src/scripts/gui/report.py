import logging
import os
import smtplib
import threading
import tkinter as tk
from email.message import EmailMessage
from tkinter import messagebox
from tkinter import ttk
from tkinter.ttk import Progressbar

from dotenv import load_dotenv

from scripts.database.queries import DatabaseManager
from scripts.gui.helpers import Helpers
from scripts.prolog_interface import PrologQueryHandler as Prolog

db_manager = DatabaseManager()  # create an instance of DatabaseManager
load_dotenv('../.env')


class Report(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self._first_focus = None
        self._min_year = None
        self._max_year = None
        self._generate_button = None
        self._alert_label = None
        self._student_alerts = None
        self._advisor_alerts = None
        self._director_alerts = None
        self._administrator_alerts = None
        self._progressbar = None
        self._generate_frame = None
        self._gpa_field = None
        self._year_field = None
        self._sender = os.getenv('EMAIL')  # get the sender's email address
        self._password = os.getenv('PASSWORD')  # get the sender's password
        self._helpers = Helpers()
        self._parent = parent
        self._alert_var = tk.StringVar()

    def generate_view(self):
        # Create report frame
        self._generate_frame = ttk.Frame(self._parent)
        self._generate_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

        # Padding
        x_padding, y_padding, f_width, l_width = 20, 20, 20, 11

        # Create button frame
        button_frame = ttk.Frame(self._generate_frame)
        button_frame.pack(fill='x', padx=10, pady=20)

        # Create year labels and entry fields
        year_label = ttk.Label(button_frame, text="Year:")
        year_label.pack(side=tk.LEFT, padx=(0, 10))

        year_var = tk.StringVar()  # Create a StringVar
        self._first_focus = True  # Flag to check if it's the first time the Spinbox gets focus
        self._year_field = ttk.Spinbox(button_frame, width=f_width - 4,
                                       state="readonly",
                                       textvariable=year_var,
                                       font=('Helvetica', 11, 'normal'))  # Associate the StringVar with the Spinbox
        self._year_field.pack(side=tk.LEFT, fill='x', expand=False)

        # Get the range of years
        def get_years():
            years = db_manager.get_years()
            self._min_year = min(years)[0]
            self._max_year = max(years)[0]

            # Update the Spinbox range
            self._year_field.configure(from_=self._min_year, to=self._max_year)

            # Set the value to max year the first time the Spinbox gets focus
            if self._first_focus:
                year_var.set(self._max_year)  # Set the default value
                self._first_focus = False  # Update the flag

            # Call this function again after 500ms (0.5 second)
            self.after(500, get_years)

        get_years()

        # Create gpa labels and entry fields
        ttk.Label(button_frame, text="OR", foreground="#7a7a7a").pack(side=tk.LEFT, padx=(20, 20))

        # Create gpa labels and entry fields
        gpa_label = ttk.Label(button_frame, text="GPA:")
        gpa_label.pack(side=tk.LEFT, padx=(0, 10))
        self._gpa_field = ttk.Entry(button_frame, width=f_width, font=('Helvetica', 11, 'normal'))
        self._gpa_field.pack(side=tk.LEFT, fill='x', expand=False)

        def submit_action():
            year = self._year_field.get()
            gpa = self._gpa_field.get()

            # Validate the input
            if gpa != "":
                # Update the default GPA
                Prolog.update_gpa(gpa)
                self._helpers.validate({"Year": (self._year_field, "int"), "GPA": (self._gpa_field, "float")},
                                       lambda: self._view_report(year, float(gpa), tree),
                                       args=False)
            else:
                # Get the default GPA
                gpa = Prolog.get_default_gpa()
                self._helpers.validate({"Year": (self._year_field, "int")},
                                       lambda: self._view_report(year, float(gpa), tree),
                                       args=False)

        # Create generate button
        self._generate_button = ttk.Button(button_frame, text="Generate", command=submit_action, style='Accent.TButton',
                                           cursor="hand2")
        self._generate_button.pack(side=tk.LEFT, fill='x', expand=False, padx=(10, 0))

        # Define columns
        columns = ("Student ID", "Student Name", "GPA Semester 1", "GPA Semester 2", "Cumulative GPA")
        column_widths = [100, 200, 200, 200, 150]
        column_alignments = ['center', 'w', 'center', 'center', 'center']

        # Create Treeview
        tree = self._helpers.create_report_tables(self._generate_frame, columns, column_widths, column_alignments, 10)

        return self._generate_frame

    def _view_report(self, year, gpa, tree):
        # Show submitted message
        messagebox.showinfo("Summary", f"Requesting students from {year}\nwith a maximum GPA of {gpa}")

        # Update the knowledge base with the given year
        db_manager.update_knowledge_base(year)

        # Clear the existing data in the tree view
        tree.delete(*tree.get_children())

        # Initialize the counter for the number of student alerts to be sent
        self._student_alerts = 0

        # Initialize the data for the PDF report
        pdf_data = [["Student ID", "Student Name", "GPA Semester 1", "GPA Semester 2", "Cumulative GPA"]]

        # Initialize dictionaries to store data for each type of alert
        (advisor_students, director_students, administrator_students,
         advisors, directors, administrators) = self._initialize_dictionaries()

        # Iterate over the results of the cumulative GPA calculation
        for results in Prolog.calculate_cumulative_gpa():
            for student in results['Results']:
                student_id, name, email, school_code, programme_code, gpa1, gpa2, cumulative_gpa = student
                if cumulative_gpa != "No GPA calculated" and cumulative_gpa <= gpa:
                    # Process each student who meets the criteria
                    self._process_student(student_id, name, email, school_code, programme_code, gpa1, gpa2,
                                          cumulative_gpa, gpa, tree, pdf_data, advisor_students, director_students,
                                          administrator_students, advisors, directors, administrators)

        # Send alerts to advisors, directors, and administrators
        self._send_alerts(advisor_students, director_students, administrator_students, advisors, directors,
                          administrators, gpa)

        # Create the PDF report and show alerts if necessary
        self._create_pdf_and_show_alerts(pdf_data, year, gpa)

    @staticmethod
    def _initialize_dictionaries():
        # Initialize empty dictionaries for storing data
        return {}, {}, {}, {}, {}, {}

    def _process_student(self, student_id, name, email, school_code, programme_code, gpa1, gpa2, cumulative_gpa, gpa,
                         tree, pdf_data, advisor_students, director_students, administrator_students, advisors,
                         directors, administrators):
        # Add the student's data to the tree view
        tree.insert("", "end", values=(student_id, name, gpa1, gpa2, cumulative_gpa))

        # Add the student's data to the PDF data
        pdf_data.append([student_id, name, gpa1, gpa2, cumulative_gpa])

        # Increment the counter for student alerts
        self._student_alerts += 1

        # Disable the generate button to prevent further requests while processing
        self._generate_button.config(state="disabled")

        # Get the advisor, director, and administrator for the student's programme and school
        advisor = db_manager.get_student_advisor(student_id)
        director = db_manager.get_programme_director(programme_code)
        administrator = db_manager.get_school_administrator(school_code)

        # Get the names of the school and programme
        school = db_manager.get_school_name(school_code)
        programme = db_manager.get_programme_name(programme_code)

        # Get the details of the advisor, director, and administrator
        advisor_id, advisor_name, advisor_email, _ = self._handle_none(advisor)
        director_id, director_name, director_email, _ = self._handle_none(director)
        administrator_id, administrator_name, administrator_email, _ = self._handle_none(administrator)

        # Initialize the dictionaries if the advisor, director, and administrator are not already in the dictionaries
        advisor_students.setdefault(advisor_id, [])
        director_students.setdefault(director_id, [])
        administrator_students.setdefault(administrator_id, [])
        advisors.setdefault(advisor_id, [])
        directors.setdefault(director_id, [])
        administrators.setdefault(administrator_id, [])

        # Add the advisor, director, and administrator to the dictionaries
        advisors[advisor_id].append({"name": advisor_name, "email": advisor_email})
        directors[director_id].append({"name": director_name, "email": director_email, "programme": programme})
        administrators[administrator_id].append(
            {"name": administrator_name, "email": administrator_email, "school": school})

        # Add the student's data to the dictionaries
        student_data = {"student_id": student_id, "name": name, "cumulative_gpa": cumulative_gpa,
                        "programme": programme, "school": school}
        advisor_students[advisor_id].append(student_data)
        director_students[director_id].append(student_data.copy())
        administrator_students[administrator_id].append({**student_data, "school": school})

        # Create a new thread to send an alert to the student
        t = threading.Thread(target=self.send_student_alert, args=(name, email, school, programme, cumulative_gpa, gpa))
        t.start()

    @staticmethod
    def _handle_none(person):
        # Return a tuple of empty strings if the person is None, otherwise return the person
        return ('', 'None', 'None', '') if person is None else person

    def _send_alerts(self, advisor_students, director_students, administrator_students, advisors, directors,
                     administrators, gpa):
        # Set the counters for the number of alerts to be sent
        self._advisor_alerts = len(advisor_students)
        self._director_alerts = len(director_students)
        self._administrator_alerts = len(administrator_students)

        # Create new threads to send alerts to advisors, directors, and administrators
        for advisor_id, advisor in advisors.items():
            t = threading.Thread(target=self.send_advisor_alerts, args=(advisor[0], advisor_students[advisor_id], gpa))
            t.start()

        for director_id, director in directors.items():
            t = threading.Thread(target=self.send_director_alerts,
                                 args=(director[0], director_students[director_id], gpa))
            t.start()

        for administrator_id, administrator in administrators.items():
            t = threading.Thread(target=self.send_administrator_alerts,
                                 args=(administrator[0], administrator_students[administrator_id], gpa))
            t.start()

    def _create_pdf_and_show_alerts(self, pdf_data, year, gpa):
        # If there are alerts to send, show the label and progress bar and create the PDF
        if (self._student_alerts > 0 or self._advisor_alerts > 0
                or self._director_alerts > 0 or self._administrator_alerts > 0):
            # Create an alert frame
            alert_frame = ttk.Frame(self._generate_frame)
            alert_frame.place(relx=0.5, rely=0.95, anchor=tk.CENTER)

            # Create a label to display the status of the email alerts
            self._alert_var.set(f"Sending email alerts")
            self._alert_label = ttk.Label(alert_frame, textvariable=self._alert_var)
            self._alert_label.pack(side=tk.LEFT, padx=(0, 10))

            # Create a progress bar to indicate that email alerts are being sent
            self._progressbar = Progressbar(alert_frame, mode='indeterminate')
            self._progressbar.pack(side=tk.LEFT, fill='x', expand=False)
            self._progressbar.start(3)

            # Specify the directory where the report will be saved
            directory = "../../reports/"

            # Create a PDF with the data
            report_name = self._helpers.create_pdf(pdf_data, year, gpa, directory)

            # Check if the file was created successfully
            if os.path.exists(report_name):
                messagebox.showinfo("Success", "Report saved as a PDF successfully.")
            else:
                messagebox.showerror("Error", "Report could not be saved as a PDF.")

    def send_email(self, recipient, subject, body):
        message = EmailMessage()
        message['Subject'] = subject
        message['From'] = self._sender
        message['To'] = self._sender  # recipient
        message.set_content(body)

        done = [False]
        t = threading.Thread(target=self._helpers.animate, args=(done,))
        t.start()

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self._sender, self._password)
            server.send_message(message)
            server.quit()

            done[0] = True
            t.join()  # Wait for the animation thread to finish

            print(f'\rAlert sent to {recipient}', flush=True)
            logging.info(f'Alert sent to {recipient}')

            return True
        except Exception as e:
            done[0] = True
            t.join()  # Wait for the animation thread to finish
            print(f'\rFailed to send alert to {recipient}', flush=True)
            logging.error(f'Failed to send alert to {recipient}: {e}')
            self._check_alerts_sent("One or more alerts failed to send", 'red')
            return False

    def send_student_alert(self, name, email, school, programme, cumulative_gpa, gpa):
        body = f"""
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

        subject = 'Alert: You are on Academic Probation'
        if self.send_email(email, subject, body):
            self._student_alerts -= 1
            self._check_alerts_sent()

    def send_advisor_alerts(self, advisor, advisor_students, gpa):
        student_list = ""

        for student in advisor_students:
            student_list += f"""
                    Student ID: {student['student_id']} 
                    Name: {student['name']} 
                    Cumulative GPA: {student['cumulative_gpa']} 
                    Programme: {student['programme']}
                    School: {student['school']}
                """

        body = f"""
                Email: {advisor['email']}
                
                Dear {advisor['name']},
    
                I hope this message finds you well. I am writing to inform you that some of your advisees, have 
                fallen below the required GPA threshold [{gpa}] for this academic term.
    
                As per our academic probation system, we kindly request your immediate attention to this matter. We 
                believe that your guidance and support can help them improve their academic performance.
                
                The list of students are as follows:
                {student_list}
                Please feel free to reach out if you need any additional information.
    
                Best regards,
                Academic Probation System
                University of Technology, Jamaica
            """

        subject = 'Urgent: Student Academic Performance'
        if self.send_email(advisor['email'], subject, body):
            self._advisor_alerts -= 1
            self._check_alerts_sent()

    def send_director_alerts(self, director, director_students, gpa):
        student_list = ""

        for student in director_students:
            student_list += f"""
                    Student ID: {student['student_id']} 
                    Name: {student['name']} 
                    Cumulative GPA: {student['cumulative_gpa']}
                    Programme: {student['programme']}
                    School: {student['school']}
                """

        body = f"""
                Email: {director['email']}
                
                Dear {director['name']},
    
                I hope this message finds you well. I am writing to bring to your attention that some students in
                {director['programme']}, have fallen below the required GPA threshold [{gpa}] for this academic term.
    
                As per our academic probation system, we kindly request your immediate attention to this matter. We 
                believe that your guidance and support can help them improve their academic performance.
                
                The list of students are as follows:
                {student_list}
                Please feel free to reach out if you need any additional information.
    
                Best regards,
                Academic Probation System
                University of Technology, Jamaica
            """

        subject = 'Concern Regarding Student Academic Performance'
        if self.send_email(director['email'], subject, body):
            self._director_alerts -= 1
            self._check_alerts_sent()

    def send_administrator_alerts(self, administrator, administrator_students, gpa):
        student_list = ""

        for student in administrator_students:
            student_list += f"""
                    Student ID: {student['student_id']} 
                    Name: {student['name']} 
                    Cumulative GPA: {student['cumulative_gpa']} 
                    Programme: {student['programme']}
                    School: {student['school']}
                """

        body = f"""
                Email: {administrator['email']}
                
                Dear {administrator['name']},
    
                I hope this message finds you well. I am writing to inform you that some student in the 
                {administrator['school']}, have fallen below the required GPA threshold [{gpa}] for this academic term.
    
                As per our academic probation system, we kindly request your immediate attention to this matter. We 
                believe that your guidance and support can help them improve their academic performance.
                
                The list of students are as follows:
                {student_list}
                Please feel free to reach out if you need any additional information.
    
                Best regards,
                Academic Probation System
                University of Technology, Jamaica
            """

        subject = 'Notification of Student Academic Performance'
        if self.send_email(administrator['email'], subject, body):
            self._administrator_alerts -= 1
            self._check_alerts_sent()

    def _check_alerts_sent(self, message="Email alerts sent!", color='green'):
        if ((self._student_alerts and self._advisor_alerts and self._director_alerts and self._administrator_alerts)
                == 0 or (color == 'red' and message == 'One or more alerts failed to send')):
            self._progressbar.destroy()
            self._alert_var.set(message)
            self._alert_label.config(foreground=color)
            self._generate_button.config(state="normal")
            self._generate_frame.after(5000, self._remove_alerts)

    def _remove_alerts(self):
        # Remove the label
        self._alert_var.set("")

# Send emails in batch eg; to 5 students at a time
