import os
import tkinter as tk
from datetime import datetime
from tkinter import ttk

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
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    table.setStyle(style)

    # Add the table to the elements to be added to the PDF
    elems.append(table)

    # Build the PDF
    pdf.build(elems)

    # Return the report name
    return path


def sort_column(tree, col, reverse):
    column_data = [(tree.set(child_id, col), child_id) for child_id in tree.get_children('')]
    column_data.sort(reverse=reverse)

    # rearrange items in sorted positions
    for index, (val, child_id) in enumerate(column_data):
        tree.move(child_id, '', index)

    # reverse sort next time column is clicked
    tree.heading(col, command=lambda: sort_column(tree, col, not reverse))


def create_treeview(frame, columns, column_widths, pad, height=23, data=None):
    # Create a style
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))

    # Create Canvas in new window
    canvas = tk.Canvas(frame)
    canvas.pack(side=tk.LEFT, fill='both', expand=True)

    # Create another frame inside the canvas
    second_frame = tk.Frame(canvas)

    # Add that new frame to a new window on the canvas
    canvas.create_window((0, 0), window=second_frame, anchor="nw")

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
    scrollbar.pack(side=tk.RIGHT, fill='y')

    # Configure the Treeview
    tree.configure(yscrollcommand=scrollbar.set)

    # Define columns
    tree["columns"] = columns

    # Format columns
    for col, width in zip(columns, column_widths):
        tree.column(col, width=width)
        tree.heading(col, text=col, command=lambda _col=col: sort_column(tree, _col, False))

    if data is not None:
        # Insert data in table
        for item in data:
            tree.insert("", "end", values=item)

    tree.pack(padx=pad)

    return tree


def create_button(frame, text, command, bg_color='#61CBEC', fg_color='#000000', font=('Arial', 12, 'normal')):
    button = tk.Button(frame, text=text, command=command)
    button.configure(background=bg_color, foreground=fg_color, font=font, relief='groove')
    button.pack(padx=100, pady=5, fill='x', expand=True)
    return button


def create_button_widget(frame, text, command, padx=5, pady=20, width=10):
    button = tk.Button(frame, text=text, font=("Helvetica", 12), width=width, command=command)
    button.pack(side="left", padx=padx, pady=pady, anchor='center')
    return button


def create_buttons(frame, fields, row, submit_action, clear_fields, close_view, x_padding=5, y_padding=20):
    # Submit and Cancel buttons
    button_frame = tk.Frame(frame)
    button_frame.grid(row=row, column=0, columnspan=3, padx=x_padding, pady=y_padding)

    create_button_widget(button_frame, "Submit", submit_action)

    create_button_widget(button_frame, "Clear", lambda: clear_fields(*fields))

    create_button_widget(button_frame, "Back", lambda: close_view())


def button_config(frame, tree, add, update, remove, back):
    add_button = tk.Button(frame, text="Add", command=add)
    update_button = tk.Button(frame, text="Update", command=lambda: update(tree))
    remove_button = tk.Button(frame, text="Remove", command=lambda: remove(tree))
    back_button = tk.Button(frame, text="Back", command=back)

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
    total_width = 4 * button_width + 2 * button_spacing  # total width of all buttons and spaces

    # Center the buttons at the bottom of the window
    add_button.place(relx=0.5, rely=0.98, x=-total_width / 2, anchor='s', width=button_width)
    update_button.place(relx=0.5, rely=0.98, x=-total_width / 2 + button_width + button_spacing, anchor='s',
                        width=button_width)
    remove_button.place(relx=0.5, rely=0.98, x=-total_width / 2 + 2 * (button_width + button_spacing), anchor='s',
                        width=button_width)
    back_button.place(relx=0.5, rely=0.98, x=-total_width / 2 + 3 * (button_width + button_spacing), anchor='s',
                      width=button_width)


def create_label_and_field(frame, text, row, padx=5, pady=20, f_width=25, l_width=11):
    tk.Label(frame, text=text, width=l_width, anchor="w", font=("Helvetica", 12)).grid(row=row, column=0, padx=padx,
                                                                                       pady=pady)
    field = tk.Entry(frame, font=("Helvetica", 12), width=f_width)
    field.grid(row=row, column=1)
    return field
