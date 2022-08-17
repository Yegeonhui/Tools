import cv2
import numpy as np
import json
from copy import deepcopy

def getjson(jsonfile):
    with open(jsonfile) as Jsonfile:
        objects = json.load(Jsonfile)
    return objects


# 자르고 싶은 포인트
x = 1500
y = 3000

image = cv2.imread('Image/air1.tif')
image1 = cv2.imread('Image/air1.tif')
h, w, c = image.shape

jsonfile = 'Image/air1.json'
objects = getjson(jsonfile)

mask0 = np.zeros((h, w), np.uint8)
mask1 = np.zeros((h, w), np.uint8)
mask2 = np.zeros((h, w), np.uint8)

for obj in range(len(objects['shapes'])):
    points = objects['shapes'][obj]['points']
    points = np.array(points, np.int32)
    if objects['shapes'][obj]['label'] == "Road":    
        mask0 = cv2.fillPoly(mask0, [points], 255)
        image1 = cv2.polylines(image1, [points],True, (0, 0, 255), 2)
    elif objects['shapes'][obj]['label'] == "Arableland":    
        mask1 = cv2.fillPoly(mask1, [points], 255)
        image1 = cv2.polylines(image1, [points], True, (0, 255, 0), 2)
    elif objects['shapes'][obj]['label'] == "Forest":    
        mask2 = cv2.fillPoly(mask2, [points], 255)
        image1 = cv2.polylines(image1, [points], True, (255, 0, 0), 2)
    elif objects['shapes'][obj]['label'] == "Openspace":    
        mask0 = cv2.fillPoly(mask0, [points], 255)
        mask1 = cv2.fillPoly(mask1, [points], 255)
        image1 = cv2.polylines(image1, [points], True, (0, 255, 255), 2)

mask = cv2.merge((mask2, mask1, mask0))
image1_c = deepcopy(image1)
image_c = deepcopy(image)
mask_c = deepcopy(mask)

cv2.imwrite("Example_Image/image.jpg", image_c[x : x+ 500, y : y + 500, :])
cv2.imwrite("Example_Image/image_line.jpg", image1_c[x : x + 500, y : y + 500, :])
cv2.imwrite("Example_Image/mask.jpg", mask_c[x : x + 500, y : y + 500, :])