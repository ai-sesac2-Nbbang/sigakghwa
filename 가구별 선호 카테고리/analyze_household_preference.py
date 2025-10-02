# 파일명: analyze_household_preference.py
# 실행위치: C:\dev\agent\
# 필요 파일: 더미데이터2000명\dummy_data_2000_users.csv, 더미데이터2000명\dummy_data_2000_posts.csv, 더미데이터2000명\dummy_data_2000_participations.csv

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import font_manager, rc
import os

def analyze_category_preference_by_household():
    """
    'dummy_data_2000' 파일을 읽어 가구원 수별 선호 카테고리를 분석하고
    누적 막대그래프로 시각화합니다.
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
    print(f"💾 STEP 2: Loading 2000-user data from '{os.getcwd()}'...")
    try:
        # ✨ 2000명 규모의 데이터를 사용합니다 ✨
        df_users = pd.read_csv('더미데이터2000명\dummy_data_2000_users.csv')
        df_posts = pd.read_csv('더미데이터2000명\dummy_data_2000_posts.csv')
        df_participations = pd.read_csv('더미데이터2000명\dummy_data_2000_participations.csv')
    except FileNotFoundError as e:
        print(f"❌ ERROR: 필수 파일({e.filename})을 찾을 수 없습니다.")
        print("    먼저 '인원수 조절 가능' 마스터 데이터 생성 코드를 2000명으로 설정하고 실행했는지 확인해주세요.")
        return

    # --- 📊 3. 데이터 병합 및 분석 ---
    print("📊 STEP 3: Merging and analyzing data...")
    
    # 3개의 데이터 파일을 하나로 합치기
    merged_df = pd.merge(df_participations, df_users, left_on='user_id', right_on='id')
    merged_df = pd.merge(merged_df, df_posts, left_on='mogu_post_id', right_on='id', suffixes=('_user', '_post'))

    # 가구원 수별로 카테고리 참여 횟수 계산
    household_category_counts = pd.crosstab(merged_df['household_size'], merged_df['category'])

    # 각 그룹 내에서의 카테고리 비율(%) 계산
    household_category_percentage = household_category_counts.div(household_category_counts.sum(axis=1), axis=0) * 100
    
    print("\n---  가구원 수별 카테고리 분포 (%) ---")
    print(household_category_percentage.round(1))

    # --- 🎨 4. 시각화 (누적 막대그래프) ---
    print("\n🎨 STEP 4: Creating visualization...")
    
    ax = household_category_percentage.plot(
        kind='bar', 
        stacked=True, 
        figsize=(12, 8),
        colormap='plasma',
        width=0.7
    )

    plt.title(' 가구원 수별 선호 카테고리 분석', fontsize=18, pad=15)
    plt.xlabel('가구원 수', fontsize=12)
    plt.ylabel('카테고리 참여 비율 (%)', fontsize=12)
    plt.xticks(rotation=0)
    plt.legend(title='카테고리', bbox_to_anchor=(1.02, 1), loc='upper left')
    plt.grid(axis='y', linestyle='--', alpha=0.6)

    # 그래프에 퍼센트(%) 텍스트 추가
    for c in ax.containers:
        labels = [f'{v.get_height():.1f}%' if v.get_height() > 5 else '' for v in c]
        ax.bar_label(c, labels=labels, label_type='center', color='white', fontsize=10, fontweight='bold')

    plt.tight_layout(rect=[0, 0, 0.85, 1])

    # --- 🖼️ 5. 이미지 파일로 저장 ---
    filename = "household_size_preference.png"
    plt.savefig(filename)
    print(f"\n✅ Chart successfully saved as '{filename}'")

# --- 스크립트 실행 ---
if __name__ == "__main__":
    analyze_category_preference_by_household()