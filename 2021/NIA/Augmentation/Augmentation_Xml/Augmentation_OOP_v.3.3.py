# Code by YGH.
# 테두리에 걸치는 object 제거 -> cv2.contour 함수 사용
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
    def __init__(self,
                 route,
                 FolderName,
                 Img,
                 Xml,
                 n,
                 crop_h,
                 crop_w,
                 gap,
                 min_object,
                 criteria,
                 save_folder,
                 output_idx):
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

        # Output 파일의 이름(확장자 미포함)
        NewName = 'CD_' + str(output_idx)
        self.NewFileName = os.path.join(self.route, self.save_folder, NewName)
        
    # xml파싱
    def xml_parsing(self):
        xml = ET.parse(self.Xml)
        root = xml.getroot()
        self.object_tags = root.findall("object")
        
        #오브젝트당 사이즈 리스트 
        self.object_size = [[0] for i in range(len(self.object_tags))]
        for n in range(len(self.object_tags)):
            x_min = int(self.object_tags[n].find("bndbox").findtext("xmin"))
            y_min = int(self.object_tags[n].find("bndbox").findtext("ymin"))
            x_max = int(self.object_tags[n].find("bndbox").findtext("xmax"))
            y_max = int(self.object_tags[n].find("bndbox").findtext("ymax"))
            cnt=((x_min,y_min),(x_max,y_min),(x_max,y_max),(x_min,y_max))
            cnt=np.array(cnt)
            self.object_size[n] = cv2.contourArea(cnt)
        return len(self.object_tags)

    def cut_image_mask(self):
        listH = np.arange(0, self.height-self.crop_w, self.gap)
        listW = np.arange(0, self.width-self.crop_h, self.gap)
        items = [listH, listW]
        prod = list(product(*items))
        for h, w in prod:
            if h <= self.height - self.crop_h and w <= self.width - self.crop_w:
                Image_crop = self.Image.crop((h,w,h+self.crop_w,w + self.crop_h))
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

                cnt=((x_Min,y_Min),(x_Max,y_Min),(x_Max,y_Max),(x_Min,y_Max))
                cnt=np.array(cnt)
                if self.object_size[n] * self.criteria / 100 <= cv2.contourArea(cnt):
                    Objects = [object_name, x_Min, y_Min, x_Max, y_Max]
                    Objects_list.append(Objects)

        if len(Objects_list)>=self.min_object:
            #format : 파일 형식 재정의, 생략하면 파일 이름 확장자에 의해 결정됨
            # Image_crop.save(self.route+self.save_folder+"/"+self.Image_name+"_"+str(self.n)+".jpg",format=None,optimize=False,exif=self.EXIF)
            Image_crop.save(self.NewFileName + ".jpg",
                            format=None, optimize=False, exif=self.EXIF)
            self.make_xml(Objects_list)

    def make_xml(self,Objects_list):
        Objects=Objects_list #cropimage안에 object개수  
      
        xml_copy=ET.parse(self.Xml)
        root=xml_copy.getroot()
        object=root.findall("object")
        # root.find("filename").text=self.Image_name+"_"+str(self.n)+".jpg"
        root.find('filename').text = self.NewFileName + '.jpg'

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
            
            # xml_copy.write(self.route+self.save_folder+"/"+self.Image_name+"_"+str(self.n)+".xml")
            xml_copy.write(self.NewFileName + '.xml')
        self.n += 1


def main(crop_h, crop_w, gap, total_object, min_object, criteria):
    route = os.getcwd()

    ListDirs = os.listdir()
    ListDirs = [D for D in ListDirs if D.startswith('(2021-')]

    # ListFolder = []
    # for idx, item in enumerate(ListDirs):
    #     for _, Dir, files in os.walk(item):
    #         for D in Dir:
    #             if D != '야장':
    #                 ListFolder.append(item + '/' + D)
    ListFolder=['File']
    for FName in ListFolder:
        # FolderName = '(2021-08-18)LW2/LW2-6(L)'
        FolderName = FName
        Image_list = glob(route + "/" + FolderName + "/*.jpg")
        xml_list = glob(route + "/" + FolderName + "/*.xml")

        save_folder = "Augmentation_v3.3"
        os.makedirs(os.path.join(route, save_folder), exist_ok=True)

        for idx in range(len(Image_list)):
            Img = Image_list[idx]
            Xml = xml_list[idx]
            A = Augmentation(route=route,
                             FolderName=FolderName,
                             Img=Img, Xml=Xml, n=0,
                             crop_h=crop_h,
                             crop_w=crop_w,
                             gap=gap,
                             min_object=min_object,
                             criteria=criteria,
                             save_folder=save_folder,
                             output_idx=idx+1)  # 0은 저장할때 카운트
            A.xml_parsing()
            # xml파싱결과 object가 10개 이상일때 수행
            if A.xml_parsing() >= total_object:
                print("5개 이상입니다.")
                print(A.xml_parsing())
                A.cut_image_mask()
                

if __name__ == "__main__":
    start = time.time()
    main(crop_h=800, crop_w=1200, gap=400, total_object=5, min_object=3, criteria=10)
    print("실행시간", time.time()-start)
