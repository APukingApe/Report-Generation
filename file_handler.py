import pandas as pd
from tkinter import filedialog
from summary_generator import generate_summary
from plot_generator import generate_plot

data = None  # Global variable to store the data

def upload_file(text_area, canvas):
    global data
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx")])
    if file_path:
        try:
            if file_path.endswith('.csv'):
                data = pd.read_csv(file_path)
            elif file_path.endswith('.xlsx'):
                data = pd.read_excel(file_path)
            generate_summary(data, text_area)  # Show summary in the text area
            generate_plot(data, canvas)  # Show plot in the canvas
        except Exception as e:
            print(f"Error: {str(e)}")
