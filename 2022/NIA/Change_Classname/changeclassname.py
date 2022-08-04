import json
import os

def handlejson(jsonfile, option, objects=''):
    if option == 'get':
        with open(jsonfile) as j:
            objects = json.load(j)        
        return objects

    elif option == 'save':
        with open(jsonfile, 'w') as j:
            json.dump(objects, j, indent='\t')

wrongname = str(input('잘못된 라벨링 된 클래스명을 입력하세요'))
correctname = str(input('수정할 클래스 명을 입력하세요'))

for idx, (root, dirs, files) in enumerate(os.walk('file')):
    Jsonfilelist = [Jsonfile for Jsonfile in files if Jsonfile.lower().endswith('json')]
    for Json in Jsonfilelist:
        print(Json)
        name = os.path.splitext(Json)[0]

        Jsonfile = os.path.join(root, Json)
        Imagefile = os.path.splitext(Jsonfile)[0] + '.jpg'

        objects = handlejson(Jsonfile, 'get')
        total_objects = len(objects['shapes'])
        for t in range(total_objects):
            if objects['shapes'][t]['label'] == wrongname:
                objects['shapes'][t]['label'] = correctname
        
        handlejson(Jsonfile, 'save', objects)