import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import pandas as pd
import numpy as np
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
from tensorflow.keras.models import load_model
import re
import time

stopwords = pd.read_csv('./stopwords.csv', index_col=0)
form_window = uic.loadUiType('./mat_zip_qt.ui')[0]
okt = Okt()

with open('./models/mat_zip.pickle', 'rb') as f:
    token = pickle.load(f)
with open('./models/encoder.pickle', 'rb') as f:
    encoder = pickle.load(f)

model = load_model('./models/mat_zip_score_prediction_model_0.4993394911289215.h5')

class Exam(QWidget, form_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btn_predict.clicked.connect(self.btn_clicked_slot)
        self.star2.hide()
        self.star3.hide()
        self.star4.hide()
        self.star5.hide()


    def btn_clicked_slot(self):
        reviews = self.review_text.text()
        print(reviews)
        reviews = re.compile('[^가-힣 ]').sub(' ', reviews)
        reviews = okt.morphs(reviews, stem=True)
        dict_data = [[reviews]]
        df = pd.DataFrame(dict_data, columns=['reviews'])
        print(df)

        Y = df['reviews']

        label = encoder.classes_
        # 한글자와 불용어 제거
        for i in range(len(Y)):
            words = []
            for j in range(len(Y[i])):
                if len(Y[i][j]) > 1:
                    if Y[i][j] not in list(stopwords['stopword']):
                        words.append(Y[i][j])
            Y[i] = ' '.join(words)
        tokened_X = token.texts_to_sequences(Y)
        for i in range(len(tokened_X)):
            if len(tokened_X[i]) > 189:
                tokened_X[i] = tokened_X[i][:189]
        X_pad = pad_sequences(tokened_X, 189)
        preds = model.predict(X_pad)
        print(label[np.argmax(preds)])
        self.star2.hide()
        self.star3.hide()
        self.star4.hide()
        self.star5.hide()
        lst = [self.star2, self.star3, self.star4, self.star5]
        for i in range(20):
            self.star2.hide()
            self.star3.hide()
            self.star4.hide()
            self.star5.hide()
            for l in lst:
                l.show()
                time.sleep(0.2)
        if label[np.argmax(preds)] == 2:
            self.star2.show()
            self.starlayout.hide()
            self.lbl_result.setText('별로에요...')
        elif label[np.argmax(preds)] == 3:
            self.star3.show()
            self.starlayout.hide()
            self.lbl_result.setText('그저 그래요...')
        elif label[np.argmax(preds)] == 4:
            self.star4.show()
            self.starlayout.hide()
            self.lbl_result.setText('좋아요 !')
        elif label[np.argmax(preds)] == 5:
            self.star5.show()
            self.starlayout.hide()
            self.lbl_result.setText('최고에요 !')





if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = Exam()
    mainWindow.show()
    sys.exit(app.exec_())