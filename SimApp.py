from tkinter import *
from tkinter import ttk
from tkinter import colorchooser
from tooltip import ToolTip
import os
import ctypes
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("SimulationDefault.MikeVerwer")


def main():
    app = SimulationApp(pan='y', zoom='y')
    app.mainloop()


class Simulation(Canvas):
    def __init__(self, parent, **kwargs):
        self.parent = parent
        canvas_args: dict = {}
        self.make_pannable = False
        self.make_zoomable = False
        for key, value in kwargs.items():
            if key in ["pan", "zoom"]:
                self.handle_kwarg(key, value)
            else:
                canvas_args[key] = value       
        super().__init__(parent, **canvas_args)
        self.do_binds()

        self.pattern_image = self.create_pattern_image(20, 20)  # Create a pattern image
        self.bind("<Configure>", self.on_configure)
        self.bind("<Button-1>", self.give_coords)

    def give_coords(self, event):
        canvasx = self.canvasx(event.x)
        canvasy = self.canvasy(event.y)
        print(f"Canvas X/Y: ({canvasx}, {canvasy})\nEvent X/Y : ({event.x}, {event.y})")

    def create_pattern_image(self, width, height):
        pattern_image = PhotoImage(width=width, height=height)
        for x in range(width):
            for y in range(height):
                if x % 20 == 0:
                    pattern_image.put("#000000", (x, y))
                if y % 20 == 0:
                    pattern_image.put("#000000", (x, y))
        return pattern_image

    def on_configure(self, event):
        self.delete("pattern")  # Clear existing pattern
        width = event.width
        height = event.height
        for x in range(0, width, 20):
            for y in range(0, height, 20):
                self.create_image(x, y, image=self.pattern_image, anchor=NW, tags="pattern")

    def handle_kwarg(self, key, value):
        if key == "pan" and value:
            self.make_pannable = True
        elif key == "zoom" and value:
            self.make_zoomable = True

    def do_binds(self):
        self.bind("<Control-Button-1>", self.give_coords)
        if self.make_zoomable:
            self.bind("<MouseWheel>", self.do_zoom) # WINDOWS ONLY
        if self.make_pannable:
            self.bind('<ButtonPress-2>', lambda event: self.scan_mark(event.x, event.y))
            self.bind("<B2-Motion>", lambda event: self.scan_dragto(event.x, event.y, gain=1))

    def give_coords(self, event):
        canvasx = self.canvasx(event.x)
        canvasy = self.canvasy(event.y)
        print(f"Canvas X/Y: ({canvasx}, {canvasy})\nEvent X/Y : ({event.x}, {event.y})")

    def do_zoom(self, event):
        x = self.canvasx(event.x)
        y = self.canvasy(event.y)
        factor = 1.001 ** event.delta
        self.scale(ALL, x, y, factor, factor)


class Sketchpad(Simulation):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.bind("<Button-1>", self.save_position)
        self.bind("<B1-Motion>", self.add_line)
        self.drawing_colour = StringVar(value='black')
        self.thickness = IntVar(value=2)

    def save_position(self, event):
        self.last_x, self.last_y = self.canvasx(event.x), self.canvasy(event.y)

    def add_line(self, event):
        x, y = self.canvasx(event.x), self.canvasy(event.y)
        self.create_line((self.last_x, self.last_y, x, y), width=2, fill=self.drawing_colour.get())
        self.last_x, self.last_y = x, y


class SimulationApp(Tk):
    # The app is a subclass of a Tk() object. This way, we can simply call `self` instead of `self.root`.
    def __init__(self, controls_frame: ttk.Frame | Frame = None, simulation: Simulation = None, 
                 scrollbars="", scrollregion: tuple = None, pan="", zoom="", **kwargs):
        super().__init__(**kwargs)
        self.header = "Default Simulation"
        self.title(self.header)
        icon_data = b'iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAACXBIWXMAAA7DAAAOwwHHb6hkAAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAABUBJREFUaIHV2VuMXWUVB/DfmltvQy+2trRIgSGaWGIQIyKagg8+GG8kpBoTozFgwosWEh/EN030SZM+mRijidrESKIRAUNQ46UQaDTxFo1QFSilLWA70E7tTJnL8uHbp3PYPWc655yNA//ky5y99p69//+9Lt/6vh24Ds97fWLbCJ7PzGMrzaQfRIQhXLLSRAbBEA5ExK0rTaRfDGErfhIRP4iI8ZUm1CsC2XZ8CB/OzH+uEJ+eEBE7hmq2t+CxiNi9EoT6wRAer9k245cR8ckV4NMzhvBBfLdmX4X9EfGF/z+l3rEjM+FOzCs50T6+mJleiwM7zguoDHtwtiZgAXesNNllCaiMuzFVEzGLD6004WUJqE7chDM1EVO47tUnlVEfSwmol1GQmQfwMcy1mcfx44jY2FemLYEIEWFthA24FNuUargOoxFGIgxHiAv+V/FAx2YuIm7Hd2rmB/DRrF7BgMRXYRMm8AbswjDG8Cz+g+N4CcfwsqrQZMqI6BxCNTftc2Fl2jtgmAyRm8k95D7yIDlNPkeeqf6eJP9OPkx+mbyWvJxcS46Ue3TJgZqAUTxSE/BfXD2AgPeRXyWfqIjPkwtk1sYCeY48TD5I3kVeSa4rItZcdlEBlYidOFkT8St0TbAuxNeRHyHvJ6e6kO42zpF/Jr9Evo0cZ2LnsgRUIj7VIZQ+0wP5cfID5KPkXA/E28c0eYj8LPlm3j+xbAGViPtqAo5h3TLf/A3kveRMn+TbPfEYeRuf39WxjC6Bz1Xx38J2pQXpighjVbLdhpuVPmsQjCrr+Bu5ZaInAZn5jFKV2nF3RGztdH21ZN2MG/AOrO+d74W3VUS8l0u39+oB+LpSn1u4BHu7XLtGmZhuxBXVw5vAEC5na88hJDNP42s18x0RsabdEGFYEXeFEmqbNCegwpq39uMB+DZOtB1vQX0BNKq0AtuVMFro81ndsJqRDX0JyMxpRUQ77oqIoPQ2SjuwUemhRpUWoWHEeL8egG8qbXYL1+Bd1e9hiz1N6xntjWFDiLm+BVQN4L0188dbd8ZI9XtWacaaxjzzpwbxAPyodrynCqPWRDenrPDmmZ33ih2cgTHHzNFBBTyoLHRa2Il3Lz7ANGb4yyaOr204j09x4uBAAqpkfqBmvkV51fOYZf9VPPSe0nVMD/K4dpzDEQ4/OagH4Ke1493Oh889q9m/lyPBE0oqNJLLx/E9HjrchIDfeWVwv5PLVmOBu+/k+Mby+eEZHErytP6TIZW1+m/K+MbkwAIy8wW076WOcex6tlzLiU+XFDmKJzH3KKOP47QSYr1iGj/Ht3CYxVI3KB5W9lVb2M3kTYwNF65j2PI0N9+jzBcv4u3KDD7k4i1GKm78RUX+j5nmIpoT8Ahubzv+BLlrsRC9hImvsOqoEgInFQ+0+qT1lYh6RCxgRvFw680fy1wsZ00J+Eft+JrF589h5rfsu09pLc4qa4rncBWuxhurcxuUGbxF/Cn8XvHwrzHbTr5JAV2+J7Sq6fy+ivR8RexFJSSexZ+UZm99JWBGmb3/hSP4K6YyO5evRgRk5mRETCp7O/WzhzjbmisWKnJnMamszsax2mIezCiJM6VqQTK7V62mPAD/1lGA72fmAkScd8nLiohhJR+iGq1zC5nLq1JNCngK19dsiR+eP8jFHe+q5Z5ru27JN90NTQo41cF2MDOf7nRxm5iB0MRM3MKZDrb7G7x/RzQpYKqDrd7oNY5X0wMv4G8N3r8jmsyBP+BnyjbKm3CgiS34i2HJ7wOvdUTEjhFsqzYTXo/Y9j+E8Ah+V+UfsQAAAABJRU5ErkJggg=='
        icon = PhotoImage(data=icon_data)
        self.iconphoto(True, icon)
        # self.iconbitmap(default='icon.ico')
        
        # Window Creation
        self.build_window(control_panel=controls_frame, simulation=simulation, scrollbars=scrollbars, scrollregion=scrollregion, pan=pan, zoom=zoom)
        self.update_idletasks()  # wait until the window is finished
        self.position_window()
    

    def position_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = self.winfo_width()
        window_height = self.winfo_height()
        x_pos = (screen_width - window_width) // 2
        self.geometry(f"+{x_pos}+25")

    
    def build_window(self, control_panel, simulation, scrollbars, scrollregion, pan, zoom):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        mainframe = ttk.Frame(self, padding=(4, 4, 4, 4))
        mainframe.grid(row=0, column=0, sticky=(N, E, S, W))
        mainframe.rowconfigure(0, weight=1)
        mainframe.columnconfigure(1, weight=1)

        if not simulation:
            self.simulation: Simulation = Sketchpad(mainframe, background='white', pan=pan, zoom=zoom)
        else:
            self.simulation: Simulation = simulation
        self.simulation.grid(row=0, column=1, sticky=(N, E, S, W))
        self.simulation.rowconfigure(0, weight=1)
        self.simulation.columnconfigure(0, weight=1)

        if scrollregion:
            try:
                self.simulation.configure(scrollregion=scrollregion)
            except Exception as e:
                print(f"Could not set scroll region.\n{e}")
                pass

        if "h" in scrollbars:
            self.sim_Hscrollbar = ttk.Scrollbar(mainframe, orient='horizontal', command=self.simulation.xview)
            self.sim_Hscrollbar.grid(row=1, column=1, sticky=(E, W))
            if not scrollregion:
                self.simulation.config(scrollregion=self.simulation.bbox("all"))
            self.simulation['xscrollcommand'] = self.sim_Hscrollbar.set
        if "v" in scrollbars:
            self.sim_Vscrollbar = ttk.Scrollbar(mainframe, orient='vertical', command=self.simulation.yview)
            self.sim_Vscrollbar.grid(row=0, column=2, sticky=(N, S))
            if not scrollregion:
                self.simulation.config(scrollregion=self.simulation.bbox("all"))
            self.simulation['yscrollcommand'] = self.sim_Vscrollbar.set

        if not control_panel:
            control_panel = ttk.Frame(mainframe)
            self.build_control_panel(control_panel)
        control_panel.grid(row=0, column=0, sticky=(N, E, S, W))

        return
    
    
    def do_bindings(self):
        self.bind()
    

    def build_control_panel(self, control_panel):
        frame: ttk.Frame = control_panel
        frame.rowconfigure(1, weight=1)
        header_frame = ttk.Frame(frame)
        header_frame.grid(row=0, column=0, sticky=(N, W), padx=10, pady=10)
        name_label = ttk.Label(header_frame, text=self.header, font="_ 24 bold")
        name_label.grid(row=0, column=0, columnspan=1000, sticky=E)
        ToolTip(name_label, "This is a ToolTip.")

        content_frame = ttk.Frame(frame)
        content_frame.grid(row=1, column=0, sticky=(N, S))
        colour_button = ttk.Button(content_frame, text='Colour', command=self.set_colour)
        colour_button.grid(row=0, column=0)
        self.colour_display = Canvas(content_frame, bg=self.simulation.drawing_colour.get(), width=20, height=20)
        self.colour_display.grid(row=0, column=1, sticky=W)
        
        return
    
    def set_colour(self, event=None):
        new_colour = colorchooser.askcolor()[1]
        self.simulation.drawing_colour.set(new_colour)
        self.colour_display.config(bg=new_colour)

    
if __name__ == '__main__':
    main()
