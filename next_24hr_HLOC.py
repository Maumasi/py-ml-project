from predict_HLOC import *
from lab_chart import *
# from time import sleep

data = 'data/EURUSD_2010-current.csv'

highs = []
lows = []
opens = []
closes = []

minutes = (30 * 60)

# only accurate up to 13 (1pm)
for hour in range(20, 24):
    print('hour round: ' + str(hour))
    count = (50 * hour)
    if count >= 200:
        count = 200
        
    time_frame = predict_HLOC(
            data = data,
            batch_size = 150 - ((hour * 3) + (int(hour / 2))),
            epochs = count,
            hour = hour
        )
    
    time_frame.highs()

    highs.append(time_frame.high)
    # give the computer a chance to cool down
    # sleep(minutes)



chart = lab_chart()
# 
chart.add_line(highs, color = 'green', label = 'Highs')
chart.add_line(lows, color = 'red', label = 'Lows')
chart.add_line(opens, color = 'black', label = 'Open')
chart.add_line(closes, color = 'blue', label = 'Close')

chart.render()
