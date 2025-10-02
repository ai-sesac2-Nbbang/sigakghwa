Markdown

# MoguMogu: 
# 공동구매 플랫폼 더미 데이터 생성 및 분석 프로젝트


> "같이 사는 즐거움, 모구모구에서 시작돼요"

생활권 기반 공동구매 플랫폼 '모구모구'의 서비스 기획 및 데이터 분석을 위한 더미 데이터 생성 및 시각화 프로젝트입니다.

## 🌟 프로젝트 특징

- **현실적인 더미 데이터:** 단순한 무작위 데이터가 아닌, 실제 사용자 행동 패턴(페르소나, 활동 시간)을 반영한 고품질의 더미 데이터를 생성합니다.
- **확장성:** 코드 상단의 변수 조절을 통해 수백 명부터 수천 명 규모까지 자유롭게 데이터 양을 조절할 수 있습니다.
- **재현 가능성:** Random Seed를 고정하여, 언제 실행해도 항상 동일한 데이터를 생성함으로써 분석 결과의 일관성을 보장합니다.
- **모듈화된 분석:** '데이터 생성' 스크립트와 다양한 '데이터 분석' 스크립트를 분리하여, 원하는 분석을 독립적으로 손쉽게 실행할 수 있습니다.

## 📂 파일 구조

C:/dev/agent/
├── 더미데이터2000명/
│   ├── dummy_data_2000_users.csv
│   ├── dummy_data_2000_posts.csv
│   └── dummy_data_2000_participations.csv
│
├── generate_dummy_data.py  (데이터 생성 마스터 코드)
│
├── analyze_power_users.py
├── analyze_category_by_age.py
├── analyze_category_by_gender.py
├── ... (기타 분석 코드들) ...
│
└── README.md (현재 이 파일)


## 🚀 시작하기

### 1. 사전 준비 (최초 1회)

프로젝트 실행에 필요한 파이썬 라이브러리들을 설치합니다. 터미널에 아래 명령어를 입력하세요.

```bash
pip install pandas faker numpy matplotlib seaborn folium
2. 데이터 생성 (분석 전 항상 1회 실행)
모든 분석의 기반이 되는 '재료'인 더미 데이터 .csv 파일들을 생성합니다.

Bash

# 1. C:\dev\agent\ 폴더로 이동
cd C:\dev\agent

# 2. 마스터 데이터 생성 코드 실행
python generate_dummy_data.py
실행이 완료되면 C:\dev\agent\더미데이터2000명\ 폴더 안에 3개의 .csv 파일이 생성됩니다.

3. 데이터 분석 및 시각화
데이터 생성이 완료된 후, 원하는 분석 코드를 실행하여 .png 또는 .html 형태의 시각화 결과물을 얻을 수 있습니다.

Bash

# 예시: '핵심 사용자(Power User)' 분석 실행
python analyze_power_users.py
📜 스크립트 목록 및 설명
1. 데이터 생성 스크립트
generate_dummy_data.py

설명: 모든 컬럼, 현실적인 페르소나, 대용량 아이템 등이 적용된 최종 '마스터 코드'입니다. 이 파일을 실행하여 모든 분석의 기반이 되는 .csv 데이터를 생성합니다.

주요 설정: 코드 상단의 NUM_USERS, NUM_POSTS, SAVE_PATH 변수를 통해 데이터 규모와 저장 위치를 쉽게 변경할 수 있습니다.

2. 분석 및 시각화 스크립트
각 스크립트는 독립적으로 실행되며, 더미데이터... 폴더에 있는 .csv 파일을 읽어 분석을 수행합니다.

분석 주제	코드 파일명	결과 파일명
핵심 사용자(Power User) TOP 10	analyze_power_users.py	power_users_top10.png
연령대별 관심 카테고리	analyze_category_by_age.py	age_group_category_preference.png
성별 선호 카테고리	analyze_category_by_gender.py	gender_category_preference.png
성별 선호 개별 상품 TOP 10	analyze_item_by_gender.py	gender_item_preference_top10.png
전체 카테고리 인기도	analyze_category_popularity.py	category_popularity_pie_chart.png
인기 가격대 분석	analyze_price_range.py	price_range_popularity.png
모집 인원별 성공률	analyze_success_rate.py	success_rate_by_target_count.png
인기 시간대 (피크 타임)	analyze_peak_hours.py	hourly_activity_trend.png
저조한 시간대 (오프 피크)	analyze_off_peak_hours.py	least_active_hours_top5.png
활동 분포 지도 (가짜 지도)	analyze_activity_map.py	activity_distribution_map.png
활동 분포 지도 (실제 지도)	analyze_real_map.py	activity_real_map.html
활동 밀집도 지도 (클러스터)	analyze_map_clusters.py	activity_map_clusters.html

Sheets로 내보내기
💡 추가 분석 아이디어 (Future Work)
'관심있다'고 한 것과 '실제 구매'의 일치도 분석

인기 게시글의 '모집 완료'까지 걸리는 시간 분석

'우수 모구장(주최자)'의 성공 패턴 분석

'사용자 레벨'과 활동량의 상관관계 분석