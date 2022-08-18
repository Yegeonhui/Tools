# 2022-08-18
# 지적도에서 국유지로 판단되는 부분을 추출해서 shapefile, geojson으로 저장
# Code by YGH

import geopandas 

def savefile(gpd):
    gdf = geopandas.GeoDataFrame([])
    gdf.crs = 32652
    for i in range(len(gpd)):
        landname = gpd['A5'][i][-1]
        if landname in state_land:
            gdf = gdf.append(geopandas.GeoDataFrame([gpd.iloc[i, :]]))
    return gdf
    

# 사유지
private_land = ['전', '답', '과', '목', '임', '염', '대', 
                '장', '학', '주','창', '양', '종', '묘', '잡']

# 국유지
state_land = ['광', '도', '철', '제', '천', '구', '유', '수', '공', '체', '유', '사']

saveroute = 'state_land'

# read shapefile
filename = '유역도_지적도/지적도 주천강 52N.shp'
gpd1 = geopandas.GeoDataFrame.from_file(filename, encoding='cp949')

filename = '유역도_지적도/지적도 광려천 52N.shp'
gpd2 = geopandas.GeoDataFrame.from_file(filename, encoding='cp949')

gdf1 = savefile(gpd1)
gdf2 = savefile(gpd2)

gdf = gdf1.append(gdf2)
gdf.crs = 32652
print(gdf)

gdf.to_file(saveroute + '.shp')
gdf.to_file(saveroute + '.geojson', driver='GeoJSON')