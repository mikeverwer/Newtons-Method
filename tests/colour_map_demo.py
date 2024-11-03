import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Import FigureCanvasTkAgg directly

# List of colormaps to demonstrate
colormaps = [
    'viridis', 'plasma', 'inferno', 'magma', 'cividis',
    'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
    'YlGn', 'YlOrBr', 'YlOrRd', 'OrRd', 'PuBu', 'BuPu',
    'GnBu', 'PuBuGn', 'BuGn', 'YlGnBu', 'YlGn',
    'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu', 'Spectral', 'coolwarm',
    'Pastel1', 'Pastel2', 'Dark2', 'Set1', 'Set2', 'Set3', 'Accent',
    'tab10', 'tab20', 'tab20b', 'tab20c',
    'flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern', 'copper'
]

class ColormapDemo(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Matplotlib Colormap Demo")
        self.geometry("400x200")

        # Create a label
        self.label = ttk.Label(self, text="Select a colormap:")
        self.label.pack(pady=10)

        # Create a combobox for colormap selection
        self.cmap_combobox = ttk.Combobox(self, values=colormaps)
        self.cmap_combobox.pack(pady=10)
        self.cmap_combobox.bind("<<ComboboxSelected>>", self.on_colormap_selected)

        # Create a button to show the selected colormap
        self.show_button = ttk.Button(self, text="Show Colormap", command=self.show_selected_colormap)
        self.show_button.pack(pady=10)

    def on_colormap_selected(self, event):
        # Enable the button when a colormap is selected
        self.show_button['state'] = 'normal'

    def show_selected_colormap(self):
        # Get the selected colormap
        cmap = self.cmap_combobox.get()
        self.show_colormap(cmap)

    def show_colormap(self, cmap):
        # Create a new window to display the colormap
        colormap_window = tk.Toplevel(self)
        colormap_window.title(cmap)

        # Generate data for the colormap
        data = np.random.rand(10, 10)

        # Create a matplotlib figure
        fig, ax = plt.subplots()
        cax = ax.imshow(data, cmap=cmap)
        fig.colorbar(cax)

        # Embed the matplotlib figure in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=colormap_window)  # Use the imported FigureCanvasTkAgg
        canvas.draw()
        canvas.get_tk_widget().pack()

if __name__ == "__main__":
    app = ColormapDemo()
    app.mainloop()
