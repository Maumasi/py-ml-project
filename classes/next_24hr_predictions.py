
class next_24(object):
    """docstring for next_24."""
    def __init__(self, arg):
        super(next_24, self).__init__()
        self.arg = arg


        from data_prep import *
        from train_model import *

        # pass in data
        data = 'data/EURUSD_2016_AUG_NOV.csv'
        # 15 min records
        data_15 = data_prep(data, custom_hour = 3, parse_time = True)

        price_open = 2
        price_high = 3
        price_low = 4
        price_close = 5

        # prep training data for prices
        high_data = data_prep(data, price_high)
        low_data = data_prep(data, price_low)
        # extract training data

        # init RNN models: this also trains the RNN model
        model_high = train_model(
                high_data.x_train,
                high_data.y_train,
                batch_size = 200,
                epochs = 5
            )

        model_low = train_model(
                low_data.x_train,
                low_data.y_train,
                batch_size = 200,
                epochs = 5
            )

        # set up traind models
        candle_high = model_high.rnn
        candle_low = model_low.rnn

        # make predictions
        p_data = 'data/EURUSD_2017_JAN_APR.csv'

        # pass in assesment data
        high_data_p = data_prep(p_data, price_high)
        low_data_p = data_prep(p_data, price_low)

        # make predictions
        high_data_p.prediction(p_data, candle_high, price_high)
        low_data_p.prediction(p_data, candle_low, price_low)

        p_highs = high_data_p.last_prediction
        p_lows = low_data_p.last_prediction
