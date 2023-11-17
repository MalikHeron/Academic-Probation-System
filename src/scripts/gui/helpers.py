import itertools
import logging
import os
import threading
import time
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer


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


def animate(done):
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done[0]:
            break
        print('\rSending alert... ' + c, end='', flush=True)
        time.sleep(0.1)


def sort_column(tree, col, reverse):
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
    tree.heading(col, command=lambda: sort_column(tree, col, not reverse))


def search(tree, data, search_text):
    # Remove all items from the tree
    for i in tree.get_children():
        tree.delete(i)

    # Reinsert items that match the search text
    for item in data:
        if search_text.lower() in str(item).lower():
            tree.insert("", "end", values=item)


def create_treeview(frame, columns, column_widths, column_alignments, pad, height=23, data=None, searchable=True,
                    padx=0):
    # Create a style
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))

    # Create Canvas in new window
    canvas = tk.Canvas(frame)
    canvas.pack(side=tk.LEFT, fill='both', expand=True)

    # Create another frame inside the canvas
    second_frame = ttk.Frame(canvas)

    # Add that new frame to a new window on the canvas
    canvas.create_window((0, 0), window=second_frame, anchor="nw")

    if searchable:
        # Create search bar
        search_frame = ttk.Frame(second_frame)
        search_frame.pack(fill='x', padx=pad, pady=10)
        search_label = ttk.Label(search_frame, text="Search:")
        search_label.pack(side=tk.LEFT, padx=(0, 10))
        search_entry = ttk.Entry(search_frame, width=20)
        search_entry.pack(side=tk.LEFT, fill='x', expand=False)

        # Update search function whenever search text is changed
        search_entry.bind('<KeyRelease>', lambda event: search(tree, data, search_entry.get()))

    def on_configure(event):
        # Update scroll region after starting 'mainloop'
        # When all widgets are in canvas
        canvas.configure(scrollregion=canvas.bbox('all'))

        # Set second frame's size to canvas's size
        second_frame.configure(width=event.width)

    canvas.bind('<Configure>', on_configure)

    # Create Treeview in second frame
    tree = ttk.Treeview(second_frame, show='headings', style="Treeview", height=height)

    # Add a Scrollbar to the Treeview
    scrollbar = ttk.Scrollbar(second_frame, orient="vertical", command=tree.yview)
    scrollbar.pack(side=tk.RIGHT, fill='y', padx=(padx), pady=10)

    # Configure the Treeview
    tree.configure(yscrollcommand=scrollbar.set)

    # Define columns
    tree["columns"] = columns

    # Format columns
    for col, width, align in zip(columns, column_widths, column_alignments):
        tree.column(col, width=width, anchor=align)
        tree.heading(col, text=col, command=lambda _col=col: sort_column(tree, _col, False))

    if data is not None:
        # Insert data in table
        for item in data:
            tree.insert("", "end", values=item)

    tree.pack(padx=pad)

    return tree


def create_report_treeview(frame, columns, column_widths, column_alignments, pad, height=23, data=None):
    # Create a style
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))

    # Create Canvas in new window
    canvas = tk.Canvas(frame)
    canvas.pack(side=tk.LEFT, fill='both', expand=True)

    # Create another frame inside the canvas
    report_frame = ttk.Frame(canvas)

    # Add that new frame to a new window on the canvas
    canvas.create_window((0, 0), window=report_frame, anchor="ne")

    def on_configure(event):
        # Update scroll region after starting 'mainloop'
        # When all widgets are in canvas
        canvas.configure(scrollregion=canvas.bbox('all'))

        # Set second frame's size to canvas's size
        report_frame.configure(width=event.width)

    canvas.bind('<Configure>', on_configure)

    # Create Treeview in second frame
    gpa_tree = ttk.Treeview(report_frame, show='headings', style="Treeview", height=height)

    # Add a Scrollbar to the Treeview
    scrollbar = ttk.Scrollbar(report_frame, orient="vertical", command=gpa_tree.yview)
    scrollbar.pack(side=tk.RIGHT, fill='y')

    # Configure the Treeview
    gpa_tree.configure(yscrollcommand=scrollbar.set)

    # Define columns
    gpa_tree["columns"] = columns

    # Format columns
    for col, width, align in zip(columns, column_widths, column_alignments):
        gpa_tree.column(col, width=width, anchor=align)
        gpa_tree.heading(col, text=col, command=lambda _col=col: sort_column(gpa_tree, _col, False))

    if data is not None:
        # Insert data in table
        for item in data:
            gpa_tree.insert("", "end", values=item)

    gpa_tree.pack(padx=pad)

    # Create another frame inside the canvas
    pdf_frame = ttk.Frame(canvas)

    # Add that new frame to a new window on the canvas
    canvas.create_window((0, 0), window=pdf_frame, anchor="nw")

    def on_configure(event):
        # Update scroll region after starting 'mainloop'
        # When all widgets are in canvas
        canvas.configure(scrollregion=canvas.bbox('all'))

        # Set second frame's size to canvas's size
        pdf_frame.configure(width=event.width)

    canvas.bind('<Configure>', on_configure)

    # Create Treeview in second frame
    file_tree = ttk.Treeview(pdf_frame, show='headings', style="Treeview", height=height)

    # Add a Scrollbar to the Treeview
    scrollbar = ttk.Scrollbar(pdf_frame, orient="vertical", command=file_tree.yview)
    scrollbar.pack(side=tk.RIGHT, fill='y')

    # Configure the Treeview
    file_tree.configure(yscrollcommand=scrollbar.set)

    pdf_columns = ("Generated Reports", "Size")
    pdf_widths = [280, 70]
    pdf_alignments = ['w', 'center']

    # Define columns
    file_tree["columns"] = pdf_columns

    # Format columns
    for col, width, align in zip(pdf_columns, pdf_widths, pdf_alignments):
        file_tree.column(col, width=width, anchor=align)
        file_tree.heading(col, text=col, command=lambda _col=col: sort_column(file_tree, _col, False))

    # Get all the PDF files from a folder
    folder_path = "../../reports"  # Replace with your folder path
    pdf_files = get_pdf_files(folder_path)

    # Store their names in the container as a list
    for pdf_file in pdf_files:
        file_size = convert_bytes(os.path.getsize(os.path.join(folder_path, pdf_file)))
        file_tree.insert("", "end", values=(pdf_file, file_size))

    # Open the selected PDF file when clicked
    def open_selected_files(event):
        for selected_item in file_tree.selection():
            open_pdf(os.path.join(folder_path, file_tree.item(selected_item)['values'][0]))

    # Bind the function to the treeview double-click event
    file_tree.bind('<Double-1>', open_selected_files)

    # Bind the function to the Enter key press event
    file_tree.bind('<Return>', open_selected_files)

    # Start a thread to update the list in real time
    threading.Thread(target=update_pdf_list, args=(folder_path, pdf_files, file_tree),
                     daemon=True).start()

    file_tree.pack(padx=(30, pad))

    return gpa_tree


def create_button(frame, text, command):
    # Create a button with the new style
    button = ttk.Button(frame, text=text, width=50, command=command, style='TButton')
    button.pack(side="top", padx=0, pady=5, anchor='center')
    return button


def create_button_widget(frame, text, command, pad_x=5, pad_y=20, width=10):
    button = ttk.Button(frame, text=text, width=width, command=command, style='TButton')
    button.pack(side="left", padx=pad_x, pady=pad_y, anchor='center')
    return button


def create_buttons(frame, fields, row, submit_action, clear_fields, close_view, x_padding=5, y_padding=20):
    # Submit and Cancel buttons
    button_frame = ttk.Frame(frame)
    button_frame.grid(row=row, column=0, columnspan=3, padx=x_padding, pady=y_padding)

    # Create the buttons
    create_button_widget(button_frame, "Clear", lambda: clear_fields(*fields))
    create_button_widget(button_frame, "Submit", submit_action)
    create_button_widget(button_frame, "Close", lambda: close_view())


def button_config(frame, tree, data_func, add, update, remove, refresh):
    add_button = ttk.Button(frame, text="Add", command=add, style='TButton')
    update_button = ttk.Button(frame, text="Update", command=lambda: update(), style='TButton')
    remove_button = ttk.Button(frame, text="Remove", command=lambda: remove(), style='TButton')
    refresh_button = ttk.Button(frame, text="Refresh", command=lambda: refresh(frame, data_func), style='TButton')

    # Initially disable the update button
    update_button.config(state='disabled')

    def on_tree_select(event):
        # Enable the update button when an item is selected
        selected = tree.selection()
        if selected:
            update_button.config(state='normal')
        else:
            update_button.config(state='disabled')

    # Bind the function to the tree's selection event
    tree.bind('<<TreeviewSelect>>', on_tree_select)

    button_width = 100  # width of the buttons
    button_spacing = 40  # space between the buttons
    total_width = 5 * button_width + 2 * button_spacing  # total width of all buttons and spaces

    # Place the buttons
    buttons = [add_button, update_button, remove_button, refresh_button]

    for i, button in enumerate(buttons):
        button.place(relx=0.55, rely=0.98, x=-total_width / 2 + i * (button_width + button_spacing), anchor='s',
                     width=button_width)


def create_label_and_field(frame, text, row, pad_x=0, pad_y=20, f_width=25, l_width=11):
    ttk.Label(frame, text=text, width=l_width, anchor="w").grid(row=row, column=0, padx=pad_x, pady=pad_y)
    field = ttk.Entry(frame, width=f_width)
    field.grid(row=row, column=1)
    return field


# Helper functions
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


def validate(fields, submit_func, args=True):
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
            # Add more validation types as needed
            else:
                # Unknown validation type
                raise ValueError(f"Unknown validation type for {field_name}.")
        except ValueError as e:
            # If validation fails, show an error message and return
            tk.messagebox.showerror("Error", f"{field_name}: {e}")
            return
        except Exception as e:
            # Handle any unexpected errors
            tk.messagebox.showerror("Error", "Failed to validate input.")
            logging.error("An error occurred in validating input:", e)
            return

    if args:
        # If all fields are successfully validated, call the submit function
        submit_func(validated_fields)
        clear_fields(*field_widgets)  # Clear all fields
    else:
        submit_func()  # Call the submit function


# Helper function to convert bytes to a more readable format
def convert_bytes(num):
    """
    this function will convert bytes to MB.... GB... etc
    """
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0


def get_pdf_files(folder_path):
    return [f for f in os.listdir(folder_path) if
            os.path.isfile(os.path.join(folder_path, f)) and f.endswith('.pdf')]


def update_pdf_list(folder_path, pdf_files, tree):
    while True:
        new_pdf_files = get_pdf_files(folder_path)
        if new_pdf_files != pdf_files:
            # Clear the tree
            tree.delete(*tree.get_children())

            # Update the list of files
            pdf_files = new_pdf_files
            for pdf_file in pdf_files:
                file_size = convert_bytes(os.path.getsize(os.path.join(folder_path, pdf_file)))
                tree.insert("", "end", values=(pdf_file, file_size))


def open_pdf(pdf_file_path):
    # Open the PDF file when clicked
    os.startfile(pdf_file_path)
