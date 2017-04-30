# -*- coding: utf-8 -*-

# Pt 1 =-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=--=--=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-==
# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# create training set
training_original = pd.read_csv('data/EURUSD_h1_current_27.csv')
training_set = training_original.iloc[:, 1:].values

# features
feature_scaler = MinMaxScaler()
training_set_scaled = feature_scaler.fit_transform(training_set)
# num to drop the last record
max_training_records = len(training_set_scaled) - 1

# getting the inputs/outputs
# train learning
x_train = training_set_scaled[:max_training_records]
# train answers: this is offset by 1
y_train = training_set_scaled[1:len(training_set_scaled)]

# reshaping
# training offset: time-step
time_step = 1
number_of_features = 5
x_train = np.reshape(x_train, (max_training_records, time_step, number_of_features))



# Pt 2 =-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=--=--=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-==
# train RNN: LSTM
# Importing the Keras libraries and packages
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM

# init RNN
rnn_regresion = Sequential()

neurons = 50
# input layer
rnn_memory = LSTM(
        units = neurons,
        activation = 'sigmoid',
        input_shape = (None, number_of_features),
        )

rnn_regresion.add(rnn_memory)


# output layer: output at time-step
rnn_regresion.add(Dense(units = 5))


# compile RNN
# rmsprop
rnn_regresion.compile(
        optimizer = 'adam',
        loss = 'mean_squared_error'
        )

# fit: train RNN

rnn_regresion.fit(
        x_train,
        y_train,
        batch_size = 150,
        epochs = 5
        )


# Pt 3 =-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=--=--=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-==

# create testing set
test_original = pd.read_csv('data/EURUSD_h1_current_27.csv')

real_price_set = test_original.iloc[:, 1:].values

# scale inputs: feature_scaler
inputs = feature_scaler.transform(real_price_set)

# turn inputs into a 3D array
input_records = len(real_price_set)
input_time_step = 1
input_features = 5
inputs = np.reshape(inputs, (input_records, input_time_step, input_features))

predicted_price = rnn_regresion.predict(inputs)

raw_predicted_price = feature_scaler.inverse_transform(predicted_price)

print('actual prices')
print(test_original)
print('')
print('very next prices')
print(raw_predicted_price)
print('')

# Pt 4: graph results =-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=--=--=-=-=-=-=-=-=-=--=


plt.plot(
        real_price_set, color = 'red',
        label = 'RED = Real EUR/USD 5min price'
        )

plt.plot(
        raw_predicted_price, color = 'green',
        label = 'GREEN = Predidcted EUR/USD 5min price'
        )

# pretty up chart
plt.title('EUR/USD 5min Price Predictions')
plt.xlabel('time')
plt.ylabel('Price')
plt.legend()
plot = plt.show()


# Pt 5: check our accuracy =-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=--=--=-=-=-=-=-=-=

import math
from sklearn.metrics import mean_squared_error

squared = math.sqrt(mean_squared_error(real_price_set, raw_predicted_price))


t = squared/800




# this may be good for using after trained models are made parsing CSVs =-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=--=--=-=-=-=-=-=-=

m_15 = 15
m_30 = 30
h_1 = 1
h_4 = 4

# init arrays for
mm_15 = []
mm_30 = []
hh_1 = []
hh_4 = []
dd_1 = []

last_hour = 0

def first_hour(hour, last_hour):
    if hour != last_hour:
        return True
    else:
        return False

    last_hour = hour
    
def no_dups(open1, close1, open2, close2):
    if open1 == open2 and close1 == close2:
        return False
    else:
        return True



t_5 = pd.read_csv('data/EURUSD_h1_pred_28.csv').values

# create arrays for the different time frames to train individual RNN's on
for row in range(len(t_5)):
    date = t_5[row][0]
    time = date[-12:-7]
    time = time.split(':')
    hh = int(time[0])
    mm = int(time[1])

    date2 = t_5[row - 1][0]
    time2 = date2[-12:-7]
    time2 = time2.split(':')
    hh2 = int(time2[0])
    mm2 = int(time2[1])
    
    no_dup = no_dups(t_5[row - 1][2], t_5[row][2], t_5[row - 1][3], t_5[row - 1][3])
    
    
    first_hour_num = first_hour(hh, last_hour)

    if hh != hh2:
        if hh == 23 and first_hour_num and no_dup:
            dd_1.append(t_5[row, 2])

        if hh % h_4 == 0 and hh > h_4 and first_hour_num and no_dup:
            hh_4.append(t_5[row, 2])

    if mm == 0 and no_dup:
        hh_1.append(t_5[row, 2])

    if mm % m_30 == 0 and row > m_30 and no_dup:
        mm_30.append(t_5[row, 2])

    if mm % m_15 == 0 and row > m_15 and no_dup:
        mm_15.append(t_5[row, 2])




print(len(dd_1))
print(len(hh_4))
print(len(hh_1))
print(len(mm_30))
print(len(mm_15))
