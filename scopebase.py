import mysql.connector
import tkinter as tk
from tkinter import ttk

# Version string
__version__ = "0.4"

def fetch_data(password):
    """Fetch data from the database."""
    conn = mysql.connector.connect(
        host='scopebase.fritz.box',
        user='sr',
        password=password,
        database='scopebase'
    )
    cursor = conn.cursor()

    # Sample query
    sample_query = (
        "SELECT `sample`.`id` `Sample-ID`, `sample`.`date` `Date`, "
        "`location`.`name` `Location`, `sample-type`.`name` `Type`, "
        "`fixation`.`name` `Fixation`, `preservative`.`name` `Preservative`, "
        "`sample`.`latitude` `Latitude`, `sample`.`longitude` `Longitude`, "
        "`sample`.`T` `T`, `sample`.`pH` `pH`, `sample`.`EC` `EC`, "
        "`sample`.`nitrate` `NO3`, `sample`.`note` `Note` "
        "FROM { oj `scopebase`.`sample` `sample` "
        "LEFT OUTER JOIN `scopebase`.`sample-type` `sample-type` ON "
        "`sample`.`sample-type_id` = `sample-type`.`id` "
        "LEFT OUTER JOIN `scopebase`.`fixation` `fixation` ON "
        "`sample`.`fixation_id` = `fixation`.`id` "
        "LEFT OUTER JOIN `scopebase`.`location` `location` ON "
        "`sample`.`location_id` = `location`.`id` "
        "LEFT OUTER JOIN `scopebase`.`preservative` `preservative` ON "
        "`sample`.`preservative_id` = `preservative`.`id` } "
        "ORDER BY `Sample-ID` DESC"
    )

    # Slide query
    slide_query = (
        "SELECT `slide`.`id` `Slide-ID`, `sample`.`id` `Sample-ID`, "
        "`sample-type`.`name` `Sample-Type`, `fixation`.`name` `Fixation`, "
        "`preservative`.`name` `Preservative`, `protocol`.`name` `Protocol`, "
        "`mounting-medium`.`name` `Mounting-Medium`, `slide`.`date` `Slide-Date`, "
        "`sample`.`date` `Sample-Date`, `location`.`name` `Location`, "
        "`sample`.`latitude` `Sample-Latitude`, `sample`.`longitude` `Sample-Longitude` "
        "FROM { oj `scopebase`.`sample` `sample` "
        "LEFT OUTER JOIN `scopebase`.`sample-type` `sample-type` ON "
        "`sample`.`sample-type_id` = `sample-type`.`id` "
        "RIGHT OUTER JOIN `scopebase`.`slide` `slide` ON "
        "`sample`.`id` = `slide`.`sample_id` "
        "RIGHT OUTER JOIN `scopebase`.`protocol` `protocol` ON "
        "`slide`.`protocol_id` = `protocol`.`id` "
        "RIGHT OUTER JOIN `scopebase`.`mounting-medium` `mounting-medium` ON "
        "`slide`.`mounting-medium_id` = `mounting-medium`.`id` "
        "LEFT OUTER JOIN `scopebase`.`preservative` `preservative` ON "
        "`sample`.`preservative_id` = `preservative`.`id` "
        "LEFT OUTER JOIN `scopebase`.`fixation` `fixation` ON "
        "`sample`.`fixation_id` = `fixation`.`id` "
        "LEFT OUTER JOIN `scopebase`.`location` `location` ON "
        "`sample`.`location_id` = `location`.`id` } "
        "ORDER BY `Slide-ID` DESC"
    )

    # Execute queries
    cursor.execute(sample_query)
    samples = cursor.fetchall()

    cursor.execute(slide_query)
    slides = cursor.fetchall()

    # Close the connection
    cursor.close()
    conn.close()

    return samples, slides

def adjust_column_width(tree, data):
    """Adjust the column widths to fit the contents."""
    for col in tree["columns"]:
        max_width = max(len(col), max(len(str(item[col_idx])) for item in data for col_idx in range(len(item))))
        tree.column(col, width=max_width * 10)  # Adjust width based on character count

def display_data(samples, slides):
    """Display the fetched data in the treeview."""
    # Clear previous data
    for item in sample_tree.get_children():
        sample_tree.delete(item)
    for item in slide_tree.get_children():
        slide_tree.delete(item)

    # Insert sample data into the treeview
    for sample in samples:
        sample_tree.insert('', 'end', values=sample)

    # Insert slide data into the treeview
    for slide in slides:
        slide_tree.insert('', 'end', values=slide)

    # Adjust column widths
    adjust_column_width(sample_tree, samples)
    adjust_column_width(slide_tree, slides)

    # Hide password entry, button, and prompt label
    password_entry.pack_forget()
    fetch_button.pack_forget()
    prompt_label.pack_forget()  # Hide the prompt label

def on_fetch_data():
    """Fetch data and display it when button is clicked."""
    password = password_entry.get()
    samples, slides = fetch_data(password)
    display_data(samples, slides)

# Create the main application window
root = tk.Tk()
root.title("ScopeBase Database Viewer")

# Start the application maximized
root.state('zoomed')

# Initially display password entry
prompt_label = tk.Label(root, text="Enter Database Password:")
prompt_label.pack(pady=5)

password_entry = tk.Entry(root, show="*")
password_entry.pack(pady=5)

# Fetch button
fetch_button = tk.Button(root, text="Fetch Data", command=on_fetch_data)
fetch_button.pack(pady=5)

# Create a notebook (tabbed interface)
notebook = ttk.Notebook(root)
notebook.pack(pady=10, fill=tk.BOTH, expand=True)

# Frame for sample data
sample_frame = ttk.Frame(notebook)
notebook.add(sample_frame, text="Sample Data")

# Frame for slide data
slide_frame = ttk.Frame(notebook)
notebook.add(slide_frame, text="Slide Data")

# Sample table
sample_tree = ttk.Treeview(sample_frame, columns=(
    "Sample-ID", "Date", "Location", "Type", "Fixation", 
    "Preservative", "Latitude", "Longitude", "T", "pH", 
    "EC", "NO3", "Note"), show="headings")

# Define column headings and align left
for col in sample_tree["columns"]:
    sample_tree.heading(col, text=col)
    sample_tree.column(col, anchor="w")  # Left alignment

# Pack the Treeview to fill the frame
sample_tree.pack(fill=tk.BOTH, expand=True)

# Slide table
slide_tree = ttk.Treeview(slide_frame, columns=(
    "Slide-ID", "Sample-ID", "Sample-Type", "Fixation", 
    "Preservative", "Protocol", "Mounting-Medium", 
    "Slide-Date", "Sample-Date", "Location", 
    "Sample-Latitude", "Sample-Longitude"), show="headings")

# Define column headings and align left
for col in slide_tree["columns"]:
    slide_tree.heading(col, text=col)
    slide_tree.column(col, anchor="w")  # Left alignment

# Pack the Treeview to fill the frame
slide_tree.pack(fill=tk.BOTH, expand=True)

# Start the application
root.mainloop()
