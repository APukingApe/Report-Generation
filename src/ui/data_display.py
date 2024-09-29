import tkinter as tk
from tkinter import Checkbutton, Label, Canvas, StringVar, IntVar, OptionMenu, Button, Toplevel, Scrollbar, Frame, Text
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from fpdf import FPDF  

class DataDisplay:
    def __init__(self, root, canvas, graph_type):
        self.root = root
        self.canvas = canvas
        self.graph_type = graph_type
        self.selected_columns = {}
        self.data = None
        self.x_axis_var = StringVar()  
        self.x_axis_var.set('')
        self.y_axis_vars = {}

    def display_data(self, data, label):
        self.data = data
        display_text = data.head(10).to_string() + "\n\nSummary Statistics:\n" + data.describe().to_string()
        label.config(text=display_text)
        self.create_checkboxes(data.columns)
    
    def open_data_window(self, data):
        window = Toplevel(self.root)
        window.title("Data Display")
        # window.geometry("500x500")
        window.state('zoomed')
        
        frame = Frame(window)
        frame.pack(fill="both", expand=True)
        
        tree = ttk.Treeview(frame, columns=list(data.columns), show="headings", height=15)
        tree.pack(side="left", fill="both", expand=True)
        # text_area = Text(frame, wrap="none", font=("Arial", 10))
        scrollbar_y = Scrollbar(frame, orient="vertical", command=tree.yview) 
        scrollbar_y.pack(side="right", fill="y")
        tree.configure(yscrollcommand=scrollbar_y.set)

        scrollbar_x = Scrollbar(window, orient="horizontal", command=tree.xview) 
        scrollbar_x.pack(side="bottom", fill="x")
        tree.configure(xscrollcommand=scrollbar_x.set)

        for col in data.columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")


        for index, row in data.head(15).iterrows():
            tree.insert("", "end", values=list(row))
            
        label = Label(window, text=data.to_string(), justify="left", anchor="nw", font=("Arial", 10), bg="white")
        label.pack(fill="both", expand=True)
        
        Button(window, text="Save as PDF", command=lambda: self.save_as_pdf(data)).pack(pady=10)
        Button(window, text="Exit", command=window.destroy).pack(pady=10)

    def create_checkboxes(self, columns):
        Label(self.root, text="Select columns for Y-axis:").grid(row=2, column=0, pady=5, sticky="nsew")

        for index, column in enumerate(columns):
            var = IntVar()
            self.selected_columns[column] = var
            Checkbutton(self.root, text=column, variable=var).grid(row=3 + index, column=0, sticky='w', padx=10)
        
        Label(self.root, text="Select column for X-axis:").grid(row=2, column=1, pady=5, sticky="nsew")
        self.x_axis_var.set(columns[0])  
        OptionMenu(self.root, self.x_axis_var, *columns).grid(row=3, column=1, padx=10)

        Button(self.root, text="Apply Selection and Plot", command=self.apply_selection_and_plot).grid(row=14, column=0, pady=5, sticky="nsew", columnspan=2)
        Button(self.root, text="Show Data in New Window", command=lambda: self.open_data_window(self.data)).grid(row=15, column=0, pady=5, sticky="nsew", columnspan=2)

    def apply_selection_and_plot(self):
        if self.data is None:
            messagebox.showerror("Error", "No data available to plot.")
            return

        selected_y_cols = [col for col, var in self.selected_columns.items() if var.get() == 1]
        selected_x_col = self.x_axis_var.get()

        if not selected_y_cols:
            messagebox.showwarning("Warning", "No columns selected for Y-axis")
            return
        
        if selected_x_col == '':
            messagebox.showwarning("Warning", "No column selected for X-axis")
            return

        filtered_data = self.data[[selected_x_col] + selected_y_cols]

        self.plot_chart(filtered_data, selected_x_col, selected_y_cols)

    def plot_chart(self, data, x_column, y_columns):
        for widget in self.canvas.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(6, 4))

        if self.graph_type.get() == "Line":
            for y_col in y_columns:
                ax.plot(data[x_column], data[y_col], label=y_col)
            ax.set_title("Line Chart")
            ax.set_xlabel(x_column)
            ax.set_ylabel("Values")
        elif self.graph_type.get() == "Bar":
            data.plot(kind='bar', x=x_column, y=y_columns, ax=ax)
            ax.set_title("Bar Chart")
        
        ax.legend()

        chart = FigureCanvasTkAgg(fig, self.canvas)
        chart.get_tk_widget().pack(fill="both", expand=True)
        plt.close(fig)

    def save_as_pdf(self, data):
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not file_path:
            return
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        for i, line in enumerate(data.to_string().split('\n')):
            pdf.cell(200, 10, txt=line, ln=True)
        
        pdf.output(file_path)
        messagebox.showinfo("Success", f"Data saved as PDF: {file_path}")
