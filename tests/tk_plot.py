import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Matplotlib in Tkinter")

        # Create a Matplotlib figure with 2 subplots
        self.figure = Figure(figsize=(10, 4), dpi=100)
        self.ax1 = self.figure.add_subplot(121)  # First subplot
        self.ax2 = self.figure.add_subplot(122)  # Second subplot

        # Plot some data for the first subplot
        self.ax1.plot([0, 1, 2, 3], [0, 1, 4, 9], label='y = x^2')
        self.ax1.set_title("Sample Plot 1")
        self.ax1.set_xlabel("X-axis")
        self.ax1.set_ylabel("Y-axis")
        self.ax1.legend()

        # Plot some data for the second subplot
        self.ax2.plot([0, 1, 2, 3], [0, 1, 2, 3], label='y = x', color='orange')
        self.ax2.set_title("Sample Plot 2")
        self.ax2.set_xlabel("X-axis")
        self.ax2.set_ylabel("Y-axis")
        self.ax2.legend()

        # Create a canvas to embed the figure
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew')

        # Add a toolbar for the figure
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.root, pack_toolbar=False)
        self.toolbar.update()
        self.toolbar.grid(row=1, column=0, sticky='nsew')

        # Configure grid weights to make the layout responsive
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=0)
        self.root.grid_columnconfigure(0, weight=1)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
