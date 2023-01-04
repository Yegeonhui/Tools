"""
2022-09-22 
LX 라벨링 진행사항 체크 
polygon, bbox, object당 카운트, 라벨링 안한 이미지
1. 디렉터리를 순차적으로 탐색
2. json 형식은 polygon도 있고, bbox도 있음 
3. xml 형식은 bbox
Code by YGH
"""

import os
import json
import xml.etree.ElementTree as ET
import cv2

def getjson(Json):
    with open(Json) as jsonfile:
        objects = json.load(jsonfile)
    return objects 

def getxml(xml):
    tree = ET.parse(xml)
    xmlroot = tree.getroot()
    return xmlroot

def get_duration(filename):
    video = cv2.VideoCapture(filename)
    return video.get(cv2.CAP_PROP_FRAME_COUNT)

total_image = 0
total_polygon = 0 
total_bbox = 0
total_mp4 = 0
total_mp4_time = 0
bbox_dict = {'House_Normal' : 0, 'House_Abnormal' : 0, 'GreenHouse_Normal' : 0, 'GreenHouse_Abnormal' : 0}
poly_dict = {'GreenHouse_Abnormal' : 0}
for idx, (root, dirs, files) in enumerate(os.walk('(2022)LX')):
    image_arr = [img for img in files if img.lower().endswith('jpg')]
    json_arr = [Json for Json in files if Json.lower().endswith('json')]
    xml_arr = [xml for xml in files if xml.lower().endswith('xml')]
    mp4_arr = [mp4 for mp4 in files if mp4.lower().endswith('mp4')]
    mov_arr = [mov for mov in files if mov.lower().endswith('mov')]
    total_mp4 += len(mp4_arr)
    total_mp4 += len(mov_arr)
    total_image += len(image_arr)
    
    # 동영상 갯수, 시간 
    for mp4 in mp4_arr:
        mp4file = os.path.join(root, mp4)
        time = get_duration(mp4file)
        total_mp4_time += int(time / 30) 

    for mov in mov_arr:
        movfile = os.path.join(root, mov)
        time = get_duration(movfile)
        total_mp4_time += int(time/30)


    for Json in json_arr:
        jfile = os.path.join(root, Json)
        print(jfile)
        objects = getjson(jfile)
        # json 파일, 폴리곤
        if objects['shapes'][0]['shape_type'] == 'polygon':
            total_polygon += 1
            for obj in objects['shapes']:
                poly_dict[obj['label']] += 1

        # json 파일, 바운딩박스
        else:
            total_bbox += 1
            for obj in objects['shapes']:
                bbox_dict[obj['label']] += 1

    for xml in xml_arr:
        total_bbox += 1
        xmlfile = os.path.join(root, xml)
        print(xmlfile)
        xmlroot = getxml(xmlfile)
        for object in xmlroot.findall('object'):
            name = object.find('name').text
            bbox_dict[name] += 1

print('bbox object 당 갯수 : ', bbox_dict, '개')
print('polygon object 당 갯수 : ', poly_dict, '개')
print('전체이미지 : ', total_image)
print('전체 폴리곤 : ', total_polygon)
print('전체 바운딩박스 : ', total_bbox)
print('전체 동영상 : ', total_mp4)
print('전체 동영상 시간 : ', total_mp4_time, '초')