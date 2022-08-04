import cv2
import os

def draw(event, x, y, flags, param):
    global ix, iy, mode, radius 
    if mode == True:
        if event == cv2.EVENT_LBUTTONDOWN:
            (ix, iy) = x, y
            print(x, y)

        elif event == cv2.EVENT_LBUTTONUP:
            cv2.line(image, (ix, iy), (x, y), (255, 255, 255), 2)
            cv2.imshow("image", image)
    else:
        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.circle(image, (x, y), radius, (255, 255, 255), 2)
            cv2.imshow("image", image)
        # 스크롤 업하면 원 크기가 증가
        # 스크롤 다운하면 원 크기 감소
        elif event == cv2.EVENT_MOUSEWHEEL:
            if flags > 0:
                radius += 1
            elif radius > 1:
                radius -= 1


radius = 3
ix, iy = (-1, -1)
mode = True
for idx, (root, dirs, files) in enumerate(os.walk("Image")):
    Image_list = [img for img in files if img.lower().endswith(".jpg")]
    for img in Image_list:
        image = cv2.imread(os.path.join(root, img))
        image = cv2.resize(image, (500, 600))
        cv2.imshow("image", image)
        cv2.setMouseCallback("image", draw, image)
        while True:
            # 키보드 입력 무한대기 
            key = cv2.waitKey(0) 

            # m을 누르면 모드변경(라인 -> 원)
            if key == ord("m"):
                mode = not mode
            elif key == 27:
                break 
            elif cv2.waitKey(0):
                break
        cv2.destroyAllWindows()