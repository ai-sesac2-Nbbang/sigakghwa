# 파일명: analyze_peak_hours.py
# 실행위치: C:\dev\agent\

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import font_manager, rc

def analyze_peak_participation_hours():
    print("📈 '가장 인기 있는 시간대' 분석을 시작합니다...")
    try:
        font_path = "c:/Windows/Fonts/malgun.ttf"
        rc('font', family=font_manager.FontProperties(fname=font_path).get_name())
    except:
        print("⚠️ 경고: 한글 폰트를 찾을 수 없습니다.")

    try:
        df_participations = pd.read_csv('더미데이터2000명\dummy_data_2000_participations.csv')
    except FileNotFoundError:
        print("❌ ERROR: '더미데이터2000명\dummy_data_2000_participations.csv' 파일을 찾을 수 없습니다.")
        return

    df_participations['applied_at'] = pd.to_datetime(df_participations['applied_at'])
    df_participations['hour_of_day'] = df_participations['applied_at'].dt.hour
    hourly_counts = df_participations['hour_of_day'].value_counts().sort_index()

    print("\n---  시간대별 참여 횟수 ---")
    print(hourly_counts)

    plt.figure(figsize=(15, 7))
    sns.lineplot(x=hourly_counts.index, y=hourly_counts.values, marker='o', color='dodgerblue')
    plt.title(' 참여가 가장 활발한 시간대 (24시간)', fontsize=18, pad=15)
    plt.xlabel('시간대', fontsize=12)
    plt.ylabel('총 참여 횟수', fontsize=12)
    plt.xticks(range(24))
    plt.grid(True, linestyle='--', alpha=0.6)
    
    peak_hour = hourly_counts.idxmax()
    peak_count = hourly_counts.max()
    plt.annotate(
        f'Peak Time!\n{peak_hour}시 ({peak_count}회)', xy=(peak_hour, peak_count),
        xytext=(peak_hour, peak_count + 5),
        arrowprops=dict(facecolor='tomato', shrink=0.05),
        fontsize=12, fontweight='bold', ha='center'
    )
    plt.tight_layout()
    
    filename = "hourly_activity_trend.png"
    plt.savefig(filename)
    print(f"\n✅ 분석 완료! '{filename}' 이름으로 그래프가 저장되었습니다.")

if __name__ == "__main__":
    analyze_peak_participation_hours()