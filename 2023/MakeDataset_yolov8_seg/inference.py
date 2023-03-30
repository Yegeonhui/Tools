"""
2023-03-28
YOLOv8 인퍼런스 프로그램
빨간색 : Compost
파란색 : Compost_C
"""

from ultralytics import YOLO
import cv2
import numpy as np
from glob import glob 

dir = '2021'
# dir = '2021'
model = YOLO('yolov8l-seg.pt')
tiff_arr = glob(dir + '/*.tif')

for tiff in tiff_arr:
    image = cv2.imread(tiff, cv2.IMREAD_UNCHANGED)
    rimage = cv2.resize(image, (1280, 1280))

    results = model(rimage)

    # 클래스
    cls = results[0].boxes.cls

    # 탐지가 안된경우 continue
    if len(cls) == 0:
        continue
    
    masks = results[0].masks
    mask_numpy = masks.data.cpu().numpy()

    for i in range(len(cls)):
        seg = np.array(masks.segments[i]) * 1280

        # Compost
        if cls[i] == 0:
            rimage = cv2.polylines(rimage, np.int32([seg]), 1, (0, 0, 255), 10)
        # Compost_C
        else:
            rimage = cv2.polylines(rimage, np.int32([seg]), 1, (255, 0, 0), 10)        
            
    rimage = cv2.resize(rimage, (1000, 1000))
    cv2.imshow('test', rimage)
    cv2.waitKey(0)
