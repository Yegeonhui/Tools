"""
2022-08-03
조식동물 json 속성값 체크
1. json파일이 없는 jpg파일 error
2. imageData가 None이 아닌부분 None처리 
3. 라벨링 안된 json파일 error
4. 속성값이 19개가 아닌경우 error
Code by YGH
"""
# 2022-08-03
# 조식동물 속성값 체크
# 속성값 19개가 아니면 오류
#
import json
import os
import shutil


def getjson(jsonfile):
    with open(jsonfile) as Jsonfile:
        objects = json.load(Jsonfile)
    return objects

attribute_error = []
for idx, (root, dirs, files) in enumerate(os.walk('file')):
    jsonlist = [img for img in files if img.lower().endswith('.json')]
    for j in jsonlist:
        name = os.path.splitext(j)[0]
        print(name)
        Img = os.path.join(root, name) + '.jpg'
        Json = os.path.join(root, name) + '.json'
        try:
            objects = getjson(Json)
        except:
            os.makedirs('json파일error', exist_ok=True)
            shutil.move(Img, 'json파일error/' + name + '.jpg')
            shutil.move(Json, 'json파일error/' + name + '.json')
        
        if objects['imageData'] != None:
            objects['imageData'] = None

        if len(objects['shapes']) == 0:
            os.makedirs('라벨링안한것/', exist_ok=True)
            shutil.copy2(Img, '라벨링안한것/' + name + '.jpg')
            shutil.copy2(Json, '라벨링안한것/' + name + '.json')

        if len(objects) != 19:
            os.makedirs('속성19error', exist_ok=True)
            shutil.copy2(Img, '속성19error/' + name + '.jpg')
            shutil.copy2(Json, '속성19error/' + name + '.json')
            attribute_error.append(Json)

print(attribute_error)

