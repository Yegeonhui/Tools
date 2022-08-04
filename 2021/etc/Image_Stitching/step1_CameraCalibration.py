import cv2
import os
from glob import glob
import numpy as np

class Camera_Calibration:
    def __init__(self, route, image_list, Distort_image_list):
        self.route = route
        self.image_list = image_list
        self.Distort_image_list = Distort_image_list


    def getCameraMatrix(self, r=7, c=7):
        # criteria : 반복을 종료할 조건(type(종료 조건), 최대 iter, epsilon값(정확도))
        # cv2.TERM_CRITERIA_EPS : 주어진 정확도(epsilon 인자)에 도달하면 반복을 중단
        # cv2.TERM_CRITERIA_MAX_ITER : max_iter 인자에 지정된 횟수만큼 반복하고 중단
        # a + b : 두가지 조건 중 하나가 만족되면 반복 중단
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TermCriteria_MAX_ITER, 30, 0.001)
        objp = np.zeros((r * c, 3), np.float32)
        objp[:, : 2] = np.mgrid[0 : r, 0 : c].T.reshape(-1, 2)
        
        objpoints = []
        imgpoints = []
        num = 0
        for Chessboard in self.image_list:
            num += 1
            img = cv2.imread(Chessboard)
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            ret,corners = cv2.findChessboardCorners(img_gray, (r, c), None)
    
            if ret:
                objpoints.append(objp)
                corners2 = cv2.cornerSubPix(img_gray, corners, (11, 11), (-1, -1), criteria)
                imgpoints.append(corners2)
                cv2.drawChessboardCorners(img, (r, c), corners2, ret)
            print(str(num)+"번째 사진 처리중")

        #메트릭스, 왜곡계수, 회전/변환 벡터 
        ret, self.mtx, self.dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, img_gray.shape[::-1], None, None)
        print(self.mtx, "cameramatrix를 구했습니다.")


    def UnDistortion(self):
        num = 0
        for image in Distort_image_list:
            num += 1
            img = cv2.imread(image)
            h, w = img.shape[: 2]
            newcameramtx, roi = cv2.getOptimalNewCameraMatrix(self.mtx, self.dist, (w, h), 1, (w, h))
            dst = cv2.undistort(img, self.mtx, self.dist, None, newcameramtx)
            x, y, w, h = roi
            dst = dst[y : y + h, x : x + w]
            img2 = cv2.resize(dst, dsize=(480, 480), interpolation=cv2.INTER_AREA)
            # cv2.imshow("img",img2)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows
            cv2.imwrite(self.route + "/UnDistortion_Image/" + str(num) + ".jpg", dst)


route = os.getcwd()
image_list = glob(route + "/Chessboard/*.jpg")
Distort_image_list = glob(route + "/Distortion_image/*.jpg")
C = Camera_Calibration(route, image_list, Distort_image_list)
C.getCameraMatrix()
C.UnDistortion()

