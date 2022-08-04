import os
import cv2

def gridmask_Augmentation(image, size, cycle):
    height, width, channel = image.shape
    axis_list = []
    for w in range(cycle, width - size, size + cycle):
        for h in range(cycle, height - size, size + cycle):
            axis_list.append((w, h))

    for axis in axis_list:
        x, y = axis
        image[y:y+size, x:x+size, :] = 0    
    return image


size = 50
cycle = 50
for idx, (root, dirs, files) in enumerate(os.walk('Image')):
    image_list = [img for img in files if img.lower().endswith('tif')]
    for image in image_list: 
        image_name = image
        image = os.path.join(root, image)
        image = cv2.imread(image)
        
        gridmask_Augmentation(image, size, cycle)
        cv2.imwrite(image_name + '.jpg', image)