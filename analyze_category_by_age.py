# 파일명: analyze_category_by_age.py
# 실행위치: C:\dev\agent\
# 필요 파일: dummy_data_200_users.csv

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import font_manager, rc
import os

def analyze_category_preference_by_age():
    """
    'dummy_data_200_users.csv' 파일을 읽어 연령대별 관심 카테고리 분포를 분석하고
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
    print(f"💾 STEP 2: Loading data from '{os.getcwd()}'...")
    try:
        df_users = pd.read_csv('dummy_data_2000_users.csv')
    except FileNotFoundError as e:
        print(f"❌ ERROR: 필수 파일({e.filename})을 찾을 수 없습니다.")
        print("    먼저 데이터 생성 코드를 실행하여 'dummy_data_2000_users.csv' 파일을 생성했는지 확인해주세요.")
        return

    # --- 📊 3. 데이터 전처리 및 분석 ---
    print("📊 STEP 3: Processing and analyzing data...")
    
    # '{카테고리1,카테고리2}' 형태의 문자열을 리스트로 변환
    df_users['categories_list'] = df_users['interested_categories'].str.strip('{}').str.split(',')
    
    # 각 사용자의 카테고리 리스트를 개별 행으로 분리 (explode)
    df_exploded = df_users.explode('categories_list')
    df_exploded.rename(columns={'categories_list': 'category'}, inplace=True)

    # 연령대별로 카테고리 개수 계산
    age_category_counts = pd.crosstab(df_exploded['age_group'], df_exploded['category'])

    # 각 연령대 그룹 내에서의 카테고리 비율(%) 계산
    age_category_percentage = age_category_counts.div(age_category_counts.sum(axis=1), axis=0) * 100
    
    print("\n--- 📊 연령대별 관심 카테고리 분포 (%) ---")
    print(age_category_percentage.round(1))

    # --- 🎨 4. 시각화 (누적 막대그래프) ---
    print("\n🎨 STEP 4: Creating visualization...")
    
    ax = age_category_percentage.plot(
        kind='bar', 
        stacked=True, 
        figsize=(12, 8),
        colormap='viridis',
        width=0.7
    )

    plt.title('🎨 연령대별 관심 카테고리 분포', fontsize=18, pad=15)
    plt.xlabel('연령대', fontsize=12)
    plt.ylabel('관심 카테고리 비율 (%)', fontsize=12)
    plt.xticks(rotation=0)
    plt.legend(title='카테고리', bbox_to_anchor=(1.02, 1), loc='upper left')
    plt.grid(axis='y', linestyle='--', alpha=0.6)

    # 그래프에 퍼센트(%) 텍스트 추가
    for c in ax.containers:
        labels = [f'{v.get_height():.1f}%' if v.get_height() > 5 else '' for v in c]
        ax.bar_label(c, labels=labels, label_type='center', color='white', fontsize=10, fontweight='bold')

    plt.tight_layout(rect=[0, 0, 0.85, 1])

    # --- 🖼️ 5. 이미지 파일로 저장 ---
    filename = "age_group_category_preference.png"
    plt.savefig(filename)
    print(f"\n✅ Chart successfully saved as '{filename}'")

# --- 스크립트 실행 ---
if __name__ == "__main__":
    analyze_category_preference_by_age()