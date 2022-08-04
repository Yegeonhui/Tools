import os
import json
import numpy as np
import shutil

def classname_check(f, objects):
    f.write('클래스 명 체크 중' + '\n')
    total_obj = len(objects['shapes'])
    for t in range(total_obj):
        if objects['shapes'][t]['label'] not in classname:
            f.write(objects['shapes'][t]['label'] + '가 잘못되었습니다.' + '\n')
            return False
        else:
            return True


def attribute_value(f, objects):
    f.write('속성 값 체크 중' + '\n')
    if len(objects) == 18:
        f.write('속성 개수 : ' + str(len(objects)) + '개로 속성값 정상' + '\n')
        return True
    else:
        f.write('속성 개수 : ' + str(len(objects)) + ' 개로 속성값 이상' + '\n')
        return False


def size(f, objects, minsize):
    total_obj = len(objects['shapes'])
    for t in range(total_obj - 1, -1, -1):
        points = objects['shapes'][t]['points'] 
        points = np.array(points, np.int32)
        # boundingbox
        if objects['shapes'][t]['shape_type'] == 'rectangle':
            lefttopx, lefttopy = points[0]
            rightdownx, rightdowny = points[1]

        #polygon
        else:
            x = points[:, 0]
            y = points[:, 1]
            lefttopx = min(x)
            rightdownx = max(x)
            lefttopy = min(y)
            rightdowny = max(y)
        w = max(lefttopx, rightdownx) - min(lefttopx, rightdownx)
        h = max(lefttopy, rightdowny) - min(lefttopy, rightdowny)

        area = w * h 
        if area <= minsize:
            f.write(str(objects['shapes'][t]['label']) + ' 크기가 작아 삭제되었습니다.' + '\n')
            del(objects['shapes'][t])     
    return objects
    

def savejson(objects, jsonfile):
    with open(jsonfile, 'w') as Jsonfile:
        json.dump(objects, Jsonfile, indent=4)


def getjson(jsonfile):
    with open(jsonfile) as Jsonfile:
        objects = json.load(Jsonfile)
    return objects


def check(f, jsonfile, minsize, path):
    jsonpath = path + '/' + jsonfile
    
    imagefile = os.path.splitext(jsonfile)[0] + '.jpg'
    print(imagefile)
    imagepath = path + '/' + imagefile
    
    os.makedirs(path + '/Done', exist_ok=True)

    # 사이즈가 작은 것은 삭제 -> 다시 저장 
    objects = getjson(jsonpath)
    objects = size(f, objects, minsize)
    
    savejson(objects, jsonpath)
    if classname_check(f, objects):
        classes = True
    else:
        classes = False
        
    if attribute_value(f, objects):
        attribute = True
    else:
        attribute = False    

    if classes and attribute:       
        shutil.move(jsonpath, path + '/Done/' + jsonfile)
        shutil.move(imagepath, path + '/Done/' + imagefile)
        #shutil.move(, path + '/Done/' + jsonfile)
        f.write('Done 폴더로 이동' + '\n')

classname = ['Echinoid', 'Starfish', 'SeaHare', 'Snail', 'EckloniaCava', 'Sargassum']