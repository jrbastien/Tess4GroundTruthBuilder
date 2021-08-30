import cv2
import numpy as np
import os
import pytesseract
from PIL import Image
from shutil import move
import sys
import platform

def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)

#check if arguments are valid
if len(sys.argv) != 3:
	print ('usage:', sys.argv[0], '[Path containing the Images folder] [Base Tesseract Trained Data]')
	sys.exit(0)
imgfolderpath0 = os.path.join(sys.argv[1],"Images")
isDirectory = os.path.isdir(imgfolderpath0)
if isDirectory is False:
    print ('No Images folder found in the given path')
    sys.exit(0)

CurrentPlatform=platform.platform(aliased=0, terse=0)

#select the path where the "Images" folder is located
imgfolderpath = sys.argv[1]
#print (os.listdir(imgpath))
all_files = os.listdir(imgfolderpath+"/Images")
for file in sorted(all_files):
    if file.endswith((".tiff", ".tif", ".jpg", ".png")):
        #finding resolution with Pillow
        a= Image.open(os.path.join(imgfolderpath,"Images", file))
        hdpi=a.info['dpi'][0]
        scale = 300/hdpi
        #reading image with OpenCV
        a= cv2.imread(os.path.join(imgfolderpath, "Images", file))
        width = int(a.shape[1]*scale)
        height = int(a.shape[0]*scale)
        dim = (width, height)
        #changing its size to size at 300 dpi
        a= cv2.resize(a, dim, interpolation=cv2.INTER_CUBIC)

        #use a downsized image for display so it fits in the monitor.  Change width or height to your liking
        #resize = ResizeWithAspectRatio(a, width=1280) # Resize by width OR
        resize = ResizeWithAspectRatio(a, height=640) # Resize by height 
        
        # Select ROI
        print (file)
        fromCenter = False
        winname = str(file) + "- Please select the line to OCR"
        cv2.namedWindow(winname)        # Create a named window
        cv2.moveWindow(winname, 40,30)  # Move it to (40,30)
        cv2.imshow(winname, resize)
        r = cv2.selectROI(winname,resize, fromCenter)
        print("Text selected:")

        # Crop 300 dpi image
        (ho, wo) = a.shape[:2]
        (hr, wr) = resize.shape[:2]
        ratio = hr/ho
        imCrop = a[int(r[1]/ratio):int((r[1]+r[3])/ratio), int(r[0]/ratio):int((r[0]+r[2])/ratio)]

        # Read line with Tesseract
        ocrtext = pytesseract.image_to_string(imCrop, lang=sys.argv[2], config="-c textord_heavy_nr=1").strip()
        print(ocrtext)

        # write cropped image at 300 dpi
        currentdir = os.path.abspath(os.getcwd())
        gt_path = os.path.join(currentdir, "model-ground-truth")
        if not os.path.exists(gt_path):
            os.makedirs(gt_path)
        filetif = os.path.splitext(file)[0] + ".tif"
        cv2.imwrite(os.path.join(gt_path, filetif),imCrop)
        im = Image.open(os.path.join(gt_path, filetif)).convert("L")
        im.save(os.path.join(gt_path, filetif), dpi=(300,300), compression=None)

        # write the ground truth text
        gt_txt_path=os.path.join(gt_path, os.path.splitext(file)[0] + ".gt.txt")
        gtfile = open(gt_txt_path,'w', newline="\n")
        gtfile.write(ocrtext + "\n")
        gtfile.close
        gtfile.flush()
        # call Notepad++ in Windows or nano on linux - whatever you like
        if CurrentPlatform.startswith('Windows'):
            os.system("Notepad++.bat "+ str(gt_txt_path))
        elif CurrentPlatform.startswith('Linux'):
            os.system("gedit "+ str(gt_txt_path))
        cv2.destroyWindow(winname)

        #move image to Images-done folder
        os.makedirs(os.path.join(imgfolderpath,"Images-done"), exist_ok=True)
        move(os.path.join(imgfolderpath,"Images", file), os.path.join(imgfolderpath,"Images-done", file))