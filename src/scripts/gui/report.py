import logging
import os
import smtplib
import threading
import tkinter as tk
from email.message import EmailMessage
from tkinter import messagebox
from tkinter import ttk
from tkinter.ttk import Progressbar

from scripts.database.queries import DatabaseManager
from scripts.gui.helpers import Helpers
from scripts.prolog_interface import PrologQueryHandler as Prolog

db_manager = DatabaseManager()  # create an instance of DatabaseManager


class Report(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.first_focus = None
        self.min_year = None
        self.max_year = None
        self.generate_button = None
        self.alert_label = None
        self.student_alerts = None
        self.advisor_alerts = None
        self.director_alerts = None
        self.administrator_alerts = None
        self.progressbar = None
        self.generate_frame = None
        self.gpa_field = None
        self.year_field = None
        self.sender = 'academicprobationsystem2023@gmail.com'
        self.password = 'eulp fsbb dore qhza'
        self.helpers = Helpers()
        self.parent = parent
        self.alert_var = tk.StringVar()

    def generate_view(self):
        # Create report frame
        self.generate_frame = ttk.Frame(self.parent)
        self.generate_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

        # Padding
        x_padding, y_padding, f_width, l_width = 20, 20, 20, 11

        # Create button frame
        button_frame = ttk.Frame(self.generate_frame)
        button_frame.pack(fill='x', padx=10, pady=20)

        # Create year labels and entry fields
        year_label = ttk.Label(button_frame, text="Year:")
        year_label.pack(side=tk.LEFT, padx=(0, 10))

        year_var = tk.StringVar()  # Create a StringVar
        self.first_focus = True  # Flag to check if it's the first time the Spinbox gets focus
        self.year_field = ttk.Spinbox(button_frame, width=f_width - 4,
                                      state="readonly",
                                      textvariable=year_var,
                                      font=('Helvetica', 11, 'normal'))  # Associate the StringVar with the Spinbox
        self.year_field.pack(side=tk.LEFT, fill='x', expand=False)

        # Get the range of years
        def get_years():
            years = db_manager.get_years()
            self.min_year = min(years)[0]
            self.max_year = max(years)[0]

            # Update the Spinbox range
            self.year_field.configure(from_=self.min_year, to=self.max_year)

            # Set the value to max year the first time the Spinbox gets focus
            if self.first_focus:
                year_var.set(self.max_year)  # Set the default value
                self.first_focus = False  # Update the flag

            # Call this function again after 500ms (0.5 second)
            self.after(500, get_years)

        get_years()

        # Create gpa labels and entry fields
        ttk.Label(button_frame, text="OR", foreground="#7a7a7a").pack(side=tk.LEFT, padx=(20, 20))

        # Create gpa labels and entry fields
        gpa_label = ttk.Label(button_frame, text="GPA:")
        gpa_label.pack(side=tk.LEFT, padx=(0, 10))
        self.gpa_field = ttk.Entry(button_frame, width=f_width, font=('Helvetica', 11, 'normal'))
        self.gpa_field.pack(side=tk.LEFT, fill='x', expand=False)

        def submit_action():
            self.helpers.validate({"Year": (self.year_field, "int")}, lambda: self.submit(tree), args=False)

        # Create generate button
        self.generate_button = ttk.Button(button_frame, text="Generate", command=submit_action, style='Accent.TButton',
                                          cursor="hand2")
        self.generate_button.pack(side=tk.LEFT, fill='x', expand=False, padx=(10, 0))

        # Define columns
        columns = ("Student ID", "Student Name", "GPA Semester 1", "GPA Semester 2", "Cumulative GPA")
        column_widths = [100, 200, 200, 200, 150]
        column_alignments = ['center', 'w', 'center', 'center', 'center']

        # Create Treeview
        tree = self.helpers.create_report_tables(self.generate_frame, columns, column_widths, column_alignments, 10)

        return self.generate_frame

    def submit(self, tree):
        # Get data
        year = self.year_field.get()
        gpa = self.gpa_field.get()

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

        # show the report
        self.view_report(year, gpa, tree)

    def view_report(self, year, gpa, tree):
        # Update the knowledge base with the given year
        db_manager.update_knowledge_base(year)

        # Clear the existing data in the tree view
        tree.delete(*tree.get_children())

        # Initialize the counter for the number of student alerts to be sent
        self.student_alerts = 0

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
        self.student_alerts += 1

        # Disable the generate button to prevent further requests while processing
        self.generate_button.config(state="disabled")

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
                        "programme": programme}
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
        self.advisor_alerts = len(advisor_students)
        self.director_alerts = len(director_students)
        self.administrator_alerts = len(administrator_students)

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
        if (self.student_alerts > 0 or self.advisor_alerts > 0
                or self.director_alerts > 0 or self.administrator_alerts > 0):
            # Create an alert frame
            alert_frame = ttk.Frame(self.generate_frame)
            alert_frame.place(relx=0.5, rely=0.95, anchor=tk.CENTER)

            # Create a label to display the status of the email alerts
            self.alert_var.set(f"Sending email alerts")
            self.alert_label = ttk.Label(alert_frame, textvariable=self.alert_var)
            self.alert_label.pack(side=tk.LEFT, padx=(0, 10))

            # Create a progress bar to indicate that email alerts are being sent
            self.progressbar = Progressbar(alert_frame, mode='indeterminate')
            self.progressbar.pack(side=tk.LEFT, fill='x', expand=False)
            self.progressbar.start(3)

            # Specify the directory where the report will be saved
            directory = "../../reports/"

            # Create a PDF with the data
            report_name = self.helpers.create_pdf(pdf_data, year, gpa, directory)

            # Check if the file was created successfully
            if os.path.exists(report_name):
                messagebox.showinfo("Success", "Report saved as a PDF successfully.")
            else:
                messagebox.showerror("Error", "Report could not be saved as a PDF.")

    def send_email(self, recipient, subject, body):
        message = EmailMessage()
        message['Subject'] = subject
        message['From'] = self.sender
        message['To'] = self.sender
        message.set_content(body)

        done = [False]
        t = threading.Thread(target=self.helpers.animate, args=(done,))
        t.start()

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.sender, self.password)
            server.send_message(message)
            server.quit()

            done[0] = True
            t.join()  # Wait for the animation thread to finish

            print(f'\rAlert sent to {recipient}', flush=True)
            logging.info(f'Alert sent to {recipient}')

            return True
        except Exception as e:
            logging.error(f'Error sending alert: {e}')
            self._check_alerts_sent("Error sending alerts!", 'red')
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
            self.student_alerts -= 1
            self._check_alerts_sent()

    def send_advisor_alerts(self, advisor, advisor_students, gpa):
        student_list = ""

        for student in advisor_students:
            student_list += f"""
                    Student ID: {student['student_id']} 
                    Name: {student['name']} 
                    Cumulative GPA: {student['cumulative_gpa']} 
                    Programme: {student['programme']}
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
            self.advisor_alerts -= 1
            self._check_alerts_sent()

    def send_director_alerts(self, director, director_students, gpa):
        student_list = ""

        for student in director_students:
            student_list += f"""
                    Student ID: {student['student_id']} 
                    Name: {student['name']} 
                    Cumulative GPA: {student['cumulative_gpa']}
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
            self.advisor_alerts -= 1
            self._check_alerts_sent()

    def send_administrator_alerts(self, administrator, administrator_students, gpa):
        student_list = ""

        for student in administrator_students:
            student_list += f"""
                    Student ID: {student['student_id']} 
                    Name: {student['name']} 
                    Cumulative GPA: {student['cumulative_gpa']} 
                    Programme: {student['programme']}
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
            self.advisor_alerts -= 1
            self._check_alerts_sent()

    def _check_alerts_sent(self, message="Email alerts sent!", color='green'):
        if self.student_alerts == 0:
            self.progressbar.destroy()
            self.alert_var.set(message)
            self.alert_label.config(foreground=color)
            self.generate_button.config(state="normal")
            self.generate_frame.after(2000, self.remove_alerts)

    def remove_alerts(self):
        # Remove the label
        self.alert_var.set("")
