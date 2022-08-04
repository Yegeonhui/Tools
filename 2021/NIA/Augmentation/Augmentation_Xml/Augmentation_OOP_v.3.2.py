# Code by YGH.
# 테두리에 걸치는 object 제거
# opencv -> pillow 변경(메타데이터를 못불러옴)
import os
import cv2
import xml.etree.ElementTree as ET
import numpy as np

from glob import glob
from itertools import product
import time
from PIL import Image
import piexif

class Augmentation:
    def __init__(self, route, FolderName, Img, Xml, n,crop_h,crop_w,gap,min_object,criteria,save_folder):
        self.route = route
        self.FolderName = FolderName

        self.Image_name = Img[Img.rfind("\\") + 1:-4]
        print(self.Image_name)
        self.Image = Image.open(Img)
        EXIF_dict = piexif.load(self.Image.info["exif"])
        self.EXIF=piexif.dump(EXIF_dict)

        self.height, self.width = self.Image.size
        self.Xml = Xml

        self.n = n
        
        self.crop_h=crop_h
        self.crop_w=crop_w
        self.gap=gap
        self.min_object=min_object

        self.criteria=criteria
        self.save_folder=save_folder

    # xml파싱
    def xml_parsing(self):
        xml = ET.parse(self.Xml)
        root = xml.getroot()
        self.object_tags = root.findall("object")
        return len(self.object_tags)

    def cut_image_mask(self):
        listH = np.arange(0, self.height, self.gap)
        listW = np.arange(0, self.width, self.gap)
        items = [listH, listW]
        prod = list(product(*items))
        for h, w in prod:
            if h <= self.height - self.crop_h and w <= self.width - self.crop_w:
                Image_crop = self.Image.crop((w,h,w+self.crop_w,h + self.crop_h))
                self.check_object(Image_crop,h,w)

    def check_object(self,Image_crop,h,w):#cropimage 좌상단 좌표
        total_object=len(self.object_tags)
        Objects_list=[]
        for n in range(total_object):
            object_name=self.object_tags[n].find("name").text
            x_min = int(self.object_tags[n].find("bndbox").findtext("xmin"))
            y_min = int(self.object_tags[n].find("bndbox").findtext("ymin"))
            x_max = int(self.object_tags[n].find("bndbox").findtext("xmax"))
            y_max = int(self.object_tags[n].find("bndbox").findtext("ymax"))
            #네꼭지점이 cropimage안에잇는지 check 
            left_top=(h<=y_min<=h+self.crop_h and w<=x_min<=w+self.crop_w)
            right_bottom=(h<=y_max<=h+self.crop_h and w<=x_max<=w+self.crop_w)
            left_bottom=(h<=y_max<=h+self.crop_h and w<=x_min<=w+self.crop_w)
            right_top=(h<=y_min<=h+self.crop_h and w<=x_max<=w+self.crop_w)
            if left_top or right_bottom or left_bottom or right_top:
                #우하단 좌표가 cropimage밖에 있으면 최대 h, 최대 w 값으로 x_max,y_max 대입 
                if y_max>=h+self.crop_h: 
                    y_max=h+self.crop_h
                if x_max>=w+self.crop_w:
                    x_max=w+self.crop_w
                if y_min<=h:
                    y_min=h
                if x_min<=w:
                    x_min=w

                x_Min=x_min-w
                y_Min=y_min-h
                x_Max=x_max-w
                y_Max=y_max-h

                if y_Min==0:
                    if 0<=y_Max<=self.criteria:
                        continue
                if x_Min==0:
                    if 0<=x_Max<=self.crop_w:
                        continue
                if self.crop_h==y_Max:
                    if self.crop_h-self.criteria<=y_Min<=self.crop_h:
                        continue
                if self.crop_w==x_Max:
                    if self.crop_w-self.criteria<=x_Min<=self.crop_w:
                        continue

                Objects = [object_name, x_Min, y_Min, x_Max, y_Max]
                Objects_list.append(Objects)

        if len(Objects_list)>=self.min_object:
            #format : 파일 형식 재정의, 생략하면 파일 이름 확장자에 의해 결정됨
            Image_crop.save(self.route+self.save_folder+"/"+self.Image_name+"_"+str(self.n)+".jpg",format=None,optimize=False,exif=self.EXIF)
            self.make_xml(Objects_list)

    def make_xml(self,Objects_list):
        Objects=Objects_list #cropimage안에 object개수  
      
        xml_copy=ET.parse(self.Xml)
        root=xml_copy.getroot()
        object=root.findall("object")
        root.find("filename").text=self.Image_name+"_"+str(self.n)+".jpg"

        cnt=0 #총 객체가 10개, cropimage 의 object가 7개이면 xml의 object가 7개가 수정되어야됨. 
        for o_idx in range(len(object)):
            cnt+=1
            if cnt<=len(Objects): #cropimage 안에 object 수 
                object[o_idx].find("name").text=Objects[o_idx][0]
                object[o_idx].find("bndbox").find("xmin").text=str(Objects[o_idx][1])
                object[o_idx].find("bndbox").find("ymin").text=str(Objects[o_idx][2])
                object[o_idx].find("bndbox").find("xmax").text=str(Objects[o_idx][3])
                object[o_idx].find("bndbox").find("ymax").text=str(Objects[o_idx][4])
            else:
                root.remove(object[o_idx])
            
            xml_copy.write(self.route+self.save_folder+"/"+self.Image_name+"_"+str(self.n)+".xml")
        self.n+=1

def main(crop_h,crop_w,gap,total_object,min_object,criteria):
    route = os.getcwd()

    ListFolder = [
        # '(2021-08-18)LW1/LW1-4(L)',
        # '(2021-08-18)LW1/LW1-5(L)',
        # '(2021-08-18)LW2/LW2-6(L)',
        #'(2021-08-18)LW11/LW11-2(L)',
        # '(2021-08-18)LW12/LW12-5(L)',
        # '(2021-08-18)LW13/LW13-6(L)',
        # '(2021-08-18)LW14/LW14-7(L)',
        # '(2021-08-18)LW14/LW14-8(L)',
        # '(2021-08-18)LW14/LW14-9(L)',
        # '(2021-08-18)LW18/LW18-2(L)',
        # '(2021-08-18)LW18/LW18-3(L)',
        # '(2021-08-18)LW27/LW27-2(L)',
        # '(2021-08-19)LW1/LW1-2(L)',
        # '(2021-08-19)LW1/LW1-3(L)',
        # '(2021-08-19)LW1/LW1-6(L)',
        # '(2021-08-19)LW2/LW2-6(L)',
        # '(2021-08-19)LW2/LW2-7(L)',
        # '(2021-08-19)LW3/LW3-1(L)',
        # '(2021-08-19)LW9/LW9-1(L)',
        # '(2021-08-19)LW10/LW10-1(L)',
        # '(2021-08-19)LW11/LW11-3(L)',
        # '(2021-08-19)LW11/LW11-4(L)',
        # '(2021-08-19)LW12/LW12-5(L)',
        # '(2021-08-19)LW13/LW13-1(L)',
        # '(2021-08-19)LW14/LW14-1(L)',
        # '(2021-08-19)LW15/LW15-1(L)',
        # '(2021-08-19)LW16/LW16-1(L)',
        # '(2021-08-19)LW16/LW16-4(L)',
        # '(2021-08-19)LW16/LW16-5(L)',
        # '(2021-08-19)LW16/LW16-6(L)',
        # '(2021-08-19)LW17/LW17-4(L)',
        # '(2021-08-19)LW17/LW17-5(L)',
        # '(2021-08-19)LW18/LW18-3(L)',
        # '(2021-08-19)LW18/LW18-4(L)',
        # '(2021-08-19)LW27/LW27-1(L)',
        # '(2021-08-20)LW1/LW1-4(L)',
        # '(2021-08-20)LW2/LW2-1(L)',
        # '(2021-08-20)LW3/LW3-2(L)',
        # '(2021-08-20)LW3/LW3-3(L)'
        # '(2021-08-20)LW31/LW31-1(L)',
        # '(2021-08-20)LW31/LW31-2(L)',
        # '(2021-08-20)LW32/LW32-1(L)',
        # '(2021-08-20)LW33/LW33-1(L)',
        # '(2021-08-20)LW33/LW33-2(L)',
        # '(2021-08-20)LW33/LW33-3(L)',
        # '(2021-08-20)LW34/LW34-1(L)',
        # '(2021-08-22)LW3/LW3-4(L)',
        # '(2021-08-22)LW3/LW3-5(L)',
        # '(2021-08-22)LW12/LW12-6(L)',
        # '(2021-08-22)LW15/LW15-1(L)',
        # '(2021-08-23)LW1/LW1-6(L)',
        # '(2021-08-23)LW1/LW1-7(L)',
        # '(2021-08-23)LW1/LW1-8(L)',
        # '(2021-08-23)LW2/LW2-1(L)',
        # '(2021-08-23)LW10/LW10-1(L)',
        # '(2021-08-23)LW11/LW11-8(L)',
        # '(2021-08-23)LW11/LW11-9(L)',
        # '(2021-08-23)LW12/LW12-7(L)',
        # '(2021-08-23)LW13/LW13-2(L)',
        # '(2021-08-23)LW13/LW13-3(L)',
        # '(2021-08-23)LW14/LW14-2(L)',
        # '(2021-08-23)LW15/LW15-2(L)',
        # '(2021-08-23)LW16/LW16-1(L)',
        # '(2021-08-23)LW17/LW17-1(L)',
        # '(2021-08-23)LW17/LW17-7(L)',
        # '(2021-08-23)LW17/LW17-8(L)',
        # '(2021-08-23)LW18/LW18-1(L)',
        # '(2021-08-23)LW18/LW18-2(L)',
        # '(2021-08-23)LW19/LW19-1(L)',
        # '(2021-08-23)LW27/LW27-1(L)'
        'File'
    ]
 
    for FName in ListFolder:
        # FolderName = '(2021-08-18)LW2/LW2-6(L)'
        FolderName = FName
        Image_list = glob(route + "/" + FolderName + "/*.jpg")
        xml_list = glob(route + "/" + FolderName + "/*.xml")

        save_folder="/Augmentation_v3.2"
        os.makedirs(route + save_folder, exist_ok=True)

        for idx in range(len(Image_list)):
            Img = Image_list[idx]
            Xml = xml_list[idx]
            A = Augmentation(route, FolderName, Img, Xml, 0 ,crop_h,crop_w,gap,min_object,criteria,save_folder)  # 0은 저장할때 카운트
            A.xml_parsing()
            # xml파싱결과 object가 10개 이상일때 수행
            if A.xml_parsing() >= total_object:
                print("5개 이상입니다.")
                print(A.xml_parsing())
                A.cut_image_mask()
                
        

if __name__=="__main__":
    start=time.time()
    main(crop_h=800,crop_w=1200,gap=300,total_object=5,min_object=3,criteria=300)
    print("실행시간",time.time()-start)
