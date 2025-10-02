# 파일명: analyze_category_popularity.py
# 실행위치: C:\dev\agent\
# 필요 파일: dummy_data_200_posts.csv, dummy_data_2000_participations.csv

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import font_manager, rc
import os

def analyze_overall_category_popularity():
    """
    'dummy_data_200' 파일을 읽어 전체 카테고리별 인기도를 분석하고
    원그래프로 시각화합니다.
    """
    # --- ⚙️ 1. 기본 설정 및 한글 폰트 설정 ---
    print("⚙️ STEP 1: Initializing script and setting up Korean font...")
    try:
        font_path = "c:/Windows/Fonts/malgun.ttf" # For Windows
        font_name = font_manager.FontProperties(fname=font_path).get_name()
        rc('font', family=font_name)
    except FileNotFoundError:
        try:
            rc('font', family='AppleGothic') # For Mac
        except:
            print("⚠️ 경고: 한글 폰트를 찾을 수 없어 그래프의 한글이 깨질 수 있습니다.")

    # --- 💾 2. 데이터 불러오기 ---
    print(f"💾 STEP 2: Loading data from '{os.getcwd()}'...")
    try:
        df_posts = pd.read_csv('dummy_data_2000_posts.csv')
        df_participations = pd.read_csv('dummy_data_2000_participations.csv')
    except FileNotFoundError as e:
        print(f"❌ ERROR: 필수 파일({e.filename})을 찾을 수 없습니다.")
        print("    먼저 데이터 생성 코드를 실행하여 데이터 파일을 생성했는지 확인해주세요.")
        return

    # --- 📊 3. 데이터 병합 및 분석 ---
    print("📊 STEP 3: Merging and analyzing data...")
    
    # 참여 데이터와 게시글 데이터를 합쳐, 각 참여가 어떤 카테고리에서 발생했는지 연결
    merged_df = pd.merge(df_participations, df_posts, left_on='mogu_post_id', right_on='id')

    # 카테고리별 참여 횟수 계산
    category_counts = merged_df['category'].value_counts()

    print("\n--- 📊 카테고리별 총 참여 횟수 ---")
    print(category_counts)

    # --- 🎨 4. 시각화 (원그래프) ---
    print("\n🎨 STEP 4: Creating visualization...")
    
    plt.figure(figsize=(10, 10))
    
    # 원그래프 생성
    plt.pie(
        category_counts,
        labels=category_counts.index,
        autopct='%1.1f%%', # 각 조각에 퍼센트 표시
        startangle=90,      # 90도에서 시작하여 보기 좋게 정렬
        colors=sns.color_palette('pastel'),
        wedgeprops={'edgecolor': 'white', 'linewidth': 2} # 조각 사이에 흰색 선 추가
    )

    plt.title('🍕 전체 카테고리 인기도 분석', fontsize=18, pad=15)
    plt.ylabel('') # 불필요한 라벨 제거

    # --- 🖼️ 5. 이미지 파일로 저장 ---
    filename = "category_popularity_pie_chart.png"
    plt.savefig(filename)
    print(f"\n✅ Chart successfully saved as '{filename}'")

# --- 스크립트 실행 ---
if __name__ == "__main__":
    analyze_overall_category_popularity()