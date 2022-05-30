import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical
import pickle

pd.set_option('display.unicode.east_asian_width', True)
df = pd.read_csv('./Crawling_data/crawling_data_concat_final.csv')

X = df['reviews']
Y = df['star_score']

encoder = LabelEncoder()
labeled_Y = encoder.fit_transform(Y)
label = encoder.classes_

with open('./models/encoder.pickle', 'wb') as f :
    pickle.dump(encoder, f)

onehot_Y = to_categorical(labeled_Y)
print(onehot_Y)

okt = Okt()

for i in range(len(X)) :
    X[i] = okt.morphs(X[i], stem=True)


stopwords = pd.read_csv('./Crawling_data/stopwords.csv', index_col = 0)


for j in range(len(X)):
    words = []
    for i in range(len(X[j])):
        if len(X[j][i]) > 1:
            if X[j][i]not in list(stopwords['stopword']):
                words.append(X[j][i])
    X[j] = ' '.join(words)

print(X)

token = Tokenizer()
token.fit_on_texts(X)

tokened_X = token.texts_to_sequences(X)
wordsize = len(token.word_index) + 1

with open('./models/mat_zip.pickle', 'wb') as f:
    pickle.dump(token, f)

max = 0
for i in range(len(tokened_X)):
    if max < len(tokened_X[i]):
        max = len(tokened_X[i])
print(max)

X_pad = pad_sequences(tokened_X, max)
print(X_pad)

X_train, X_test, Y_train, Y_test = train_test_split(
    X_pad, onehot_Y, test_size=0.1)
print(X_train.shape, Y_train.shape)
print(X_test.shape, Y_test.shape)

xy = X_train, X_test, Y_train, Y_test
np.save('./Crawling_data/mat_zip_data_max{}_wordsize_{}'.format(max, wordsize), xy)

