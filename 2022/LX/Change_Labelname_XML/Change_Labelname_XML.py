"""
2022-10-13
1. 라벨링 워커 실수로 House_Normal -> House Normal 로 라벨링
2. 기존 라벨링명으로 수정하는 코드 
Code by YGH
"""

import os
import xml.etree.ElementTree as ET

def getxml(xmlfile):
    xml = ET.parse(xmlfile)
    xmlroot = xml.getroot()
    return xmlroot

def savexml(xmlfile, xmlroot):
    tree = ET.ElementTree(xmlroot)
    tree.write(xmlfile)

for idx, (root, dirs, files) in enumerate(os.walk('(2022)LX')):
    xml_arr = [xml for xml in files if xml.lower().endswith('xml')]
    for xml in xml_arr:
        print(xml)
        xmlfile = os.path.join(root, xml)
        xmlroot = getxml(xmlfile)
        total_object = len(xmlroot.findall('object'))
        for i in range(total_object):
            label_name = xmlroot.findall('object')[i].find('name').text
            # ex) House Normal -> _으로 쪼갰을때 길이가 1
            if len(label_name.split('_')) == 1:
                label_name = label_name.replace(' ', '_')
                print(label_name)
                xmlroot.findall('object')[i].find('name').text = label_name
            else:
                continue
        
        savexml(xmlfile, xmlroot)
    
    