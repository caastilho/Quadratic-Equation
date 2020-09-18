
# Convert RGBA to HEX
def convert(R, G, B, A=None):
    """Convert RGB color to HEX."""

    # Normal convertion
    if A == None: 
        R = f"{R:02x}"
        G = f"{G:02x}"
        B = f"{B:02x}"
    
    # Alpha convertion
    else:
        alpha_0 = (1 - A[0])
        alpha_1 = A[0]     

        R = str(int(alpha_0 * A[1][0] + alpha_1 * R))
        G = str(int(alpha_0 * A[1][1] + alpha_1 * G))
        B = str(int(alpha_0 * A[1][2] + alpha_1 * B))
    
    # Return value
    return f"#{R}{G}{B}"


# Get the roots of the equation
def equationRoots(a, b, c):
    """Return roots."""

    delta = (b**2) + (-4*a*c)

    # Real root
    if delta >= 0:
        root_1 = [(-b + delta ** 0.5) / (2 * a), 0]
        root_2 = [(-b - delta ** 0.5) / (2 * a), 0]
    
    # Lateral root
    elif delta < 0:
        imaginary = abs((abs(delta) ** 0.5) / (2 * a))
        root_1 = [-b / (2 * a), imaginary]
        root_2 = [-b / (2 * a), imaginary]

    return (root_1, root_2)


# Map values
def mapped(value, x1, y1, x2, y2):
    return x2 + (y2 - x2) * ((value - x1) / (y1 - x1))


# Filter values
def filterTerms(*values):
    """Filter equation terms"""

    a = values[0]
    b = values[1]
    c = values[2]


    #  "A"  T E R M  #
    a_term = f" {round(a, 2)}x²"
    if len(str(a).strip("-")) == 1: a_term = a_term.replace("1", "")

    #  "B"  T E R M  #
    b_term = f" + {abs(round(b, 2))}x" if b > 0 else f" - {abs(round(b, 2))}x"
    if len(str(b).strip("-")) == 1: b_term = b_term.replace("1", " ")
    if b == 0: b_term = ""
 
    #  "C"  T E R M  #
    c_term = f" + {abs(round(c, 2))}" if c > 0 else f" - {abs(round(c, 2))}"
    if c == 0: c_term = ""


    # Get equation
    equation = f"y ={a_term}{b_term}{c_term}"
    return equation

def filterRoots(r1, r2):
    """Filter roots"""

    # Get strings
    if r1[1] == r2[1] == 0:
            group = "As raízes são reais."
            roots = "{" + f"{round(r2[0], 4)}, {round(r1[0], 4)}" + "}"
            solution = f"S = {roots}"
        
    else: 
        group = "As raízes são complexas."
        roots = "{"+f"{round(r2[0], 3)} + {round(r2[1], 3)}i, {round(r1[0], 3)} - {round(r1[1], 3)}i"+"}"
        solution = f"S = {roots}"

    # Return
    return [group, solution]


# Get point
def addPoints(parabola, x, y, offset=None):
    """Convert parabola points"""

    x_value = parabola.X + mapped(x, -parabola.x_size, parabola.x_size, -parabola.length, parabola.length)
    y_value = parabola.Y - mapped(y, -parabola.y_size, parabola.y_size, -parabola.length, parabola.length)
    
    x_off = 0; y_off = 0
    if offset != None:
        x_off = offset[0]; y_off = offset[1]

    parabola.points.append((x_value + x_off, y_value + y_off))
