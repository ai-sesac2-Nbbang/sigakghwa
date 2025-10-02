# 파일명: analyze_map_clusters.py
# 실행위치: C:\dev\agent\
# 필요 파일: dummy_data_200_posts.csv
# 목적: 활동 밀집 지역을 지도 위에 마커 클러스터로 시각화

import pandas as pd
import folium
from folium.plugins import MarkerCluster # 클러스터 기능을 위한 도구

def analyze_activity_clusters_map():
    """
    'dummy_data_200_posts.csv' 파일을 읽어 실제 지도 위에 활동 밀집도를
    마커 클러스터(Marker Cluster)로 시각화합니다.
    """
    print("🗺️ '활동 밀집 지역' 분석을 시작합니다...")
    
    # --- 💾 1. 데이터 불러오기 및 처리 ---
    print("💾 STEP 1: Loading and processing data...")
    try:
        df_posts = pd.read_csv('더미데이터2000명\dummy_data_2000_posts.csv')
    except FileNotFoundError:
        print("❌ ERROR: '더미데이터2000명\dummy_data_2000_posts.csv' 파일을 찾을 수 없습니다.")
        return

    if 'mogu_market' not in df_posts.columns:
        print("❌ ERROR: 'mogu_market' 위치 정보가 없습니다.")
        return
        
    df_posts[['lon', 'lat']] = df_posts['mogu_market'].str.extract(r'POINT\((.*) (.*)\)').astype(float)
    
    # --- 🎨 2. 클러스터 지도 생성 ---
    print("🎨 STEP 2: Creating cluster map...")
    
    seoul_map = folium.Map(location=[37.5665, 126.9780], zoom_start=11)
    
    # 마커 클러스터 객체 생성
    marker_cluster = MarkerCluster().add_to(seoul_map)

    # 데이터프레임을 돌면서 클러스터에 원형 마커 추가
    for idx, row in df_posts.iterrows():
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=5,
            color='blue', # 모든 원의 색상을 파란색으로 통일
            fill=True,
            fill_color='blue',
            popup=f"<strong>{row['name']}</strong>" # 클릭 시 나올 팝업 정보
        ).add_to(marker_cluster) # 지도(seoul_map)가 아닌 클러스터(marker_cluster)에 추가
        
    # --- 💾 3. HTML 파일로 저장 ---
    filename = "activity_map_clusters.html"
    seoul_map.save(filename)
    print(f"\n✅ 분석 완료! '{filename}' 이름으로 클러스터 지도가 저장되었습니다.")


if __name__ == "__main__":
    analyze_activity_clusters_map()