import pickle
from PIL.ExifTags import TAGS
from PIL import Image
from glob import glob
import piexif

def checkexif(imagefile):
    exif_dict = piexif.load(imagefile)
    thumbnail = exif_dict.pop("thumbnail")
    if thumbnail is not None:
        with open("thumbnail.jpg", "wb+") as f:
            f.write(thumbnail)
    for ifd_name in exif_dict:
        print("\n{0} IFD:".format(ifd_name))
        for key in exif_dict[ifd_name]:
            try:
                print(key, exif_dict[ifd_name][key][:10])
            except:
                print(key, exif_dict[ifd_name][key])


def showexif(imagefile):
    image = Image.open(imagefile)
    info = image._getexif()
    image.close()

    taglabel = {}
    
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        #print(decoded, tag)
        if type(value) is bytes:
            try:
                taglabel[decoded] = pickle.loads(value)
            except:
                taglabel[decoded] = 1
        else:
            taglabel[decoded] = value
    print(taglabel)
    
    
    
