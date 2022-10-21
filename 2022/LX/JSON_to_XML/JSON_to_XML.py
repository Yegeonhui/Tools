"""
# JSON to XML
목적 : LX 사업간 초기에 Bbox를 labelme로 했었음 
json 파일을 xml 파일로 변경
2022-10-12
"""

import json
import os
import numpy as np
import xml.etree.ElementTree as ET
import cv2

class Jsontoxml:
    def __init__(self, root, Image, Json):
        self.root = root
        self.Image = Image
        self.Json = Json

    def getJson(self):
        with open(os.path.join(self.root, self.Json)) as jsonFile:
            self.Objects = json.load(jsonFile)
    
    def MakeXml(self):
        xml_root = ET.Element('annotation')
        ET.SubElement(xml_root, 'folder').text = self.root.split('\\')[-1]
        ET.SubElement(xml_root, 'filename').text = self.Image
        ET.SubElement(xml_root, 'path').text = os.path.join(self.root, self.Image)
        
        source = ET.SubElement(xml_root, 'source')
        ET.SubElement(source, 'database').text = 'Unknown'

        img_array = np.fromfile(os.path.join(self.root, self.Image), np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        height, width, depth = img.shape
        size = ET.SubElement(xml_root, 'size')
        ET.SubElement(size, 'width').text = str(width)
        ET.SubElement(size, 'height').text = str(height)
        ET.SubElement(size, 'depth').text = str(depth)
        
        ET.SubElement(xml_root, 'segmented').text = '0'
        
        total_object = len(self.Objects['shapes'])
        for object_idx in range(total_object):
            object = ET.SubElement(xml_root, 'object')
            
            ET.SubElement(object, 'name').text = self.Objects['shapes'][object_idx]['label']
            ET.SubElement(object, 'pose').text = 'Unspectified'
            ET.SubElement(object, 'truncated').text = '0'
            ET.SubElement(object, 'difficult').text = '0'
            
            points = self.Objects['shapes'][object_idx]['points']
            points = np.array(points)
            x = points[:, 0]
            y = points[:, 1]
            
            x_min = int(min(x))
            x_max = int(max(x))
            
            y_min = int(min(y))
            y_max = int(max(y))
            
            bndbox = ET.SubElement(object, 'bndbox')
            ET.SubElement(bndbox, 'xmin').text = str(x_min)
            ET.SubElement(bndbox, 'ymin').text = str(y_min)
            ET.SubElement(bndbox, 'xmax').text = str(x_max)
            ET.SubElement(bndbox, 'ymax').text = str(y_max)
    
        tree = ET.ElementTree(xml_root)
        tree.write(os.path.join(os.getcwd(), self.root, self.Image[:-4] + '.xml'))   

def main():
    for idx, (root, dirs, files) in enumerate(os.walk('(2022)LX')):
        Jsonlist = [Json for Json in files if Json.lower().endswith('.json')]
        for Json in Jsonlist:
            name = os.path.splitext(Json)[0]
            
            imagefile = name + '.JPG'
            jsonfile = name + '.json'
            
            J = Jsontoxml(root, imagefile, jsonfile)
            J.getJson()
            J.MakeXml()
            
        
if __name__ == '__main__':
    main()