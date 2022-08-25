"""
2022-08-25
json파일 -> Yolo로 변경
Code by YGH
"""

import json
import os

def getjson(jsonfile):
    with open(jsonfile) as jsonfile:
        objects = json.load(jsonfile)
    return objects

def JSON_to_YOLO(name, objects):
    # open txt
    f = open(savepath, 'w')

    imageHeight = objects['imageHeight']
    imageWidth = objects['imageWidth']
    
    for i in range(len(objects['shapes'])):
        label = objects['shapes'][i]['label']
        points = objects['shapes'][i]['points']
        
        # json파일의 좌상단 x,y 우하단 x,y를 int형식으로 불러옴
        lefttopx = int(points[0][0])
        lefttopy = int(points[0][1])
        rightdownx = int(points[1][0])
        rightdowny = int(points[1][1])

        # YOLO형식의 바운딩박스 XYWH를 구함
        BboxW = abs(lefttopx - rightdownx) 
        BboxH = abs(lefttopy - rightdowny) 
        BboxX = (lefttopx + (BboxW / 2))
        BboxY = (lefttopy + (BboxH / 2)) 

        X = BboxX / imageWidth
        Y = BboxY / imageHeight
        W = BboxW / imageWidth
        H = BboxH / imageHeight

        f.write('{} {} {} {} {}\n'.format(class_dict[label], X, Y, W, H))

    f.close()


def make_classestxt(class_dict):
    f = open(dir + '/classes.txt', 'w')
    for key, value in class_dict.items():
        f.write(key + '\n')
    f.close()

dir = 'Bbox'
class_dict = {'Heliocidaris_crassispina' : '0', 'Conch' : '1', 'Asterina_pectinifera' : '2', 
              'Turbo_cornutus' : '3', 'Hemicentrotus' : '4', 'Sea_hare' : '5', 'Asterias_amurensis' : '6'}
# make classes.txt
# make_classestxt(class_dict)

for idx, (root, dirs, files) in enumerate(os.walk(dir)):
    jsonarr = list(j for j in files if j.lower().endswith('.json'))
    for file in jsonarr:
        name = os.path.splitext(file)[0]
        print(name)
        imagefile = os.path.join(root, name) + '.jpg'
        jsonfile = os.path.join(root, name) + '.json'

        objects = getjson(jsonfile)

        savepath = os.path.join(root, name) + '.txt'
        JSON_to_YOLO(savepath, objects)



        