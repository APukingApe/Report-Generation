from fpdf import FPDF
from tkinter import filedialog, messagebox

class PDFExporter:
    @staticmethod  
    def export_to_pdf(report_list):
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not file_path:
            return
        
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        for idx, report in enumerate(report_list):
            pdf.cell(200, 10, txt=f"Report {idx + 1}", ln=True)
            for line in report.split('\n'):
                pdf.cell(200, 10, txt=line, ln=True)
            pdf.ln(10)  
            
        pdf.output(file_path)
        messagebox.showinfo("Success", f"All reports saved as PDF: {file_path}")
