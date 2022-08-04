import os
import cv2

def get_option(option):
    if option == 'png_to_jpg':
        source = 'png'
        destination = 'jpg'
    elif option =='jpg_to_png':
        source = 'jpg'
        destination = 'png'
    return source, destination


#option = 'jpg_to_png'
option = 'png_to_jpg'
source, destination = get_option(option)

os.makedirs(destination, exist_ok = True)
for idx, (root, dirs, files) in enumerate(os.walk(source)):
    imagelist = [image for image in files if image.lower().endswith(source)]
    for image in imagelist:
        name = os.path.splitext(image)[0]
        print(name)
        image = cv2.imread(os.path.join(root, image))
        cv2.imwrite(destination + '/' + name + '.' + destination, image)
    
        