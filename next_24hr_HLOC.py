from predict_HLOC import *
from lab_chart import *

data = 'data/EURUSD_2010-current.csv'

highs = []
lows = []
opens = []
closes = []

for hour in range(1, 24):
    print('hour round: ' + str(hour))
        
    time_frame = predict_HLOC(
            data = data,
            batch_size = 150 - ((hour * 3) + (int(hour / 2))),
            epochs = (50 * hour),
            hour = hour
        )

    highs.append(time_frame.high)
    lows.append(time_frame.low)
    opens.append(time_frame.open)
    closes.append(time_frame.close)


print('highs')
print(highs)

print('lows')
print(lows)

print('opens')
print(opens)

print('closes')
print(closes)

chart = lab_chart()
# 
chart.add_line(highs, color = 'green', label = 'Highs')
chart.add_line(lows, color = 'red', label = 'Lows')
chart.add_line(opens, color = 'black', label = 'Open')
chart.add_line(closes, color = 'blue', label = 'Close')

chart.render()
