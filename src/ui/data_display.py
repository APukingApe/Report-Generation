import tkinter as tk
from tkinter import Checkbutton, Label, Canvas, StringVar, IntVar, OptionMenu, Button, Toplevel, Scrollbar, Frame, Text
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from fpdf import FPDF  

def clear_treeview(tree):
    for item in tree.get_children():
        tree.delete(item)

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

    def display_data(self, data):
        self.data = data
        display_text = data.head(10).to_string() + "\n\nSummary Statistics:\n" + data.describe().to_string()
        # label.config(text=display_text)
        self.create_checkboxes(data.columns)

    def sort_column(self, tree, col, reverse):
        # Sort the data using pandas
        sorted_data = self.data.sort_values(by=[col], ascending=not reverse)

        # Re-insert the sorted data into the Treeview
        self.insert_data_into_treeview(tree, sorted_data)

        # Track the current sorted column and direction
        self.sorted_column = col
        self.sort_reverse = reverse        

    def insert_data_into_treeview(self, tree, data):
        self.clear_treeview(tree)
        for index, row in data.iterrows():
            values = [str(value) for value in row]
            tree.insert("", "end", values=values)

    def sortby(self, tree, col, descending):
        """ Sort tree contents when a column header is clicked. """
        
        data_list = [(tree.set(child, col), child) for child in tree.get_children('')]
        
        try:
            data_list.sort(key=lambda t: float(t[0]), reverse=descending)
        except ValueError:
            data_list.sort(key=lambda t: t[0], reverse=descending)
        
        for index, (val, item) in enumerate(data_list):
            tree.move(item, '', index)
        
        tree.heading(col, command=lambda _col=col: self.sortby(tree, _col, not descending))
    
    def open_report_window(self, data):
        window = Toplevel(self.root)
        window.title("Statistics Report")
        window.geometry("600x400")

        text_widget = Text(window, bd=2, relief="ridge") 
        text_widget.pack(fill="both", expand=True, padx=10, pady=10)  

        report = data.describe().transpose().to_string()

        text_widget.insert("1.0", report)

        button_frame = Frame(window)
        button_frame.pack(side="bottom", fill="x", padx=5, pady=5)

        Button(button_frame, text="Save as PDF", command=lambda: self.save_as_pdf_report(report)).pack(side="left", padx=10, pady=10)
        Button(button_frame, text="Exit", command=window.destroy).pack(side="right", padx=10, pady=10)

    def open_data_window(self, data):
        window = Toplevel(self.root)
        window.title("Data Display")
        window.state('zoomed')  # auto zoom

        frame = Frame(window)
        frame.pack(fill="both", expand=True)

        # Insert tree view
        tree = ttk.Treeview(frame, columns=list(data.columns), show="headings", height=15)
        tree.pack(side="left", fill="both", expand=True)

        # Add scroller
        scrollbar_y = Scrollbar(frame, orient="vertical", command=tree.yview)
        scrollbar_y.pack(side="right", fill="y")
        tree.configure(yscrollcommand=scrollbar_y.set)

        scrollbar_x = Scrollbar(window, orient="horizontal", command=tree.xview)  # 放在窗口的底部
        scrollbar_x.pack(side="bottom", fill="x")
        tree.configure(xscrollcommand=scrollbar_x.set)

        for col in data.columns:
            tree.heading(col, text=col, command=lambda _col=col: self.sortby(tree, _col, False))
            tree.column(col, width=100, anchor="center")

        clear_treeview(tree)  # 
        for index, row in data.iterrows():
            values = [str(value) for value in row]
            tree.insert("", "end", values=values)

        button_frame = Frame(window)
        button_frame.pack(side="bottom", fill="x", padx=5, pady=5)

        Button(button_frame, text="Save as PDF", command=lambda: self.save_as_pdf(data)).pack(side="left", padx=10, pady=10)
        Button(button_frame, text="Exit", command=window.destroy).pack(side="right", padx=10, pady=10)

    # def create_checkboxes(self, columns):
    #     Label(self.root, text="Select columns for Y-axis:").grid(row=2, column=0, pady=5, sticky="nsew")

    #     for index, column in enumerate(columns):
    #         var = IntVar()
    #         self.selected_columns[column] = var
    #         Checkbutton(self.root, text=column, variable=var).grid(row=3 + index, column=0, sticky='w', padx=10)
        
    #     Label(self.root, text="Select column for X-axis:").grid(row=2, column=1, pady=5, sticky="nsew")
    #     self.x_axis_var.set(columns[0])  
    #     OptionMenu(self.root, self.x_axis_var, *columns).grid(row=3, column=1, padx=10)

    #     Button(self.root, text="Apply Selection and Plot", command=self.apply_selection_and_plot).grid(row=14, column=0, pady=5)
    #     Button(self.root, text="Show Raw Data ", command=lambda: self.open_data_window(self.data)).grid(row=15, column=0, pady=5)
    #     Button(self.root, text="Show Report", command=lambda: self.open_report_window(self.data)).grid(row=16, column=0, pady=5)
    def create_checkboxes(self, columns):
        Label(self.root, text="Select columns for Y-axis:").grid(row=1, column=0, columnspan=len(columns), pady=5, sticky="ew")
        
        for index, column in enumerate(columns):
            var = IntVar()
            self.selected_columns[column] = var
            Checkbutton(self.root, text=column, variable=var).grid(row=2, column=index, sticky='ew', padx=5)

        Label(self.root, text="Select column for X-axis:").grid(row=1, column=len(columns), pady=5, sticky="nsew")
        
        self.x_axis_var.set(columns[0])  
        OptionMenu(self.root, self.x_axis_var, *columns).grid(row=2, column=len(columns), padx=10, sticky="ew")

        Button(self.root, text="Apply Selection and Plot", command=self.apply_selection_and_plot).grid(row=14, column=0, pady=5, columnspan=2, sticky='ew')
        Button(self.root, text="Show Raw Data", command=lambda: self.open_data_window(self.data)).grid(row=15, column=0, pady=5, columnspan=2, sticky='ew')
        Button(self.root, text="Show Report", command=lambda: self.open_report_window(self.data)).grid(row=16, column=0, pady=5, columnspan=2, sticky='ew')

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
