import seaborn as sns
import numpy as np
from sklearn import preprocessing
import pandas as pd
pd.set_option('display.max_seq_items', None)
df = pd.read_csv('./Crawling_data/crawling_data_concat_final.csv')
# df.info()

# print(df.head().isnull())
# print(df['star_score'].unique())

# print(df['reviews'].value_counts(ascending=True))

for i in range(len(df)):
    if df.iloc[i, 1] == ' ':
        df.iloc[i, 1] = np.nan
print(df.isna().sum())
for i in range(len(df)):
    if df.iloc[i, 1] == '의정부 배달 불가능한 음식점 배달해드립니다 주문만 해주세요 주문은 카톡 트루미스 친추':
        df.iloc[i, 1] = np.nan
print(df.isna().sum())
df.dropna(inplace=True)

df.reset_index(inplace=True, drop=True)
# df.info()

df.to_csv('./Crawling_data/mat_zip_preprocessing.csv', index = False)