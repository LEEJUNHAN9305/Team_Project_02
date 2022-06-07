import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
import pandas as pd
import numpy as np
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
from tensorflow.keras.models import load_model
import re
import time

stopwords = pd.read_csv('./Crawling_data/stopwords.csv', index_col=0)
form_window = uic.loadUiType('./mat_zip_review_predict_QT_UI.ui')[0]
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
        self.pixmap = QPixmap()
        self.pixmap.load('./Image/score.png')
        self.score.setPixmap(self.pixmap)
    def btn_clicked_slot(self):
        self.lbl_result.setText('')
        self.pixmap.load('./Image/score.png')
        self.score.setPixmap(self.pixmap)
        reviews = self.review_text.toPlainText()
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
        print(type(label[np.argmax(preds)]))

        print('debug1')
        # for i in range(20):
        #     self.star2.hide()
        #     self.star3.hide()
        #     self.star4.hide()
        #     self.star5.hide()
        #     for l in lst:
        #         l.show()
        #         time.sleep(0.2)
        print('debug2')

        evaluation = int(label[np.argmax(preds)])
        print('debug3')
        print(evaluation)
        if evaluation == 2:
            self.pixmap.load('./Image/Two_score.png')
            self.score.setPixmap(self.pixmap)
            print('debug2')
            self.lbl_result.setText('별로예요...')
            print('debug2')
        elif evaluation == 3:
            self.pixmap.load('./Image/Three_score.png')
            self.score.setPixmap(self.pixmap)
            print('debug3')
            self.lbl_result.setText('그저 그래요...')
            print('debug3')
        elif evaluation == 4:
            self.pixmap.load('./Image/Four_score.png')
            self.score.setPixmap(self.pixmap)
            self.lbl_result.setText('좋아요 !')
        elif evaluation == 5:
            self.pixmap.load('./Image/Five_score.png')
            self.score.setPixmap(self.pixmap)
            self.lbl_result.setText('최고예요 !')





if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = Exam()
    mainWindow.show()
    sys.exit(app.exec_())