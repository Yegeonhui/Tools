# 2022-08-17
# 유역도에서 광려천, 주천강을 지나는 유역도만 불러와서 shp파일, geojson파일로 저장 
# 특이하게 레코드를 먼저 선언해주고 poly를 넣는 형식
# Code by YGH

import shapefile
from shapely.geometry import Polygon
import geopandas 

def saveshapefile():
    w = shapefile.Writer('new_유역도')

    # 레코드 추가, 텍스트 필드는 'C' 유형을 사용하여 생성
    for i in range(len(idxarr)):
        w.field('name', 'C')

    for s in range(len(shape.shapeRecords())):
        if s in idxarr:
            feature = shape.shapeRecords()[s]
            first = feature.shape.__geo_interface__
            coordinates = first['coordinates']
            w.poly(coordinates)

    for i in range(len(idxarr)):
        w.record('polygon')

    w.close()


def savegeojson():
    shape = shapefile.Reader('new_유역도.shp')
    gdf = geopandas.GeoSeries([Polygon([]) for i in range(len(shape.shapeRecords()))])
    for s in range(len(shape.shapeRecords())):
        feature = shape.shapeRecords()[s]
        first = feature.shape.__geo_interface__
        coordinates = first['coordinates'][0]
        gdf[s] = Polygon(coordinates)

    gdf.crs = 32652
    gdf.to_file('new_유역도.geojson', driver='GeoJSON')

# 주천강 -> 죽동천597, 주천강610, 광려천 777
idxarr = [596, 609, 776]

# read 유역도
shape = shapefile.Reader('유역도/유역도 52N.shp')
saveshapefile()
savegeojson()