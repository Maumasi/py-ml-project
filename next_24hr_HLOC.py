from predict_HLOC import *
from lab_chart import *
import csv
# from time import sleep

# 1 hour data
data = 'data/EURUSD_2010-current.csv'

# 5 min data
# data = 'data/EURUSD_5min_pred_27.csv'
times = []
highs = []
lows = []
opens = []
closes = []



# minutes = (30 * 60)

# only accurate up to 13 (1pm)
for time_ref in range(1, 3):
    print('Time round: ' + str(time_ref))
    count = 1 # (20 * time_ref)
    hour = time_ref
    min_5 = (time_ref * 5)

    # 200 seems to be a good ref to boil down loss levels
    if count >= 200:
        count = 200

    # for predicting custom hour intervals
    time_frame = predict_HLOC(
            data = data,
            batch_size = 150 - ((hour * 3) + (int(hour / 2))),
            epochs = count,
            hour = hour
        )


    # for predicting 5 minute intervals
    # time_frame = predict_HLOC(
    #         data = data,
    #         batch_size = 150 - ((time_ref * 3) + (int(time_ref / 2))),
    #         epochs = count,
    #         minute = min_5
    #     )

    time_frame.all()




    times.append(hour)
    opens.append(time_frame.open)
    highs.append(time_frame.high)
    lows.append(time_frame.low)
    closes.append(time_frame.close)
    # give the computer a chance to cool down
    # sleep(minutes)


# make csv file
output_data = []
chart_data = []
headers = ['time', 'open', 'high', 'low', 'close']
output_data.append(headers)

# prep predictions for CSV file
for i in range(len(times)):
    data = [times[i], opens[i], highs[i], lows[i], closes[i]]
    output_data.append(data)

# write to CSV
with open('some.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(output_data)

# chart = lab_chart()
#
# chart.add_line(highs, color = 'green', label = 'High')
# chart.add_line(lows, color = 'red', label = 'Lows')
# chart.add_line(opens, color = 'black', label = 'Open')
# chart.add_line(closes, color = 'blue', label = 'Close')
#
# chart.render()
