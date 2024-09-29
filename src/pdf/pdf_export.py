from fpdf import FPDF
from tkinter import messagebox
import os

class PDFExporter:
    @staticmethod

    def export_to_pdf():
        chart_path = r"C:\Users\Administrator\Desktop\Material Hang Zhao\Report Generator\chart.png"
        pdf_path = r"C:\Users\Administrator\Desktop\Material Hang Zhao\Report Generator\src\pdf\report.pdf"

        if not os.path.exists(chart_path):
            messagebox.showerror("Error", "No chart found to export. Please generate a chart first.")
            return
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt="Data Report", ln=True, align="C")
        pdf.image(chart_path, x=10, y=20, w=180)

        pdf.output(pdf_path)
        
        messagebox.showinfo("Success", f"PDF report generated successfully as '{pdf_path}'!")