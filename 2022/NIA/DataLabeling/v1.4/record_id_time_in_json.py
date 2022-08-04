import json
import datetime
from PIL import Image
import piexif
import pickle

def changeexif(imagefile, ID):
    image = Image.open(imagefile)
    exifData = image._getexif()
    
    if exifData is None:
        exifData = {}

    data = pickle.dumps(ID)
    exif_ifd = {piexif.ExifIFD.UserComment: data}
    zeroth_ifd = {piexif.ImageIFD.Artist: ID.encode('ascii')}
    exif_dict = {"0th" : zeroth_ifd, "Exif": exif_ifd}

    exif_dat = piexif.dump(exif_dict)
    image.save(imagefile, exif=exif_dat)


def getjson(jsonfile):
    with open(jsonfile) as Jsonfile:
        objects = json.load(Jsonfile)
    return objects


def check_id_time(objects):
    total_obj = len(objects['shapes'])
    for o in range(total_obj):
        label = objects['shapes'][o]['label']
        if label == 'test':
            return True
    return False 
    

def record_id_time(f, imagefile, jsonfile, ID):
    objects = getjson(jsonfile)
    if check_id_time(objects):
        f.write('새로 작업하는 이미지 입니다.' + '\n')
        now = datetime.datetime.now()

        f.write('json 파일에 id, opentime 생성' + '\n')
        objects['ID'] = ID
        objects['Opentime'] = now.strftime('%Y-%m-%d %H:%M:%S')
        with open(jsonfile, 'w') as Jsonfile:
            json.dump(objects, Jsonfile, indent=4)
        
        f.write('exif에 id 생성' + '\n')
        changeexif(imagefile, ID)
    else:
        f.write('작업이 완료된 이미지 입니다.' + '\n')