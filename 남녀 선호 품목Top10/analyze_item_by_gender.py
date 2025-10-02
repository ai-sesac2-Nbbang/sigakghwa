# 파일명: analyze_item_by_gender.py
# 실행위치: C:\dev\agent\
# 필요 파일: dummy_data_2000_users.csv, dummy_data_2000_posts.csv, dummy_data_2000_participations.csv
# 목적: 성별에 따른 선호 아이템을 분석하고 시각화

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import font_manager, rc
import os

def analyze_item_preference_by_gender():
    """
    'dummy_data_2000' 파일을 읽어 성별로 선호하는 개별 상품 TOP 10을 분석하고
    수평 그룹 막대그래프로 시각화합니다.
    """
    # --- ⚙️ 1. 기본 설정 및 한글 폰트 설정 ---
    print("⚙️ STEP 1: Initializing script and setting up Korean font...")
    try:
        font_path = "c:/Windows/Fonts/malgun.ttf"
        rc('font', family=font_manager.FontProperties(fname=font_path).get_name())
    except:
        try: rc('font', family='AppleGothic')
        except: print("⚠️ 경고: 한글 폰트를 찾을 수 없어 그래프의 한글이 깨질 수 있습니다.")

    # --- 💾 2. 데이터 불러오기 ---
    print(f"💾 STEP 2: Loading 2000-user data from '{os.getcwd()}'...")
    try:
        df_users = pd.read_csv('더미데이터2000명\dummy_data_2000_users.csv')
        df_posts = pd.read_csv('더미데이터2000명\dummy_data_2000_posts.csv')
        df_participations = pd.read_csv('더미데이터2000명\dummy_data_2000_participations.csv')
    except FileNotFoundError as e:
        print(f"❌ ERROR: 필수 파일({e.filename})을 찾을 수 없습니다.")
        return

    # --- 📊 3. 데이터 병합 및 분석 ---
    print("📊 STEP 3: Merging and analyzing data...")
    
    merged_df = pd.merge(df_participations, df_users, left_on='user_id', right_on='id')
    merged_df = pd.merge(merged_df, df_posts, left_on='mogu_post_id', right_on='id', suffixes=('_user', '_post'))

    # 1. 전체적으로 가장 인기있는 상품 TOP 10 선정
    top_10_items = merged_df['name_post'].value_counts().head(10).index.tolist()
    
    # 2. TOP 10 상품 데이터만 필터링
    df_top10 = merged_df[merged_df['name_post'].isin(top_10_items)]
    
    # 3. TOP 10 상품에 대해 성별 참여 횟수 계산
    gender_item_counts = pd.crosstab(df_top10['name_post'], df_top10['gender'])
    gender_item_counts.rename(columns={'male': '남성', 'female': '여성'}, inplace=True)
    
    # 4. 총합 순으로 정렬
    gender_item_counts['total'] = gender_item_counts['남성'] + gender_item_counts['여성']
    gender_item_counts = gender_item_counts.sort_values(by='total', ascending=True) # 그래프를 위해 오름차순 정렬

    print("\n--- 📊 성별 선호 개별 상품 TOP 10 (참여 횟수) ---")
    print(gender_item_counts[['남성', '여성', 'total']])

    # --- 🎨 4. 시각화 (수평 그룹 막대그래프) ---
    print("\n🎨 STEP 4: Creating visualization...")
    
    ax = gender_item_counts[['남성', '여성']].plot(
        kind='barh', # 'h'를 붙여 수평 막대그래프 생성
        figsize=(12, 10),
        colormap='coolwarm',
        width=0.8
    )

    plt.title('🌲 성별 선호 개별 상품 TOP 10', fontsize=18, pad=15)
    plt.xlabel('총 참여 횟수', fontsize=12)
    plt.ylabel('상품명', fontsize=12)
    plt.legend(title='성별')
    plt.grid(axis='x', linestyle='--', alpha=0.7)

    plt.tight_layout()
    
    # --- 🖼️ 5. 이미지 파일로 저장 ---
    filename = "gender_item_preference_top10.png"
    plt.savefig(filename)
    print(f"\n✅ Chart successfully saved as '{filename}'")


if __name__ == "__main__":
    analyze_item_preference_by_gender()