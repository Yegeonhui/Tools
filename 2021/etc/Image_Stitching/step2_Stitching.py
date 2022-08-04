import cv2
import os
from glob import glob

class Stitching:
    def __init__(self,route):
        self.route = route

    def getImage(self):
        File_list = glob(self.route + "/UnDistortion_Image/*.jpg")
        self.Image_Stitching(File_list)

    def Image_Stitching(self,File_list):
        imgs=[]
        for File in File_list:
            img = cv2.imread(File)
            imgs.append(img)
        
        #객체생성
        stitcher = cv2.Stitcher_create()

        #이미지 스티칭
        status,dst = stitcher.stitch(imgs)
        if status != cv2.Stitcher_OK:
            print("Stitch failed!")

        cv2.imwrite(self.route + "/Stitching/Stitching_Image.jpg", dst)
        dst = cv2.resize(dst, dsize=(360,240), interpolation=cv2.INTER_AREA)
        cv2.imshow('dst', dst)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

route = os.getcwd()
S = Stitching(route)
S.getImage()
