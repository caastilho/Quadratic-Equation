from local_tools import convert
from tkinter.font import Font


# Custom entry class for python
class Entry:

    def __init__(self, canvas, default, length, var, exception=None):
        self.state = 0
        self.text = ""
        self.var = var.upper()
        self.exception = exception
        self.tick = 0
        self.canvas = canvas

        self.font_1 = Font(family="Cambria", size=18)
        self.font_2 = Font(family="Cambria", size=22)
        
        self.width = length
        self.height = 60
        self.default = default 
        self.color = convert(195, 195, 195)

        # Create image object
        self.create_underlines()

    def coordinates(self, x, y):
        """Define coordinates."""
        self.x = x
        self.y = y

    def create_underlines(self):
        """Create underlines settings for Entry."""

        self.lines = [
        (0, {"fill": convert(195, 195, 195), "width": 1}),
        (0, {"fill": convert(100, 100, 100), "width": 1}),
        (2, {"fill": convert(255, 0, 0), "width":2})
        ]


    # Get Entry text
    def get(self, default):
        """Get current entry text."""

        value = self.text.strip("-").strip("+").replace(".", "")

        # Exception
        try: 
            if int(value) == int(self.exception): return default
        except: 
            pass

        # Return value
        if value.isnumeric():
            return float(self.text)

        # Return default text
        else:
            return default


    # Draw entry on canvas
    def create(self):
        """Place entry on canvas."""

        settings = self.lines[self.state]
        
        new_x1 = self.x - settings[0]
        new_x2 = self.x + self.width + settings[0]
        color = settings[1].get("fill")

        # Create underline
        underline = self.canvas.create_line(new_x1, self.y, new_x2, self.y, **settings[1])
        
        # Create content: 0, 1
        if self.state != 2:
            
            # Get text
            text = self.default if self.text == "" else f"{self.var} = {self.text}"

            # Filter text
            if len(self.text) > 34:
                start = len(self.text) - 33
                text = self.text[start:]

            # Create text on canvas
            text = self.canvas.create_text(self.x + self.width / 2, self.y-10, 
                font=self.font_1, 
                text=text, 
                anchor="s", 
                fill=color
            )

            # Return "trash"
            return [text, underline]

        # Create content: 2
        else:

            text = self.text
            if len(self.text) > 33:
                start = len(self.text) - 33
                text = self.text[start:]

            # Draw text
            text_index = self.canvas.create_text(self.x + self.width / 2, self.y-10, 
                font=self.font_2, 
                text=f"{self.var} = {text}", 
                anchor="s", 
                fill=color
            )

            bounds = self.canvas.bbox(text_index)

            # Draw pointer
            pointer = 0
            if self.tick % 50 < 28:
                x = bounds[2]
                y = self.y - self.height + 20
                pointer = self.canvas.create_line(x, y, x, self.y - 10, fill=color)

            self.tick += 1
            self.tick %= 100

            # Return "trash"
            return [text_index, pointer, underline]


    # Interactions
    def collision(self, x, y):
        """Check mouse collision"""

        if self.state != 2:
            if self.x < x < self.x + self.width and self.y > y > self.y - self.height: self.state = 1
            else: self.state = 0

    def click(self, event):
        """Check mouse click."""

        x, y = (event.x, event.y)

        if self.x < x < self.x + self.width and self.y > y > self.y - self.height: 
            self.state = 2
            self.tick = 0

        else: 
            self.state = 0

    def write(self, key):
        """Write on the widget."""

        code = key.keycode
        key = key.char

        if self.state == 2:

            # Especial key: "delete"
            if key == "": 
                self.text = self.text[:-1]

            # Igonre especials keys
            elif len(repr(key)) > 3 or key == "\r" or code == 66: 
                pass

            # Normal key
            elif key in "+-" and self.text == "":
                self.text += key

            elif key.isnumeric() or key == ".":
                self.text += key
