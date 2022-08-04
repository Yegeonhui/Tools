import os
import piexif
import xml.etree.ElementTree as ET
from PIL import Image

class Augmentation:
    def __init__(self, root, Img, Xml):
        self.root = root
        
        self.Img_name = Img[:-4]
        
        self.Img = Image.open(os.path.join(self.root, Img))
        self.Xml = os.path.join(self.root, Xml)
    
    #gtype, object 불러옴 / N_R_list = rope, net 만 저장 
    def Xml_parsing(self):
        xml = ET.parse(self.Xml)
        root = xml.getroot()
        self.gtype = root.find("gtype").text
        
        object = root.findall("object")
        self.N_R_list=[]
        for o_cnt in range(len(object)):
            object_name = object[o_cnt].find("name").text
            object_name = object_name[object_name.rfind(")")+1 : ]
            if object_name == "Rope" or object_name == "Net":
                xmin = int(object[o_cnt].find("bndbox").find("xmin").text)
                ymin = int(object[o_cnt].find("bndbox").find("ymin").text)
                xmax = int(object[o_cnt].find("bndbox").find("xmax").text)
                ymax = int(object[o_cnt].find("bndbox").find("ymax").text)

                self.N_R_list.append((object_name, xmin, ymin, xmax, ymax))
        
        return self.N_R_list

    def Crop_Method(self, crop_w, crop_h, cnt = 1):
        W, H = self.Img.size
        
        EXIF_dict = piexif.load(self.Img.info['exif'])
        EXIF=piexif.dump(EXIF_dict) 

        for i in range(len(self.N_R_list)):
            xmin = self.N_R_list[i][1]
            ymin = self.N_R_list[i][2]
            xmax = self.N_R_list[i][3]
            ymax = self.N_R_list[i][4]
            
            # 홀수일때
            if (xmax - xmin) % 2 == 1:
                xmax += 1
            if (ymax - ymin) % 2 == 1:
                ymax += 1    

            px = (crop_w - (xmax - xmin)) // 2 
            py = (crop_h - (ymax - ymin)) // 2 
            
            if (xmin - px) >= 0 and (xmax + px) <= W:
                c_xmin = xmin - px 
                c_xmax = xmax + px 
            elif (xmin - px) < 0:
                c_xmin = 0
                c_xmax = crop_w
            elif (xmax + px) > W:
                c_xmax = W
                c_xmin = W - crop_w

            if (ymin - py) >= 0 and (ymax + py) <= H:
                c_ymin = ymin - py
                c_ymax = ymax + py 
            elif (ymin - py) < 0:
                c_ymin = 0
                c_ymax = crop_h
            elif (ymax + py) > H:
                c_ymax = H
                c_ymin = H - crop_h  

            Crop_Img = self.Img.crop((c_xmin, c_ymin, c_xmax, c_ymax))
    
            Crop_Img.save(os.path.join(self.root, self.gtype, self.Img_name) + "_" + str(cnt) + ".jpg", format = None, optimize = False, exif = EXIF) 
            cnt += 1

def main(crop_w = 1200, crop_h = 800):
    # for idx, (root, dirs, files) in enumerate(os.walk('Screen')):
    #     print(root, dirs, files)

    route_list=os.walk('Screen')
    for idx, (root, dirs, files) in enumerate(route_list):
        if 'sand' or 'gravel' or 'mud' in dirs:
            pass

        ListImg = [img for img in files if img.lower().endswith("jpg")]
        ListXml = [xml for xml in files if xml.lower().endswith("xml")]
        
        if len(ListImg) != 0:
            os.makedirs(root + "/sand", exist_ok = True)
            os.makedirs(root + "/gravel", exist_ok = True)
            os.makedirs(root + "/mud", exist_ok = True)
            
        for idx in range(len(ListImg)):
            print(ListImg[idx])

            A = Augmentation(root, ListImg[idx], ListXml[idx])

            # N_R_list -> Net, Rope의 정보가 담긴 리스트 
            N_R_list = A.Xml_parsing()            

            print(len(N_R_list))
            if len(N_R_list) != 0:             
                A.Crop_Method(crop_w, crop_h)

        


if __name__ == "__main__":
    main(crop_w = 1200, crop_h = 800)

