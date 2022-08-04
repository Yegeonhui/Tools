import xml.etree.ElementTree as ET
import cv2
import os
import numpy as np

def getXml(Xml):
    Xml = ET.parse(Xml)
    xmlroot = Xml.getroot()
    return xmlroot


for idx, (root, dirs, files) in enumerate(os.walk("Image")):
    Image_list = [Img for Img in files if Img.lower().endswith(".jpg")]
    Xml_list = [Xml for Xml in files if Xml.lower().endswith(".xml")]
    print(Image_list)
    if len(Image_list) != 0:  
        for i in range(len(Image_list)):
            img_name = Image_list[i]
            print(img_name)
            Xml_name = Xml_list[i]

            img = os.path.join(root, img_name)
            Xml = os.path.join(root, Xml_name)
            
            img = cv2.imread(img)
            img = np.array(img, np.uint8)
            
            xmlroot = getXml(Xml)
            
            objects = xmlroot.findall("object")
            
            for n in range(len(objects)):
                xmin = int(objects[n].find("bndbox").find("xmin").text)
                xmax = int(objects[n].find("bndbox").find("xmax").text)
                ymin = int(objects[n].find("bndbox").find("ymin").text)
                ymax = int(objects[n].find("bndbox").find("ymax").text)
                img = cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 0, 255), 3)
                
            cv2.imshow("img", img)
            cv2.waitKey(0)
            cv2.imwrite(os.path.join("drawImage", img_name), img)
        