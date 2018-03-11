from PIL import Image, ImageDraw # Needed for image manipulation
import webcolors # needed to rename rgb colors to css named colors

class Point:
    # A Point just stores it's position and color with the
    # beifit of easily being able to use it for a string that
    # works as a css box-shadow.
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
    def __str__(self):
        return "{}px {}px {}".format(self.x, self.y, self.color)

def pointsToCSS(points):
    # pointsToCSS takes a list of points and returns CSS for
    # the background color and box shadows.
    out = ""
    # if there is a point with pos 0,0 have the background
    # color be it's color. If not the background color should
    # be transparent.
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

    # For each additional point add a box shadow.
    out += ";\n  box-shadow: "
    for point in points:
        if not (point.x == 0 and point.y == 0):
            out += str(point) + ",\n    "
    out = out[:-6]+";"
    return out

def rgb_to_css_color(rgb):
    # rgb to css color uses webcolor to see if there is a named
    # css color equivilent to the rgb color passed in, and if not
    # returns a string in the form "rgb(1,2,3)"
    try:
        return webcolors.rgb_to_name(rgb)
    except ValueError:
        return "rgb"+str(rgb)

scale = 4 # scale is how much image is scaled from the jpeg to CSS.
          # having the css image bigger allows us to show off that
          # the image is dithered by using a border radius to turn
          # each css "pixel" (box-shadow) into a circle.
css_template = """
div.kitten {{
  width: {}px;
  height: {}px;
  border-radius: 50%;
  {}
}}
""" # The css_template for the CSS. Scale gets put in the first
    # two {}s, and the background color and box shadows get put
    # in the last {}.


# Opens up the image of the kitten
kitten = Image.open("css_dithering/create_css/kitten.jpeg")
kitten.show()
imageSize = kitten.size

# Creates a new blank image.
outImage = Image.new('RGB', imageSize, (255, 255, 255))

# Loads the images pixels so they can be manipulated.
outPixels = outImage.load()
inPixels = kitten.load()

# Creates an empty list of points. (see Point class)
points = []

# Sets up number of colors used in dithering
numColors = 4
colorFactor = numColors-1

# Next block does the dithering and adds points to the points list.

# Loop through all pixel indexes.
for y in range(imageSize[1]):
    for x in range(imageSize[0]):

        # Get the original pixel, round it to the nearest color in the pallet,
        # then get the error between the actual pixel's color and the color that
        # was used.
        inPixel = kitten.getpixel((x,y))
        outPixel = tuple(map(lambda x: int(round(x*colorFactor/255)*255/colorFactor), inPixel))
        pixelError = tuple(map(lambda a, b: a-b, inPixel, outPixel))

        # The next block moves the error to the surrounding pixels as per the
        # Floyd-Steinberg image dithering algorithm.

        # The tupplets in the list contain: the x offset, the y offset,
        # and the amount of error to be transferred to the pixel with that
        # displacement.
        for offset in [(1,0,7/16), (-1,1,3/16), (0,1,5/16), (1,1,1/16)]:
            # Gets the absulote value of the pixel to add the error to
            # using the current position and the offset.
            moveErrorToX = x+offset[0]
            moveErrorToY = y+offset[1]

            # Checks the pixel to add the error to is in the image.
            if moveErrorToX > 0 and moveErrorToX < imageSize[0] \
            and moveErrorToY > 0 and moveErrorToY < imageSize[1]:
                # Adds error to the pixel.
                oldPixel = kitten.getpixel((moveErrorToX, moveErrorToY))
                newPixel = tuple(map(lambda a, b: a + int(b * offset[2]), oldPixel, pixelError))
                inPixels[moveErrorToX, moveErrorToY] = newPixel

        # Writes outPixel to the image
        outPixels[x,y] = outPixel

        # Adds a point with the color of outPixel and correct position to points.
        points.append(Point(x*scale, y*scale, rgb_to_css_color(outPixel)))

# shows the output image.
outImage.show()

# Takes out all white points, as background is allready white.
points = list(filter(lambda a: a.color != "white", points))

# Creates the final CSS by formatting the css_template.
css = css_template.format(scale, scale, pointsToCSS(points))

#print(css)

# Writes the CSS to kitten.css
with open("css_dithering/kitten.css", 'w') as css_file:
    css_file.write(css)
