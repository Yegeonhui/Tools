# 에러출력되게 변경, error파일 생성-> 완료된 파일만 done파일에 들어가게 
import PySimpleGUI as sg
import base64
import pyperclip
from glob import glob
import os
from record_id_time_in_json import record_id_time
from integrity_check import check
from subprocess import Popen
import numpy as np
import datetime

class MakeGUI():
    def getimage(self, image):
        with open(image, 'rb') as img:
            base64_string = base64.b64encode(img.read())
        return base64_string


    def makegui(self):
        sg.theme('Black')
        layout = [
                  [sg.Text('Step1. 로그인')],
                  [sg.Text('Path'), sg.InputText(key='Path'), sg.FolderBrowse('Select_Folder', size=(12, 1), key='Select_Folder')],
                  [sg.Text('  ID  '), sg.InputText(key='ID'), sg.Button('Login', size=(12, 1))],
                  [sg.Text('            Echinoid             '), sg.Text('             Starfish             '), sg.Text('            SeaHare             ')], 
                  [
                    sg.Button('', image_data=self.getimage('example_image/Echinoid.png'), key='Echinoid'),
                    sg.Button('', image_data=self.getimage('example_image/Starfish.png'), key='Starfish'),
                    sg.Button('', image_data=self.getimage('example_image/SeaHare.png'), key='SeaHare'),
                  ],
                  [sg.Text('               Snail              '), sg.Text('          EckloniaCava        '), sg.Text('          Sargassum          ')],
                  [
                    sg.Button('', image_data=self.getimage('example_image/Snail.png'), key='Snail'),
                    sg.Button('', image_data=self.getimage('example_image/EckloniaCava.png'), key='EckloniaCava'),
                    sg.Button('', image_data=self.getimage('example_image/Sargassum.png'), key='Sargassum')
                  ],
                  [sg.Text('* 참고 활용 : 그림 클릭 시 Ctrl + C 됨')],
                  [sg.Text('----------------------------------------------------------------------------------------------------------------------')],
                  [sg.Text('Step2. 무결성 체크'), sg.Button('Integrity Check', size=(30, 1), key='integrity'), sg.Button('Exit', size=(10, 1) )],
                  ]
        window = sg.Window('Data Processing', layout, grab_anywhere = True, element_justification='c')
        return window


    def makegui_noimage(self):
        sg.theme('Black')
        size = (18, 9)
        layout = [
                  [sg.Text('Step1. 로그인')],
                  [sg.Text('Path'), sg.InputText(key='Path'), sg.FolderBrowse('Select_Folder', size=(12, 1), key='Select_Folder')],
                  [sg.Text('  ID  '), sg.InputText(key='ID'), sg.Button('Login', size=(12, 1))],
                  [sg.Text('            Echinoid             '), sg.Text('             Starfish             '), sg.Text('            SeaHare             ')], 
                  [
                    sg.Button('', key='Echinoid', size=size),
                    sg.Button('', key='Starfish', size=size),
                    sg.Button('', key='SeaHare', size=size),
                  ],
                  [sg.Text('               Snail              '), sg.Text('          EckloniaCava        '), sg.Text('          Sargassum          ')],
                  [
                    sg.Button('', key='Snail', size=size),
                    sg.Button('', key='EckloniaCava', size=size),
                    sg.Button('', key='Sargassum', size=size)
                  ],
                  [sg.Text('* 참고 활용 : 그림 클릭 시 Ctrl + C 됨')],
                  [sg.Text('----------------------------------------------------------------------------------------------------------------------')],
                  [sg.Text('Step2. 무결성 체크'), sg.Button('Integrity Check', size=(30, 1), key='integrity'), sg.Button('Exit', size=(10, 1) )],
                  ]
        window = sg.Window('Data Processing', layout, grab_anywhere = True, element_justification='c')
        return window


def runLabelme():
    python_file = "C:/ProgramData/Anaconda3/envs/labelme/pythonw.exe"
    labelme_file = "C:/ProgramData/Anaconda3/envs/labelme/Lib/site-packages/labelme/__main__.py"
    if np.__version__[:4] == '1.22':
        Popen(python_file + ' ' + labelme_file)
        
m = MakeGUI()
try: #이미지 경로
    window = m.makegui()
except:
    window = m.makegui_noimage()
object = ['Echinoid', 'Starfish', 'SeaHare', 'Snail', 'EckloniaCava', 'Sargassum']
minsize = 5000
flag = True
now = datetime.datetime.now()
date = str(now.year) + str(now.month) + str(now.day) + str(now.hour) + str(now.minute)

try:
    while True:    
        event, values = window.read()    
        Path = values['Path']
        if flag:
            f = open(Path + '/' + date + '.txt', 'w')
            flag = False
            f.close()
        f = open(Path + '/' + date + '.txt', 'a')

        if event in object:
            pyperclip.copy(event)
            f.write(event + "이미지를 클릭했습니다." + '\n')

        if event == 'Login':
            f.write('경로 :' + Path + '\n' + 
                    'ID :' + str(values['ID']) + '\n' + 
                    '로그인 했습니다.' + '\n')
            imagelist = glob(values['Path'] + '/*.jpg')
            for image in imagelist:
                jpgfile = os.path.split(image)[-1]
                imagename = os.path.splitext(jpgfile)[0]
                
                jsonfile = Path + '/' + imagename + '.json'
                imagefile = Path + '/' + imagename + '.jpg'
                
                f.write('\n' + jpgfile + ' 메타데이터 작업하는 중' + '\n')
                record_id_time(f, imagefile, jsonfile, str(values['ID']))
                f.write(jpgfile + ' 메타데이터 작업 끝' + '\n')
            
            f.write('\n' + 'labelme 실행중' + '\n')
            runLabelme()
            f.write('\n' + 'labelme 종료' + '\n')

        if event == 'integrity':
            f.write("integrity Check를 클릭했습니다." + '\n')
            jsonlist = glob(values['Path'] + '/*.json')
            for Json in jsonlist:
                jsonfile = os.path.split(Json)[-1]
                f.write('\n' + jsonfile + ' 무결성 체크 중' + '\n')
                check(f, jsonfile, minsize, Path)
                f.write(jsonfile + ' 무결성 체크 끝' + '\n')
            f.close()

        if event == sg.WIN_CLOSED or event in (None, 'Exit'):
            f.write('\n' + event + "를 클릭했습니다." + '\n')
            f.close()
            break
        if event in (None, 'Exit'):
            break

except Exception as e:
   print(e)
window.close()


