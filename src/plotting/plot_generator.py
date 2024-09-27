import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def generate_plot(data, canvas, chart_type):
    try:
        fig, ax = plt.subplots()

        if chart_type == "Line":
            data.plot(kind='line', title='Line Chart', ax=ax)
        elif chart_type == "Bar":
            data.plot(kind='bar', title='Bar Chart', ax=ax)

        # Display plot in Tkinter canvas
        canvas_agg = FigureCanvasTkAgg(fig, master=canvas)
        canvas_agg.draw()
        canvas_agg.get_tk_widget().pack()

        plt.close(fig)  # Close the figure after embedding
    except Exception as e:
        print(f"Error occurred while plotting: {str(e)}")
