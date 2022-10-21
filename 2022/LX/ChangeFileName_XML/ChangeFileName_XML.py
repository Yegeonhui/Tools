"""
2022-10-18
1. bbox 데이터셋 만들때 파일명 중복 확인 
2. 새로운 이름으로 변경
3. xml파일 파일명 수정
Code by YGH
"""

import os
import shutil
import xml.etree.ElementTree as ET


# pasre -> filename 수정 및 저장 
def change_filename(xmlfile, new_name):
    xml = ET.parse(xmlfile)
    xmlroot = xml.getroot()
    xmlroot.find('filename').text = new_name + '.JPG'
    tree = ET.ElementTree(xmlroot)
    tree.write('bbox_dataset/' + str(new_name) + '.xml')

os.makedirs('bbox_dataset', exist_ok=True)
cnt = 0
for idx, (root, dirs, files) in enumerate(os.walk('2022-10-18 bbox')):
    xml_arr = [xml for xml in files if xml.lower().endswith('xml')]
    for xml in xml_arr:
        print(cnt)
        name = os.path.splitext(xml)[0]
        xmlfile = os.path.join(root, name) + '.xml'
        imgfile = os.path.join(root, name) + '.jpg'
        
        newname = (4 - len(str(cnt))) * str(0) + str(cnt)
        
        xmlroot = change_filename(xmlfile, newname)
        shutil.copy2(imgfile, 'bbox_dataset/' + newname + '.JPG')
        cnt += 1

