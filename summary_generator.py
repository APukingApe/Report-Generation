from tkinter import messagebox

def generate_summary(data, text_area):
    summary = data.describe()
    text_area.delete(1.0, 'end')  # Clear previous content
    text_area.insert('end', summary.to_string())  # Insert summary into text area

