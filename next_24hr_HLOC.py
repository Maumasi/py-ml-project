from predict_HLOC import *
from lab_chart import *
import time
import csv
# from time import sleep

# 1 hour data
data = 'data/EURUSD_h1_current_27.csv'

# 5 min data
# data = 'data/EURUSD_5min_pred_27.csv'
times = []
highs = []
lows = []
opens = []
closes = []


# only accurate up to 13 (1pm)
for time_ref in range(1, 20):
    print('Time round: ' + str(time_ref))
    count = 1# (20 * time_ref)
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
    
    
    # call price to measure
    # .all()
    # .highs()
    # .lows()
    # .opens()
    # .closes()
    time_frame.highs()


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
localtime = time.localtime(time.time())
file_name = '{0}_{1}_{2}_prediction.csv'.format(localtime.tm_year, localtime.tm_mon, localtime.tm_mday)
with open(file_name, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(output_data)

print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
print('FINISHED')
print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')

# chart = lab_chart()
#
# chart.add_line(highs, color = 'green', label = 'High')
# chart.add_line(lows, color = 'red', label = 'Lows')
# chart.add_line(opens, color = 'black', label = 'Open')
# chart.add_line(closes, color = 'blue', label = 'Close')
#
# chart.render()
