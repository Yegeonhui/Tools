import os
import cv2
import xml.etree.ElementTree as ET
import numpy as np

from itertools import product
from PIL import Image
import piexif 

class Augmentation:
    def __init__(self,
                 root,
                 Img,
                 Xml,
                 n,
                 crop_h,
                 crop_w,
                 gap,
                 min_object,
                 criteria):
        self.root = root
        # print("root",root)

        self.Image_name = os.path.split(Img)[1][:-4]
        print(self.Image_name)

        self.Image = Image.open(os.path.join(self.root, Img))

        EXIF_dict = piexif.load(self.Image.info['exif'])
        self.EXIF=piexif.dump(EXIF_dict) 

        self.width, self.height = self.Image.size
        self.Xml = os.path.join(self.root,Xml)

        self.n = n 

        self.crop_h = crop_h
        self.crop_w = crop_w
        self.gap = gap
        self.min_object = min_object
        self.criteria = criteria
        
        #output 경로
        self.NewFileRoute = os.path.join(self.root, 'split', self.Image_name)
    
    def xy_minmax(self, n):
        xmin = int(self.object_tags[n].find("bndbox").findtext("xmin"))
        ymin = int(self.object_tags[n].find("bndbox").findtext("ymin"))
        xmax = int(self.object_tags[n].find("bndbox").findtext("xmax"))
        ymax = int(self.object_tags[n].find("bndbox").findtext("ymax"))

        return xmin, ymin, xmax, ymax

    #xml 파싱 / 오브젝트 개수 / 오브젝트 당 사이즈 
    def xml_parsing(self):
        xml = ET.parse(self.Xml)
        root = xml.getroot()
        self.object_tags = root.findall("object")

        self.object_size = [[0] for i in range(len(self.object_tags))]
        for n in range(len(self.object_tags)):
            xmin, ymin, xmax, ymax = self.xy_minmax(n)

            point = ((xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax))
            point = np.array(point)
            
            # 오브젝트당 사이즈 리스트
            self.object_size[n] = cv2.contourArea(point)

        # 오브젝트 개수
        return len(self.object_tags)

    def cut_image_mask(self):
        listH = np.arange(0, self.height - self.crop_h, self.gap)
        listW = np.arange(0, self.width - self.crop_w, self.gap)
        items = [listH, listW]
        prod = list(product(*items))
        for h, w in prod:
            if h <= self.height - self.crop_h and w <= self.width - self.crop_w:
                Image_crop = self.Image.crop((w, h, w + self.crop_w, h + self.crop_h))
                self.check_object(Image_crop, h, w)
                self.n += 1 
    
    def check_object(self, Image_crop, h, w):
        total_object = len(self.object_tags)
        Objects_list = []
        for n in range(total_object):
            object_name = self.object_tags[n].find("name").text
            xmin, ymin, xmax, ymax = self.xy_minmax(n)

            left_top = (h <= ymin <= h + self.crop_h and w <= xmin <= w + self.crop_w)
            right_bottom = (h <= ymax <= h + self.crop_h and w <= xmax <= w + self.crop_w)
            left_bottom = ( h <= ymax <= h+self.crop_h and w <= xmin <= w + self.crop_w)
            right_top = (h <= ymin <= h + self.crop_h and w <= xmax <= w + self.crop_w)
            
            if left_top or right_bottom or left_bottom or right_top:
                if xmin <= w:
                    xmin = w
                if ymin <= h:
                    ymin = h
                if xmax >= w + self.crop_w:
                    xmax = w + self.crop_w
                if ymax >= h + self.crop_h:
                    ymax = h + self.crop_h
                
                xmin = xmin - w
                ymin = ymin - h 
                xmax = xmax - w
                ymax = ymax - h 
                
                point = ((xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax))
                point = np.array(point)

                if self.object_size[n] * self.criteria / 100 <= cv2.contourArea(point):
                    Objects = [object_name, xmin, ymin, xmax, ymax]
                    Objects_list.append(Objects)
        
        if len(Objects_list) >= self.min_object:
            Image_crop.save(self.NewFileRoute + "_" + str(self.n) + ".jpg", format = None, optimize = False, exif = self.EXIF) 
            self.make_xml(Objects_list)

    def make_xml(self,Objects_list):
        Objects = Objects_list[:]
        
        xml_copy = ET.parse(self.Xml)
        root = xml_copy.getroot()
        object= root.findall("object")

        root.find("filename").text = os.path.split(self.NewFileRoute)[1] + "_" + str(self.n) + ".jpg"

        cnt=0
        for o_idx in range(len(object)):
            cnt+=1
            if cnt <= len(Objects):
                object[o_idx].find("name").text=Objects[o_idx][0]
                object[o_idx].find("bndbox").find("xmin").text=str(Objects[o_idx][1])
                object[o_idx].find("bndbox").find("ymin").text=str(Objects[o_idx][2])
                object[o_idx].find("bndbox").find("xmax").text=str(Objects[o_idx][3])
                object[o_idx].find("bndbox").find("ymax").text=str(Objects[o_idx][4])
            else:
                root.remove(object[o_idx])

        xml_copy.write(self.NewFileRoute + "_" + str(self.n) + ".xml")
            

def main(crop_h, crop_w, gap, total_object, min_object, criteria):
    for idx, (root, dirs, files) in enumerate(os.walk('RawData')):
        if len(files) != 0 and os.path.split(root)[1] != "야장" and os.path.split(root)[1] != 'split':
            # if 'split' in dirs:
            #     pass
            # else:
                ListImg = [img for img in files if img.lower().endswith(".jpg")]
                ListXml = [xml for xml in files if xml.lower().endswith(".xml")]

                print(ListImg)

                for idx in range(len(ListImg)):
                    try:
                        os.makedirs(root + "/split", exist_ok=True)
                        A = Augmentation(root = root, 
                                         Img = ListImg[idx], 
                                         Xml = ListXml[idx],
                                         n = 0,
                                         crop_h = crop_h,
                                         crop_w = crop_w,
                                         gap = gap,
                                         min_object = min_object,
                                         criteria = criteria)
                        A.xml_parsing()
                        if A.xml_parsing() >= total_object:
                            print("5개 이상입니다.")
                        print(total_object)

                        A.cut_image_mask()
                    except Exception as e:
                        print(ListImg[idx],e)

if __name__ == "__main__":
    main(crop_h=800, crop_w=1200, gap=400, total_object=4, min_object=3, criteria=10)