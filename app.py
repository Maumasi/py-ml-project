
from data_prep import *
from train_model import *

# pass in data
data = 'data/EURUSD_2016_AUG_NOV.csv'
# 15 min records
data_15 = data_prep(data)
data_15 = data_15.mm_30

price_open = 2
price_high = 3
price_low = 4
price_close = 5

training_data = data_prep(data, price_close)
x_train = training_data.x_train
y_train = training_data.y_train

# train models
model = train_model(x_train, y_train)

model.train()



# set up traind model
f = model.rnn

