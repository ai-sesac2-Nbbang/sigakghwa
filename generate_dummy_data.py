# 파일명: generate_dummy_data.py (진짜 최종 마스터 + 인원수 조절 가능 버전)
# 실행위치: C:\dev\agent\

import pandas as pd
from faker import Faker
import numpy as np
import uuid
import random
from datetime import datetime, timedelta
import os

# --- ✨ Seed 고정 ✨ ---
SEED = 42
random.seed(SEED)
np.random.seed(SEED)
Faker.seed(SEED)

# --- ✨✨ 인원수와 게시글 수를 여기서 쉽게 조절하세요! ✨✨ ---
NUM_USERS = 2000
NUM_POSTS = 800  # 사용자 200명에 맞춰 게시글 수도 80개로 조절


def generate_final_master_data():
    """
    상단에서 정의된 인원수만큼, 모든 분석에 필요한 '완전한' 데이터를 생성합니다.
    """
    print(f"⚙️ [마스터 코드 실행] {NUM_USERS}명 규모의 완전한 데이터 생성을 시작합니다...")
    
    fake = Faker('ko_KR')
    SEOUL_BOUNDS = {"min_lat": 37.43, "max_lat": 37.70, "min_lon": 126.73, "max_lon": 127.18}
    def generate_random_point_in_seoul():
        r_lat = random.uniform(SEOUL_BOUNDS["min_lat"], SEOUL_BOUNDS["max_lat"]); r_lon = random.uniform(SEOUL_BOUNDS["min_lon"], SEOUL_BOUNDS["max_lon"])
        return f"POINT({r_lon:.6f} {r_lat:.6f})"

    # --- 👨‍👩‍👧‍👦 1-1. 사용자 데이터 생성 (모든 컬럼 포함) ---
    print(f"👨‍👩‍👧‍👦 {NUM_USERS}명의 사용자 데이터를 생성 중...")
    users_data = []
    for i in range(NUM_USERS):
        birth_date = fake.date_of_birth(minimum_age=20, maximum_age=55); age = (datetime.now().date() - birth_date).days // 365
        if 20 <= age < 30: age_group = '20대'
        elif 30 <= age < 40: age_group = '30대'
        else: age_group = '40대 이상'
        wish_spots_list = [f'(""{random.choice(["우리집","회사"])}"",""{generate_random_point_in_seoul()}"")' for _ in range(random.randint(1,2))]
        users_data.append({
            'id': str(uuid.uuid4()),'name': fake.name(),'nickname': f"{fake.user_name()}_{i}",'email': fake.email(),'phone_number': fake.phone_number(),
            'birth_date': birth_date,'gender': np.random.choice(['male','female']),'profile_image_url': f'https://picsum.photos/id/{i+500}/200/200',
            'interested_categories': f"{{{','.join(random.sample(['생활용품','식품간식류','패션잡화','뷰티헬스케어'], random.randint(1,3)))}}}",
            'wish_markets': f"{{{','.join([generate_random_point_in_seoul() for _ in range(random.randint(1,2))])}}}",'wish_spots': f"{{{','.join(wish_spots_list)}}}",
            'reported_count': np.random.choice([0,1,2], p=[0.95,0.04,0.01]),'created_at': fake.date_time_between(start_date='-1y'),
            'updated_at': fake.date_time_between(start_date='-1y'),'age': age,'age_group': age_group,
            'household_size': np.random.choice(['1인 가구','2인 가구','3인 이상 가구'], p=[0.6,0.25,0.15]),'level': random.randint(1,25)
        })
    df_users = pd.DataFrame(users_data)
    
    # --- 🛒 1-2. 게시글 데이터 생성 (모든 컬럼 포함) ---
    print(f"🛒 {NUM_POSTS}개의 게시글 데이터를 생성 중...")
    post_samples = {"소불고기/목살":"식품간식류","라면/즉석밥":"식품간식류","나이키 맨투맨":"패션잡화","기저귀":"생활용품","롤화장지":"생활용품","올리브영 선크림":"뷰티헬스케어"}
    posts_data = []
    for _ in range(NUM_POSTS):
        item_name = random.choice(list(post_samples.keys())); created_time = fake.date_time_between(start_date='-2M')
        posts_data.append({'id': str(uuid.uuid4()),'user_id': random.choice(df_users['id'].tolist()),'name': item_name,'description': f"대용량 {item_name} 함께!",'price': random.randint(100,500)*100,'mogu_market': generate_random_point_in_seoul(),'mogu_spot': generate_random_point_in_seoul(),'mogu_datetime': fake.date_time_between(start_date=created_time, end_date='+1M'),'status': 'recruiting','target_count': random.randint(3,8),'joined_count': 0,'category': post_samples[item_name],'created_at': created_time})
    df_posts = pd.DataFrame(posts_data)

    # --- ⭐ 1-3. 참여 데이터 생성 (모든 컬럼 포함) ---
    print("⭐ 현실화된 시간 로직으로 참여 데이터를 생성 중...")
    participations_data = []; hours = list(range(24)); probabilities = np.array([0.01,0.005,0.005,0.005,0.005,0.01,0.02,0.03,0.04,0.05,0.05,0.06,0.08,0.07,0.04,0.03,0.03,0.04,0.05,0.07,0.08,0.09,0.06,0.02]); probabilities /= probabilities.sum()
    for index, post in df_posts.iterrows():
        num_participants = random.randint(2, post['target_count']); potential_participants = [pid for pid in df_users['id'] if pid != post['user_id']]
        if len(potential_participants) < num_participants: continue
        selected_participants = random.sample(potential_participants, num_participants); df_posts.loc[index, 'joined_count'] = len(selected_participants)
        for user_id in selected_participants:
            realistic_hour = np.random.choice(hours, p=probabilities); base_date = fake.date_time_between(start_date=post['created_at'], end_date=post['mogu_datetime']).replace(hour=realistic_hour, minute=random.randint(0, 59))
            participations_data.append({'user_id': user_id,'mogu_post_id': post['id'],'status': 'accepted','applied_at': base_date, 'decided_at': base_date + timedelta(hours=random.randint(1, 6))})
    df_participations = pd.DataFrame(participations_data)
    print("✅ 데이터 생성 완료!")

    # --- 💾 PART 2: 최종 파일 저장 ---
    print("\n⚙️ PART 2: 생성된 최종 데이터 파일을 저장합니다...")
    df_users.to_csv(f'dummy_data_{NUM_USERS}_users.csv', index=False, encoding='utf-8-sig')
    df_posts.to_csv(f'dummy_data_{NUM_USERS}_posts.csv', index=False, encoding='utf-8-sig')
    df_participations.to_csv(f'dummy_data_{NUM_USERS}_participations.csv', index=False, encoding='utf-8-sig')
    print(f"✅ 저장 완료! {NUM_USERS}명 규모의 데이터 파일 3개가 생성되었습니다.")

if __name__ == "__main__":
    generate_final_master_data()