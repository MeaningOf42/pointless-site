from PIL import Image, ImageDraw
import webcolors

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

def rgb_to_css_color(rgb):
    try:
        return webcolors.rgb_to_name(rgb)
    except ValueError:
        return "rgb"+str(rgb)

scale = 4
css_template = """
div.kitten {{
  width: {}px;
  height: {}px;
  border-radius: 50%;
  {}
}}
"""



kitten = Image.open("css_dithering/create_css/kitten.jpeg")
kitten.show()
imageSize = kitten.size

outImage = Image.new('RGB', imageSize, (255, 255, 255))
outPixels = outImage.load()

points = []
numColors = 4
colorFactor = numColors-1
for x in range(imageSize[0]):
    for y in range(imageSize[1]):
        inPixel = kitten.getpixel((x,y))
        outPixel = tuple(map(lambda x: int(round(x*colorFactor/255)*255/colorFactor), inPixel))
        outPixels[x,y] = outPixel
        points.append(Point(x*scale, y*scale, rgb_to_css_color(outPixel)))

outImage.show()

css = css_template.format(scale, scale, pointsToCSS(points))

#print(css)
with open("css_dithering/kitten.css", 'w') as css_file:
    css_file.write(css)
