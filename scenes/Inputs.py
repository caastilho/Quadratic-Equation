from tkinter.font import Font

from local_tools import convert, equationRoots, filterRoots, filterTerms
from elements.entry import Entry


# Input area class: "Inputs"
class Inputs:

    def __init__(self, app, canvas):
        self.canvas = canvas
        self.app = app
        self.previous = None
        self.div_index = None

        self.height = canvas.winfo_height() 
        self.width = canvas.winfo_width()
        self.Y = self.height / 2    
        self.X = self.width / 4

        # Create fonts
        self.solution_font = Font(family="Cambria", size=26)
        self.group_font    = Font(family="Cambria", slant="italic", size=20)
        self.vertice_font  = Font(family="Cambria", size=20)


        # Create colors
        self.group_color = convert(85, 82, 100)

        # Create values
        self.a = 1
        self.b = 0
        self.c = 0

        self.to_delete = list()
        self.entries_indexes = list()
        self.entries = dict()

        # Setup slicers
        self.setupObjects()

    def setupObjects(self):
        """Setup slicers objects"""
        
        color = convert(255, 0, 0)
        offset = 200
        start = 36

        # Setup objects
        entries_names = [["a", "0"], ["b", None], ["c", None]]
        for index, value in enumerate(entries_names):
            exception = value[1]
            name = value[0]

            entry = Entry(self.canvas, f"{name.upper()} = ?", 175, name, exception)
            entry.coordinates(start+index*offset, self.Y)
            self.entries[name] = entry

        # Bind methods
        self.app.bind("<Button-1>", self.click)
        self.app.bind("<Key>", self.write)

    def getInputs(self):
        """Return slicers."""

        # Return variable
        terms = list(self.entries.values()) 
        return terms


    # Run methods
    def run(self):
        """Run methods."""
    
        # Get terms
        self.a = self.entries["a"].get(1)
        self.b = self.entries["b"].get(0)
        self.c = self.entries["c"].get(0)

        array = [self.a, self.b, self.c]

        if self.previous == None or array != self.previous:
            self.trash()   
            self.to_delete = list()
            self.equation()
        
        self.div()
        self.objects()
        self.previous = array


        # Check entry collision
        x, y = self.mouse()
        for entry in self.entries.values():
            entry.collision(x, y)

        # Return roots
        return (self.r1, self.r2)


    # Display methods
    def equation(self):
        """Display equations"""

        #  G E T   T E R M S  #
        self.r1, self.r2 = equationRoots(self.a, self.b, self.c)
        group, solution = filterRoots(self.r1, self.r2)
        equation = filterTerms(self.a, self.b, self.c)

        delta = (self.b ** 2) - 4 * self.a * self.c
        vertice = f"vértice = ({round(-self.b/(2*self.a), 3)}, {round(-delta/(4*self.a), 3)})"
        

        #  D R A W   T E R M S  #
        self.to_delete.append(self.canvas.create_text(36, 590, text=vertice, fill="white", font=self.vertice_font, anchor="w"))
        self.to_delete.append(self.canvas.create_text(36, 660, text=group, fill=self.group_color, font=self.group_font, anchor="w"))

        # Draw equation
        size = 35
        while True:

            # Get font
            font = Font(family="Cambria", weight="bold", size=size)

            # Draw equation
            index = self.canvas.create_text(
                self.X, self.Y-300, 
                text=equation, 
                font=font, 
                fill="white", 
                anchor="n"
            )

            # Break condition
            if self.canvas.bbox(index)[2] < (self.width / 2) - 20:
                self.to_delete.append(index)
                break
    
            self.canvas.delete(index)

            # Decrease value
            size -= 2


        # Draw solution
        size = 26
        while True:

            # Get font
            font = Font(family="Cambria", size=size)

            # Draw equation
            index = self.canvas.create_text(
                36, 600, 
                text=solution, 
                fill="white", 
                font=self.solution_font, 
                anchor="nw"
            )

            # Break condition
            if self.canvas.bbox(index)[2] < (self.width / 2) - 20:
                self.to_delete.append(index)
                break
    
            self.canvas.delete(index)

            # Decrease value
            size -= 2 

    def objects(self):
        """Update slicers."""   

        for entry in self.entries_indexes:
            self.canvas.delete(entry)

        # Update object
        for entry in self.entries.values(): 
            self.entries_indexes.extend(entry.create())

    def div(self):
        """Create division."""

        if self.div_index != None:
            self.canvas.delete(self.div)

        # Create div
        self.div_index = self.canvas.create_line(
            self.X*2 + 10, 50, self.X*2 + 10, self.height-50,
            fill=self.group_color
        )


    # Clear canvas
    def trash(self):
        """Delete items from canvas."""
        for item in self.to_delete: self.canvas.delete(item)


    # Bind events
    def click(self, event):
        """Handle click events.""" 

        # Check click event: "entries"
        for entry in self.entries.values():
            entry.click(event)

    def write(self, event):
        """Handle key events."""

        # Check key event: "entries"
        for entry in self.entries.values():
            entry.write(event)

    def mouse(self):
        """Get mouse position."""

        x = self.app.winfo_pointerx() - self.app.winfo_rootx()
        y = self.app.winfo_pointery() - self.app.winfo_rooty()
        return x, y
