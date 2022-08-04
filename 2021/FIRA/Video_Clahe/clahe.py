import os
import cv2
import time

def bgr_Contrast(img):
    b, g, r = cv2.split(img)
    clahe = cv2.createCLAHE(clipLimit=3.0,tileGridSize=(8,8))
    cl_b = clahe.apply(b)
    cl_g = clahe.apply(g)
    cl_r = clahe.apply(r)
    cl_img = cv2.merge((cl_b, cl_g, cl_r))
    return cl_img


def videocapture(video):
    videoname = video[:-4]
    cap = cv2.VideoCapture(os.path.join(root, video))
    w = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    frame = 0
    
    frame_array = []
    
    while True:
        frame += 1
        success, image = cap.read()
        
        if cap.get(cv2.CAP_PROP_FRAME_COUNT) < frame :
            break 
        if success == False:
            print("프레임 추출 실패!")
        else:   
            cl_image = bgr_Contrast(image)
            frame_array.append(cl_image)
        if frame % 30 == 0:
            print(str(frame / 30) + "초")
        if frame == 300: 
            break
        if cv2.waitKey(10) == 27:
            break    
                  
    # 객체 생성
    out = cv2.VideoWriter("Clahe_video/" + videoname + ".mp4", cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))
    
    # 프레임 불러와서 동영상 만들기 
    for idx in range(len(frame_array)):
        out.write(frame_array[idx])
    out.release()        


start = time.time()
os.makedirs("Clahe_video", exist_ok = True)
for idx, (root, dirs, files) in enumerate(os.walk("video")):
    Video_list = [video for video in files if video.lower().endswith(".mp4")]
    for video in Video_list:
        print(video)
        videocapture(video)
print("걸린 시간 : ", time.time() -  start)
        
        