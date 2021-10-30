# Tesseract 4 Ground Truth Builder Tools
Build new ground truth train data for Tesseract 4

## Overview

1. Ground Truth made from real images
2. Ground Truth made from text2Image
3. Training

## Prerequesites

### Ground truth from real images
Python 3.6 or higher, opencv-python, opencv-contrib-python, tesseract, pytesseract and the trained data for the language of your choice.  On Windows, it uses Notepad++, on Linux, Gedit.  Edit the python script to use the editor of your choice.

### Ground truth from text2image
Python 3.6 or higher, tesseract text2image utility


## Ground Truth made from real images

Put your images in the Images folder.
Run:
```bash
gtbuilder_img.py [Path containing the Images folder] [Base Tesseract Trained Data]
````
For instance:
````bash
gtbuilder_img.py D:\Temp\GTBuilder\Images eng
````
This will bring up each image individually and let you select the line to extract.  When you move your cursor over the image, you will see that it changes to a cross.  You should then be able to "rope and zone" the region of interest.  Once you are satisfied with the selection, hit enter.  This will now bring up your text editor with the text recognized by Tesseract.  You can then edit it for misread character and save it.  The snippet of the image and the text will be saved in the `model-ground-truth` folder.  The image is then moved to the `Images-done` folder and the process start again for the next image until all images are done.

## Ground Truth made from text2image

Prior to Tesseract 4, it was possible to build training images containing entire page of training text.  This was done with the program text2image.  This is still available in Tesseract 4.  The idea is:

1. Create a text containing multiple line of text (base-ground-truth.txt).  A carriage return is needed after each sentence or line.
2. Place your font in a ./fonts folder where the script is executed
2. The code splits the base-ground-truth text in individual files containing a single line of text for each font to be trained on
3. It then creates an image with Text2Image for all those individual files
4. Finally, it autocrops them to remove any white border

To execute, run:
````bash
gtbuilder_text2image.py [Font to use in training]
````
Notice:  On Windows, it may be difficult to run text2Image.  Make sure it runs first in a command prompt.  If you get the error "Unable to open '/tmp/fonts.conf' for writing", add to the text2Image instructions `--fontconfig_tmpdir=C:/Users/youruser/Documents/folder_to_write_the_font_cache`.

## Training

Combine base truth data made from real images with the one made with Text2Image.
Train as per instruction provided on [Tesseract training page](https://github.com/tesseract-ocr/tesstrain)
