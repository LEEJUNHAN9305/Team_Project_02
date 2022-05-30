import pandas as pd


df = pd.DataFrame()
for path in range(3):
    df_temp = pd.read_csv(f'./Crawling_data/crawling_data_concat_{path}.csv')
    df = pd.concat([df, df_temp])
df.dropna(inplace=True)
df.reset_index(inplace=True, drop=True)
print(df.head())
print(df.tail())
df.info()
df.to_csv('./crawling_data/crawling_data_concat_final.csv', index=False)