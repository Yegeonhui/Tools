# 2022-08-17
# 유역도에서 광려천, 주천강을 지나는 유역도만 불러와서 shp파일, geojson파일로 저장 
# Code by YGH

import geopandas 

def savefile(gpd, saveroute):
    gdf = geopandas.GeoDataFrame([])
    gdf.crs = 32652
    for i in range(len(gpd)):
        if i in idxarr:
            gdf = gdf.append(geopandas.GeoDataFrame([gpd.iloc[i, :]]))
    gdf.to_file(saveroute + '.shp')
    gdf.to_file(saveroute + '.geojson', driver='GeoJSON')

# 주천강 -> 죽동천597, 주천강610, 광려천 777
idxarr = [596, 609, 776]
saveroute = 'new_유역도'

# read 유역도
gpd = geopandas.GeoDataFrame.from_file('유역도_지적도/유역도 52N.shp', encoding='cp949')
savefile(gpd, saveroute)
