
# Import modules
from PIL import Image, ImageTk
import platform, os

from tkinter import Tk
from tkinter import Canvas
from local_tools import convert

from scenes.Inputs import Inputs
from scenes.Parabola import Parabola


# Main app class: "Launch"
class Launcher(Tk):

    def __init__(self):
        super().__init__()

        # Call methods
        self.construct()
        self.canvas()
        self.looper()

        # End mainloop
        self.mainloop()


    # Construtuct environment 
    def construct(self): 
        """Construct environment."""

        # Get geometry
        self.WIDTH = 1280; self.HEIGHT = 720
        xoff = (self.winfo_screenwidth()  - self.WIDTH)  // 2
        yoff = (self.winfo_screenheight() - self.HEIGHT) // 2

        geometry = f"{self.WIDTH}x{self.HEIGHT}+{xoff}+{yoff}"

        # Setup instances
        system = platform.system()
        if system == "Linux": 
            image = "assets/background.png"
            icon = os.getcwd() + "/assets/icon.ico"
            
            # Setup icon
            loaded = Image.open(icon)
            icon = ImageTk.PhotoImage(loaded)
            self.tk.call("wm", "iconphoto", self._w, icon)

        elif system == "Windows": 
            image = "assets\\background.png"
            icon = "assets\\icon.ico"

            # Setup icon
            self.iconbitmap(icon)
        
        background = Image.open(image)
        self.BACKGROUND = ImageTk.PhotoImage(background)
        self.one = self.BACKGROUND

        # Configure root
        self.resizable(0, 0)
        self.title("Quadratic Equation")
        self.geometry(geometry)

    def canvas(self):
        """Create canvas object."""

        size = 500

        # Create inputs canvas
        self.MAIN_CANVAS = Canvas(self, highlightthickness=0)
        self.MAIN_CANVAS.place(x=0, y=0, width=self.WIDTH, height=self.HEIGHT)
        self.update()

        self.MAIN_CANVAS.create_image(0, 0, image=self.BACKGROUND, anchor="nw")
        self.INPUTS = Inputs(self, self.MAIN_CANVAS)
        terms = self.INPUTS.getInputs()

        # Create shape canvas
        self.SHAPE_CANVAS = Canvas(self, highlightthickness=0)
        self.SHAPE_CANVAS.place(x=self.WIDTH-50, y=self.HEIGHT/2, width=size, height=size, anchor="e")
        self.update()

        self.SHAPE_CANVAS.create_image(size+50, size/2, image=self.BACKGROUND, anchor="e")
        self.PARABOLA = Parabola(self.SHAPE_CANVAS, self.BACKGROUND, terms)


    # Loop canvas
    def looper(self):
        """Loop events."""

        roots = self.INPUTS.run()
        self.PARABOLA.run(roots)

        self.after(5, self.looper)


# Launch app
if __name__ == "__main__":
    Launcher()
