from tkinter import messagebox

def generate_summary(data, text_area):
    summary = data.describe()
    text_area.delete(1.0, 'end')  
    text_area.insert('end', summary.to_string())  

