"""
2023-03-28
YOLOV8-segmentation 학습용 데이터셋 만드는 코드 
1. tile 영상(대부분 5000*5000*3) 
2. resize 후 4차원 데이터셋 생성 (batch, 2560, 2560, 3)
3. 4차원데이터셋 4분할 -> (batch *4, 1280, 1280, 3)
3. mask에 contour 추출 후 coco dataset 형식으로 저장
"""

import os
import json 
import cv2
import numpy as np

"""
json파일 불러오는 함수
Args : 
        jsonfile : json파일 경로

Return : 
        objects : json파일 내부 dict

"""
def getjson(jsonfile):
    with open(jsonfile, 'rb') as f:
        objects = json.load(f)
    return objects


def show(tif, mask):
    rtif = cv2.resize(tif, (500, 500))
    rmask0 = cv2.resize(mask[:, :, 0], (500, 500))
    rmask1 = cv2.resize(mask[:, :, 1], (500, 500))
    rmask2 = cv2.resize(mask[:, :, 2], (500, 500))
    
    cv2.imshow('tiff', rtif)
    cv2.imshow('0', rmask0)
    cv2.imshow('1', rmask1)
    cv2.imshow('2', rmask2)
    cv2.waitKey(0)


"""
json파일로 mask 만들기 
Arg : 
        objects : json파일 내부 dict
Return : 
        mask : json  vhdlsxm 

"""
def makemask(objects):
    h, w, c = tif.shape
    mask0 = np.zeros((h, w))
    mask1 = np.zeros((h, w))
    mask2 = np.ones((h, w)) * 255.
    for s in objects['shapes']:
        label = s['label']
        points = s['points']
        points = np.array(points, np.int32)
        if label == 'Compost':
            mask0 = cv2.fillPoly(mask0, [points], 255)
        else:
            mask1 = cv2.fillPoly(mask1, [points], 255)
        mask2 = cv2.fillPoly(mask2, [points], 0)
    mask = cv2.merge((mask0, mask1, mask2))
    return mask


"""
batch 이미지를 split 하는 함수 
Args :
        cnt : 몇번째로 들어오는 이미지 인지
        img : split하는 이미지 or mask 
Return : 
        new_image : 분할 한 후 합친 이미지 
"""
def splitimage(img):
    new_image = np.zeros((4, size, size, 3))
    new_image[0, :, :, :] = img[:size, :size, :]
    new_image[1, :, :, :] = img[size:, :size, :]
    new_image[2, :, :, :] = img[:size, size:, :]
    new_image[3, :, :, :] = img[size:, size:, :]
    return new_image


def mask_to_YOLO(mask, i):
    # open txt
    f = open(save_path + '/' + str(i) + '.txt', 'w')
    for c in range(mask.shape[2] - 1):
        # 야적퇴비 0, 야적퇴비_C 1
        
        cmask = np.array(mask[:, :, c], np.uint8)
        #ret, binary = cv2.threshold(cmask, 127, 255, cv2.THRESH_BINARY)
        contour, hierarchy = cv2.findContours(cmask, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        for con in contour:
            coor = np.array(con, np.int32)
            coor = coor.reshape(coor.shape[0] * coor.shape[1] * coor.shape[2])

            # 상대좌표로 변경
            coor = coor / size
            f.write('{} '.format(c))
            for idx, co in enumerate(coor):
                f.write('{} '.format(co))
            f.write('\n')
    f.close()


"""
클래스 txt생성
Args:
        savepath : 저장할 경로
"""                    
def make_classestxt():
    f = open(save_path + '/classes.txt', 'w')
    for key, value in class_dict.items():
        f.write(key + '\n')
    f.close()
    
    
# 객체 dictinary 
class_dict = {'Compost' : 0, 'Compost_C' : 1}
save_path = 'YOLO_Dataset'
size = 1280

# tif 파일 갯수
tifcount = 0
for idx, (root, dirs, files) in enumerate(os.walk('Image')):
    image_arr = [img for img in files if img.lower().endswith('tif')]
    for tif in image_arr:
        tifcount += 1
print('tif파일 : ', tifcount)

# 클래스 txt 생성
os.makedirs(save_path, exist_ok=True)
make_classestxt()
try:
    cnt = 0
    for idx, (root, dirs, files) in enumerate(os.walk('Image')):
        image_arr = [img for img in files if img.lower().endswith('tif')]
        for tif in image_arr:
            name = os.path.splitext(tif)[0]
            print(name)
                    
            tiffile = os.path.join(root, name + '.tif')
            jsonfile = os.path.join(root, name + '.json')

            ff = np.fromfile(tiffile, np.uint8)
            tif = cv2.imdecode(ff, cv2.IMREAD_UNCHANGED)[:, :, :3]
            
            objects = getjson(jsonfile)
            mask = makemask(objects)
            
            # 크기가 5000이 아니면 제로패딩 5000*5000으로 설정
            h, w, c = tif.shape 
            if h != 5000 or w != 5000:
                tif = cv2.copyMakeBorder(tif, 0, 5000-h, 0, 5000-w, cv2.BORDER_CONSTANT, value=[0, 0, 0])
                mask = cv2.copyMakeBorder(tif, 0, 5000-h, 0, 5000-w, cv2.BORDER_CONSTANT, value=[0, 0, 255])

            tif = cv2.resize(tif, (size*2, size*2))
            mask = cv2.resize(mask, (size*2, size*2))
            new_tif = splitimage(tif)
            new_mask = splitimage(mask)

            for i in range(4):
                # 검은 배경은 continue
                if np.sum(new_tif[i, :, :, :]) == 0.0:
                    continue
            
                # save 
                cv2.imwrite(save_path + '/' + str(i + cnt) + '.jpg', new_tif[i, :, :, :])
                mask_to_YOLO(new_mask[i, :, :, :], i + cnt)
            
            new_mask
            cnt += 1
except:
    print('error')

        



        
            
                
            




            
