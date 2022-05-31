import seaborn as sns
import numpy as np
from sklearn import preprocessing
import pandas as pd
pd.set_option('display.max_seq_items', None)
df = pd.read_csv('./Crawling_data/crawling_data_concat_final.csv')
#리뷰평이 10자 미만인 리뷰 NaN화
for i in range(len(df)):
    if len(df.iloc[i, 1]) < 10 :
        df.iloc[i, 1] = np.nan
#리뷰평이 공백인 리뷰 NaN화
for i in range(len(df)):
    if df.iloc[i, 1] == ' ':
        df.iloc[i, 1] = np.nan
#리뷰평에서 발견된 광고 NaN화
for i in range(len(df)):
    if df.iloc[i, 1] == '의정부 배달 불가능한 음식점 배달해드립니다 주문만 해주세요 주문은 카톡 트루미스 친추':
        df.iloc[i, 1] = np.nan
#NaN값 제거
df.dropna(inplace=True)
#1점 데이터 제거 - 데이터가 적음
df1 = df[df['star_score'] == 1].index
df = df.drop(df1)
#downsampling -> 안 하기로 결정
# df_5 = df[df['star_score'] == 5]
# df_4 = df[df['star_score'] == 4]
# df_3 = df[df['star_score'] == 3]
# df_2 = df[df['star_score'] == 2]
# df_5 = df_5.sample(8500)
# df_4 = df_4.sample(8500)
# df_3 = df_3.sample(8500)
# df = pd.concat([df_5, df_4, df_3, df_2], axis=0)
df.reset_index(inplace=True, drop=True)
df.to_csv('./Crawling_data/mat_zip_preprocessing_05.csv', index = False)