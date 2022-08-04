import os 
import shapefile
from shapely.geometry import Point, LineString
import geopandas
from pyproj import Proj, transform
import time
import json
import warnings


# 좌표계 변환
def change_coordinate(point):
    epsg32652 = Proj(init='epsg:32652')
    wgs84 = Proj(init='epsg:4326')
    # epsg32652는 m 단위
    X1, Y1 = transform(wgs84, epsg32652, point[0], point[1])
    return (X1, Y1)


def makekoreacoastline():
    # epsg32652로 바꾼 shape파일
    shape = shapefile.Reader('coast/Z_NGII_N3L_E0080000_utm.shp')

    gdf = geopandas.GeoSeries([LineString([]) for i in range(len(shape))])
    for s in range(len(shape.shapeRecords())):
        print(s)
        feature = shape.shapeRecords()[s]
        first = feature.shape.__geo_interface__  
        coordinates = first['coordinates']
        gdf[s] = LineString(coordinates)  
    print(gdf)
    gdf.crs = 32652
    gdf.to_file('coastline.geojson', driver='GeoJSON')
    return gdf


def handlejson(jsonfile, option, objects=''):
    if option == 'get':
        with open(jsonfile) as j:
            objects = json.load(j)        
        return objects

    elif option == 'save':
        with open(jsonfile, 'w') as j:
            json.dump(objects, j, indent='\t')


start = time.time()
# 경고 끄기
warnings.filterwarnings('ignore')

for idx, (root, dirs, files) in enumerate(os.walk('Cdistwriter')):
    jsonlist = [Json for Json in files if Json.lower().endswith('.json')]
    for j in jsonlist:
        print(j)
        jsonfile = os.path.join(root, j)
        objects = handlejson(jsonfile=jsonfile, option='get')
        
        lat = objects['Latitude']
        lon = objects['Longitude']
        
        point = (lat, lon)
        
        # flag = true : 해안선 코드 만들기
        flag = False
        point = change_coordinate(point)
        point = Point(point)
        point.crs = 32652

        if flag:
            gdf = makekoreacoastline()
        else:
            gdf = geopandas.read_file('coastline.geojson')

        distance = gdf.distance(point)

        # 최소거리 
        distance = round(distance.min(axis=0), 2)
        print(distance)

        objects['CDist'] = distance

        handlejson(jsonfile=jsonfile, option='save', objects=objects)

# 시간측정
print(time.time() - start)


