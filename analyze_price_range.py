# 파일명: analyze_price_range.py
# 실행위치: C:\dev\agent\
# 필요 파일: dummy_data_200_posts.csv, dummy_data_200_participations.csv

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import font_manager, rc
import os

def analyze_price_range_popularity():
    """
    'dummy_data_200' 파일을 읽어 참여가 활발한 가격대를 분석하고
    히스토그램으로 시각화합니다.
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
    
    # 참여 데이터와 게시글 데이터를 합쳐, 각 참여가 어떤 가격의 상품에서 발생했는지 연결
    merged_df = pd.merge(df_participations, df_posts, left_on='mogu_post_id', right_on='id')

    print("\n--- 📊 참여가 발생한 상품들의 가격 통계 ---")
    # describe() 함수로 간단한 기술 통계 출력
    print(merged_df['price'].describe().apply(lambda x: f"{x:,.0f}"))


    # --- 🎨 4. 시각화 (히스토그램) ---
    print("\n🎨 STEP 4: Creating visualization...")
    
    plt.figure(figsize=(12, 7))
    
    # 히스토그램 생성
    ax = sns.histplot(
        data=merged_df, 
        x='price', 
        bins=10,       # 가격 범위를 10개 구간으로 나눔
        kde=True,      # 부드러운 분포 곡선 추가
        color='skyblue'
    )

    plt.title('💰 참여가 가장 활발한 가격대 분석', fontsize=18, pad=15)
    plt.xlabel('상품 가격 (원)', fontsize=12)
    plt.ylabel('총 참여 횟수', fontsize=12)
    
    # X축 눈금에 콤마(,) 추가
    ax.get_xaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
    plt.xticks(rotation=15) # X축 라벨 살짝 회전

    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    # --- 🖼️ 5. 이미지 파일로 저장 ---
    filename = "price_range_popularity.png"
    plt.savefig(filename)
    print(f"\n✅ Chart successfully saved as '{filename}'")

# --- 스크립트 실행 ---
if __name__ == "__main__":
    analyze_price_range_popularity()