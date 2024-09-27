import pandas as pd
from tkinter import filedialog

class FileOperations:
    @staticmethod
    def upload_file():
        file_types = [("Excel files", "*.xlsx"), ("Excel files", "*.xls"), ("CSV files", "*.csv")]
        file_path = filedialog.askopenfilename(filetypes=file_types)
        if file_path:
            return file_path, FileOperations.read_data(file_path)
        return None, None

    @staticmethod
    def read_data(file_path):
        if file_path.endswith('.csv'):
            return pd.read_csv(file_path)
        elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
            return pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file format")
