import tkinter as tk
from datetime import datetime
from tkinter import ttk

from scripts.database.queries import DatabaseManager
from scripts.gui.helpers import Helpers

db_manager = DatabaseManager()  # create an instance of DatabaseManager


class Dialog(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self._first_focus = None
        self._year_field = None
        self._max_year = None
        self._min_year = None
        self._field_name = None
        self.transient(parent)  # Set the parent window
        self.grab_set()  # This makes the dialog modal
        self._module_field = None
        self._semester_field = None
        self._id_field = None
        self._input_field = None
        self._window_height = None
        self._window_width = None
        self._result = None
        self._helpers = Helpers()
        # Padding
        self._x_padding, self._y_padding, self._f_width, self._l_width = 20, 20, 28, 11

    def initialize_properties(self, title, window_width, window_height):
        # Remove the resize and minimize buttons
        self.resizable(False, False)
        self.attributes('-toolwindow', True)

        # Set window title and icon
        self.title(title)

        # Set window size
        self._window_width = window_width
        self._window_height = window_height

        # Get screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate position
        position_top = int(screen_height / 2 - self._window_height / 2)
        position_right = int(screen_width / 2 - self._window_width / 2)

        # Set window size and position
        self.geometry(f"{self._window_width}x{self._window_height}+{position_right}+{position_top}")

    def student_dialog(self, title, submit_action):
        # Initialize window properties
        self.initialize_properties(title, 660, 480)

        # Create the input frame
        self.frame = ttk.Frame(self, padding=[50, 0])
        self.frame.grid(row=0, column=0, sticky="nsew")

        # Student ID label and field
        student_id_field = self._helpers.create_label_and_field(self.frame, "ID Number", 2, f_width=self._f_width + 15)

        # Student Name label and field
        student_name_field = self._helpers.create_label_and_field(self.frame, "Full Name", 3,
                                                                  f_width=self._f_width + 15)

        # Student Email label and field
        student_email_field = self._helpers.create_label_and_field(self.frame, "Email", 4, f_width=self._f_width + 15)

        # School label and field
        ttk.Label(self.frame, text="School", width=self._l_width, anchor="w").grid(row=5, column=0,
                                                                                   pady=self._y_padding)
        school_list = db_manager.get_schools()
        school_names = [school[1] for school in school_list]  # Extract school names
        school_var = tk.StringVar()  # Create a StringVar to hold the school value
        school_field = ttk.Combobox(self.frame, state="readonly", values=school_names, width=self._f_width + 12,
                                    textvariable=school_var, font=('Helvetica', 11, 'normal'))
        school_field.grid(row=5, column=1)

        # Programme label and field
        ttk.Label(self.frame, text="Programme", width=self._l_width, anchor="w").grid(row=6, column=0,
                                                                                      pady=self._y_padding)
        programme_var = tk.StringVar()  # Create a StringVar to hold the programme value
        programme_field = ttk.Combobox(self.frame, state="disabled", values=[], width=self._f_width + 12,
                                       textvariable=programme_var, font=('Helvetica', 11, 'normal'))
        programme_field.grid(row=6, column=1)

        # Advisor label and field
        ttk.Label(self.frame, text="Advisor", width=self._l_width, anchor="w").grid(row=7, column=0,
                                                                                    pady=self._y_padding)
        advisor_list = db_manager.get_advisors()
        advisor_names = [advisor[1] for advisor in advisor_list]  # Extract school names
        advisor_names.append('None')  # Append 'None' to the list
        advisor_field = ttk.Combobox(self.frame, state="readonly", values=advisor_names, width=self._f_width + 12,
                                     font=('Helvetica', 11, 'normal'))
        advisor_field.grid(row=7, column=1)

        # Monitor changes to the school field and update the programme field accordingly
        def update_programmes(*args):
            school = school_var.get()
            if school:
                faculty = school_list[school_names.index(school)][0]  # Get the faculty for the selected school
                programme_field['state'] = 'readonly'  # Enable the programme field
                programme_list = db_manager.get_programmes(faculty)  # Get programmes for the selected school
                programme_names = [programme[1] for programme in programme_list]  # Extract programme names
                programme_var.set('')  # Clear the current programme value
                programme_field['values'] = programme_names  # Update the programme field values
            else:
                programme_field['state'] = 'disabled'  # Disable the programme field
                programme_var.set('')  # Clear the current programme value
                programme_field['values'] = []  # Clear the programme field values

        school_var.trace('w', update_programmes)  # Call update_programmes when the school value changes

        # Create buttons
        self._helpers.create_dialog_buttons(self.frame, [student_id_field,
                                                         student_name_field,
                                                         student_email_field,
                                                         school_field,
                                                         programme_field,
                                                         advisor_field], 8, submit_action, self._helpers.clear_fields,
                                            self.destroy)

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
        mod_code_field = self._helpers.create_label_and_field(self.frame, "Module Code", 2, f_width=self._f_width + 3)

        # Module Name label and field
        mod_name_field = self._helpers.create_label_and_field(self.frame, "Module Name", 3, f_width=self._f_width + 3)

        # Credits label and field
        ttk.Label(self.frame, text="Credits", width=self._l_width, anchor="w").grid(row=4, column=0,
                                                                                    padx=self._x_padding,
                                                                                    pady=self._y_padding)
        mod_credits_field = ttk.Combobox(self.frame, state="readonly", values=["1", "2", "3", "4"],
                                         width=self._f_width, font=('Helvetica', 11, 'normal'))
        mod_credits_field.grid(row=4, column=1)

        # Create buttons
        self._helpers.create_dialog_buttons(self.frame, [mod_code_field, mod_name_field, mod_credits_field], 5,
                                            submit_action,
                                            self._helpers.clear_fields, self.destroy)

        mod_code_field.focus_set()  # Make the entry field focused

        return self.frame, mod_code_field, mod_name_field, mod_credits_field

    def details_dialog(self, title, submit_action):
        # Initialize window properties
        self.initialize_properties(title, 570, 430)

        # Create the input frame
        self.frame = ttk.Frame(self, padding=[20, 0])
        self.frame.grid(row=0, column=0, sticky="nsew")

        # ID number label and field
        ttk.Label(self.frame, text="ID Number", width=self._l_width, anchor="w").grid(row=2, column=0,
                                                                                      padx=self._x_padding,
                                                                                      pady=self._y_padding)
        if title == "Add Details":
            student_list = db_manager.get_students()
            student_ids = [student[0] for student in student_list]  # Extract module codes
            id_field = ttk.Combobox(self.frame, state="readonly", values=student_ids, width=self._f_width + 1,
                                    font=('Helvetica', 11, 'normal'))
            id_field.grid(row=2, column=1)

            # Module label and field
            ttk.Label(self.frame, text="Module", width=self._l_width, anchor="w").grid(row=3, column=0,
                                                                                       padx=self._x_padding,
                                                                                       pady=self._y_padding)
            module_list = db_manager.get_modules()
            module_names = [module[1] for module in module_list]  # Extract module names
            module_field = ttk.Combobox(self.frame, state="readonly", values=module_names,
                                        width=self._f_width + 1, font=('Helvetica', 11, 'normal'))
            module_field.grid(row=3, column=1)
        else:
            id_field = self._helpers.create_label_and_field(self.frame, "ID Number", 2, f_width=self._f_width + 4)
            module_field = self._helpers.create_label_and_field(self.frame, "Module", 3, f_width=self._f_width + 4)

        # Grade Point label and field
        gpa_field = self._helpers.create_label_and_field(self.frame, "GPA", 4, f_width=self._f_width + 4)

        # Semester label and field
        ttk.Label(self.frame, text="Semester", width=self._l_width, anchor="w").grid(row=5, column=0,
                                                                                     padx=self._x_padding,
                                                                                     pady=self._y_padding)
        semester_field = ttk.Combobox(self.frame, state="readonly", values=["1", "2"], width=self._f_width + 1,
                                      font=('Helvetica', 11, 'normal'))
        semester_field.grid(row=5, column=1)

        # Year label and field
        ttk.Label(self.frame, text="Year", width=self._l_width, anchor="w").grid(row=6, column=0, padx=self._x_padding,
                                                                                 pady=self._y_padding)
        current_year = datetime.now().year  # Get the current year
        year_var = tk.StringVar()  # Create a StringVar
        year_var.set("2023")  # Set the default value
        year_field = ttk.Spinbox(self.frame, from_=2000, to=current_year, width=self._f_width - 2,
                                 state="readonly", textvariable=year_var,
                                 font=('Helvetica', 11, 'normal'))  # Associate the StringVar with the Spinbox
        year_field.grid(row=6, column=1, padx=self._x_padding, pady=self._y_padding)

        # Create buttons
        self._helpers.create_dialog_buttons(self.frame, [id_field, gpa_field, module_field, semester_field,
                                                         year_field], 7, submit_action, self._helpers.clear_fields,
                                            self.destroy)

        id_field.focus_set()  # Make the entry field focused

        return self.frame, id_field, module_field, gpa_field, semester_field, year_field, year_var

    def staff_dialog(self, title, submit_action):
        # Initialize window properties
        self.initialize_properties(title, 550, 480)

        # Create the input frame
        self.frame = ttk.Frame(self, padding=[50, 0])
        self.frame.grid(row=0, column=0, sticky="nsew")

        # Staff ID label and field
        id_field = self._helpers.create_label_and_field(self.frame, "ID Number", 2, f_width=self._f_width + 3)

        # Staff Name label and field
        name_field = self._helpers.create_label_and_field(self.frame, "Full Name", 3, f_width=self._f_width + 3)

        # Staff Email label and field
        email_field = self._helpers.create_label_and_field(self.frame, "Email", 4, f_width=self._f_width + 3)

        # Position label and field
        ttk.Label(self.frame, text="Position", width=self._l_width, anchor="w").grid(row=5, column=0,
                                                                                     pady=self._y_padding)
        position_field = ttk.Combobox(self.frame, state="readonly",
                                      values=["Administrator", "Advisor", "Director", "Lecturer", "None"],
                                      width=self._f_width,
                                      font=('Helvetica', 11, 'normal'))
        position_field.grid(row=5, column=1)

        # Username label and field
        username_field = self._helpers.create_label_and_field(self.frame, "Username", 6, f_width=self._f_width + 3)
        username_field.config(state="disabled")  # Disable username field

        # Password label and field
        password_field = self._helpers.create_label_and_field(self.frame, "Password", 7, f_width=self._f_width + 3,
                                                              is_password=True)
        password_field.config(state="disabled")  # Disable password field

        # Create buttons
        self._helpers.create_dialog_buttons(self.frame,
                                            [id_field, name_field, email_field, position_field, username_field,
                                             password_field], 8,
                                            submit_action, self._helpers.clear_fields,
                                            self.destroy)

        id_field.focus_set()  # Make the entry field focused

        # Event handler for position_field
        def on_position_changed(event):
            selected_position = position_field.get()
            if selected_position == "Administrator":
                username_field.config(state="enabled")  # Show username field
                password_field.config(state="enabled")  # Show password field
            else:
                username_field.config(state="disabled")  # Disable username field
                password_field.config(state="disabled")  # Disable password field

        # Bind the event handler to the '<<ComboboxSelected>>' event
        position_field.bind("<<ComboboxSelected>>", on_position_changed)

        return self.frame, id_field, name_field, email_field, position_field, username_field, password_field

    def faculty_dialog(self, title, submit_action):
        # Initialize window properties
        self.initialize_properties(title, 660, 300)

        # Create the input frame
        self.frame = ttk.Frame(self, padding=[15, 0])
        self.frame.grid(row=0, column=0, sticky="nsew")

        # Faculty Code label and field
        code_field = self._helpers.create_label_and_field(self.frame, "Code", 2, f_width=self._f_width + 15)

        # Faculty Name label and field
        name_field = self._helpers.create_label_and_field(self.frame, "Name", 3, f_width=self._f_width + 15)

        # Admin label and field
        ttk.Label(self.frame, text="Administrator", width=self._l_width, anchor="w").grid(row=4, column=0,
                                                                                          padx=self._x_padding,
                                                                                          pady=self._y_padding)
        admin_list = db_manager.get_administrators()
        admin_names = [admin[1] for admin in admin_list]
        admin_names.append('None')  # Append 'None' to the list
        admin_field = ttk.Combobox(self.frame, state="readonly", values=admin_names,
                                   width=self._f_width + 12, font=('Helvetica', 11, 'normal'))
        admin_field.grid(row=4, column=1)

        # Create buttons
        self._helpers.create_dialog_buttons(self.frame, [code_field, name_field, admin_field], 5,
                                            submit_action, self._helpers.clear_fields,
                                            self.destroy)

        code_field.focus_set()  # Make the entry field focused

        return self.frame, code_field, name_field, admin_field

    def school_dialog(self, title, submit_action):
        # Initialize window properties
        self.initialize_properties(title, 680, 300)

        # Create the input frame
        self.frame = ttk.Frame(self, padding=[15, 0])
        self.frame.grid(row=0, column=0, sticky="nsew")

        # School Code label and field
        code_field = self._helpers.create_label_and_field(self.frame, "Code", 2, f_width=self._f_width + 18)

        # School Name label and field
        name_field = self._helpers.create_label_and_field(self.frame, "Name", 3, f_width=self._f_width + 18)

        # Faculty label and field
        ttk.Label(self.frame, text="Faculty", width=self._l_width, anchor="w").grid(row=4, column=0,
                                                                                    padx=self._x_padding,
                                                                                    pady=self._y_padding)
        faculty_list = db_manager.get_faculties()
        faculty_names = [faculty[1] for faculty in faculty_list]
        faculty_names.append('None')  # Append 'None' to the list
        faculty_field = ttk.Combobox(self.frame, state="readonly", values=faculty_names,
                                     width=self._f_width + 15, font=('Helvetica', 11, 'normal'))
        faculty_field.grid(row=4, column=1)

        # Create buttons
        self._helpers.create_dialog_buttons(self.frame, [code_field, name_field, faculty_field], 5,
                                            submit_action, self._helpers.clear_fields,
                                            self.destroy)

        code_field.focus_set()  # Make the entry field focused

        return self.frame, code_field, name_field, faculty_field

    def programme_dialog(self, title, submit_action):
        # Initialize window properties
        self.initialize_properties(title, 660, 360)

        # Create the input frame
        self.frame = ttk.Frame(self, padding=[15, 0])
        self.frame.grid(row=0, column=0, sticky="nsew")

        # Programme Code label and field
        code_field = self._helpers.create_label_and_field(self.frame, "Code", 2, f_width=self._f_width + 15)

        # Programme Name label and field
        name_field = self._helpers.create_label_and_field(self.frame, "Name", 3, f_width=self._f_width + 15)

        # School label and field
        ttk.Label(self.frame, text="School", width=self._l_width, anchor="w").grid(row=4, column=0,
                                                                                   padx=self._x_padding,
                                                                                   pady=self._y_padding)
        school_list = db_manager.get_schools()
        school_names = [school[1] for school in school_list]
        school_names.append('None')  # Append 'None' to the list
        school_field = ttk.Combobox(self.frame, state="readonly", values=school_names,
                                    width=self._f_width + 12, font=('Helvetica', 11, 'normal'))
        school_field.grid(row=4, column=1)

        # Director label and field
        ttk.Label(self.frame, text="Director", width=self._l_width, anchor="w").grid(row=5, column=0,
                                                                                     padx=self._x_padding,
                                                                                     pady=self._y_padding)
        director_list = db_manager.get_directors()
        director_names = [director[1] for director in director_list]
        director_names.append('None')  # Append 'None' to the list
        director_field = ttk.Combobox(self.frame, state="readonly", values=director_names,
                                      width=self._f_width + 12, font=('Helvetica', 11, 'normal'))
        director_field.grid(row=5, column=1)

        # Create buttons
        self._helpers.create_dialog_buttons(self.frame, [code_field, name_field, school_field, director_field], 6,
                                            submit_action, self._helpers.clear_fields,
                                            self.destroy)

        code_field.focus_set()  # Make the entry field focused

        return self.frame, code_field, name_field, school_field, director_field

    def single_input_dialog(self, text, get_func, get_id):
        # Initialize window properties
        self.initialize_properties("Input Required", 500, 150)

        # Create the input frame
        frame = ttk.Frame(self)
        frame.grid(row=0, column=1, sticky="nsew")

        ttk.Label(frame, text=text, width=self._l_width, anchor="w").grid(row=0, column=0, padx=self._x_padding,
                                                                          pady=self._y_padding)
        # Get data
        data_list = get_func()
        # Extract data values
        if get_id:
            data_values = [data[0] for data in data_list]
        else:
            data_values = [data[1] for data in data_list]
        self._input_field = ttk.Combobox(frame, state="readonly", values=data_values, width=self._f_width,
                                         font=('Helvetica', 11, 'normal'))
        self._input_field.grid(row=0, column=1)

        self._field_name = text

        def submit_action():
            self._helpers.validate({self._field_name: (self._input_field, "str")}, self.submit_single, args=False)

        # Submit and Cancel buttons
        button_frame = ttk.Frame(self)
        button_frame.grid(row=1, column=0, columnspan=3)

        # Create the buttons
        self._helpers.create_button_widget(button_frame, "Confirm", submit_action)
        self._helpers.create_button_widget(button_frame, "Cancel", self.destroy)

        # Make the entry field focused
        self._input_field.focus_set()

    def multi_input_dialog(self):
        # Initialize window properties
        self.initialize_properties("Input Required", 500, 340)

        # Create the input frame
        frame = ttk.Frame(self)
        frame.grid(row=0, column=1, sticky="nsew")

        # ID number label and field
        ttk.Label(frame, text="Student ID", width=self._l_width, anchor="w").grid(row=0, column=0, padx=self._x_padding,
                                                                                  pady=self._y_padding)
        student_list = db_manager.get_students()
        student_ids = [student[0] for student in student_list]  # Extract module codes
        self._id_field = ttk.Combobox(frame, state="readonly", values=student_ids, width=self._f_width,
                                      font=('Helvetica', 11, 'normal'))
        self._id_field.grid(row=0, column=1)

        # Module label and field
        ttk.Label(frame, text="Module", width=self._l_width, anchor="w").grid(row=1, column=0, padx=self._x_padding,
                                                                              pady=self._y_padding)
        module_list = db_manager.get_modules()
        module_names = [module[1] for module in module_list]  # Extract module names
        self._module_field = ttk.Combobox(frame, state="readonly", values=module_names, width=self._f_width,
                                          font=('Helvetica', 11, 'normal'))
        self._module_field.grid(row=1, column=1)

        # Semester label and field
        ttk.Label(frame, text="Semester", width=self._l_width, anchor="w").grid(row=2, column=0, padx=self._x_padding,
                                                                                pady=self._y_padding)
        self._semester_field = ttk.Combobox(frame, state="readonly", values=["1", "2"], width=self._f_width,
                                            font=('Helvetica', 11, 'normal'))
        self._semester_field.grid(row=2, column=1)

        # Create year labels and entry fields
        ttk.Label(frame, text="Year", width=self._l_width, anchor="w").grid(row=3, column=0, padx=self._x_padding,
                                                                            pady=self._y_padding)
        year_var = tk.StringVar()  # Create a StringVar
        self._first_focus = True  # Flag to check if it's the first time the Spinbox gets focus
        self._year_field = ttk.Spinbox(frame, width=self._f_width - 4,
                                       state="readonly",
                                       textvariable=year_var,
                                       font=('Helvetica', 11, 'normal'))  # Associate the StringVar with the Spinbox
        self._year_field.grid(row=3, column=1)

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

        def submit_action():
            self._helpers.validate({"ID": (self._id_field, "int"),
                                    "Module": (self._module_field, "str"),
                                    "Semester": (self._semester_field, "int")},
                                   self.submit_multi, args=False)

        # Confirm and Cancel buttons
        button_frame = ttk.Frame(self)
        button_frame.grid(row=3, column=1, columnspan=3)

        # Create the buttons
        self._helpers.create_button_widget(button_frame, "Confirm", submit_action)
        self._helpers.create_button_widget(button_frame, "Cancel", self.destroy)

        # Make the entry field focused
        self._id_field.focus_set()

    def submit_single(self):
        self._result = self._input_field.get()
        self.destroy()

    def submit_multi(self):
        self._result = [str(self._id_field.get()).strip(), str(self._module_field.get()).strip(),
                        str(self._semester_field.get()).strip(), str(self._year_field.get()).strip()]
        self.destroy()

    @property
    def result(self):
        return self._result
