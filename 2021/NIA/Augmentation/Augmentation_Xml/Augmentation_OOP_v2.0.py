# Code by YGH.

import os
import cv2
import xml.etree.ElementTree as ET
import numpy as np

from glob import glob
from itertools import product
import time

class Augmentation:
    def __init__(self, route, FolderName, Image, Xml, n):
        self.route = route
        self.FolderName = FolderName

        self.Image = Image
        self.Image_name = self.Image[Image.rfind("\\") + 1:-4]
        print(self.Image_name)
        self.Image = cv2.imread(Image)

        self.height, self.width, channel = self.Image.shape
        self.Xml = Xml

        self.n = n

    # xml파싱
    def xml_parsing(self):
        xml = ET.parse(self.Xml)
        root = xml.getroot()
        self.object_tags = root.findall("object")
        return len(self.object_tags)

    # masks.shape=(heigh,width,object개수)
    def make_masks(self):
        # total_object : 사진에 포함된 객체의 수
        total_object = len(self.object_tags)

        # object의 이름 리스트 / ex) [pastic, matal ...]
        self.object_name_list = [[] for i in range(total_object)]
        self.masks=np.zeros((self.height,self.width,1))
        
        for n in range(total_object):
            masks_depth = 0
            mask = np.zeros((self.height, self.width, 1))

            object_name = self.object_tags[n].find("name").text
            self.object_name_list[n] = object_name

            # object별 x 최대,최소 / y 최대,최소
            x_min = int(self.object_tags[n].find("bndbox").findtext("xmin"))
            y_min = int(self.object_tags[n].find("bndbox").findtext("ymin"))
            x_max = int(self.object_tags[n].find("bndbox").findtext("xmax"))
            y_max = int(self.object_tags[n].find("bndbox").findtext("ymax"))

            point = [[x_min, y_min], [x_max, y_min], [x_max, y_max], [x_min, y_max]]
            point = np.array(point, np.int32)
        

            mask[:, :, 0] = cv2.fillConvexPoly(mask[:, :, 0], point, n + 1)

            while True:
                # 겹치는 부분이 있다면 새로운 차원의 마스크를 추가시켜준다.
                if self.masks.shape[2] == masks_depth:
                    self.masks = np.append(self.masks, mask, axis=2)
                    break
                # 기존의 마스크와 새로만들어진 마스크가 겹치는 부분이 없다면 곱했을때 무조건 0이 나와야된다.
                # 겹치는부분이 없다면 기존의 마스크에 마스크를 추가시켜준다.
                if np.array_equal(self.masks[:, :, masks_depth] * mask[:, :, 0],
                                  np.zeros((self.height, self.width))):  # np.array_equl(a,b)
                    msk = np.copy(self.masks[:, :, masks_depth])
                    self.masks[:, :, masks_depth] = cv2.fillConvexPoly(msk, point, n + 1)
                    break
                masks_depth += 1

    # cropsize설정해서 이미지, 마스크 짜르기 / ex) 가로1000, 세로 800, 간격 500으로 자르겠다.
    def cut_image_mask(self, crop_h=800, crop_w=1200, gap=300):
        listH = np.arange(0, self.height, gap)
        listW = np.arange(0, self.width, gap)
        items = [listH, listW]
        prod = list(product(*items))

        for _, (h, w) in enumerate(prod):
            if h <= self.height - crop_h and w <= self.width - crop_w:
                Image_crop = self.Image[h:h + crop_h, w:w + crop_w, :]
                masks_crop = self.masks[h:h + crop_h, w:w + crop_w, :]
                self.aug(Image_crop, masks_crop)

    # Augmentation수행
    def aug(self, Image_crop, masks_crop, min_object=3):
        total_object = len(self.object_tags)  # object의 총개수

        Objects = []
        for obj in range(total_object):
            for m_cnt in range(self.masks.shape[2]):
                if len(np.where(masks_crop[:, :, m_cnt] == obj + 1)[0]) != 0:
                    coordinate = np.where(masks_crop[:, :, m_cnt] == obj + 1)
                    y_min = coordinate[0][0]
                    x_min = coordinate[1][0]
                    y_max = coordinate[0][-1]
                    x_max = coordinate[1][-1]
                    Objects.append([self.object_name_list[obj], x_min, y_min, x_max, y_max])
                    break

        # 크롭한 이미지 중 object가 n개 이상이여야 실행
        if len(Objects) >= min_object:
            self.n += 1
            cv2.imwrite(
                self.route + "/Augmentation_" + self.FolderName + "/" + self.Image_name + "_" + str(self.n) + ".jpg",
                Image_crop)

            xml_copy = ET.parse(self.Xml)
            root = xml_copy.getroot()
            object = root.findall("object")
            root.find("filename").text = self.Image_name + "_" + str(self.n) + ".jpg"
 
            cnt = 0  # 총 객체가 10개, cropimage 의 object가 7개이면 xml의 object가 7개가 수정되어야됨.
            for o_idx in range(len(object)):
                cnt += 1
                if cnt <= len(Objects):  # cropimage 안에 object 수
                    object[o_idx].find("name").text = Objects[o_idx][0]
                    object[o_idx].find("bndbox").find("xmin").text = str(Objects[o_idx][1])
                    object[o_idx].find("bndbox").find("ymin").text = str(Objects[o_idx][2])
                    object[o_idx].find("bndbox").find("xmax").text = str(Objects[o_idx][3])
                    object[o_idx].find("bndbox").find("ymax").text = str(Objects[o_idx][4])
                else:
                    root.remove(object[o_idx])

                xml_copy.write(self.route + "/Augmentation_" + self.FolderName + "/" + self.Image_name + "_" + str(
                    self.n) + ".xml")


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
start=time.time()
for FName in ListFolder:
    # FolderName = '(2021-08-18)LW2/LW2-6(L)'
    FolderName = FName
    Image_list = glob(route + "/" + FolderName + "/*.jpg")
    xml_list = glob(route + "/" + FolderName + "/*.xml")

    os.makedirs(route + "/Augmentation_" + FolderName, exist_ok=True)
    for idx in range(len(Image_list)):

        Image = Image_list[idx]
        Xml = xml_list[idx]

        A = Augmentation(route, FolderName, Image, Xml, 0)  # 0은 저장할때 카운트
        A.xml_parsing()

        # xml파싱결과 object가 10개 이상일때 수행
        if A.xml_parsing() >= 5:
            print("5개 이상입니다.")
            print(A.xml_parsing())
            A.make_masks()
            A.cut_image_mask()
print("실행시간",time.time()-start)
