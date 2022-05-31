import numpy as np
import pandas as pd

pd.set_option('display.max_seq_items', None)
df = pd.read_csv('./Crawling_data/crawling_data_concat_final.csv')

# 리뷰가 10글자 미만인 리뷰 NaN화
for i in range(len(df)):
    if len(df.iloc[i, 1]) < 10 :
        df.iloc[i, 1] = np.nan

# 리뷰가 공백인 리뷰 NaN화
for i in range(len(df)):
    if df.iloc[i, 1] == ' ':
        df.iloc[i, 1] = np.nan

# 리뷰평가 발견된 광고 NaN화
for i in range(len(df)):
    if df.iloc[i, 1] == '의정부 배달 불가능한 음식점 배달해드립니다 주문만 해주세요 주문은 카톡 트루미스 친추':
        df.iloc[i, 1] = np.nan

# 위에서 NaN 으로 바꾼 불필요한 데이터 제거
df.dropna(inplace=True)

# 샘플링을 할 때 데이터가 너무 적어서 별점 1점짜리 데이터는 삭제
df1 = df[df['star_score'] == 1].index
df = df.drop(df1)

# downsampling
# df_5 = df[df['star_score'] == 5]
# df_4 = df[df['star_score'] == 4]
# df_3 = df[df['star_score'] == 3]
# df_2 = df[df['star_score'] == 2]
# df_5 = df_5.sample(8500)
# df_4 = df_4.sample(8500)
# df_3 = df_3.sample(8500)
# df = pd.concat([df_5, df_4, df_3, df_2], axis=0)

# reset_index 로 index 맞추고 저장
df.reset_index(inplace=True, drop=True)

df.to_csv('./Crawling_data/mat_zip_preprocessing_05.csv', index = False)