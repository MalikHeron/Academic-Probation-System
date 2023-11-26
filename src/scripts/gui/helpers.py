import itertools
import logging
import os
import re
import threading
import time
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk

import sv_ttk
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer


class Helpers:

    def __init__(self):
        self._refresh_button = None
        self._delete_button = None
        self._update_button = None
        self._add_button = None

        # Load the icon and keep it in memory
        self._dark_refresh_icon = tk.PhotoImage(file="../../res/reload-dark.png")
        self._dark_delete_icon = tk.PhotoImage(file="../../res/delete-dark.png")
        self._dark_update_icon = tk.PhotoImage(file="../../res/update-dark.png")
        self._dark_add_icon = tk.PhotoImage(file="../../res/add-dark.png")

        # Load the icon and keep it in memory
        self._light_refresh_icon = tk.PhotoImage(file="../../res/reload-light.png")
        self._light_delete_icon = tk.PhotoImage(file="../../res/delete-light.png")
        self._light_update_icon = tk.PhotoImage(file="../../res/update-light.png")
        self._light_add_icon = tk.PhotoImage(file="../../res/add-light.png")

    @staticmethod
    def create_pdf(data, year, gpa, directory):
        # Get the current date and time
        now = datetime.now()
        # Format the date and time as a string
        now_str = now.strftime("%Y-%m-%d_%H-%M-%S")
        # Append the date and time to the report name
        report_name = f"Report_{now_str}.pdf"
        # Combine the directory and the report name
        path = os.path.join(directory, report_name)

        pdf = SimpleDocTemplate(path, pagesize=letter)
        styles = getSampleStyleSheet()

        # Add headers
        elems = [Paragraph("University of Technology", styles['Title']),
                 Paragraph("<para align=center>Academic Probation Alert GPA Report</para>", styles['Normal']),
                 Paragraph(f"<para align=center>Year: {year}</para>", styles['Normal']),
                 Paragraph(f"<para align=center>GPA: {gpa}</para>", styles['Normal']), Spacer(1, 20)]

        # Create table
        table = Table(data)

        # Add a table style
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),

            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),

            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])
        table.setStyle(style)

        # Add the table to the elements to be added to the PDF
        elems.append(table)

        # Build the PDF
        pdf.build(elems)

        # Return the report name
        return path

    @staticmethod
    def animate(done):
        for c in itertools.cycle(['|', '/', '-', '\\']):
            if done[0]:
                break
            print('\rSending alert... ' + c, end='', flush=True)
            time.sleep(0.1)

    def _sort_column(self, tree, col, reverse):
        column_data = [(tree.set(child_id, col), child_id) for child_id in tree.get_children('')]

        # Check if the column data are digits and sort accordingly
        if all(item[0].isdigit() for item in column_data):
            column_data.sort(key=lambda t: int(t[0]), reverse=reverse)
        else:
            column_data.sort(reverse=reverse)

        # rearrange items in sorted positions
        for index, (val, child_id) in enumerate(column_data):
            tree.move(child_id, '', index)

        # reverse sort next time column is clicked
        tree.heading(col, command=lambda: self._sort_column(tree, col, not reverse))

    @staticmethod
    def search(tree, data, search_text):
        # Remove all items from the tree
        for i in tree.get_children():
            tree.delete(i)

        # Reinsert items that match the search text
        for item in data:
            if search_text.lower() in str(item).lower():
                tree.insert("", "end", values=item)

    @staticmethod
    def create_search_bar(frame):
        # Create a frame for the search bar
        search_frame = ttk.Frame(frame)
        search_frame.pack(fill='x', padx=10, pady=10)
        # Create a search label and entry
        search_label = ttk.Label(search_frame, text="Search:")
        search_label.pack(side=tk.LEFT, padx=(0, 10))
        search_entry = ttk.Entry(search_frame, width=20, font=('Helvetica', 11, 'normal'))
        search_entry.pack(side=tk.LEFT, fill='x', expand=False)

        return search_entry

    def _configure_scrollbar(self, canvas, frame, height, pad_x=0):
        def on_configure(event):
            # Update scroll region after starting 'mainloop'
            # When all widgets are in canvas
            canvas.configure(scrollregion=canvas.bbox('all'))

            # Set second frame's size to canvas's size
            frame.configure(width=event.width)

        canvas.bind('<Configure>', on_configure)

        # Create Treeview in second frame
        tree = ttk.Treeview(frame, show='headings', style="Treeview", height=height)

        # Add a Scrollbar to the Treeview
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        scrollbar.grid(row=0, column=1, sticky='ns', padx=pad_x, pady=10)
        scrollbar.grid_remove()  # Initially hide the scrollbar

        # Update the scrollbar every 100ms
        self._update_scrollbar(tree, scrollbar)

        # Configure the Treeview
        tree.configure(yscrollcommand=scrollbar.set)

        return tree, scrollbar

    def _update_scrollbar(self, tree, scrollbar, height=23, grid=True):
        # Check if the number of items in the tree is greater than the specified height
        if len(tree.get_children()) > height:
            # If grid is True, use the grid method to show the scrollbar
            if grid:
                scrollbar.grid()
            # If grid is False, use the pack method to show the scrollbar
            else:
                scrollbar.pack(side=tk.RIGHT, fill='y')
        else:
            # If the number of items in the tree is not greater than the height, hide the scrollbar
            if grid:
                scrollbar.grid_remove()
            else:
                scrollbar.pack_forget()
        # Call this function again after 100 milliseconds to keep the scrollbar updated
        tree.after(100, lambda: self._update_scrollbar(tree, scrollbar, grid=grid))

    def create_view_table(self, frame, columns, column_widths, column_alignments, remove_func, height=23, data=None,
                          pad_x=0):
        # Create Canvas in new window
        canvas = tk.Canvas(frame)
        canvas.pack(side=tk.LEFT, fill='both', expand=True)

        # Create another frame inside the canvas
        second_frame = ttk.Frame(canvas)

        # Add that new frame to a new window on the canvas
        canvas.create_window((0, 0), window=second_frame, anchor="nw")

        # Configure the scrollbar
        tree, scrollbar = self._configure_scrollbar(canvas, second_frame, height, pad_x)

        # Pack the Treeview into the new frame
        tree.grid(row=0, column=0)

        # Define columns
        tree["columns"] = columns

        # Format columns
        for col, width, align in zip(columns, column_widths, column_alignments):
            tree.column(col, width=width, anchor=align)
            tree.heading(col, text=col, command=lambda _col=col: self._sort_column(tree, _col, False))

        if data is not None:
            # Insert data in table
            for item in data:
                tree.insert("", "end", values=item)

        def delete_record(event):
            logging.info(event)
            remove_func()

        # Bind the function to the Delete key press event
        tree.bind('<Delete>', delete_record)

        return tree

    def create_report_tables(self, frame, columns, column_widths, column_alignments, pad, height=23, data=None):
        # Create Canvas in new window
        canvas = tk.Canvas(frame, takefocus=False)
        canvas.pack(side=tk.LEFT, fill='both', expand=True)

        # Create another frame inside the canvas
        report_frame = ttk.Frame(canvas, takefocus=False)

        # Add that new frame to a new window on the canvas
        canvas.create_window((0, 0), window=report_frame, anchor="ne")

        # Configure the scrollbar
        gpa_tree, gpa_scrollbar = self._configure_scrollbar(canvas, report_frame, height)

        # Define columns
        gpa_tree["columns"] = columns

        # Format columns
        for col, width, align in zip(columns, column_widths, column_alignments):
            gpa_tree.column(col, width=width, anchor=align)
            gpa_tree.heading(col, text=col, command=lambda _col=col: self._sort_column(gpa_tree, _col, False))

        if data is not None:
            # Insert data in table
            for item in data:
                gpa_tree.insert("", "end", values=item)

        # Pack the Treeview into the new frame
        gpa_tree.pack(padx=pad)

        # Create another frame inside the canvas
        pdf_frame = ttk.Frame(canvas, takefocus=False)

        # Create a frame for the Treeview and the Scrollbar
        tree_frame = ttk.Frame(pdf_frame, takefocus=False)

        # Create Treeview in the new frame
        file_tree = ttk.Treeview(tree_frame, show='headings', style="Treeview", height=height)

        # Add a Scrollbar to the Treeview
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=file_tree.yview)

        # Pack the Treeview and the Scrollbar into the new frame
        file_tree.pack(side=tk.LEFT, fill='both', expand=True)
        scrollbar.pack(side=tk.RIGHT, fill='y')
        scrollbar.pack_forget()  # Initially hide the scrollbar

        # Update the scrollbar every 100ms
        self._update_scrollbar(file_tree, scrollbar, grid=False)

        # Configure the Treeview
        file_tree.configure(yscrollcommand=scrollbar.set)

        # Pack the new frame into the pdf_frame
        tree_frame.pack()

        # Add that new frame to a new window on the canvas
        canvas.create_window((0, 0), window=pdf_frame, anchor="nw")

        def on_configure(event):
            # Update scroll region after starting 'mainloop'
            # When all widgets are in canvas
            canvas.configure(scrollregion=canvas.bbox('all'))

            # Set second frame's size to canvas's size
            pdf_frame.configure(width=event.width)

        canvas.bind('<Configure>', on_configure)

        pdf_columns = ("Generated Reports", "Size")
        pdf_widths = [280, 70]
        pdf_alignments = ['w', 'center']

        # Define columns
        file_tree["columns"] = pdf_columns

        # Format columns
        for col, width, align in zip(pdf_columns, pdf_widths, pdf_alignments):
            file_tree.column(col, width=width, anchor=align)
            file_tree.heading(col, text=col, command=lambda _col=col: self._sort_column(file_tree, _col, False))

        # Get all the PDF files from a folder
        folder_path = "../../reports"  # Replace with your folder path
        pdf_files = self.get_pdf_files(folder_path)

        # Store their names in the container as a list
        for pdf_file in pdf_files:
            file_size = self.convert_bytes(os.path.getsize(os.path.join(folder_path, pdf_file)))
            file_tree.insert("", "end", values=(pdf_file, file_size))

        # Open the selected PDF file when clicked
        def open_selected_files(event):
            logging.info(event)
            for selected_item in file_tree.selection():
                self.open_pdf(os.path.join(folder_path, file_tree.item(selected_item)['values'][0]))

        # Bind the function to the treeview double-click event
        file_tree.bind('<Double-1>', open_selected_files)

        # Bind the function to the Enter key press event
        file_tree.bind('<Return>', open_selected_files)

        # Start a thread to update the list in real time
        threading.Thread(target=self._update_pdf_list, args=(folder_path, pdf_files, file_tree),
                         daemon=True).start()

        # Pack the Treeview into the new frame
        file_tree.pack(padx=(30, pad))

        # Create a delete button
        delete_button = ttk.Button(pdf_frame, text="Delete", state="disabled", cursor="hand2", takefocus=False)

        # Function to delete a file
        def delete_file(event):
            logging.info(event)
            selected_items = file_tree.selection()  # get selected items

            if messagebox.askokcancel("Confirm", "Are you sure you want to delete the selected item(s)?"):
                # Delete all selected items
                for selected_item in selected_items:
                    file_path = os.path.join(folder_path, file_tree.item(selected_item)['values'][0])
                    os.remove(file_path)  # remove the file
                    file_tree.delete(selected_item)  # remove item from treeview

        # Update delete button state based on treeview selection
        def update_delete_button(event):
            logging.info(event)
            if file_tree.selection():
                delete_button.config(state="normal")
            else:
                delete_button.config(state="disabled")

        # Bind the function to the treeview select event
        file_tree.bind('<<TreeviewSelect>>', update_delete_button)

        # Bind the function to the Delete key press event
        file_tree.bind('<Delete>', delete_file)

        # Set the command of the delete button to the delete_file function
        delete_button.config(command=lambda: delete_file(None))

        # Pack the delete button into the pdf_frame
        delete_button.pack(padx=(30, pad), pady=(10, 0))

        return gpa_tree

    @staticmethod
    def create_button_widget(frame, text, command, pad_x=5, pady=20, width=10):
        button = ttk.Button(frame, text=text, width=width, command=command, style='TButton', cursor="hand2",
                            takefocus=False)
        button.pack(side="left", padx=pad_x, pady=pady, anchor='center')
        return button

    def create_dialog_buttons(self, frame, fields, row, submit_action, clear_fields, destroy, x_padding=5,
                              y_padding=20):
        # Submit and Cancel buttons
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=row, column=0, columnspan=3, padx=x_padding, pady=y_padding)

        # Create the buttons
        self.create_button_widget(button_frame, "Clear", lambda: clear_fields(*fields))
        self.create_button_widget(button_frame, "Submit", submit_action)
        self.create_button_widget(button_frame, "Cancel", lambda: destroy())

    def create_crud_buttons(self, frame, tree, data_func, add, update, delete, refresh):
        # Create a new frame to hold the buttons
        button_frame = ttk.Frame(frame)

        self._add_button = ttk.Button(button_frame, text="Add", command=add, style='TButton', cursor="hand2",
                                      takefocus=False,
                                      image=self._light_add_icon,
                                      compound=tk.LEFT)
        self._update_button = ttk.Button(button_frame, text="Update", command=lambda: update(), style='TButton',
                                         cursor="hand2",
                                         takefocus=False, image=self._light_update_icon,
                                         compound=tk.LEFT)
        self._delete_button = ttk.Button(button_frame, text="Delete", command=lambda: delete(), style='TButton',
                                         cursor="hand2",
                                         takefocus=False, image=self._light_delete_icon,
                                         compound=tk.LEFT)
        self._refresh_button = ttk.Button(button_frame, text="Refresh", command=lambda: refresh(frame, data_func),
                                          style='TButton',
                                          cursor="hand2", takefocus=False, image=self._light_refresh_icon,
                                          compound=tk.LEFT)
        # Place the buttons
        buttons = [self._add_button, self._update_button, self._delete_button, self._refresh_button]

        # Pack the buttons into the new frame
        for button in buttons:
            button.pack(side=tk.LEFT, padx=10)  # padx adds some space between the buttons

        # Place the new frame at the bottom center of the window
        button_frame.place(relx=0.5, rely=0.98, anchor='s')

        def update_icons():
            current_theme = sv_ttk.get_theme()
            if current_theme == "light":
                self._refresh_button.config(image=self._light_refresh_icon)
                self._delete_button.config(image=self._light_delete_icon)
                self._update_button.config(image=self._light_update_icon)
                self._add_button.config(image=self._light_add_icon)
            elif current_theme == "dark":
                self._refresh_button.config(image=self._dark_refresh_icon)
                self._delete_button.config(image=self._dark_delete_icon)
                self._update_button.config(image=self._dark_update_icon)
                self._add_button.config(image=self._dark_add_icon)

            # Call this function again after 500ms (0.5 second)
            button_frame.after(500, update_icons)

        # Call the function once to start the loop
        update_icons()

        # Initially disable the update button
        self._update_button.config(state='disabled')

        def on_tree_select(event):
            logging.info(event)
            # Enable the update button when only one item is selected
            selected = tree.selection()
            if len(selected) == 1:
                self._update_button.config(state='normal')
                tree.bind('<Control-u>', lambda e: update())
            else:
                self._update_button.config(state='disabled')
                tree.bind('<Control-u>', lambda e: None)

        # Bind the function to the tree's selection event
        tree.bind('<<TreeviewSelect>>', on_tree_select)

        # Bind the functions to the keyboard shortcuts
        tree.bind('<Control-a>', lambda event: add())
        tree.bind('<Control-r>', lambda event: refresh(frame, data_func))
        tree.bind('<Control-d>', lambda event: delete())

    @staticmethod
    def create_label_and_field(frame, text, row, padx=0, pad_y=20, f_width=25, l_width=11, is_password=False):
        ttk.Label(frame, text=text, width=l_width, anchor="w").grid(row=row, column=0, padx=padx, pady=pad_y)

        # Create field
        if is_password:
            field = ttk.Entry(frame, width=f_width, font=('Helvetica', 11, 'normal'), show="*")
        else:
            field = ttk.Entry(frame, width=f_width, font=('Helvetica', 11, 'normal'))
        field.grid(row=row, column=1)

        return field

    # Helper functions
    @staticmethod
    def clear_fields(*fields):
        # Clear all fields and set to default values
        for field in fields:
            if isinstance(field, tk.Text):
                field.delete("1.0", tk.END)
            elif isinstance(field, ttk.Combobox):
                field.set("")
            elif isinstance(field, ttk.Entry):
                field.delete(0, tk.END)
            elif isinstance(field, tk.StringVar):
                field.set("")
            elif isinstance(field, ttk.Spinbox):
                field.delete(0, tk.END)
                field.insert(0, "2016")

    def validate(self, fields, submit_func, dialog=None, destroy=False, args=True):
        validated_fields = {}  # Store the validated fields
        field_widgets = []  # Store the field widgets

        for field_name, (input_field, validation_type) in fields.items():
            try:
                # Get the input value
                input_value = input_field.get()
                field_widgets.append(input_field)  # Add the input field widget to the list
                if validation_type == "int":
                    # Validate as an integer
                    if input_value.isdigit():
                        validated_fields[field_name] = input_value
                    else:
                        raise ValueError("is not a valid integer.")
                elif validation_type == "str":
                    # Validate as a non-empty string
                    if input_value.strip():
                        validated_fields[field_name] = input_value
                    else:
                        raise ValueError("cannot be empty.")
                elif validation_type == "float":
                    # Validate as a decimal number
                    if input_value.replace(".", "", 1).isdigit():
                        if float(input_value) < 0 or float(input_value) > 4:
                            raise ValueError("must be a decimal number between 0 and 4.")
                        validated_fields[field_name] = input_value
                    else:
                        raise ValueError("is not a valid decimal number.")
                elif validation_type == "email":
                    # Validate as an email
                    if re.match(r"[^@]+@[^@]+\.[^@]+", input_value):
                        validated_fields[field_name] = input_value
                    else:
                        raise ValueError("is not a valid email.")
                elif validation_type == "password":
                    if validated_fields["Position"] == "Administrator":
                        if len(input_value) < 8:
                            raise ValueError("must be at least 8 characters long.")
                        if not re.search(r"[0-9]", input_value):
                            raise ValueError("must contain at least one number.")
                        if not re.search(r"[A-Z]", input_value):
                            raise ValueError("must contain at least one uppercase letter.")
                        if not re.search(r"[a-z]", input_value):
                            raise ValueError("must contain at least one lowercase letter.")
                        else:
                            validated_fields[field_name] = input_value
                    else:
                        validated_fields[field_name] = input_value
                elif validation_type == "username":
                    if validated_fields["Position"] == "Administrator":
                        # Validate as a username
                        if len(input_value) >= 4:
                            validated_fields[field_name] = input_value
                        else:
                            raise ValueError("must be at least 4 characters long.")
                    else:
                        validated_fields[field_name] = input_value
                # Add more validation types as needed
                else:
                    # Unknown validation type
                    raise ValueError(f"Unknown validation type for {field_name}.")
            except ValueError as e:
                # If validation fails, show an error message and return
                tk.messagebox.showerror("Error", f"{field_name} {e}")
                return
            except Exception as e:
                # Handle any unexpected errors
                tk.messagebox.showerror("Error", "Failed to validate input.")
                logging.error("An error occurred in validating input:", e)
                return

        if args:
            # If all fields are successfully validated, call the submit function
            success = submit_func(validated_fields)
            # Destroy the dialog if specified
            if success and destroy:
                dialog.destroy()
            elif success:
                self.clear_fields(*field_widgets)
        else:
            submit_func()  # Call the submit function

    # Helper function to convert bytes to a more readable format
    @staticmethod
    def convert_bytes(num):
        """
        this function will convert bytes to MB.... GB... etc
        """
        for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if num < 1024.0:
                return "%3.1f %s" % (num, x)
            num /= 1024.0

    @staticmethod
    def get_pdf_files(folder_path):
        return [f for f in os.listdir(folder_path) if
                os.path.isfile(os.path.join(folder_path, f)) and f.endswith('.pdf')]

    def _update_pdf_list(self, folder_path, pdf_files, tree):
        try:
            new_pdf_files = self.get_pdf_files(folder_path)
            if new_pdf_files != pdf_files:
                # Clear the tree
                tree.delete(*tree.get_children())

                # Update the list of files
                pdf_files = new_pdf_files
                for pdf_file in pdf_files:
                    file_size = self.convert_bytes(os.path.getsize(os.path.join(folder_path, pdf_file)))
                    tree.insert("", "end", values=(pdf_file, file_size))

            # Schedule the next update
            tree.after(1000, self._update_pdf_list, folder_path, pdf_files, tree)  # Update every 1 second
        except Exception as e:
            logging.error(f"An error occurred in updating the PDF list: {e}")

    @staticmethod
    def open_pdf(pdf_file_path):
        try:
            # Open the PDF file when clicked
            os.startfile(pdf_file_path)
        except Exception as e:
            logging.error("An error occurred in opening the PDF file:", e)
