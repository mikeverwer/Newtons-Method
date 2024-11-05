import tkinter as tk
from tkinter import messagebox
from sympy import sympify, latex
import matplotlib.pyplot as plt
from PIL import Image, ImageTk

plt.rcParams['mathtext.fontset'] = 'stix'  # Use STIX fonts for math text

class MathExpressionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Math Expression to LaTeX Converter")

        # Entry widget for user input
        self.entry = tk.Entry(root, width=50)
        self.entry.pack(pady=10)

        # Button to convert expression
        self.convert_button = tk.Button(root, text="Convert to LaTeX", command=self.convert_to_latex)
        self.convert_button.pack(pady=5)

        # Label to display the LaTeX output
        self.output_label = tk.Label(root, text="", justify=tk.LEFT)
        self.output_label.pack(pady=10)

        # Canvas to display the LaTeX rendered image
        self.canvas = tk.Canvas(root, width=400, height=100)
        self.canvas.pack()

    def convert_to_latex(self):
        # Get the expression from the entry widget
        expression = self.entry.get()
        try:
            # Convert the expression to a SymPy object
            sympy_expr = sympify(expression)
            # Convert the SymPy expression to LaTeX
            latex_expr = latex(sympy_expr)

            # Update the output label with the LaTeX expression
            self.output_label.config(text=f"LaTeX: {latex_expr}")

            # Render the LaTeX expression to an image and display it
            self.render_latex(latex_expr)

        except Exception as e:
            messagebox.showerror("Error", f"Invalid expression: {e}")

    def render_latex(self, latex_expr):
        # Render the LaTeX expression to an image using matplotlib
        try:
            # Create a figure and axis
            fig, ax = plt.subplots(figsize=(4, 1))  # Adjust size as needed
            sfont = {'fontname':'serif'}
            ax.text(0.5, 0.5, f"${latex_expr}$", fontsize=20, ha='center', va='center')
            ax.axis('off')  # Hide axes

            # Save the figure to a file
            plt.savefig('latex_output.png', bbox_inches='tight', pad_inches=0.1)
            plt.close(fig)  # Close the figure to free memory

            # Load the image and display it on the canvas
            self.display_image('latex_output.png')
        except Exception as e:
            messagebox.showerror("Error", f"Could not render LaTeX: {e}")

    def display_image(self, image_path):
        # Load the image using PIL
        img = Image.open(image_path)
        img = img.resize((400, 100), Image.LANCZOS)  # Resize image to fit canvas
        self.img_tk = ImageTk.PhotoImage(img)

        # Clear the canvas and display the new image
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img_tk)
        self.canvas.image = self.img_tk  # Keep a reference to avoid garbage collection

if __name__ == "__main__":
    root = tk.Tk()
    app = MathExpressionApp(root)
    root.mainloop()
