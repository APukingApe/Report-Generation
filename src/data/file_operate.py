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
        try:
            if file_path.endswith('.csv'):
                # Try reading with UTF-8 encoding first
                try:
                    return pd.read_csv(file_path, encoding='utf-8')
                except UnicodeDecodeError:
                    # If there's a UnicodeDecodeError, try ISO-8859-1
                    return pd.read_csv(file_path, encoding='ISO-8859-1')

            elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
                return pd.read_excel(file_path)

            else:
                raise ValueError("Unsupported file format")
        
        except Exception as e:
            print(f"Error occurred while reading the file: {str(e)}")
            raise e

