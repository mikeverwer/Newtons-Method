from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tooltip import ToolTip
import os
import re
import sympy as sp
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from PIL import Image, ImageTk
# import ctypes
# ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("SimulationDefault.MikeVerwer")

plt.rcParams['mathtext.fontset'] = 'stix'  # Use STIX fonts for math text


def main():
    app = NewtonApp()
    app.mainloop()


class NewtonApp(Tk):
    # The app is a subclass of a Tk() object. This way, we can simply call `self` instead of `self.root`.
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.header = "Newton's Method"
        self.title(self.header)
        icon_data = b'iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAACXBIWXMAAA7DAAAOwwHHb6hkAAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAABUBJREFUaIHV2VuMXWUVB/DfmltvQy+2trRIgSGaWGIQIyKagg8+GG8kpBoTozFgwosWEh/EN030SZM+mRijidrESKIRAUNQ46UQaDTxFo1QFSilLWA70E7tTJnL8uHbp3PYPWc655yNA//ky5y99p69//+9Lt/6vh24Ds97fWLbCJ7PzGMrzaQfRIQhXLLSRAbBEA5ExK0rTaRfDGErfhIRP4iI8ZUm1CsC2XZ8CB/OzH+uEJ+eEBE7hmq2t+CxiNi9EoT6wRAer9k245cR8ckV4NMzhvBBfLdmX4X9EfGF/z+l3rEjM+FOzCs50T6+mJleiwM7zguoDHtwtiZgAXesNNllCaiMuzFVEzGLD6004WUJqE7chDM1EVO47tUnlVEfSwmol1GQmQfwMcy1mcfx44jY2FemLYEIEWFthA24FNuUargOoxFGIgxHiAv+V/FAx2YuIm7Hd2rmB/DRrF7BgMRXYRMm8AbswjDG8Cz+g+N4CcfwsqrQZMqI6BxCNTftc2Fl2jtgmAyRm8k95D7yIDlNPkeeqf6eJP9OPkx+mbyWvJxcS46Ue3TJgZqAUTxSE/BfXD2AgPeRXyWfqIjPkwtk1sYCeY48TD5I3kVeSa4rItZcdlEBlYidOFkT8St0TbAuxNeRHyHvJ6e6kO42zpF/Jr9Evo0cZ2LnsgRUIj7VIZQ+0wP5cfID5KPkXA/E28c0eYj8LPlm3j+xbAGViPtqAo5h3TLf/A3kveRMn+TbPfEYeRuf39WxjC6Bz1Xx38J2pQXpighjVbLdhpuVPmsQjCrr+Bu5ZaInAZn5jFKV2nF3RGztdH21ZN2MG/AOrO+d74W3VUS8l0u39+oB+LpSn1u4BHu7XLtGmZhuxBXVw5vAEC5na88hJDNP42s18x0RsabdEGFYEXeFEmqbNCegwpq39uMB+DZOtB1vQX0BNKq0AtuVMFro81ndsJqRDX0JyMxpRUQ77oqIoPQ2SjuwUemhRpUWoWHEeL8egG8qbXYL1+Bd1e9hiz1N6xntjWFDiLm+BVQN4L0188dbd8ZI9XtWacaaxjzzpwbxAPyodrynCqPWRDenrPDmmZ33ih2cgTHHzNFBBTyoLHRa2Il3Lz7ANGb4yyaOr204j09x4uBAAqpkfqBmvkV51fOYZf9VPPSe0nVMD/K4dpzDEQ4/OagH4Ke1493Oh889q9m/lyPBE0oqNJLLx/E9HjrchIDfeWVwv5PLVmOBu+/k+Mby+eEZHErytP6TIZW1+m/K+MbkwAIy8wW076WOcex6tlzLiU+XFDmKJzH3KKOP47QSYr1iGj/Ht3CYxVI3KB5W9lVb2M3kTYwNF65j2PI0N9+jzBcv4u3KDD7k4i1GKm78RUX+j5nmIpoT8Ahubzv+BLlrsRC9hImvsOqoEgInFQ+0+qT1lYh6RCxgRvFw680fy1wsZ00J+Eft+JrF589h5rfsu09pLc4qa4rncBWuxhurcxuUGbxF/Cn8XvHwrzHbTr5JAV2+J7Sq6fy+ivR8RexFJSSexZ+UZm99JWBGmb3/hSP4K6YyO5evRgRk5mRETCp7O/WzhzjbmisWKnJnMamszsax2mIezCiJM6VqQTK7V62mPAD/1lGA72fmAkScd8nLiohhJR+iGq1zC5nLq1JNCngK19dsiR+eP8jFHe+q5Z5ru27JN90NTQo41cF2MDOf7nRxm5iB0MRM3MKZDrb7G7x/RzQpYKqDrd7oNY5X0wMv4G8N3r8jmsyBP+BnyjbKm3CgiS34i2HJ7wOvdUTEjhFsqzYTXo/Y9j+E8Ah+V+UfsQAAAABJRU5ErkJggg=='
        icon = PhotoImage(data=icon_data)
        self.iconphoto(True, icon)
        # self.iconbitmap(default='icon.ico')

        self.x = sp.symbols('x')
        
        # Window Creation
        self.build_window()
        self.update_idletasks()  # wait until the window is finished
        self.position_window()
        self.do_bindings()
    

    def position_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = self.winfo_width()
        window_height = self.winfo_height()
        x_pos = (screen_width - window_width) // 2
        self.geometry(f"+{x_pos}+25")

    
    def build_window(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        mainframe = ttk.Frame(self, padding=(4, 4, 4, 4))
        mainframe.grid(row=0, column=0, sticky=(N, E, S, W))
        mainframe.rowconfigure(0, weight=1)
        mainframe.columnconfigure(1, weight=1)

        base_canvas = Canvas(mainframe, background='white')
        base_canvas.grid(row=0, column=1, sticky=(N, E, S, W))
        base_canvas.rowconfigure(0, weight=1)
        base_canvas.columnconfigure(0, weight=1)

        control_panel = ttk.Frame(mainframe)
        self.build_control_panel(control_panel)
        control_panel.grid(row=0, column=0, sticky=(N, E, S, W))

        return
    

    def do_bindings(self):
        self.function_input_entry.bind("<Any-KeyRelease>", lambda event: self.print_pretty())

    
    def print_pretty(self):
        func_input = self.function_input_entry.get()

        # Sanitize the input: allow valid characters and functions
        # This regex allows digits, operators, x, whitespace, parentheses, and common functions
        valid_input_pattern = r"^(?:\d+|\b(?:x|asin|acos|atan|sin|cos|tan|exp|ln|log|sqrt)\b|\+|\-|\*{1,2}|\^|\/|\(|\)|\s)+$"
        if not re.match(valid_input_pattern, func_input):
            self.input_error_label.config(text="Invalid input. Please use only numbers, x, and mathematical operators.")
            pass
        
        else:
            # Replace '^' with '**' for Python syntax
            func_input = func_input.replace('^', '**')

            try:
                self.input_error_label.config(text="")
                expr = sp.sympify(func_input)
                latex_expr = sp.latex(expr)

                self.render_latex(latex_expr)   

            except (ValueError, TypeError) as e:
                # Handle the specific exceptions
                # self.input_error_label.config(text=f"Error: {str(e)}")
                pass

            except sp.SympifyError:
                self.input_error_label.config(text="Invalid input. Please enter a valid mathematical expression.")
                pass
        return
    
    
    def render_latex(self, latex_expr):
        # Render the LaTeX expression to an image using matplotlib
        try:
            # Create a figure and axis
            fig, ax = plt.subplots(figsize=(4, 1))  # Adjust size as needed
            ax.text(0,0.9, f"${latex_expr}$", fontsize=18, ha='left', va='top')
            ax.axis('off')  # Hide axes

            # Save the figure to a file
            plt.savefig('latex_output.png', bbox_inches='tight', pad_inches=0, facecolor='#F0F0F0', edgecolor='none')
            plt.close(fig)  # Close the figure to free memory

            # Load the image and display it on the canvas
            self.display_image('latex_output.png')
        except Exception as e:
            messagebox.showerror("Error", f"Could not render LaTeX: {e}")


    def display_image(self, image_path):
        # Load the image using PIL
        img = Image.open(image_path)
        # width, height = img.size
        # print(f"Image size: {width} x {height} pixels")
        # img = img.resize((width, height), Image.LANCZOS)  # Resize image to fit canvas
        self.pretty_function = ImageTk.PhotoImage(img)

        # Clear the canvas and display the new image
        self.pretty_function_display.delete("all")
        self.pretty_function_display.create_image(0, 0, anchor=NW, image=self.pretty_function)
        self.pretty_function_display.image = self.pretty_function  # Keep a reference to avoid garbage collection
        
        self.pretty_function_display.config(scrollregion=self.pretty_function_display.bbox("all"))  


    def build_control_panel(self, control_panel):
        frame: ttk.Frame = control_panel
        frame.rowconfigure(1, weight=1)
        header_frame = ttk.Frame(frame)
        header_frame.grid(row=0, column=0, sticky=(N, W), padx=10, pady=10)
        name_label = ttk.Label(header_frame, text=self.header, font="_ 24 bold")
        name_label.grid(row=0, column=0, columnspan=1000, sticky=E)
        ToolTip(name_label, "This is a ToolTip.")

        self.content_frame = ttk.Frame(frame)
        self.content_frame.grid(row=1, column=0, sticky=(N, S))

        function_input_string = "Enter the function f(x):"
        function_input_label = ttk.Label(self.content_frame, text=function_input_string, font="Times")
        function_input_label.grid(row=0, column=0, sticky=W)

        self.input_error_label = ttk.Label(self.content_frame, text="")
        self.input_error_label.grid(row=1, column=0, sticky=W)

        # # Define a custom style for the ttk.Entry widget
        # cambria_math_font = font.Font(family="Cambria Math", size=14)
        # style = ttk.Style()
        # style.configure("Custom.TEntry", background="lightgray", foreground="black", font=cambria_math_font)
            
        self.function_input_entry = ttk.Entry(self.content_frame, width=30, font="Times")
        self.function_input_entry.insert(0, "sin(5*x) - x + exp(x) - 2")
        self.function_input_entry.grid(row=2, column=0)

        self.pretty_function_display = Canvas(self.content_frame, width=250, height=60)
        self.pretty_function_display.grid(row=3, column=0, sticky=W)

        self.scrollbar = Scrollbar(self.content_frame, orient="horizontal", command=self.pretty_function_display.xview)
        self.scrollbar.grid(row=4, column=0, sticky=EW)
        self.pretty_function_display.configure(xscrollcommand=self.scrollbar.set)

        # self.print_pretty()

        print_pretty_button = ttk.Button(self.content_frame, text="Print Pretty", command=self.print_pretty)
        print_pretty_button.grid(row=5, column=0)
        
        return

    
if __name__ == '__main__':
    main()
