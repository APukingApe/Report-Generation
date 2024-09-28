from tkinter import Label, Checkbutton, IntVar, Button, messagebox, StringVar, OptionMenu
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DataDisplay:
    def __init__(self, root, canvas, graph_type):
        self.root = root
        self.canvas = canvas
        self.graph_type = graph_type
        self.selected_columns = {}
        self.data = None
        self.x_axis_var = StringVar()  # 保存x轴的列名
        self.x_axis_var.set('')  # 初始化为空
        self.y_axis_vars = {}  # 保存y轴选择的列

    def display_data(self, data, label):
        self.data = data  # 存储数据到 self.data
        display_text = data.head().to_string() + "\n\nSummary Statistics:\n" + data.describe().to_string()
        label.config(text=display_text)
        self.create_checkboxes(data.columns)

    def create_checkboxes(self, columns):
        Label(self.root, text="Select columns for Y-axis:").grid(row=2, column=0, pady=5, sticky="nsew")

        # 创建Checkbutton供用户选择y轴
        for index, column in enumerate(columns):
            var = IntVar()
            self.selected_columns[column] = var
            Checkbutton(self.root, text=column, variable=var).grid(row=3 + index, column=0, sticky='w', padx=10)
        
        # 创建下拉菜单供用户选择x轴
        Label(self.root, text="Select column for X-axis:").grid(row=2, column=1, pady=5, sticky="nsew")
        self.x_axis_var.set(columns[0])  # 默认选择第一列作为x轴
        OptionMenu(self.root, self.x_axis_var, *columns).grid(row=3, column=1, padx=10)

        Button(self.root, text="Apply Selection and Plot", command=self.apply_selection_and_plot).grid(row=14, column=0, pady=5, sticky="nsew", columnspan=2)

    def apply_selection_and_plot(self):
        if self.data is None:  
            messagebox.showerror("Error", "No data available to plot.")
            return

        # 获取用户选择的y轴列
        selected_y_cols = [col for col, var in self.selected_columns.items() if var.get() == 1]
        selected_x_col = self.x_axis_var.get()

        if not selected_y_cols:
            messagebox.showwarning("Warning", "No columns selected for Y-axis")
            return
        
        if selected_x_col == '':
            messagebox.showwarning("Warning", "No column selected for X-axis")
            return

        # 过滤数据，基于用户选择的 x 和 y 列
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

        # 显示图表
        chart = FigureCanvasTkAgg(fig, self.canvas)
        chart.get_tk_widget().pack(fill="both", expand=True)
        plt.close(fig)
