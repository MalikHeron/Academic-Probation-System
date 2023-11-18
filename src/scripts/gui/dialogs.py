import tkinter as tk
from datetime import datetime
from tkinter import ttk

from scripts.database.queries import DatabaseManager
from scripts.gui.helpers import Helpers

db_manager = DatabaseManager()  # create an instance of DatabaseManager


class Dialog(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.module_field = None
        self.semester_field = None
        self.id_field = None
        self.input_field = None
        self.window_height = None
        self.window_width = None
        self.result = None
        self.helpers = Helpers()
        # Padding
        self.x_padding, self.y_padding, self.f_width, self.l_width = 20, 20, 28, 11

    def initialize_properties(self, title, window_width, window_height):
        # Remove the resize and minimize buttons
        self.resizable(False, False)
        self.attributes('-toolwindow', True)

        # Set window title and icon
        self.title(title)

        # Set window size
        self.window_width = window_width
        self.window_height = window_height

        # Get screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate position
        position_top = int(screen_height / 2 - self.window_height / 2)
        position_right = int(screen_width / 2 - self.window_width / 2)

        # Set window size and position
        self.geometry(f"{self.window_width}x{self.window_height}+{position_right}+{position_top}")

    def student_dialog(self, title, submit_action):
        # Initialize window properties
        self.initialize_properties(title, 660, 500)

        # Create the input frame
        self.frame = ttk.Frame(self, padding=[50, 0])
        self.frame.grid(row=0, column=0, sticky="nsew")

        # Student ID label and field
        student_id_field = self.helpers.create_label_and_field(self.frame, "ID Number", 2, f_width=self.f_width + 15)

        # Student Name label and field
        student_name_field = self.helpers.create_label_and_field(self.frame, "Full Name", 3, f_width=self.f_width + 15)

        # Student Email label and field
        student_email_field = self.helpers.create_label_and_field(self.frame, "Email", 4, f_width=self.f_width + 15)

        # School label and field
        ttk.Label(self.frame, text="School", width=self.l_width, anchor="w").grid(row=5, column=0,
                                                                                  pady=self.y_padding)
        school_list = db_manager.get_schools()
        school_names = [school[2] for school in school_list]  # Extract school names
        school_var = tk.StringVar()  # Create a StringVar to hold the school value
        school_field = ttk.Combobox(self.frame, state="readonly", values=school_names, width=self.f_width + 12,
                                    textvariable=school_var, font=('Helvetica', 11, 'normal'))
        school_field.grid(row=5, column=1)

        # Programme label and field
        ttk.Label(self.frame, text="Programme", width=self.l_width, anchor="w").grid(row=6, column=0,
                                                                                     pady=self.y_padding)
        programme_var = tk.StringVar()  # Create a StringVar to hold the programme value
        programme_field = ttk.Combobox(self.frame, state="disabled", values=[], width=self.f_width + 12,
                                       textvariable=programme_var, font=('Helvetica', 11, 'normal'))
        programme_field.grid(row=6, column=1)

        # Advisor label and field
        ttk.Label(self.frame, text="Advisor", width=self.l_width, anchor="w").grid(row=7, column=0,
                                                                                   pady=self.y_padding)
        advisor_list = db_manager.get_advisors()
        advisor_names = [advisor[1] for advisor in advisor_list]  # Extract school names
        advisor_field = ttk.Combobox(self.frame, state="readonly", values=advisor_names, width=self.f_width + 12,
                                     font=('Helvetica', 11, 'normal'))
        advisor_field.grid(row=7, column=1)

        # Monitor changes to the school field and update the programme field accordingly
        def update_programmes(*args):
            school = school_var.get()
            if school:
                faculty = school_list[school_names.index(school)][0]  # Get the faculty for the selected school
                programme_field['state'] = 'readonly'  # Enable the programme field
                programme_list = db_manager.get_programmes(faculty)  # Get programmes for the selected school
                programme_names = [programme[3] for programme in programme_list]  # Extract programme names
                programme_var.set('')  # Clear the current programme value
                programme_field['values'] = programme_names  # Update the programme field values
            else:
                programme_field['state'] = 'disabled'  # Disable the programme field
                programme_var.set('')  # Clear the current programme value
                programme_field['values'] = []  # Clear the programme field values

        school_var.trace('w', update_programmes)  # Call update_programmes when the school value changes

        # Create buttons
        self.helpers.create_dialog_buttons(self.frame, [student_id_field,
                                                        student_name_field,
                                                        student_email_field,
                                                        school_field,
                                                        programme_field,
                                                        advisor_field], 8, submit_action, self.helpers.clear_fields, self.destroy)

        student_id_field.focus_set()  # Make the entry field focused

        return (self.frame, student_id_field, student_name_field, student_email_field, school_field, programme_field,
                advisor_field)

    def module_dialog(self, title, submit_action):
        # Initialize window properties
        self.initialize_properties(title, 560, 300)

        # Create the input frame
        self.frame = ttk.Frame(self, padding=[30, 0])
        self.frame.grid(row=0, column=0, sticky="nsew")

        # Module Code label and field
        mod_code_field = self.helpers.create_label_and_field(self.frame, "Module Code", 2, f_width=self.f_width + 3)

        # Module Name label and field
        mod_name_field = self.helpers.create_label_and_field(self.frame, "Module Name", 3, f_width=self.f_width + 3)

        # Credits label and field
        ttk.Label(self.frame, text="Credits", width=self.l_width, anchor="w").grid(row=4, column=0,
                                                                                   padx=self.x_padding,
                                                                                   pady=self.y_padding)
        mod_credits_field = ttk.Combobox(self.frame, state="readonly", values=["1", "2", "3", "4"],
                                         width=self.f_width - 1, font=('Helvetica', 11, 'normal'))
        mod_credits_field.grid(row=4, column=1)

        # Create buttons
        self.helpers.create_dialog_buttons(self.frame, [mod_code_field, mod_name_field, mod_credits_field], 5, submit_action,
                                           self.helpers.clear_fields, self.destroy)

        mod_code_field.focus_set()  # Make the entry field focused

        return self.frame, mod_code_field, mod_name_field, mod_credits_field

    def details_dialog(self, title, submit_action):
        # Initialize window properties
        self.initialize_properties(title, 570, 450)

        # Create the input frame
        self.frame = ttk.Frame(self, padding=[20, 0])
        self.frame.grid(row=0, column=0, sticky="nsew")

        # ID number label and field
        ttk.Label(self.frame, text="ID Number", width=self.l_width, anchor="w").grid(row=2, column=0,
                                                                                     padx=self.x_padding,
                                                                                     pady=self.y_padding)
        if title == "Add Details":
            student_list = db_manager.get_students()
            student_ids = [student[0] for student in student_list]  # Extract module codes
            id_field = ttk.Combobox(self.frame, state="readonly", values=student_ids, width=self.f_width + 1,
                                    font=('Helvetica', 11, 'normal'))
            id_field.grid(row=2, column=1)

            # Module label and field
            ttk.Label(self.frame, text="Module", width=self.l_width, anchor="w").grid(row=3, column=0,
                                                                                      padx=self.x_padding,
                                                                                      pady=self.y_padding)
            module_list = db_manager.get_modules()
            module_names = [module[1] for module in module_list]  # Extract module names
            module_field = ttk.Combobox(self.frame, state="readonly", values=module_names,
                                        width=self.f_width + 1, font=('Helvetica', 11, 'normal'))
            module_field.grid(row=3, column=1)
        else:
            id_field = self.helpers.create_label_and_field(self.frame, "ID Number", 2, f_width=self.f_width + 4)
            module_field = self.helpers.create_label_and_field(self.frame, "Module", 3, f_width=self.f_width + 4)

        # Grade Point label and field
        gpa_field = self.helpers.create_label_and_field(self.frame, "GPA", 4, f_width=self.f_width + 4)

        # Semester label and field
        ttk.Label(self.frame, text="Semester", width=self.l_width, anchor="w").grid(row=5, column=0,
                                                                                    padx=self.x_padding,
                                                                                    pady=self.y_padding)
        semester_field = ttk.Combobox(self.frame, state="readonly", values=["1", "2"], width=self.f_width + 1,
                                      font=('Helvetica', 11, 'normal'))
        semester_field.grid(row=5, column=1)

        # Year label and field
        ttk.Label(self.frame, text="Year", width=self.l_width, anchor="w").grid(row=6, column=0, padx=self.x_padding,
                                                                                pady=self.y_padding)
        current_year = datetime.now().year  # Get the current year
        year_var = tk.StringVar()  # Create a StringVar
        year_field = ttk.Spinbox(self.frame, from_=2016, to=current_year, width=self.f_width - 2,
                                 state="readonly", textvariable=year_var,
                                 font=('Helvetica', 11, 'normal'))  # Associate the StringVar with the Spinbox
        year_field.grid(row=6, column=1, padx=self.x_padding, pady=self.y_padding)

        # Create buttons
        self.helpers.create_dialog_buttons(self.frame, [id_field, gpa_field, module_field, semester_field,
                                                        year_field], 7, submit_action, self.helpers.clear_fields, self.destroy)

        id_field.focus_set()  # Make the entry field focused

        return self.frame, id_field, gpa_field, module_field, semester_field, year_field, year_var

    def single_input_dialog(self, text):
        # Initialize window properties
        self.initialize_properties("Input Required", 500, 150)

        # Create the input frame
        frame = ttk.Frame(self)
        frame.grid(row=0, column=1, sticky="nsew")

        if text == "Student ID:":
            # ID number label and field
            ttk.Label(frame, text=text, width=self.l_width, anchor="w").grid(row=0, column=0, padx=self.x_padding,
                                                                             pady=self.y_padding)
            student_list = db_manager.get_students()
            student_ids = [student[0] for student in student_list]  # Extract module codes
            self.input_field = ttk.Combobox(frame, state="readonly", values=student_ids, width=self.f_width,
                                            font=('Helvetica', 11, 'normal'))
            self.input_field.grid(row=0, column=1)
        else:
            # Module label and field
            ttk.Label(frame, text=text, width=self.l_width, anchor="w").grid(row=1, column=0, padx=self.x_padding,
                                                                             pady=self.y_padding)
            module_list = db_manager.get_modules()
            module_names = [module[1] for module in module_list]  # Extract module names
            self.input_field = ttk.Combobox(frame, state="readonly", values=module_names, width=self.f_width,
                                            font=('Helvetica', 11, 'normal'))
            self.input_field.grid(row=1, column=1)

        def submit_action():
            if text == "Student ID:":
                self.helpers.validate({"ID": (self.input_field, "int")}, self.submit_single, args=False)
            else:
                self.helpers.validate({"Module": (self.input_field, "str")}, self.submit_single, args=False)

        # Submit and Cancel buttons
        button_frame = ttk.Frame(self)
        button_frame.grid(row=1, column=0, columnspan=3)

        # Create the buttons
        self.helpers.create_button_widget(button_frame, "Confirm", submit_action)
        self.helpers.create_button_widget(button_frame, "Cancel", self.destroy)

        # Make the entry field focused
        self.input_field.focus_set()

    def multi_input_dialog(self):
        # Initialize window properties
        self.initialize_properties("Input Required", 500, 250)

        # Create the input frame
        frame = ttk.Frame(self)
        frame.grid(row=0, column=1, sticky="nsew")

        # ID number label and field
        ttk.Label(frame, text="Student ID", width=self.l_width, anchor="w").grid(row=0, column=0, padx=self.x_padding,
                                                                                 pady=self.y_padding)
        student_list = db_manager.get_students()
        student_ids = [student[0] for student in student_list]  # Extract module codes
        self.id_field = ttk.Combobox(frame, state="readonly", values=student_ids, width=self.f_width,
                                     font=('Helvetica', 11, 'normal'))
        self.id_field.grid(row=0, column=1)

        # Module label and field
        ttk.Label(frame, text="Module", width=self.l_width, anchor="w").grid(row=1, column=0, padx=self.x_padding,
                                                                             pady=self.y_padding)
        module_list = db_manager.get_modules()
        module_names = [module[1] for module in module_list]  # Extract module names
        self.module_field = ttk.Combobox(frame, state="readonly", values=module_names, width=self.f_width,
                                         font=('Helvetica', 11, 'normal'))
        self.module_field.grid(row=1, column=1)

        # Semester label and field
        ttk.Label(frame, text="Semester", width=self.l_width, anchor="w").grid(row=2, column=0, padx=self.x_padding,
                                                                               pady=self.y_padding)
        self.semester_field = ttk.Combobox(frame, state="readonly", values=["1", "2"], width=self.f_width,
                                           font=('Helvetica', 11, 'normal'))
        self.semester_field.grid(row=2, column=1)

        def submit_action():
            self.helpers.validate({"ID": (self.id_field, "int"),
                              "Module": (self.module_field, "str"),
                              "Semester": (self.semester_field, "int")},
                             self.submit_multi, args=False)

        # Confirm and Cancel buttons
        button_frame = ttk.Frame(self)
        button_frame.grid(row=3, column=1, columnspan=3)

        # Create the buttons
        self.helpers.create_button_widget(button_frame, "Confirm", submit_action)
        self.helpers.create_button_widget(button_frame, "Cancel", self.destroy)

        # Make the entry field focused
        self.id_field.focus_set()

    def submit_single(self):
        self.result = self.input_field.get()
        self.destroy()

    def submit_multi(self):
        self.result = [str(self.id_field.get()).strip(), str(self.module_field.get()).strip(),
                       str(self.semester_field.get()).strip()]
        self.destroy()
