import sys
import tkinter as tk
from tkinter import Label, Canvas, StringVar, OptionMenu, Button
from tkinter import messagebox
from src.data.file_operate import FileOperations
from src.ui.data_display import DataDisplay
from src.pdf.pdf_export import PDFExporter

root = None
window_created = False
def create_gui():
    global root, window_created 
    if not window_created:
        print("Creating new window")  # 在 create_gui 函数中打印
        root = tk.Tk()
        root.title("Data Visualization Tool")
        print("New window created")  # 确保窗口每次创建时打印
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        window_width = int(screen_width * 0.4)
        window_height = int(screen_height * 0.8)
        root.geometry(f"{window_width}x{window_height}")

        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)

        canvas = Canvas(root, bg="white", highlightthickness=2, highlightbackground="black")  # 设置边框
        canvas.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        graph_type = StringVar(value="Line")
        data_display = DataDisplay(root, canvas, graph_type)

        tk.OptionMenu(root, graph_type, "Line", "Bar").grid(row=13, column=0, pady=5)
        tk.Button(root, text="Upload CSV/Excel", command=lambda: handle_file_upload(data_display)).grid(row=14, column=0, pady=5)
        tk.Button(root, text="Export to PDF", command=PDFExporter.export_to_pdf).grid(row=15, column=0, pady=5)

        tk.Button(root, text="Exit", command=exit_application).grid(row=16, column=0, pady=5)

        root.mainloop()

def exit_application():
    global root, window_created  
    if root is not None:
        print("Exiting application")
        root.quit()  
        root.destroy()  
        root = None
        window_created = False  
        sys.exit(0)

def handle_file_upload(data_display):
    print("upload file")
    file_path, data = FileOperations.upload_file()
    if file_path and data is not None:
        messagebox.showinfo("Success", f"File loaded successfully: {file_path}")
        data_display.display_data(data)
    else:
        messagebox.showwarning("Warning", "No file selected")


create_gui()