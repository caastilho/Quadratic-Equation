import tkinter
from tkinter.font import Font
from local_tools import mapped, convert


# Slicer class
class Slicer:
    """
    Custom slicer for tkinter.\n
    *values
        - canvas: surface to be draw
        -  value: default value
        -  start: start value
        -   stop: stop value
    
    **kwargs
        - color_x: gradient color start
        - color_y: gradient color stop
    """

    # Construct environment
    def __init__(self, *values, **kwargs):
        self.canvas = values[0]
        self.width = 255
        self.height = 8

        self.decimals = 2

        # Custom font
        self.value_font = Font(family="Cambria", size=16) 

        # Get values
        self.value = values[1]
        self.start = values[2]
        self.stop  = values[3]

        self.current_width = mapped(self.value, self.start, self.stop, 0, self.width)
        self.label_color = convert(195, 195, 195)
        self.backbar_offset = 3

        # Get color
        self.color = kwargs["color"]
        self.text_color = kwargs["text"]


    # Return the value
    def get(self):
        """Get the slicer values."""
        return round(self.value, self.decimals)


    # User's methods
    def place(self, x, y):
        """Place the slicer on canvas."""
        
        self.x = x
        self.y = y

        # Create bars
        self.back_bar = self.canvas.create_rectangle(
            x - self.backbar_offset - 1, y - self.height - self.backbar_offset - 1, 
            x + self.width + self.backbar_offset, y + self.height + self.backbar_offset, 
            fill="", outline=self.color
        )
        
        self.progress_bar = self.canvas.create_rectangle(
            x, y - self.height, x + self.current_width, y + self.height,
            fill=self.color, outline=""
        )

        # Create text 
        self.text = self.canvas.create_text(x + self.width + 15, y, 
            text=f"{int(self.value)}", fill=self.text_color, font=self.value_font, anchor="w"
        )

        # Bind bar
        self.canvas.tag_bind(self.back_bar, "<B1-Motion>", self.__onDrag)
        self.canvas.tag_bind(self.progress_bar, "<B1-Motion>", self.__onDrag)

        # Change items layer
        self.canvas.tag_raise(self.text)
        self.canvas.tag_raise(self.back_bar)
        self.canvas.tag_raise(self.progress_bar)

    def update(self):
        """Update coordinates and color"""

        # Update progress bar
        position = (self.x, self.y - self.height, self.x + self.current_width, self.y + self.height)
        self.canvas.coords(self.progress_bar, position[0], position[1], position[2], position[3])
        self.canvas.itemconfig(self.progress_bar, fill=self.color)

        # Update text
        self.canvas.itemconfig(self.text, text=f"{int(self.value)}")

    def click(self, event):
        """Click event"""

        if self.x < event.x <= self.x + self.width and self.y < event.y < self.y + self.height:
            self.value = int(mapped(event.x, self.x, self.x + self.width, self.start, self.stop))
            self.current_width = event.x - self.x


    # Bind methods
    def __onDrag(self, event):
        """Bind function on <B1-Motion>."""
        
        # If event is inside slider
        if self.x < event.x <= self.x + self.width:
            self.value = int(mapped(event.x, self.x, self.x + self.width, self.start, self.stop))
            self.current_width = event.x - self.x
        
        # If event is greater than width
        elif event.x > self.x + self.width:
            self.value = self.stop
            self.current_width = self.width
        
        # If event is smaller than x
        elif self.x < event.x:
            self.value = self.start
            self.current_width = self.x
