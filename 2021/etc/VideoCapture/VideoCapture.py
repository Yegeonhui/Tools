import cv2
import os

start_second = 10
cut_time = 3

os.makedirs(os.getcwd() + "/frame", exist_ok = True)
for idx, (root, dirs, files) in enumerate(os.walk("video")):
    Video_list = [video for video in files if video.lower().endswith(".mp4")]
    for video in Video_list:
        name = os.path.splitext(video)[0]
        cap = cv2.VideoCapture(os.path.join(root, video))

        # fps 
        fps = cap.get(cv2.CAP_PROP_FPS)
        print(fps)
        
        # 동영상 총 프레임
        total_frame = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        
        # 지정 초 부터 시작
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_second * fps)
        
        while True:
            frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
            print(frame)
            
            success, image = cap.read()
            
            if cap.get(cv2.CAP_PROP_FRAME_COUNT) == frame :
                break 
            
            if frame % (fps * cut_time) == 0:
                if success == False:
                    print("프레임 추출 실패") 
                try:
                    cv2.imwrite("frame/" + name + "_" + str(frame / fps) + ".jpg", image)
                    print("saved imaged" + name + "_" + str(frame / fps) + ".jpg")
                except:
                    print("오류")
            
            if cv2.waitKey(10) == 27:
                break
            
