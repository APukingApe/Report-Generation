import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def generate_plot(data, canvas):
    try:
        if 'Close' in data.columns:  # Assuming 'Close' is a column for demo purposes
            fig, ax = plt.subplots()
            data['Close'].plot(kind='line', title='Line Chart of Close Prices', ax=ax)

            # Display plot in Tkinter canvas
            canvas_agg = FigureCanvasTkAgg(fig, master=canvas)
            canvas_agg.draw()
            canvas_agg.get_tk_widget().pack()

            plt.close(fig)  # Close the figure after embedding
        else:
            print("'Close' column not found for plotting")
    except Exception as e:
        print(f"Error occurred while plotting: {str(e)}")
