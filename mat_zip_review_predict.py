import pandas as pd
import numpy as np
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical
import pickle
from tensorflow.keras.models import load_model
import re

reviews = input()
reviews = re.compile('[^가-힣 ]').sub(' ', reviews)
reviews = Okt.morphs(reviews, stem=True)
dict_data = [[reviews]]
df = pd.DataFrame(dict_data, columns=['reviews'])
print(df)

Y = df['reviews']

with open('./models/encoder.pickle', 'rb') as f:
    encoder = pickle.load(f)

label = encoder.classes_

stopwords=pd.read_csv('./stopwords.csv', index_col=0)

# 한글자와 불용어 제거
for i in range(len(Y)) :
    words = []
    for j in range(len(Y[i])):
        if len(Y[i][j]) > 1:
            if Y[i][j] not in list(stopwords['stopword']):
                words.append(Y[i][j])
    Y[i] = ' '.join(words)

# 토큰화 하기
with open('./models/mat_zip.pickle', 'rb') as f:
    token = pickle.load(f)

tokened_X = token.texts_to_sequences(Y)

# 예측대상 padding
for i in range(len(tokened_X)) :
    if len(tokened_X[i]) > 189 :
        tokened_X[i] = tokened_X[i][:189]
X_pad = pad_sequences(tokened_X, 189)

# 모델 예측
model = load_model('./models/mat_zip_score_predict_model_0.4993394911289215.h5')
preds = model.predict(X_pad)

# 모델이 최상위로 분류한 카테고리와 차상위로 높게 분류한 카테고리로 다중분류
predicts = []
for pred in preds:
    most = label[np.argmax(pred)]   # 예측값의 가장 큰 값을 선언해두고
    pred[np.argmax(pred)] = 0       # 0으로 만듦
    second = label[np.argmax(pred)] # 그럼 두번째로 큰 값으로 선언할 수 있음
    predicts.append([most, second]) # 예측값의 가장 큰 값의 indexing number로 index한 값과 두번째로 큰 값을 list 형태로 predicts에 삽입
df['predict'] = predicts
print(df)