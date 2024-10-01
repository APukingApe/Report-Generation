from pathlib import Path
import time
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
    def __init__(self, root, canvas, graph_type, report_list):
        self.root = root
        self.canvas = canvas
        self.graph_type = graph_type
        self.selected_columns = {}
        self.data = None
        self.x_axis_var = StringVar()  
        self.x_axis_var.set('')
        self.y_axis_vars = {}
        self.report_list = report_list
        #self.canvas.config(width=300, height=200)

    def display_data(self, data):
        self.data = data
#        display_text = data.head(10).to_string() + "\n\nSummary Statistics:\n" + data.describe().to_string()
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

        # Generate the DataFrame for report (DataFrame, not string)
        report_df = data.describe().transpose() 

        # Create a Text widget to display the report as a string for viewing
        text_widget = Text(window, bd=2, relief="ridge") 
        text_widget.pack(fill="both", expand=True, padx=10, pady=10)

        # Convert the DataFrame to string and display in the Text widget
        report_str = report_df.to_string()
        text_widget.insert("1.0", report_str)

        # Add buttons at the bottom
        button_frame = Frame(window)
        button_frame.pack(side="bottom", fill="x", padx=5, pady=5)

        # When 'Add to report' is clicked, add the DataFrame report to the list
        Button(button_frame, text="Add to report", command=lambda: self.save_as_pdf(report_df)).pack(side="left", padx=10, pady=10)
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

        clear_treeview(tree)  
        for index, row in data.iterrows():
            values = [str(value) for value in row]
            tree.insert("", "end", values=values)

        button_frame = Frame(window)
        button_frame.pack(side="bottom", fill="x", padx=5, pady=5)

        Button(button_frame, text="Save to report", command=lambda: self.save_as_pdf(data)).pack(side="left", padx=10, pady=10)
        Button(button_frame, text="Exit", command=window.destroy).pack(side="right", padx=10, pady=10)


 
    def create_checkboxes(self, columns):
        Label(self.root, text="Select column for X-axis:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.x_axis_var.set(columns[0])  
        OptionMenu(self.root, self.x_axis_var, *columns).grid(row=0, column=1, padx=10, pady=5, sticky="w")

        Label(self.root, text="Select columns for Y-axis:").grid(row=0, column=2, padx=10, pady=5, sticky="w")
        
        y_frame = Frame(self.root)
        y_frame.grid(row=1, column=2, padx=10, pady=5, sticky="nsew") 

        self.y_listbox = tk.Listbox(y_frame, selectmode="multiple", exportselection=0, height=6)
        self.y_listbox.pack(side="left", fill="y")

        scrollbar_y = Scrollbar(y_frame, orient="vertical")
        scrollbar_y.pack(side="right", fill="y")
        self.y_listbox.config(yscrollcommand=scrollbar_y.set)
        scrollbar_y.config(command=self.y_listbox.yview)

        for col in columns:
            self.y_listbox.insert(tk.END, col)

        Label(self.root, text="Select Chart Type:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        OptionMenu(self.root, self.graph_type, "Line", "Bar", "Pie").grid(row=2, column=1, padx=10, pady=5, sticky="w")

        Button(self.root, text="Apply Selection and Plot", command=self.apply_selection_and_plot).grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        Button(self.root, text="Show Raw Data", command=lambda: self.open_data_window(self.data)).grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        Button(self.root, text="Show Report", command=lambda: self.open_report_window(self.data)).grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        Button(self.root, text="Save to report", command=lambda: self.save_canvas_to_report()).grid(row=6, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

    def apply_selection_and_plot(self):
        if self.data is None:
            messagebox.showerror("Error", "No data available to plot.")
            return

        selected_y_indices = self.y_listbox.curselection()
        selected_y_cols = [self.y_listbox.get(i) for i in selected_y_indices]
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

        self.fig, ax = plt.subplots(figsize=(6, 4))

        if self.graph_type.get() == "Line":
            for y_col in y_columns:
                ax.plot(data[x_column], data[y_col], label=y_col)
            ax.set_title("Line Chart")
            ax.set_xlabel(x_column)
            ax.set_ylabel("Values")
        elif self.graph_type.get() == "Bar":
            data.plot(kind='bar', x=x_column, y=y_columns, ax=ax)
            ax.set_title("Bar Chart")

        elif self.graph_type.get() == "Pie":
            if len(y_columns) != 1:
                messagebox.showwarning("Warning", "Pie chart requires exactly one Y-axis column.")
                return
            pie_data = data[y_columns[0]].value_counts()  # 使用 value_counts 汇总数据
            labels = pie_data.index
            sizes = pie_data.values

            ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')  # 保持饼图为圆形
            ax.set_title(f"Pie Chart for {y_columns[0]}") 

        ax.legend()

        chart = FigureCanvasTkAgg(self.fig, self.canvas)
        chart.get_tk_widget().pack(fill="both", expand=True)
        #plt.close(self.fig)

    def save_canvas_to_report(self):
        if not hasattr(self, 'fig'):
            print("No figure found to save.")
            messagebox.showwarning("Warning", "No figure found to save.")
            return

        timestamp = time.strftime("%Y%m%d-%H%M%S")
        image_file = f"plot_{timestamp}.png"
        
        image_path = Path.cwd() / image_file

        self.fig.savefig(image_path)

        if image_path.exists():
            print(f"Image saved successfully at {image_path}")
            self.report_list.append({"type": "image", "file": str(image_path)})  # 添加到报告列表
            plt.close(self.fig) 
            messagebox.showinfo("Success", f"Canvas image added to the report as {image_file}")
        else:
            print(f"Failed to save image at {image_path}")
            messagebox.showwarning("Warning", f"Failed to save image at {image_path}")

    def save_as_pdf(self, report_content):
        self.report_list.append(report_content)
        messagebox.showinfo("Success", "Report added to the PDF list.")
