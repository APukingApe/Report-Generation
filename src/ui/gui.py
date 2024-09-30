import sys
import tkinter as tk
from tkinter import Entry, Frame, Label, Canvas, StringVar, OptionMenu, Button, Toplevel
from tkinter import messagebox
from src.data.file_operate import FileOperations
from src.ui.data_display import DataDisplay
from src.pdf.pdf_export import PDFExporter

root = None
window_created = False
def create_gui():
    global root, window_created 
    if not window_created:
        root = tk.Tk()
        root.title("Data Visualization Tool")
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        window_width = int(screen_width * 0.4)
        window_height = int(screen_height * 0.8)
        root.geometry(f"{window_width}x{window_height}")
        button_frame = Frame(root)
        button_frame.grid(row=20, column=0, sticky='ew', padx=10, pady=10)
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)

        canvas = Canvas(root, bg="white", highlightthickness=2, highlightbackground="black") 
        canvas.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        graph_type = StringVar(value="Line")
        data_display = DataDisplay(root, canvas, graph_type)

        tk.OptionMenu(root, graph_type, "Line", "Bar").grid(row=13, column=0, pady=5)
        tk.Button(root, text="Upload CSV/Excel", command=lambda: handle_file_upload(data_display)).grid(row=14, column=0, pady=5)
        # tk.Button(root, text="Export to PDF", command=PDFExporter.export_to_pdf).grid(row=15, column=0, pady=5)
        #tk.Button(root, text="Upload CSV/Excel", command=data_display.load_data).grid(row=2, column=0, pady=10)

        # tk.Button(root, text="Exit", command=exit_application).grid(row=18, column=0, sticky='sw', pady=5)
        #tk.Button(button_frame, text="Upload CSV/Excel", command=lambda: handle_file_upload(data_display)).grid(row=0, column=0, padx=5)
        #tk.Button(root, text="Open Export to PDF Window", command=data_display.open_export_window).pack(pady=20)

        # Export to PDF 按钮
        tk.Button(button_frame, text="Export to PDF", command=PDFExporter.export_to_pdf).grid(row=0, column=1, padx=5)

        # Exit 按钮
        tk.Button(button_frame, text="Exit", command=exit_application).grid(row=0, column=2, padx=5)

        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        button_frame.grid_columnconfigure(2, weight=1)
        root.mainloop()

def exit_application():
    global root, window_created  
    if root is not None:
        root.quit()  
        root.destroy()  
        root = None
        window_created = False  
        sys.exit(0)

def handle_file_upload(data_display):
    file_path, data = FileOperations.upload_file()
    if file_path and data is not None:
        messagebox.showinfo("Success", f"File loaded successfully: {file_path}")
        data_display.display_data(data)
    else:
        messagebox.showwarning("Warning", "No file selected")

create_gui()