import tkinter as tk
from tkinter import Label, Canvas, StringVar, OptionMenu, Button
from tkinter import messagebox
from src.data.file_operate import FileOperations
from src.ui.data_display import DataDisplay
from src.pdf.pdf_export import PDFExporter

def create_gui():
    root = tk.Tk()
    root.title("Report Generator with PDF Export")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    
    window_width = int(screen_width * 0.4)
    window_height = int(screen_height * 0.8)
    root.geometry(f"{window_width}x{window_height}")
    # root.geometry("800x600+100+200")

    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    label = Label(root, text="", justify="left", anchor="nw", bg="white", font=("Arial", 10), wraplength=680, width=100, height=15)
    label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

    canvas = Canvas(root, bg="white", highlightthickness=2, highlightbackground="black")  # 设置边框
    canvas.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
    graph_type = StringVar(value="Line")
    data_display = DataDisplay(root, canvas, graph_type)
    OptionMenu(root, graph_type, "Line", "Bar").grid(row=13, column=0, pady=5)
    Button(root, text="Upload CSV/Excel", command=lambda: handle_file_upload(label, data_display)).grid(row=14, column=0, pady=5)
    Button(root, text="Export to PDF", command=PDFExporter.export_to_pdf).grid(row=15, column=0, pady=5)
    Button(root, text="Exit", command=root.destroy).grid(row=16, column=0, pady=5)
    root.mainloop()

def handle_file_upload(label, data_display):
    file_path, data = FileOperations.upload_file()
    if file_path and data is not None:
        messagebox.showinfo("Success", f"File loaded successfully: {file_path}")
        data_display.display_data(data, label)
    else:
        messagebox.showwarning("Warning", "No file selected")


create_gui()