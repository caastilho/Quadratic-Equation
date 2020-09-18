from tkinter.font import Font

from local_tools import convert, mapped, equationRoots, addPoints
from math import sqrt, ceil


# Parabola shape class: "Parabola"
class Parabola:

    def __init__(self, canvas, image, terms):
        self.canvas = canvas
        self.width = canvas.winfo_width()
        self.height = canvas.winfo_height()
        self.previous = None

        # Setup fonts & colors
        self.root_font = Font(family="Cambria", size="18")
        self.plane_color = convert(85, 82, 100)
        self.background = image

        # Setup dimensions
        self.amount = 10
        self.length = 250

        self.X = self.width / 2
        self.Y = self.height / 2

        # Setup entries
        self.a_entry = terms[0]
        self.b_entry = terms[1]
        self.c_entry = terms[2]


    # Change the equation
    def run(self, roots):
        
        # Get terms
        self.a = self.a_entry.get(1)
        self.b = self.b_entry.get(0)
        self.c = self.c_entry.get(0)

        size_x = abs(-self.b / (2 * self.a))
        size_y = abs(-((self.b ** 2) - 4 * self.a * self.c) / (4 * self.a))
        size = max(int(size_x), int(size_y), 1) * 3

        self.y_size = size
        self.x_size = size

        new = [self.a, self.b, self.c]

        # Get parabola settings  
        if self.previous == None or self.previous != new:
            self.canvas.delete("trash")
            self.getRoots(roots)
            self.getPoints()

            # Call functions
            self.plane()
            self.parabola()

        # Set previous
        self.previous = new


    # Draw methods
    def plane(self):
        root_config = {"fill": self.plane_color, "font": self.root_font}

        x_increment = (self.length * 2) / (self.x_size * 2)
        y_increment = (self.length * 2) / (self.y_size * 2)
        closest = 10 ** (len(str(self.x_size)) - 1)

        color = self.plane_color
        offset = 15
        major_size = 10

        # Create axis lines
        self.canvas.create_line(self.X, self.Y-self.length-offset, self.X, self.Y+self.length+offset, fill=color, width=2, tags="trash")
        self.canvas.create_line(self.X-self.length-offset, self.Y, self.X+self.length+offset, self.Y, fill=color, width=2, tags="trash")

        # Create largets root
        self.canvas.create_text(self.X-self.length+5, self.Y+5, text=self.x_size, anchor="nw", **root_config, tags="trash")
        self.canvas.create_text(self.X+10, self.Y-self.length+10, text=self.y_size, anchor="nw", **root_config, tags="trash")

        # Create X axis
        for trace in range(self.x_size):

            # Get size
            size = major_size / 2
            if trace % (closest*5) == 0 and trace != 0: size = major_size
            elif trace % closest != 0: continue 

            x_value_positive = self.X + ((trace + 1) * x_increment)
            x_value_negative = self.X + ((trace + 1) * -x_increment)
            self.canvas.create_line(x_value_positive, self.Y-size, x_value_positive, self.Y+size, fill=color, tags="trash")
            self.canvas.create_line(x_value_negative, self.Y-size, x_value_negative, self.Y+size, fill=color, tags="trash")
        
        # Create Y axis
        for trace in range(self.y_size):

            # Get size
            size = major_size / 2
            if trace % (closest*5) == 0 and trace != 0: size = major_size
            elif trace % closest != 0: continue 

            y_value_positive = self.Y + ((trace + 1) * y_increment)
            y_value_negative = self.Y + ((trace + 1) * -y_increment)
            self.canvas.create_line(self.X-size, y_value_positive, self.X+size, y_value_positive, fill=color, tags="trash")
            self.canvas.create_line(self.X-size, y_value_negative, self.X+size, y_value_negative, fill=color, tags="trash")

    def parabola(self):
        
        # Draw points
        self.canvas.create_polygon(self.points, 
            fill="", 
            outline="red", 
            width=1.3, 
            tags="trash", 
            smooth=1
        )


    # Get methods
    def getRoots(self, roots):

        # Get roots
        self.root_1, self.root_2 = roots

        # Get groups
        if self.root_1[1] == 0: self.group = "Real"
        else: self.group = "Lateral"
        
    def getPoints(self):
        self.points = list()
        length = self.length * 2
        offset = -1 if self.a < 0 else 1
    
        # Especial points
        y = self.y_size * offset
        x = equationRoots(self.a, self.b, -y)
        addPoints(self, x[0][0], y)
        addPoints(self, x[0][0], y, [0, -50 * offset])

        # Get bounds
        start = mapped(x[0][0], -self.x_size, self.x_size, 0, length)
        stop = mapped(x[1][0], -self.x_size, self.x_size, 0, length)
        increment = (length - start - (length - stop)) / (self.amount - 1)

        # Get points
        for index in range(self.amount):
            x_value = mapped(start + index * increment, 0, self.length*2, -self.x_size, self.x_size)
            y_value = (self.a * x_value**2) + (self.b * x_value) + self.c
            addPoints(self, x_value, y_value)


        # Especial points
        addPoints(self, x[1][0], y)
        addPoints(self, x[1][0], y, [0, -50 * offset])
