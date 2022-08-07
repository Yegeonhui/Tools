import json
import os

def getjson(Json):
    with open(Json, 'r') as jsonFile:
        Objects = json.load(jsonFile)
    return Objects


Change_object_name = ["", "brown", "Phanerogam", "Brown", "Red", "Brown", "Brown"]
for idx, (root, dirs, files) in enumerate(os.walk("Image")):
    JsonList = [Json for Json in files if Json.lower().endswith(".json")]
    for Json_idx in range(len(JsonList)):
        print(JsonList[Json_idx])
        
        Json = os.path.join(root, JsonList[Json_idx])
        Objects = getjson(Json)
        total_object = len(Objects['shapes'])
        try:
            for num in range(total_object):
                label = Objects['shapes'][num]['label'] 
                if Objects['shapes'][num]['label']  == 'brown':
                    Objects['shapes'][num]['label'] = 'Brown'
                elif Objects['shapes'][num]['label']  == 'red':
                    Objects['shapes'][num]['label']  = 'Red'
                if Objects['shapes'][num]['label']  == 'phanerogam':
                    Objects['shapes'][num]['label']  = 'Phanerogam'
                #Objects['shapes'][num]['label'] = Change_object_name[int(label)]
        except:
            pass
        # dump를 해줘야 json 파일이 수정됨
        with open(Json, 'w') as jsonFile:
            json.dump(Objects, jsonFile, indent = 2)
            
