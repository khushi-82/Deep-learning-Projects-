# -*- coding: utf-8 -*-
"""DL IMDB REVIEW - SENTIMENT ANALYSIS

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1IR_oIQ0h9V_6Uu-s0fzgWy35dMo8kEAT
"""

pip install kaggle

"""IMPORTING THE DEPENDENCIES"""

import os
import json

from zipfile import ZipFile
import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,Embedding, LSTM
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

"""DATA COLLECTION THROUGH KAGGLE API"""

kaggle_dictionary=json.load(open('kaggle.json'))

kaggle_dictionary.keys()

#setup kaggle credentials as environment variables
os.environ["KAGGLE_USERNAME"]= kaggle_dictionary["username"]
os.environ["KAGGLE_KEY"]= kaggle_dictionary["key"]

!kaggle datasets download -d lakshmi25npathi/imdb-dataset-of-50k-movie-reviews

!ls

#unzip the datset file
with ZipFile('imdb-dataset-of-50k-movie-reviews.zip','r') as zip_ref:
  zip_ref.extractall()

!ls

"""LOADING THE DATASET"""

data = pd.read_csv('IMDB Dataset.csv')

data.shape

data.head()

data.tail()

data["sentiment"].value_counts()

data.replace({"sentiment": {"positive":1, "negative":0}}, inplace=True)

data.head()

#split data into training data and testing data
train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)

print(train_data.shape)
print(test_data.shape)

"""DATA PREPROCESSING"""

#tokenisation text data (converting words or phrases into particular number-integerr )
tokenizer = Tokenizer(num_words=5000)
tokenizer.fit_on_texts(train_data["review"])
X_train= pad_sequences(tokenizer.texts_to_sequences(train_data["review"]), maxlen=200)
X_test= pad_sequences(tokenizer.texts_to_sequences(test_data["review"]), maxlen=200)

print(X_train)
print(X_test)

Y_train = train_data["sentiment"]
Y_test = test_data["sentiment"]

print(Y_train)
print(Y_test)

"""BUILDING THE LSTM MODEL (LONG SHORT TERM MEMORY ) - kind of rnn, time series dataset:trend following  , where the input data is linked to previous datset , sequential way , doesnt look on individual dat input"""

#build the model
#adding dropout to prevent from overfitting
model = Sequential()
model.add(Embedding(input_dim=5000, output_dim=128, input_length=200))
model.add(LSTM(128, dropout=0.2, recurrent_dropout=0.2))
model.add(Dense(1, activation="sigmoid"))

model.summary()

5000*128

#compile the model
model.compile(optimizer="adam" , loss="binary_crossentropy", metrics=["accuracy"])

"""TRAINING THE MODEL"""

model.fit(X_train, Y_train , epochs=5, batch_size=64, validation_split=0.2)

"""model evaluation"""

loss, accuracy = model.evaluate(X_test , Y_test)
print(f"Test Loss: {loss}")
print(f"Test Accuracy: {accuracy}")

"""PREDICTIVE SYSTEM BUILDING"""

def predict_sentiment(review):
  #tokenise and pad the review
  sequence = tokenizer.texts_to_sequences([review]) #Corrected method name
  padded_sequence = pad_sequences(sequence, maxlen=200)
  prediction = model.predict(padded_sequence)
  sentiment = "positive" if prediction[0][0] >0.5 else "negative "
  return  sentiment

#example usage
new_review = " This movie was okay  not that  good "
sentiment = predict_sentiment(new_review)
print(f"The sentiment of the review is {sentiment}")

#example usage
new_review = " This movie was  good "
sentiment = predict_sentiment(new_review)
print(f"The sentiment of the review is {sentiment}")