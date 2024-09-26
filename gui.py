from tkinter import Tk, Button, Text, Canvas
from file_handler import upload_file
from report_generator import export_to_pdf

def create_gui():
    root = Tk()
    root.title("Report Generator with PDF Export")

    # Text area for displaying the summary
    text_area = Text(root, height=15, width=80)
    text_area.pack(pady=10)

    # Canvas for displaying charts
    canvas = Canvas(root, width=600, height=400)
    canvas.pack(pady=10)

    # Upload button
    upload_button = Button(root, text="Upload CSV/Excel", command=lambda: upload_file(text_area, canvas))
    upload_button.pack(pady=10)

    # Export to PDF button
    export_button = Button(root, text="Export to PDF", command=export_to_pdf)
    export_button.pack(pady=10)

    # Start the GUI
    root.mainloop()
