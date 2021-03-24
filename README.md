# Tess4GroundTruthBuilder
Build new ground truth train data  for Tesseract 4

## Overview

1. Ground Truth made from real images
2. Ground Truth made from text2Image
3. Training

## Prerequesites

Python 3.6 or higher, opencv-python and pytesseract

## Ground Truth made from real images

Put your images in the Images folder.
Edit line 89 of gtbuilder.py to use the text editor of your choice.  Run:
```bash
gtbuilder.py [Path containing the Images folder] [Base Tesseract Trained Data]
````
For instance:
````bash
gtbuilder.py D:\Temp\GTBuilder\Images eng
````
This will bring up each image individually and let you select the line to extract.  When you move your cursor over the image, you will see that it changes to a cross.  You should then be able to "rope and zone" the region of interest.  Once you are satisfied with the selection, hit enter.  This will now bring up your text editor with the text recognized by Tesseract.  You can then edit it for misread character and save it.  The snippet of the image and the text will be saved in the `model-ground-truth` folder.  The image is then moved to the `Images-done` folder and the process start again for the next image until all images are done.

## Ground Truth made from real images

Prior to Tesseract 4, it was possible to build training images containing entire page of training text.  This was used done with the program text2image.  This is still available in Tesseract 4.  The idea is:

1. Create a text containing multiple line of text (base-ground-truth.txt)
2. Split the base-ground-truth in individual files containing a single line of text for each font to be trained on
3. Create an image with Text2Image for all those individual files
4. Autocrop them to remove any white border

This is currently done with bash scripts and ImageMagick and this is partially hardcoded.  This will be rewritten in python.

## Training

Combine base truth data made from real images with the one made with Text2Image.
Train as per instruction provided on [Tesseract training page](https://github.com/tesseract-ocr/tesstrain)

