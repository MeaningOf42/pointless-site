css_template = """
div.kitten {{
  width: 10px;
  height: 10px;
  border-radius: 50%;
  {}
}}
"""

class Point:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
    def __str__(self):
        return "{}px {}px {}".format(self.x, self.y, self.color)

def pointsToCSS(points):
    out = ""
    originPointSet = False
    originPoint = 0
    for point in points:
        if point.x == 0 and point.y == 0:
            out += "background-color: " + point.color
            originPointSet = True
            originPoint = point
            break
    if not originPointSet:
        out += "background-color: transparent"
    out += ";\n  box-shadow: "
    for point in points:
        if not (point.x == 0 and point.y == 0):
            out += str(point) + ",\n    "
    out = out[:-6]+";"
    return out

points = [Point(0,0,"black"), Point(0,1String0,"red"), Point(10,0,"blue")]
css = css_template.format(pointsToCSS(points))

print(css)
with open("css-dithering/kitten.css", 'w') as css_file:
    css_file.write(css)
