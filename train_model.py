
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM

class train_model(object):
    """docstring for train_model."""
    def __init__(self, x_train, y_train):
        super(train_model, self).__init__()
        self.x_train = x_train
        self.y_train = y_train
        self.rnn = Sequential()


    def train(self, neurons = 80, batch_size = 80, epochs = 100):
        # init RNN
        # rnn_regresion = Sequential()

        # input layer
        rnn_memory = LSTM(
                units = neurons,
                activation = 'sigmoid',
                input_shape = (None, 1),
                )

        self.rnn.add(rnn_memory)

        # output layer: output at time-step
        self.rnn.add(Dense(units = 1))

        # compile RNN
        # rmsprop
        self.rnn.compile(
                optimizer = 'adam',
                loss = 'mean_squared_error'
                )

        # fit: train RNN
        self.rnn.fit(
                self.x_train,
                self.y_train,
                batch_size = batch_size,
                epochs = epochs
                )
