This exercise in pointless coding was inspired by [The Coding Train's Coding Challenge #90](https://www.youtube.com/watch?v=0L2n8Tg2FwI&t=857s) which gave me the inspiration to try image dithering and [Wenting Zhang's "Make CSS your secret super drawing tool" talk](https://www.youtube.com/watch?v=Y0_FMCji3iE) that inspired me to display an image using only CSS.

You may notice that the html for this page only contains two tags, none of which are image tags. This is because the true magic goes on in the CSS and the python script used to create it.

First of: how does the page display an image without an image tag. Well css allows you to have an unlimited number of box shadows, all in different colors. I simply used css with enough box shadows to create an image. You can imagine doing this by hand would be an amazingly time consuming and tricky business, so I wrote a script to do it for me.

In the create_css folder there is a python script, create_css.py that uses an image of a kitten to create css that creates an image using box shadows. The script also uses  [Floyd-Steinberg dithering](https://en.wikipedia.org/wiki/Floyd%E2%80%93Steinberg_dithering) to stylize the image.
