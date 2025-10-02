# 파일명: analyze_power_users.py
# 실행위치: C:\dev\agent\
# 필요 파일: dummy_data_200_users.csv, dummy_data_200_participations.csv

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import font_manager, rc
import os

def find_and_visualize_power_users():
    """
    'dummy_data_200' 파일을 읽어 가장 활동적인 사용자 TOP 10을 찾아
    막대그래프로 시각화합니다.
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
        df_users = pd.read_csv('더미데이터2000명\dummy_data_2000_users.csv')
        df_participations = pd.read_csv('더미데이터2000명\dummy_data_2000_participations.csv')
    except FileNotFoundError as e:
        print(f"❌ ERROR: 필수 파일({e.filename})을 찾을 수 없습니다.")
        print("    먼저 데이터 생성 코드를 실행하여 데이터 파일을 생성했는지 확인해주세요.")
        return

    # --- 📊 3. 핵심 사용자 분석 ---
    print("📊 STEP 3: Analyzing to find top 10 power users...")
    participation_counts = df_participations['user_id'].value_counts().reset_index()
    participation_counts.columns = ['user_id', 'participation_count']
    top_10_users = participation_counts.head(10)
    top_10_details = pd.merge(top_10_users, df_users, left_on='user_id', right_on='id')

    print("\n---  핵심 사용자(Power User) TOP 10 ---")
    print(top_10_details[['nickname', 'name', 'participation_count']].to_string(index=False))

    # --- 🎨 4. 시각화 ---
    print("\n🎨 STEP 4: Creating visualization...")
    plt.figure(figsize=(12, 8))
    
    barplot = sns.barplot(
        x='participation_count', 
        y='nickname', 
        data=top_10_details, 
        palette='rocket_r',
        orient='h'
    )
    
    plt.title('우리 서비스의 핵심 사용자 TOP 10', fontsize=18, pad=15)
    plt.xlabel('총 참여 횟수', fontsize=12)
    plt.ylabel('닉네임', fontsize=12)
    plt.grid(axis='x', linestyle='--', alpha=0.6)
    
    for p in barplot.patches:
        width = p.get_width()
        plt.text(width + 0.1, p.get_y() + p.get_height() / 2,
                 f'{int(width)}회', va='center', fontsize=11)

    plt.tight_layout()
    
    # --- 🖼️ 5. 이미지 파일로 저장 ---
    filename = "power_users_top10.png"
    plt.savefig(filename)
    print(f"\n✅ Chart successfully saved as '{filename}'")

# --- 스크립트 실행 ---
if __name__ == "__main__":
    find_and_visualize_power_users()