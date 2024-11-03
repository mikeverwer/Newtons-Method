import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Matplotlib in Tkinter")

        # Create a Matplotlib figure
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)

        # Plot some data
        self.ax.plot([0, 1, 2, 3], [0, 1, 4, 9], label='y = x^2')
        self.ax.set_title("Sample Plot")
        self.ax.set_xlabel("X-axis")
        self.ax.set_ylabel("Y-axis")
        self.ax.legend()

        # Create a canvas to embed the figure
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew')

        # Add a toolbar for zoom and pan functionalities
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
