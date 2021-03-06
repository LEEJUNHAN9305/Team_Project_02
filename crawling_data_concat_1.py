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
df.reset_index(inplace=True, drop=True)
print(df.head())
print(df.tail())
df.info()
df.to_csv('./crawling_data/crawling_data_concat_1.csv', index=False)