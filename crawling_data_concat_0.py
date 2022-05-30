import pandas as pd
import glob
import datetime

data_path = glob.glob('./Crawling_data/*')
print(data_path)

df = pd.DataFrame()
for path in data_path:
    df_temp = pd.read_csv(path)
    df = pd.concat([df, df_temp])
df.dropna(inplace=True)
df.reset_index(inplace=True, drop=True) #인덱스가 있는 것을 합친다면 인덱스를 버림
df.info()
df.to_csv('./Crawling_data/crawling_data_concat_0.csv', index=False)