from fpdf import FPDF
from tkinter import messagebox
import os

class PDFExporter:
    @staticmethod
    def export_to_pdf():
        if not os.path.exists("chart.png"):
            messagebox.showerror("Error", "No chart found to export. Please generate a chart first.")
            return
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Data Report", ln=True, align="C")
        pdf.image("chart.png", x=10, y=20, w=180)
        pdf.output("/product/report.pdf")
        messagebox.showinfo("Success", "PDF report generated successfully as 'report.pdf'!")
