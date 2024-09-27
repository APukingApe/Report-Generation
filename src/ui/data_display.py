from tkinter import Label, Checkbutton, IntVar, Button, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DataDisplay:
    def __init__(self, root, canvas, graph_type):
        self.root = root
        self.canvas = canvas
        self.graph_type = graph_type
        self.selected_columns = {}

    def display_data(self, data, label):
        display_text = data.head().to_string() + "\n\nSummary Statistics:\n" + data.describe().to_string()
        label.config(text=display_text)
        self.create_checkboxes(data.columns)

    def create_checkboxes(self, columns):
        Label(self.root, text="Select columns to display:").grid(row=2, column=0, pady=5, sticky="nsew")
        for index, column in enumerate(columns):
            var = IntVar()
            self.selected_columns[column] = var
            Checkbutton(self.root, text=column, variable=var).grid(row=3 + index, column=0, sticky='w', padx=10)
        Button(self.root, text="Apply Selection and Plot", command=self.apply_selection_and_plot).grid(row=14, column=0, pady=5)

    def apply_selection_and_plot(self):
        selected_cols = [col for col, var in self.selected_columns.items() if var.get() == 1]
        if not selected_cols:
            messagebox.showwarning("Warning", "No columns selected")
            return
        filtered_data = self.data[selected_cols]
        self.plot_chart(filtered_data)

    def plot_chart(self, data):
        for widget in self.canvas.winfo_children():
            widget.destroy()
        fig, ax = plt.subplots(figsize=(6, 4))
        if self.graph_type.get() == "Line":
            data.plot(ax=ax, kind='line', title="Line Chart")
        elif self.graph_type.get() == "Bar":
            data.plot(ax=ax, kind='bar', title="Bar Chart")
        chart = FigureCanvasTkAgg(fig, self.canvas)
        chart.get_tk_widget().pack(fill="both", expand=True)
        plt.close(fig)
