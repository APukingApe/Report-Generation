from pathlib import Path
import sys
import tkinter as tk
from tkinter import Entry, Frame, Label, Canvas, StringVar, Button, Toplevel
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image

from fpdf import FPDF
import pandas as pd
from src.data.file_operate import FileOperations
from src.ui.data_display import DataDisplay
from src.pdf.pdf_export import PDFExporter

report_list = []
root = None
window_created = False
def create_gui():
    global root, window_created 
    if not window_created:
        root = tk.Tk()
        root.title("Report Generator")
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        global report_list


        # window_width = int(screen_width * 0.4)
        # window_height = int(screen_height * 0.8)
        #root.geometry(f"{window_width}x{window_height}")
        #root.geometry("900x800")

        button_frame = Frame(root)
        button_frame.grid(row=20, column=0, sticky='ew', padx=10, pady=10)
        root.grid_rowconfigure(1, weight=1)
        root.grid_columnconfigure(0, weight=1)

        
        # canvas = Canvas(root, bg="white", highlightthickness=2, highlightbackground="black") 
        # canvas.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        graph_type = StringVar(value="Line")
        data_display = DataDisplay(root, None, graph_type, report_list)

        tk.Button(button_frame, text="Upload CSV/Excel", command=lambda: handle_file_upload(data_display)).grid(row=0, column=0, padx=5)

        Button(button_frame, text="Export Reports to PDF", command=lambda: export_all_reports_to_pdf(report_list)).grid(row=0, column=1, padx=5)

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
    root.geometry("900x800")
    file_path, data = FileOperations.upload_file()
    if file_path and data is not None:
        messagebox.showinfo("Success", f"File loaded successfully: {file_path}")
        data_display.display_data(data)
        if data_display.canvas is None:
            data_display.canvas = Canvas(root, bg="white", highlightthickness=2, highlightbackground="black")
            data_display.canvas.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        
    else:
            messagebox.showwarning("Warning", "No file selected")
            
def export_all_reports_to_pdf(report_list):
    if not report_list:
        messagebox.showwarning("Warning", "No reports to export.")
        return

    # Ask where to save the PDF
    file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if not file_path:
        return

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font('Arial', '', 12)

    # Iterate through each report in report_list
    for report in report_list:
        if isinstance(report, pd.DataFrame):
            pdf.add_page()
            pdf.set_font('Arial', '', 12)

            headers = report.columns
            col_widths = [max(30, len(str(header)) * 5) for header in headers]  # Adjust column width

            # Add headers to PDF
            for i, header in enumerate(headers):
                pdf.cell(col_widths[i], 10, str(header), border=1, align='C')
            pdf.ln()

            # Add each row of data
            for _, row in report.iterrows():
                for i, value in enumerate(row):
                    value_str = str(value)
                    pdf.cell(col_widths[i], 10, value_str, border=1, align='C')
                pdf.ln()

        elif isinstance(report, dict) and report.get("type") == "image":
            # Handle image file
            image_file = report.get("file")

            if Path(image_file).exists():
                print(f"Inserting image {image_file} into PDF")  # Debugging message
                pdf.add_page()

                # Open the image using PIL and get its size
                image = Image.open(image_file)
                image_width, image_height = image.size

                # Convert to PDF size (210mm x 297mm for A4), maintaining aspect ratio
                max_width = 190  # Keep margins in mind
                max_height = 270
                ratio = min(max_width / image_width, max_height / image_height)
                width = image_width * ratio
                height = image_height * ratio

                # Insert image into PDF
                pdf.image(image_file, x=10, y=10, w=width, h=height)
            else:
                print(f"Image file not found: {image_file}")  # Debugging message
                messagebox.showwarning("Warning", f"Image file not found: {image_file}")

    pdf.output(file_path)
    messagebox.showinfo("Success", f"Reports saved to PDF: {file_path}")

    # # Clean up images
    # for report in report_list:
    #     if isinstance(report, dict) and report.get('type') == 'image':
    #         image_path = Path(report['file'])
    #         try:
    #             if image_path.exists():
    #                 image_path.unlink()  # Delete the image file
    #                 print(f"Deleted {image_path}")
    #         except Exception as e:
    #             print(f"Error deleting {image_path}: {str(e)}")
    #             messagebox.showerror("Error", f"Failed to delete {image_path}: {str(e)}")

create_gui()
