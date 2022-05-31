import pandas as pd
import glob
import datetime

data_path = glob.glob('./crawling_data/*')
print(data_path)
df = pd.DataFrame()
for path in data_path[1:]:
    df_temp = pd.read_csv(path)
    df = pd.concat([df, df_temp])
df.dropna(inplace=True)
df.reset_index(inplace=True, drop=True) #인덱스가 있는 것을 합친다면 인덱스를 버림
print(df.head())
print(df.tail())
df.info()
df.to_csv('./crawling_data/crawling_data_concat_0.csv', index=False)