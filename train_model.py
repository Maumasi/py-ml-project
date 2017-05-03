
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM

class train_model(object):
    """docstring for train_model."""
    def __init__(self, x_train, y_train, neurons = 100, batch_size = 150, epochs = 50):
        super(train_model, self).__init__()
        self.x_train = x_train
        self.y_train = y_train
        self.neurons = neurons
        self.batch_size = batch_size
        self.epochs = epochs
        self.rnn = Sequential()
        self.__train()


    def __train(self, neurons = 100, batch_size = 80, epochs = 100):
        # init RNN
        # rnn_regresion = Sequential()

        # input layer
        rnn_memory = LSTM(
                units = self.neurons,
                activation = 'sigmoid',
                input_shape = (None, 5),
                )

        self.rnn.add(rnn_memory)

        # output layer: output at time-step
        self.rnn.add(Dense(units = 5))

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
                batch_size = self.batch_size,
                epochs = self.epochs
                )
