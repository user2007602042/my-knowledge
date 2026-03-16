import os
import geopandas as gpd

print("🚀 폴더 내의 모든 SHP 파일을 찾아 자동 변환합니다...\n")

# 1. 현재 폴더에 있는 모든 파일 중 확장자가 .shp인 것만 자동으로 찾기
shp_files = [f for f in os.listdir() if f.endswith('.shp')]

if not shp_files:
    print("❌ 현재 폴더에 SHP 파일이 없습니다. 파일 위치를 다시 확인해주세요!")
else:
    for shp_file in shp_files:
        # 출력 파일명 자동 생성 (예: 용지경계.shp -> 용지경계.geojson)
        geojson_file = shp_file.replace('.shp', '.geojson')
        
        print(f"[{shp_file}] 변환 중...")
        try:
            # 한글 깨짐 방지용 cp949 인코딩
            gdf = gpd.read_file(shp_file, encoding='cp949')
            
            # 좌표계 변환 (2097 -> 4326)
            gdf.set_crs(epsg=2097, allow_override=True, inplace=True)
            gdf = gdf.to_crs(epsg=4326)
            
            # GeoJSON 저장
            gdf.to_file(geojson_file, driver='GeoJSON')
            print(f"  👉 성공! '{geojson_file}' 생성 완료\n")
        except Exception as e:
            print(f"  ❌ 실패! 에러 내용: {e}\n")

print("🎉 모든 변환 작업이 종료되었습니다!")