import os
from PIL import Image, ImageOps

subdirectory = "model-ground-truth"
gtfile = open("base-ground-truth.txt")
# split base-ground-truth txt into multiple images per line
lines = gtfile.read().split('\n')
for (n, line)  in enumerate(lines[:-1]):
    # write a file for each line
    open("./model-ground-truth/model-ground-truth-line{}".format(n+1) + ".gt.txt", "w" ).write(line)
    # create the corresponding image with Text2Image.  See text2image --help to change options
    os.system("text2image --ptsize=14 --xsize=14400 --ysize=300 --exposure=-1 --fonts_dir=./fonts --strip_unrenderable_words --leading=32 --char_spacing=0.0 --exposure=0 --outputbase=\"" + "./model-ground-truth/model-ground-truth-line{}".format(n+1) + "\" --font=\"tintin\" --text=\"" + "./model-ground-truth/model-ground-truth-line{}".format(n+1) + ".gt.txt" + "\" --resolution=300")
    # remove the box file that is only need for Tesseract 3.x training.
    os.remove("./model-ground-truth/model-ground-truth-line{}".format(n+1) + ".box")
    # Save the cropped to text image
    image=Image.open("./model-ground-truth/model-ground-truth-line{}".format(n+1) + ".tif") 
    invert_im = ImageOps.invert(image.convert('RGB'))
    x1,y1,x2,y2=invert_im.getbbox() 
    im1 = image.crop((x1, y1, x2, y2)) 
    im1.save("./model-ground-truth/model-ground-truth-line{}".format(n+1) + ".tif") 