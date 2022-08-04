import os
from glob import glob
import cv2
import xml.etree.ElementTree as ET
import numpy as np
import time

class Augmentation:
    def __init__(self,route,Image,Xml,crop_h,crop_w,gap,n,min_object):
        self.route=route
        
        self.Image=Image
        self.Image_name=self.Image[Image.rfind("\\")+1:-4]
        print(self.Image_name)
        self.Image=cv2.imread(Image)
        
        self.height,self.width,channel=self.Image.shape
        self.Xml=Xml

        self.crop_h=crop_h
        self.crop_w=crop_w
        self.gap=gap
        
        self.n=n
        self.min_object=min_object
    #xml파싱 
    def xml_parsing(self):
        xml=ET.parse(self.Xml)
        root=xml.getroot()
        self.object_tags=root.findall("object")
        return len(self.object_tags)

    #masks.shape=(heigh,width,object개수)
    def make_masks(self):
        #total_object : 사진에 포함된 객체의 수 
        total_object=len(self.object_tags)
    
        #object의 이름 리스트 / ex) [pastic, matal ...]
        self.object_name_list=[[]for i in range(total_object)]

        self.masks=np.zeros((self.height,self.width,total_object))
        for n in range(total_object):
            mask=np.zeros((self.height,self.width))

            object_name=self.object_tags[n].find("name").text
            self.object_name_list[n]=object_name

            #object별 x 최대,최소 / y 최대,최소 
            x_min=int(self.object_tags[n].find("bndbox").findtext("xmin"))
            y_min=int(self.object_tags[n].find("bndbox").findtext("ymin"))
            x_max=int(self.object_tags[n].find("bndbox").findtext("xmax"))
            y_max=int(self.object_tags[n].find("bndbox").findtext("ymax"))

            point=[[x_min,y_min],[x_max,y_min],[x_max,y_max],[x_min,y_max]]
            point=np.array(point,np.int32)

            mask=cv2.fillConvexPoly(mask,point,255)
            self.masks[:,:,n]=mask[:,:]

    #cropsize설정해서 이미지, 마스크 짜르기 / ex) 가로1000, 세로 800, 간격 500으로 짜르겠다.
    def cut_image_mask(self):
        for h in range(0,self.height,self.gap):
            for w in range(0,self.width,self.gap):
                if h<=self.height-self.crop_h and w<=self.width-self.crop_w:
                    Image_crop=self.Image[h:h+self.crop_h,w:w+self.crop_w,:]
                    masks_crop=self.masks[h:h+self.crop_h,w:w+self.crop_w,:]
                    self.aug(Image_crop,masks_crop)

    #Augmentation수행
    def aug(self,Image_crop,masks_crop):
        total_object=len(self.object_tags) #object의 총개수

        Objects=[]
        for obj in range(total_object):
            coordinate=np.where(masks_crop[:,:,obj]==255)
            
            #크롭한 이미지중 object가 존재하지 않는 마스크는 제외시킴
            if len(coordinate[0])!=0:
                y_min=coordinate[0][0]
                x_min=coordinate[1][0]
                y_max=coordinate[0][-1]
                x_max=coordinate[1][-1]
                Objects.append([self.object_name_list[obj],x_min,y_min,x_max,y_max])

        #크롭한 이미지 중 object가 n개 이상이여야 실행 
        if len(Objects)>=self.min_object:      
            self.n+=1    
            cv2.imwrite(self.route+"/Augmentation/"+self.Image_name+"_"+str(self.n)+".jpg",Image_crop)   
            
            
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
                
                xml_copy.write(self.route+"/Augmentation/"+self.Image_name+"_"+str(self.n)+".xml")

def main(crop_h,crop_w,gap,dirname,min_object):
    route=os.getcwd()
    Image_list=glob(route+"/"+dirname+"/*.jpg")
    xml_list=glob(route+"/"+dirname+"/*.xml")

    os.makedirs(route+"/Augmentation",exist_ok=True)
    for idx in range(len(Image_list)):
        
        Image=Image_list[idx]
        Xml=xml_list[idx]

        A=Augmentation(route,Image,Xml,crop_h,crop_w,gap,0,min_object)#0은 저장할때 카운트
        A.xml_parsing()
        
        #xml파싱결과 object가 10개 이상일때 수행 
        if A.xml_parsing()>=10:
            print("10개 이상입니다.")
            A.make_masks()
            A.cut_image_mask()


if __name__=='__main__':
    start=time.time()
    main(crop_h=800,crop_w=1000,gap=500,dirname="File",min_object=3)   
    print("실행시간",time.time()-start)