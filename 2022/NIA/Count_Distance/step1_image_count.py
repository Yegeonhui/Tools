import json
import os
import numpy as np
from dict import debris_garbage_dict
import pandas as pd
from glob import glob

def getjson(jsonfile):
    with open(jsonfile) as j:
        objects = json.load(j)
    
    return objects

# 이미지내 객체 비율
def ratio_of_objects(objects):
    # size of image
    height = objects['imageHeight']
    width = objects['imageWidth']

    imagesize = height * width 

   # object ratio in image 
    object_ratio_arr = [] 
    maxratio = 0
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
        if maxratio < (object_size / imagesize * 100):
            maxratio = (object_size / imagesize * 100)
        object_ratio_arr.append((label, object_size / imagesize * 100))
           
    return maxratio, object_ratio_arr 
    
# 이미지 내 객체 개수
def count_objects(objects):
    object_dic = debris_garbage_dict()
    for o in range(len(objects['shapes'])):
        label = objects['shapes'][o]['label']
        object_dic[label] += 1
    
    return object_dic

# 객체 개수의 최대치가 여러개 인지 확인 
def check_arr(object_dic):
    #최대치가 여러개이다.
    flag = True

    checkarr = []
    for key, value in object_dic.items():
        if max(object_dic.values()) == value:
            checkarr.append(key)

    if len(checkarr) == 1: 
        flag = False

    return checkarr, flag
# 근, 중, 원인지 
def split_distance(maxratio):
    #원
    if maxratio <= 20:
        return 2
    #중
    if maxratio <= 60: 
        return 1
    #근
    else:
        return 0

arr = []
# 근, 중, 원거리
dict0 = debris_garbage_dict()
dict1 = debris_garbage_dict()
dict2 = debris_garbage_dict()
total_dict = debris_garbage_dict()

for idx, (root, dirs, files) in enumerate(os.walk('test')):
    jsonarr = [Json for Json in files if Json.lower().endswith('json')]
    for Json in jsonarr:
        dirname  = root.split('\\')[1]
        name = os.path.splitext(Json)[0]
        print(name)

        jsonfile = os.path.join(root, name + '.json')
        objects = getjson(jsonfile)
        
        # 라벨링 객체가 없는 경우
        if len(objects['shapes']) == 0:
            continue
    
        # maxratio : 근, 원, 중 인지 판별
        # object_ratio_arr : 오브젝트별 이미지 내 차지하는 비율
        maxratio, object_ratio_arr = ratio_of_objects(objects)

        # count objects
        try:
            object_dic = count_objects(objects)    
        except Exception as e:
            print('클래스명 오류', e)
        
        # 객체 개수가 제일 큰게 여러개 인지 판별
        checkarr, flag = check_arr(object_dic)
        
        # 객체 개수가 최대인 것이 여러개인 경우, 
        # 여러개 중 제일 큰 비율을 차지하는 라벨명
        if flag:
            maxratio = 0
            for label, ratio in object_ratio_arr:
                if label in checkarr:
                    if maxratio < ratio:
                        maxratio = ratio 

            for label, ratio in object_ratio_arr:
                if maxratio == ratio:
                    maxlabel = label    
        else:
            maxlabel = checkarr[0]    
        

        flag = split_distance(maxratio)

        if flag == 0:
            dict0[maxlabel] += 1
        elif flag ==1:
            dict1[maxlabel] += 1
        else:
            dict2[maxlabel] += 1
        total_dict[maxlabel] += 1
        # 밀집도 확인
        arr.append(maxratio)

df0 = pd.DataFrame(list(dict0.items()), columns=['classname', '근'])
df1 = pd.DataFrame(list(dict1.items()), columns=['classname', '중'])
df2 = pd.DataFrame(list(dict2.items()), columns=['classname', '원'])
# 합계
df3 = pd.DataFrame(list(total_dict.items()), columns=['classname', '합계'])

df = pd.concat([df0, df1.iloc[:, [1]], df2.iloc[:, [1]], df3.iloc[:, [1]]], axis=1)

# 거리별 클래스 총합

# 근, 중, 원
dist0 = 0
dist1 = 0
dist2 = 0
dist3 = 0
for r in range(len(df)):
    dist0 += df.iloc[r, 1]
    dist1 += df.iloc[r, 2]
    dist2 += df.iloc[r, 3]
    dist3 += df.iloc[r, 4]

df = df.append({'근' : dist0, '중' : dist1, '원' : dist2, '합계' : dist3}, 
                ignore_index=True)

df.to_excel(dirname + '.xlsx')


        

            