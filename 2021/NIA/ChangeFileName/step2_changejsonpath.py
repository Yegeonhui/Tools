import os
import json 

for idx, (root, dirs, files) in enumerate(os.walk("Image")):
    JsonList = [Json for Json in files if Json.lower().endswith(".json")]
    print(JsonList)
    for n in range(len(JsonList)):
        print(JsonList[n])
        Json = os.path.join(root, JsonList[n])
        #data = os.path.split(Json)[1][:-4] + ".jpg"
        data = JsonList[n][: -5] + ".jpg"

        with open(Json, 'r') as jsonFile:
            Objects = json.load(jsonFile)
            Objects['imagePath'] = data

        with open(Json, 'w') as jsonFile:
            json.dump(Objects, jsonFile, indent = 2)
