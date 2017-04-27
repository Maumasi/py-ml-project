# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import MinMaxScaler


class data_prep(object):
    """docstring for data_prep."""
    def __init__(self, data, price_position = 2, custom_hour = 1, custom_minute = 15, parse_time = False):
        super(data_prep, self).__init__()
        self.x_train = []
        self.y_train = []
        # init arrays for
        self.custom_hh = []
        self.custom_mm = []
        self.mm_15 = []
        self.mm_30 = []
        self.hh_1 = []
        self.hh_4 = []
        self.dd_1 = []
        self.predicted_price = []
        self.last_prediction = 0.0
        self.feature_scaler = MinMaxScaler()
        # prep data and set time frames
        self.__prep(data, price_position)
        self.__parse_time_frames(data, custom_hour = custom_hour, custom_minute = custom_minute, price_position = price_position, parse_time = parse_time)
        
    def prediction(self, data, rnn, price_position = 3):
        p_data = pd.read_csv(data)
        p_data = p_data.iloc[:, price_position:price_position + 1].values
        # self.feature_scaler.fit_transform(p_data)
        
        inputs = self.feature_scaler.transform(p_data)
        # input fields
        records = len(p_data)
        time_step = 1
        features = 1
        inputs = np.reshape(inputs, (records, time_step, features))
        # make predictions
        predicted_price = rnn.predict(inputs)
        self.predicted_price = self.feature_scaler.inverse_transform(predicted_price)
        last_prediction = float(self.predicted_price[len(self.predicted_price) - 1][0])
        self.last_prediction = float(int(last_prediction * 100000)) / 100000
            


    def __prep(self, data, price_position = 3):

        if isinstance(data, str):
            # create training set
            training_original = pd.read_csv(data)
            training_set = training_original.iloc[:, price_position:price_position + 1].values

        else:
            training_set = data

        training_set_scaled = self.feature_scaler.fit_transform(training_set)
        # num to drop the last record
        max_training_records = len(training_set_scaled) - 1

        # getting the inputs/outputs
        # train learning
        x_train = training_set_scaled[:max_training_records]
        # train answers: this is offset by 1
        self.y_train = training_set_scaled[1:len(training_set_scaled)]

        # reshaping
        # training offset: time-step
        time_step = 1
        number_of_features = 1
        x_train = np.reshape(x_train, (max_training_records, time_step, number_of_features))
        self.x_train = x_train

    # the time frame defaults are only for referance, thaey can be augmented but it is not suggested. Parse time frames into...
    # min: 5, 15, 30
    # hr: 1, 4, 23
    def __parse_time_frames(self, data, custom_hour, custom_minute, price_position = 2, parse_time = False, m_15 = 15, m_30 = 30, h_1 = 1, h_4 = 4):
        if not parse_time:
            return -1
        t_5 = pd.read_csv(data).values
        # create arrays for the different time frames to train individual RNN's on
        for row in range(len(t_5)):
            date = t_5[row][1]
            
            time = date[-12:-7]
            time = time.split(':')
            hh = int(time[0])
            mm = int(time[1])

            date2 = t_5[row - 1][1]
            time2 = date2[-12:-7]
            time2 = time2.split(':')
            hh2 = int(time2[0])
            mm2 = int(time2[1])
            
            # prevent multiple hous from being pushed to time frame array
            last_hour = 0
            first_hour_num = self.__first_hour(hh, last_hour)
            # prevent any dup prices. This happens on times recorded on closed market hours
            no_dup = self.__no_dups(t_5[row - 1][2], t_5[row][2], t_5[row - 1][3], t_5[row - 1][3])

            if hh != hh2:
                if hh == 23 and first_hour_num and no_dup:
                    self.dd_1.append(t_5[row, price_position])

                if hh % h_4 == 0 and hh > h_4 and first_hour_num and no_dup:
                    self.hh_4.append(t_5[row, price_position])
                
                if hh % custom_hour == 0 and hh > custom_hour and first_hour_num and no_dup:
                    self.custom_hh.append(t_5[row, price_position])

            if mm == 0 and no_dup:
                self.hh_1.append(t_5[row, price_position])

            if mm % m_30 == 0 and row > m_30 and no_dup:
                self.mm_30.append(t_5[row, price_position])

            if mm % m_15 == 0 and row > m_15 and no_dup:
                self.mm_15.append(t_5[row, price_position])
            
            if mm % custom_minute == 0 and row > custom_minute and no_dup:
                self.custom_mm.append(t_5[row, price_position])


    # only used to parse records into time frames
    def __first_hour(self, hour, last_hour):
        if hour != last_hour:
            return True
        else:
            return False

        last_hour = hour

    def __no_dups(self, open1, close1, open2, close2):
        if open1 == open2 and close1 == close2:
            return False
        else:
            return True
