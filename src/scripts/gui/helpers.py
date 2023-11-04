import tkinter as tk
from tkinter import ttk


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


def create_button(frame, text, command, bg_color='#61CBEC', fg_color='#000000', font=('Arial', 12, 'normal'),
                  relief='groove'):
    button = tk.Button(frame, text=text, command=command)
    button.configure(background=bg_color, foreground=fg_color, font=font, relief=relief)
    button.pack(padx=40, pady=5, fill='x', expand=True)
    return button


def button_config(frame, tree, add, remove, back):
    add_button = tk.Button(frame, text="Add", command=add)
    remove_button = tk.Button(frame, text="Remove", command=lambda: remove(tree))
    back_button = tk.Button(frame, text="Back", command=back)

    button_width = 100  # width of the buttons
    button_spacing = 40  # space between the buttons
    total_width = 3 * button_width + 2 * button_spacing  # total width of all buttons and spaces

    # Center the buttons at the bottom of the window
    add_button.place(relx=0.5, rely=0.98, x=-total_width / 2, anchor='s', width=button_width)
    remove_button.place(relx=0.5, rely=0.98, x=-total_width / 2 + button_width + button_spacing, anchor='s',
                        width=button_width)
    back_button.place(relx=0.5, rely=0.98, x=-total_width / 2 + 2 * (button_width + button_spacing), anchor='s',
                      width=button_width)
