import pandas as pd
import glob
import datetime

data_path = glob.glob('./Crawling_data/*') #* 파일 싹 다 가져오기
print(data_path)


df = pd.DataFrame()
for path in data_path[0:] :
    df_temp = pd.read_csv(path)
    df = pd.concat([df, df_temp], ignore_index=True)
df.dropna(inplace = True)
df.reset_index(inplace= True, drop=True)

print(df.head())
print(df.tail())
# print(df['category'].value_counts())
df.info()
df.to_csv('./Crawling_data/crawling_data_concat_2.csv', index = False)