import cv2
import os

for idx, (root, dirs, files) in enumerate(os.walk('Image')):
    Image_list = [img for img in files if img.lower().endswith('.jpg')]
    for img in Image_list:
        Image = cv2.imread(os.path.join(root,img), cv2.IMREAD_GRAYSCALE)

        # 이미지 임계처리
        ret, th1 = cv2.threshold(Image, 127, 255, cv2.THRESH_BINARY)
        # blockSize 영역의 모든 픽셀에 평균 가중치를 적용
        th2 = cv2.adaptiveThreshold(Image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, 2)
        # blockSize 영역의 모든 픽셀에 중심점으로부터의 거리에 대한 가우시안 가중치 적용
        th3 = cv2.adaptiveThreshold(Image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 2)

        Image = cv2.resize(Image, dsize = (480, 480))

        th1 = cv2.resize(th1, dsize = (480, 480))
        th2 = cv2.resize(th2, dsize = (480, 480))
        th3 = cv2.resize(th3, dsize = (480, 480))

        cv2.imshow("origin", Image)
        cv2.imshow("th1", th1)
        cv2.imshow("th2", th2)
        cv2.imshow("th3", th3)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

