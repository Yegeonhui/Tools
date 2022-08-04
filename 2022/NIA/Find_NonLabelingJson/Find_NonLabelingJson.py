import json
import os
import shutil
 
def get_json(Jsonfile):
    with open(Jsonfile) as Json:
        objects = json.load(Json)
    return objects

os.makedirs('객체x', exist_ok=True)
os.makedirs('객체ㅇ', exist_ok=True)

for idx, (root, dirs, files) in enumerate(os.walk('file')):
    Jsonfilelist = [Jsonfile for Jsonfile in files if Jsonfile.lower().endswith('json')]
    for Json in Jsonfilelist:
        print(Json)
        name = os.path.splitext(Json)[0]

        Jsonfile = os.path.join(root, Json)
        Imagefile = os.path.splitext(Jsonfile)[0] + '.jpg'
        
        objects = get_json(Jsonfile)
        if len(objects['shapes']) == 0: 
            shutil.copy2(Jsonfile, '객체x/' + name + '.json')
            shutil.copy2(Imagefile, '객체x/' + name + '.jpg')
        else:
            shutil.copy2(Jsonfile, '객체ㅇ/' + name + '.json')
            shutil.copy2(Imagefile, '객체ㅇ/' + name + '.jpg')

                