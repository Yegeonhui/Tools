import cv2
from jsonform import getjsonform
import json
import os

def bgr_Contrast(img):
    b, g, r = cv2.split(img)
    clahe = cv2.createCLAHE(clipLimit=3.0,tileGridSize=(8,8))
    clahe_b = clahe.apply(b)
    clahe_g = clahe.apply(g)
    clahe_r = clahe.apply(r)
    clahe_img = cv2.merge((clahe_b, clahe_g, clahe_r))
    return clahe_img
    

def get_frame(start, end, fps):
    frame_array = [i for i in range(start, end, fps)] 
    return frame_array


def save_change_json(jsonname, imagePath, water_env, obj_info, h, w):
    objects = getjsonform()
    objects['imagePath'] = imagePath + '.jpg'
    objects['imageHeight'] = h 
    objects['imageWidth'] = w
    objects['Temp'] = water_env['Temp']
    objects['Salinity'] = water_env['Salinity']
    objects['Do'] = water_env['Do']
    objects['pH'] = water_env['pH']
    objects['Transparency'] = water_env['Transparency']
    objects['longitude'] = water_env['lon']
    objects['latitude'] = water_env['lat']
    objects['Depth'] = water_env['Depth']
    objects['obj_info'] = obj_info

    with open(jsonname + '.json', 'w') as jsonfile:
        json.dump(objects, jsonfile, indent=4)


def videofiltering(video, interval, savepath, water_env):
    cap = cv2.VideoCapture(video)
    fps = round(cap.get(cv2.CAP_PROP_FPS))
    
    startframe = int(0 * fps)
    endframe = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) #끝나는시간 * fps
    frame_array = get_frame(startframe, endframe, fps * interval)
    
    cnt = 0

    for f in frame_array:
        cnt+=1
        cap.set(cv2.CAP_PROP_POS_FRAMES, f)
        success, image = cap.read()
        
        if success == False:
            print("프레임 추출 실패!")
        else:   
            clahe_img = bgr_Contrast(image)
            h, w, _ = image.shape
            
            cv2.imwrite(savepath + "/" + str(cnt) + '.jpg', clahe_img)
            save_change_json(savepath + "/" + str(cnt), str(cnt), water_env, None, h, w)
            
        print(str(cnt * interval) + "초")
        
        if cv2.waitKey(10) == 27:
            break    


def imagefiltering(image, savepath, water_env, obj_info):
    imagenamejpg = os.path.split(image)[-1]
    imagename = os.path.splitext(imagenamejpg)[0]
    
    # 이미지 clahe 적용
    image = cv2.imread(image)
    clahe_img = bgr_Contrast(image)
    
    # 이미지 저장
    cv2.imwrite(savepath + "/" + imagenamejpg, clahe_img)
    h, w, _ = clahe_img.shape
    # json 파일 생성
    save_change_json(savepath + "/" + imagename, imagename, water_env, obj_info, h, w)