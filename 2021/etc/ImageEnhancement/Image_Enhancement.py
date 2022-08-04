import os
import cv2
from glob import glob
import numpy as np

class Image_Enhancement:
    def __init__(self, img):
        self.img = img


    def cannyedge(self, img):
        edges = cv2.Canny(img, 50, 200)
        return edges


    # 수동 normaliztion
    def hist_normalization(self, img):
        b, g, r = cv2.split(img)
        b = cv2.normalize(b, None, 40, 80, cv2.NORM_MINMAX)
        g = cv2.normalize(g, None, 90, 150, cv2.NORM_MINMAX)
        r = cv2.normalize(r, None, 40, 80, cv2.NORM_MINMAX)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.normalize(gray , None, 120, 130, cv2.NORM_MINMAX)
        img_norm2 = cv2.merge((g, g, g))
        return img_norm2


    def lab_Contrast(self, img):
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=3.0,tileGridSize=(8, 8))
        cl = clahe.apply(l)
        limg = cv2.merge((cl,a,b))
        final = cv2.cvtColor(limg,cv2.COLOR_LAB2BGR)
        return final


    def bgr_Contrast(self, img):
        b, g, r = cv2.split(img)
        clahe = cv2.createCLAHE(clipLimit=3.0,tileGridSize=(8, 8))
        cl_b = clahe.apply(b)
        cl_g = clahe.apply(g)
        cl_r = clahe.apply(r)
        cl_img = cv2.merge((cl_b, cl_g, cl_r))
        return cl_img


    def sharpening(self, img):
        sharpening_mask1 = np.array([[-1,-1,-1],[-1,9,-1],[-1,-1,-1]]) 
        sharpening_mask2 = np.array([[0,-1,0],[-1,5,-1],[0,-1,0]])

        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        
        sharpening_out1 = cv2.filter2D(gray,-1,sharpening_mask1) 
        sharpening_out2 = cv2.filter2D(gray,-1,sharpening_mask2)
        return sharpening_out1
        

    def Laplacian(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        Laplacian = cv2.Laplacian(img, -1)
        return Laplacian


    def sobelx(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        sobelx = cv2.Sobel(img, 3, 1, 1, ksize = 1)
        return sobelx


option = 'cannyedge'
option = 'lab_Contrast'
option = 'bgr_Contrast'
option = 'sharpening'
option = 'Laplacian'
option = 'sobelx'

route = os.getcwd() 
Imagelist = glob(route + "/Image/" + "*.jpg")
os.makedirs(option, exist_ok=True)
for idx, (root, dirs, files) in enumerate(os.walk('Image')):
    ImageList = [img for img in files if img.lower().endswith(".jpg")]
    for n in range(len(ImageList)):
        name = ImageList[n][:-4]
        print(name)
        img = cv2.imread(os.path.join(root, ImageList[n]))
        E = Image_Enhancement(img)
        if option == 'cannyedge':
            img = E.cannyedge(img)
        elif option == 'lab_Contrast':
            img = E.lab_Contrast(img)
        elif option == 'bgr_Contrast':
            img = E.bgr_Contrast(img)
        elif option == 'sharpening':
            img = E.sharpening(img)
        elif option == 'Laplacian':
            img = E.Laplacian(img)
        elif option == 'sobelx':
            img = E.sobelx(img)
        
        #img=cv2.resize(img,dsize=(300,550))
        cv2.imwrite(route + "/" + option + "/"+ name + ".jpg", img)
