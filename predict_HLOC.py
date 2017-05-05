
from data_prep import *
from train_model import *

class predict_HLOC(object):
    """docstring for predict_HLOC."""
    def __init__(self, data, batch_size = 50, epochs = 100, hour = 1, minute = 1):
        super(predict_HLOC, self).__init__()
        self.hour = hour
        self.minute = minute
        self.data = data
        self.batch_size = batch_size
        self.epochs = epochs
        self.high = 0.0
        self.low = 0.0
        self.open = 0.0
        self.close = 0.0
        # pass in data for custom hour
        self.filtered_data_hh = data_prep(self.data, custom_hour = self.hour, parse_time = True)
        self.hour_data = self.filtered_data_hh.custom_hh
        # pass data for custom minute
        self.filtered_data_mm = data_prep(self.data, custom_minute = self.minute, parse_time = True)
        self.minute_data = self.filtered_data_mm.custom_mm

        
    def all(self):
        price_open = 2
        price_high = 3
        price_low = 4
        price_close = 5

        # prep training data for prices
        data = data_prep(self.hour_data, price_high)
        #low_data = data_prep(self.hour_data, price_low)
        #open_data = data_prep(self.hour_data, price_open)
        #close_data = data_prep(self.hour_data, price_close)
        # extract training data

        # init RNN models: this also trains the RNN model
        model_high = train_model(
                data.x_train,
                data.y_train,
                batch_size = self.batch_size,
                epochs = self.epochs
            )

        model_low = train_model(
                data.x_train,
                data.y_train,
                batch_size = self.batch_size,
                epochs = self.epochs
            )

        model_open = train_model(
                data.x_train,
                data.y_train,
                batch_size = self.batch_size,
                epochs = self.epochs
            )

        model_close = train_model(
                data.x_train,
                data.y_train,
                batch_size = self.batch_size,
                epochs = self.epochs
            )

        # set up traind models
        candle_high = model_high.rnn
        candle_low = model_low.rnn
        candle_open = model_open.rnn
        candle_close = model_close.rnn

        # pass in assesment data
        high_data_p = data_prep(self.data, price_high)
        low_data_p = data_prep(self.data, price_low)
        open_data_p = data_prep(self.data, price_open)
        close_data_p = data_prep(self.data, price_close)

        # make predictions
        high_data_p.prediction(self.data, candle_high, price_high)
        low_data_p.prediction(self.data, candle_low, price_low)
        open_data_p.prediction(self.data, candle_open, price_open)
        close_data_p.prediction(self.data, candle_close, price_close)

        # pass the next prediction for the given hour
        self.high = high_data_p.last_prediction
        self.low = low_data_p.last_prediction
        self.open = open_data_p.last_prediction
        self.close = close_data_p.last_prediction
        
    
        
    def highs(self):
        price_high = 3
        # prep training data for prices
        high_data = data_prep(self.hour_data, price_high)
        # init RNN models: this also trains the RNN model
        model_high = train_model(
                high_data.x_train,
                high_data.y_train,
                batch_size = self.batch_size,
                epochs = self.epochs
            )
        # set up traind models
        candle_high = model_high.rnn
        # pass in assesment data
        high_data_p = data_prep(self.data, price_high)
        # make predictions
        high_data_p.prediction(self.data, candle_high, price_high) 
        # pass the next prediction for the given hour
        self.high = high_data_p.last_prediction
        
    def lows(self):
        price_low = 4
        # prep training data for prices
        low_data = data_prep(self.hour_data, price_low)
        # init RNN models: this also trains the RNN model
        model_low = train_model(
                low_data.x_train,
                low_data.y_train,
                batch_size = self.batch_size,
                epochs = self.epochs
            )
        # set up traind models
        candle_low = model_low.rnn
        # pass in assesment data
        low_data_p = data_prep(self.data, price_low)
        # make predictions
        low_data_p.prediction(self.data, candle_low, price_low)
        # pass the next prediction for the given hour
        self.low = low_data_p.last_prediction
    
    
    def opens(self):
        price_open = 2

        # prep training data for prices
        open_data = data_prep(self.hour_data, price_open)
        # init RNN models: this also trains the RNN model
        model_open = train_model(
                open_data.x_train,
                open_data.y_train,
                batch_size = self.batch_size,
                epochs = self.epochs
            )
        # set up traind models
        candle_open = model_open.rnn
        # pass in assesment data
        open_data_p = data_prep(self.data, price_open)
        # make predictions
        open_data_p.prediction(self.data, candle_open, price_open)
        # pass the next prediction for the given hour
        self.open = open_data_p.last_prediction
        
    
    def closes(self):
        price_close = 5
        # prep training data for prices
        close_data = data_prep(self.hour_data, price_close)
        # extract training data
        # init RNN models: this also trains the RNN model
        model_close = train_model(
                close_data.x_train,
                close_data.y_train,
                batch_size = self.batch_size,
                epochs = self.epochs
            )
        # set up traind models
        candle_close = model_close.rnn
        # pass in assesment data
        close_data_p = data_prep(self.data, price_close)
        # make predictions
        close_data_p.prediction(self.data, candle_close, price_close)
        # pass the next prediction for the given hour
        self.close = close_data_p.last_prediction
        
