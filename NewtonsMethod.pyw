from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tooltip import ToolTip
import os
import re
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from PIL import Image, ImageTk

plt.rcParams['mathtext.fontset'] = 'stix'  # Use STIX fonts for math text - serif, italicized font

def main():
    app = NewtonApp()
    app.mainloop()


class NewtonApp(Tk):
    # The app is a subclass of a Tk() object. This way, we can simply call `self` instead of `self.root`.
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Title and icon
        self.header = "Newton's Method"
        self.title(self.header)
        self.iconbitmap('NM-icon.ico')
                
        # icon_data = b'iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAACXBIWXMAAA7DAAAOwwHHb6hkAAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAABUBJREFUaIHV2VuMXWUVB/DfmltvQy+2trRIgSGaWGIQIyKagg8+GG8kpBoTozFgwosWEh/EN030SZM+mRijidrESKIRAUNQ46UQaDTxFo1QFSilLWA70E7tTJnL8uHbp3PYPWc655yNA//ky5y99p69//+9Lt/6vh24Ds97fWLbCJ7PzGMrzaQfRIQhXLLSRAbBEA5ExK0rTaRfDGErfhIRP4iI8ZUm1CsC2XZ8CB/OzH+uEJ+eEBE7hmq2t+CxiNi9EoT6wRAer9k245cR8ckV4NMzhvBBfLdmX4X9EfGF/z+l3rEjM+FOzCs50T6+mJleiwM7zguoDHtwtiZgAXesNNllCaiMuzFVEzGLD6004WUJqE7chDM1EVO47tUnlVEfSwmol1GQmQfwMcy1mcfx44jY2FemLYEIEWFthA24FNuUargOoxFGIgxHiAv+V/FAx2YuIm7Hd2rmB/DRrF7BgMRXYRMm8AbswjDG8Cz+g+N4CcfwsqrQZMqI6BxCNTftc2Fl2jtgmAyRm8k95D7yIDlNPkeeqf6eJP9OPkx+mbyWvJxcS46Ue3TJgZqAUTxSE/BfXD2AgPeRXyWfqIjPkwtk1sYCeY48TD5I3kVeSa4rItZcdlEBlYidOFkT8St0TbAuxNeRHyHvJ6e6kO42zpF/Jr9Evo0cZ2LnsgRUIj7VIZQ+0wP5cfID5KPkXA/E28c0eYj8LPlm3j+xbAGViPtqAo5h3TLf/A3kveRMn+TbPfEYeRuf39WxjC6Bz1Xx38J2pQXpighjVbLdhpuVPmsQjCrr+Bu5ZaInAZn5jFKV2nF3RGztdH21ZN2MG/AOrO+d74W3VUS8l0u39+oB+LpSn1u4BHu7XLtGmZhuxBXVw5vAEC5na88hJDNP42s18x0RsabdEGFYEXeFEmqbNCegwpq39uMB+DZOtB1vQX0BNKq0AtuVMFro81ndsJqRDX0JyMxpRUQ77oqIoPQ2SjuwUemhRpUWoWHEeL8egG8qbXYL1+Bd1e9hiz1N6xntjWFDiLm+BVQN4L0188dbd8ZI9XtWacaaxjzzpwbxAPyodrynCqPWRDenrPDmmZ33ih2cgTHHzNFBBTyoLHRa2Il3Lz7ANGb4yyaOr204j09x4uBAAqpkfqBmvkV51fOYZf9VPPSe0nVMD/K4dpzDEQ4/OagH4Ke1493Oh889q9m/lyPBE0oqNJLLx/E9HjrchIDfeWVwv5PLVmOBu+/k+Mby+eEZHErytP6TIZW1+m/K+MbkwAIy8wW076WOcex6tlzLiU+XFDmKJzH3KKOP47QSYr1iGj/Ht3CYxVI3KB5W9lVb2M3kTYwNF65j2PI0N9+jzBcv4u3KDD7k4i1GKm78RUX+j5nmIpoT8Ahubzv+BLlrsRC9hImvsOqoEgInFQ+0+qT1lYh6RCxgRvFw680fy1wsZ00J+Eft+JrF589h5rfsu09pLc4qa4rncBWuxhurcxuUGbxF/Cn8XvHwrzHbTr5JAV2+J7Sq6fy+ivR8RexFJSSexZ+UZm99JWBGmb3/hSP4K6YyO5evRgRk5mRETCp7O/WzhzjbmisWKnJnMamszsax2mIezCiJM6VqQTK7V62mPAD/1lGA72fmAkScd8nLiohhJR+iGq1zC5nLq1JNCngK19dsiR+eP8jFHe+q5Z5ru27JN90NTQo41cF2MDOf7nRxm5iB0MRM3MKZDrb7G7x/RzQpYKqDrd7oNY5X0wMv4G8N3r8jmsyBP+BnyjbKm3CgiS34i2HJ7wOvdUTEjhFsqzYTXo/Y9j+E8Ah+V+UfsQAAAABJRU5ErkJggg=='
        # icon = PhotoImage(data=icon_data)
        # self.iconphoto(True, icon)

        # Initialize variables
        self.x = sp.symbols('x')
        self.f = None
        self.df = None
        self.valid_expression: bool = True
        self.plots_figure = Figure(figsize=(16, 9), dpi=100)
        self.newton_ax = self.plots_figure.add_subplot(211)
        self.function_ax = self.plots_figure.add_subplot(212)
        
        # Window Creation
        self.build_window()
        self.update_idletasks()  # wait until the window is finished
        self.position_window()
        self.do_bindings()
        return    

    def position_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = self.winfo_width()
        window_height = self.winfo_height()
        x_pos = (screen_width - window_width) // 2
        self.geometry(f"+{x_pos}+25")
        return
    
    def do_bindings(self):
        self.math_input_entry.bind("<Any-KeyRelease>", lambda event: self.print_pretty_math())
        return
    
    def build_window(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        mainframe = ttk.Frame(self, padding=(4, 4, 4, 4))
        mainframe.grid(row=0, column=0, sticky=(N, E, S, W))
        mainframe.rowconfigure(0, weight=1)
        mainframe.columnconfigure(1, weight=1)

        base_canvas = Canvas(mainframe, background='white', width=900, height=600)
        base_canvas.grid(row=0, column=1, sticky=(N, E, S, W))
        base_canvas.rowconfigure(0, weight=1)
        base_canvas.columnconfigure(0, weight=1)
        self.build_plots_panel(base_canvas)

        control_panel_frame = ttk.Frame(mainframe)
        self.build_control_panel(control_panel_frame)
        control_panel_frame.grid(row=0, column=0, sticky=(N, E, S, W))
        return
    
    def build_plots_panel(self, base_canvas: Canvas):
        self.plots_canvas = FigureCanvasTkAgg(self.plots_figure, master=base_canvas)
        # self.plots_canvas.draw()
        self.plots_canvas.get_tk_widget().grid(row=0, column=0, sticky=NSEW)

        self.toolbar = NavigationToolbar2Tk(self.plots_canvas, base_canvas, pack_toolbar=False)
        self.toolbar.update()
        self.toolbar.grid(row=1, column=0, sticky=W)
        return

    def build_control_panel(self, control_panel):
        frame: ttk.Frame = control_panel
        frame.rowconfigure(1, weight=1)
        header_frame = ttk.Frame(frame)
        header_frame.grid(row=0, column=0, sticky=(N, W), padx=10, pady=10)
        name_label = ttk.Label(header_frame, text=self.header, font="_ 24 bold")
        name_label.grid(row=0, column=0)
        ToolTip(name_label, "This is a ToolTip.")

        self.content_frame = ttk.Frame(frame)
        self.content_frame.grid(row=1, column=0, sticky=(N, S))

        math_function_input_label = ttk.Label(self.content_frame, text="Enter the function f(x):")
        math_function_input_label.grid(row=0, column=0, sticky=W)

        self.input_error_label = ttk.Label(self.content_frame, text="")
        self.input_error_label.grid(row=1, column=0, sticky=W)
            
        self.math_input_entry = ttk.Entry(self.content_frame, width=30, font="Times")
        self.math_input_entry.insert(0, "sin(5*x) - x + exp(x) - 2")
        self.math_input_entry.grid(row=2, column=0)

        self.pretty_math_display = Canvas(self.content_frame, width=250, height=60)
        self.pretty_math_display.grid(row=3, column=0, sticky=W)

        self.scrollbar = Scrollbar(self.content_frame, orient="horizontal", command=self.pretty_math_display.xview)
        self.scrollbar.grid(row=4, column=0, sticky=EW)
        self.pretty_math_display.configure(xscrollcommand=self.scrollbar.set)

        guess_frame = ttk.Frame(self.content_frame)
        guess_frame.grid(row=6, column=0, sticky=W, pady=4)
        guess_label = ttk.Label(guess_frame, text="Enter an initial guess: ")
        guess_label.grid(row=0, column=0, sticky=W)
        self.guess_entry = ttk.Entry(guess_frame, width=10)
        self.guess_entry.insert(0, "0")
        self.guess_entry.grid(row=0, column=1, sticky=W)

        plot_button = ttk.Button(self.content_frame, text="Plot", command=self.execute_method)
        plot_button.grid(row=99, column=0, sticky=W)
        return
    
    def print_pretty_math(self):
        func_input = self.math_input_entry.get()

        # Sanitize the input: allow valid characters and functions
        # This regex allows digits, operators, x, whitespace, parentheses, and common functions
        valid_pattern = r"^(?:\d+|\b(?:x|asin|acos|atan|sin|cos|tan|exp|ln|log|sqrt)\b|\+|\-|\*{1,2}|\^|\/|\(|\)|\s)+$"
        if not re.match(valid_pattern, func_input):
            self.input_error_label.config(text="Invalid input.\nPlease use only numbers, x, and mathematical\noperators.")
            self.valid_expression = False
        
        else:
            # Replace '^' with '**' for Python syntax
            func_input = func_input.replace('^', '**')

            try:
                self.input_error_label.config(text="")
                expr = sp.sympify(func_input)
                latex_expr = sp.latex(expr)
                derivative = expr.diff(self.x)

                self.f = sp.lambdify(self.x, expr, 'numpy')
                self.df = sp.lambdify(self.x, derivative, 'numpy')

                self.render_latex(latex_expr)  
                self.valid_expression = True 

            except (ValueError, TypeError) as e:
                # Handle the specific exceptions
                # self.input_error_label.config(text=f"Error: {str(e)}")
                pass

            except sp.SympifyError:
                self.input_error_label.config(text="Invalid input.\nPlease enter a valid mathematical expression.")
                pass
        return  
    
    def render_latex(self, latex_expr):
        # Render the LaTeX expression to an image using matplotlib.
        # We use matplotlib instead of sympy.preview() to avoid packaging actual LaTeX
        # We avoid using plt.rcParams['text.usetex'] for the same reason
        try:
            # Create a figure and axis
            fig, ax = plt.subplots(figsize=(3, 0.5))
            ax.text(0,0.9, f"${latex_expr}$", fontsize=18, ha='left', va='top')
            ax.axis('off')  # Hide axes

            # Save the figure to a file
            plt.savefig('latex_output.png', bbox_inches='tight', pad_inches=0, facecolor='#F0F0F0', edgecolor='none')
            plt.close(fig)  # Close the figure to free memory

            self.display_image('latex_output.png')
        except Exception as e:
            messagebox.showerror("Error", f"Could not render LaTeX: {e}")
        return

    def display_image(self, image_path):
        # Load the image using PIL
        img = Image.open(image_path)
        self.pretty_function = ImageTk.PhotoImage(img)

        # Clear the canvas and display the new image
        self.pretty_math_display.delete("all")
        self.pretty_math_display.create_image(0, 0, anchor=NW, image=self.pretty_function)
        self.pretty_math_display.image = self.pretty_function  # Keep a reference to avoid garbage collection
        
        # Set the scrollregion for the image
        self.pretty_math_display.config(scrollregion=self.pretty_math_display.bbox("all"))
        return

    def execute_method(self):
        guess = self.guess_entry.get()
        # try:
        guess = float(guess)
        self.input_error_label.config(text="")
        if self.valid_expression:
            root, x_history, error_code = self.newton_method(self.f, self.df, guess)
            self.newton_ax.clear()
            self.plot_function_and_tangents(self.f, self.df, x_history)
            self.plots_canvas.draw()
        else:
            self.input_error_label.config(text="Can not plot. Function input is not a valid expression.")
        # except: 
        #     self.input_error_label.config(text="Initial guess must be a number.")
        return
    
    def newton_method(self, f, df, x0, tol=1e-6, max_iter=100):
        """
        Finds the root of a function using Newton's method.

        Parameters:
        f (function): The function whose root is to be found.
        df (function): The derivative of the function f.
        x0 (float): The initial guess for the root.
        tol (float): The tolerance for the root.
        max_iter (int): The maximum number of iterations.

        Returns:
        float: The root of the function.
        list: The history of x values at each iteration.
        """
        error_code = None
        x = x0
        x_history = [x]
        for i in range(max_iter):
            fx = f(x)
            print(f"Approximate root for iteration {i+1} is {x:.6f}")
            if abs(fx) < tol:
                return x, x_history, error_code
            dfx = df(x)
            if dfx == 0:
                print("Derivative is zero at the current point, can not continue.")
                error_code = "0 derivative"
                return x, x_history, error_code
            x = x - fx / dfx
            x_history.append(x)
        print("Maximum number of iterations reached without convergence.")
        error_code = "max iterations"
        return x, x_history, error_code
    
    def plot_function_and_tangents(self, f, df, x_history):
        # Define the range for x values
        x_min = min(x_history + [-2]) - 0.05
        x_max = max(x_history + [2]) + 0.05
        x = np.linspace(x_min, x_max, 500)

        # Plot the function
        self.newton_ax.plot(x, [f(xi) for xi in x], label='Function')

        cmap = plt.get_cmap('Dark2')  # Color map for each iteration
        for i in range(len(x_history)):
            xi = x_history[i]
            fx = f(xi)
            dfx = df(xi)
            if dfx != 0:
                x_int = xi - fx / dfx
                this_color = cmap(i / max(1, len(x_history) - 1))
                self.newton_ax.plot([xi, x_int], [fx, 0], '--', color=this_color, label=f'Iteration {i+1}')  # Tangent line
                self.newton_ax.plot([xi, xi], [fx, 0], '--', color=this_color)                               # Vertical line to function
                self.newton_ax.plot(xi, fx, 'o', color=this_color, markersize=7)

        self.newton_ax.plot(x_history[-1], f(x_history[-1]), 'ro', markersize=10, label='Root')
        self.newton_ax.axhline(y=0, color='r', linestyle='-')                                               # Highlight x-axis
        self.newton_ax.set_xlabel('x')
        self.newton_ax.set_ylabel('f(x)')
        self.newton_ax.set_title('Newton\'s Method')
        self.newton_ax.legend()
        self.newton_ax.grid()

        plt.show(block=False)
        plt.pause(0.1)
        return

    
if __name__ == '__main__':
    main()
