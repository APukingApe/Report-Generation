from typing import Self
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def generate_plot(data, canvas, chart_type, x_column=None, y_columns=None):
    for widget in canvas.winfo_children():
        widget.destroy()    
    
    try:
        fig, ax = plt.subplots()
        ax.spines['top'].set_linewidth(1.5)
        ax.spines['right'].set_linewidth(1.5)
        ax.spines['bottom'].set_linewidth(1.5)
        ax.spines['left'].set_linewidth(1.5)

        if x_column is None:
            x_data = data.index  
        else:
            x_data = data[x_column] 

        if y_columns is None:
            y_columns = data.columns 


        if chart_type == "Line":
            for y_column in y_columns:
                ax.plot(x_data, data[y_column], label=y_column)  
            ax.set_title('Line Chart')

        elif chart_type == "Bar":
            data.plot(kind='bar', x=x_column, y=y_columns, title='Bar Chart', ax=ax)  

        ax.legend()

        canvas_agg = FigureCanvasTkAgg(fig, master=canvas)
        canvas_agg.draw()
        canvas_agg.get_tk_widget().pack()

        plt.close(fig)  

    except Exception as e:
        print(f"Error occurred while plotting: {str(e)}")
