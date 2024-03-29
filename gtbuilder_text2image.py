import os
from PIL import Image, ImageOps
import sys

#check if arguments are valid
if len(sys.argv) != 2:
	print ('usage:', sys.argv[0], '[Font to use in training]')
	sys.exit(0)

subdirectory = "model-ground-truth"
os.makedirs(os.path.join(os. getcwd(),subdirectory), exist_ok=True) #create the model-ground-truth directory if not exist
gtfile = open("base-ground-truth.txt")
# split base-ground-truth txt into multiple images per line
lines = gtfile.read().split('\n')
for (n, line)  in enumerate(lines[:-1]):
    # write a file for each line
    gtfile = open("./model-ground-truth/model-ground-truth-line{}".format(n+1) + ".gt.txt", "w" )
    gtfile.write(line + "\n")
    gtfile.close()
    # create the corresponding image with Text2Image.  See text2image --help to change options
    os.system("text2image --ptsize=14 --xsize=14400 --ysize=300 --exposure=-1 --fonts_dir=./fonts --strip_unrenderable_words --leading=32 --char_spacing=0.0 --exposure=0 --outputbase=\"" + "./model-ground-truth/model-ground-truth-line{}".format(n+1) + "\" --font=\"" + sys.argv[1] + "\" --text=\"" + "./model-ground-truth/model-ground-truth-line{}".format(n+1) + ".gt.txt" + "\" --resolution=300")
    # delete the box file that is only need for Tesseract 3.x training.
    os.remove("./model-ground-truth/model-ground-truth-line{}".format(n+1) + ".box")
    # Save the cropped image
    image=Image.open("./model-ground-truth/model-ground-truth-line{}".format(n+1) + ".tif") 
    invert_im = ImageOps.invert(image.convert('RGB')) #convert to RGB
    x1,y1,x2,y2=invert_im.getbbox() #invert image as crop works on black pixels
    im1 = image.crop((x1, y1, x2, y2)) #crop the orinal image as per coordinates found on inverted image
    # Add a white border of 10 pixels around the image
    new_img = ImageOps.expand(im1, border=(10,10,10,10), fill="white")
    new_img.save("./model-ground-truth/model-ground-truth-line{}".format(n+1) + ".tif", dpi=(300,300)) 