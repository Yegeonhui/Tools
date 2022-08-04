import json
import os
import numpy as np
import shutil

def getjson(jsonfile):
    with open(jsonfile) as j:
        objects = json.load(j)
    return objects

def ratio_of_objects(objects):
    # size of image
    height = objects['imageHeight']
    width = objects['imageWidth']

    imagesize = height * width 

   # object ratio in image 
    object_ratio_arr = []  
    for o in range(len(objects['shapes'])):
        label = objects['shapes'][o]['label']
        points = np.array(objects['shapes'][o]['points'])

        # bbx
        if objects['shapes'][o]['shape_type'] == 'rectangle':
            object_width = abs(points[0, 0] - points[1, 0])
            object_height = abs(points[0, 1] - points[1, 1])

        # polygon
        else:
            y = points[:, 0]
            x = points[:, 1]

            object_height = max(y) - min(y)    
            object_width = max(x) - min(x)     

         # size of objects  
        object_size = object_height * object_width
        object_ratio_arr.append(object_size / imagesize * 100)
    return object_ratio_arr

threshold = 10
os.makedirs('greater_then_threshold', exist_ok=True)
for idx, (root, dirs, files) in enumerate(os.walk('test')):
    imgarr = [img for img in files if img.lower().endswith('jpg')]
    for img in imgarr:
        name = os.path.splitext(img)[0]
        print(name)

        imgfile = os.path.join(root, img)
        jsonfile = os.path.join(root, name + '.json')
        objects = getjson(jsonfile)

        ratio_arr = ratio_of_objects(objects)
        for ratio in ratio_arr:
            # threshold 보다 큰 경우
            if ratio > threshold:
                shutil.move(imgfile, 'greater_then_threshold/' + name + '.jpg')
                shutil.move(jsonfile, 'greater_then_threshold/' + name + '.json')
                break