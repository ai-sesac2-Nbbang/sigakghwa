# 파일명: analyze_success_rate.py
# 실행위치: C:\dev\agent\
# 필요 파일: dummy_data_200_posts.csv

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import font_manager, rc
import os

def analyze_success_rate_by_target_count():
    """
    'dummy_data_200_posts.csv' 파일을 읽어 모집 인원별 성공률을 분석하고
    박스 플롯으로 시각화합니다.
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
        df_posts = pd.read_csv('더미데이터2000명\dummy_data_2000_posts.csv')
    except FileNotFoundError as e:
        print(f"❌ ERROR: 필수 파일({e.filename})을 찾을 수 없습니다.")
        print("    먼저 데이터 생성 코드를 실행하여 데이터 파일을 생성했는지 확인해주세요.")
        return

    # --- 📊 3. 데이터 전처리 및 분석 ---
    print("📊 STEP 3: Processing and analyzing data...")
    
    # 성공률 계산 (실제 참여 인원 / 목표 인원)
    # 목표 인원이 0인 경우를 대비하여 0으로 나눌 때 오류가 나지 않도록 처리
    df_posts['success_rate'] = (df_posts['joined_count'] / df_posts['target_count'].replace(0, pd.NA) * 100).fillna(0)

    print("\n--- 📊 모집 인원 수별 성공률 통계 ---")
    # 보기 쉽게 간단한 통계만 출력
    print(df_posts.groupby('target_count')['success_rate'].describe()[['mean', '50%', 'std']].round(1))


    # --- 🎨 4. 시각화 (박스 플롯) ---
    print("\n🎨 STEP 4: Creating visualization...")
    
    plt.figure(figsize=(12, 8))
    
    ax = sns.boxplot(
        x='target_count',
        y='success_rate',
        data=df_posts,
        palette='pastel'
    )

    plt.title(' 모집 인원별 공동구매 성공률 분포', fontsize=18, pad=15)
    plt.xlabel('목표 인원 수 (명)', fontsize=12)
    plt.ylabel('성공률 (%)', fontsize=12)
    
    # Y축 눈금을 퍼센트(%) 형식으로 변경
    ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: f"{int(x)}%"))
    
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    # --- 🖼️ 5. 이미지 파일로 저장 ---
    filename = "success_rate_by_target_count.png"
    plt.savefig(filename)
    print(f"\n✅ Chart successfully saved as '{filename}'")

# --- 스크립트 실행 ---
if __name__ == "__main__":
    analyze_success_rate_by_target_count()