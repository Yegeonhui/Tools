from PIL import Image
from PIL.ExifTags import TAGS
import shutil
import os
import PySimpleGUI as sg

def getexif(image):
    img = Image.open(image)
    info = img._getexif()
    
    taglabel = {}
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        taglabel[decoded] = value
    img.close()
    return taglabel


def main():
    sg.theme('Dark Blue 3')
    layout = [
        [sg.Text('NonGPS Image selector')],
        [sg.InputText(),sg.FolderBrowse('Select Folder')],
        [sg.Button('Ok'),sg.Button('Exit')]
    ]

    window=sg.Window('IREM-tech.',layout)

    while True:
        event,values = window.read()
        if event == sg.WIN_CLOSED or event=='Exit':
            break
        if event == "Ok":
            path = values['Select Folder']

            for idx, (root, dirs, files) in enumerate(os.walk(path)):
                imagelist = [img for img in files if img.lower().endswith('.jpg')]
                for image in imagelist:
                    name = os.path.splitext(image)[0]
                    print(name)
                    
                    image = os.path.join(root, name + '.jpg')
                    xml = os.path.join(root, name + '.xml')

                    taglabel = getexif(image)
                
                    if float(taglabel['GPSInfo'][4][0]) == 0:
                        os.makedirs(root + "/NonGPS", exist_ok=True)
                        shutil.move(image, root + "/NonGPS/" + name + '.jpg')
                        shutil.move(xml, root + "/NonGPS/" + name + '.xml')


if __name__=='__main__':
    main()

