import os
import shutil

for idx, (root, dirs, files) in enumerate(os.walk("file")):
    if 'list.txt' in files:
        os.makedirs(root + '/검수통과', exist_ok=True)
        os.makedirs(root + '/반려', exist_ok=True)
  
        f = open(root + '/list.txt', 'r')
        lines = f.readlines()
        linelist = [0 for i in range(len(lines))]
        cnt = 0
        for line in lines:
            linelist[cnt] = line.strip() + '.jpg'
            cnt += 1 
    
        imagejsonlist = os.listdir(root +'/before')
        imagelist = [img for img in imagejsonlist if img.lower().endswith('jpg')]
        for f in imagelist:
            f1 = os.path.splitext(f)[0]
            jsonname = os.path.splitext(f)[0] + '.json'

            jsonfile = root + '/before/' + jsonname
            imagefile = root + '/before/' +  f
            if f in linelist:
                shutil.copy2(imagefile, root + '/반려/' + f1 + '.jpg')
                shutil.copy2(jsonfile, root + '/반려/' + f1 + '.json')
            else:
                shutil.copy2(imagefile, root + '/검수통과/' + f1 + '.jpg')
                shutil.copy2(jsonfile, root + '/검수통과/' + f1 + '.json')