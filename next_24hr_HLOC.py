from predict_HLOC import *
from lab_chart import *
import time
import csv
# from time import sleep

# 1 hour data
# data = 'data/EURUSD_h1_pred_28.csv'

# 5 min data
# data = 'data/EURUSD_5min_pred_27.csv'

# case study day 1 for: May 1st
data = 'data/case_study/EURUSD_h1_case_study_D1_for_2017_5_1.csv'

# hr1 test data
# test_data = 'data/test_accuracy/EURUSD_test_pred_for_28.csv'

# 30 min test data
# test_30_min = 'test/EURUSD_30_m_test.csv'

# arrays used to record to ouput CSV file
times = []
highs = []
lows = []
opens = []
closes = []

# define the iteration range for recording records
# also used with naming the ouput CSV file
price_point = 'highs-and-lows'
traget_month = 'May'
taget_day = 1
# target range
start = 1  # start iteration
stop = 24   # stop iteration

# ranges for 24hrs
# hours:    1 - 24
# minutes:  1 - 1440
mm_30 = 30

# Methods finished being called
# .all()
# .highs() +
# .lows() +
# .opens() +
# .closes()


# only accurate up to 13 (1pm)
for time_ref in range(start, stop):
    batch_size = 50 # (50 - ((time_ref * 5) + (int(time_ref / 2))))
    if batch_size < 5:
        batch_size = 5

    print('Time round: {0}'.format(time_ref))
    print('Batch size: {0}'.format(batch_size))
    count = 10 # (10 + time_ref)
    hour = time_ref
    minutes = (time_ref * mm_30)

    # 200 seems to be a good ref to boil down loss levels
    if count >= 20:
        count = 20

    if batch_size == 5:
        count = 20

    # for predicting custom hour intervals
    time_frame = predict_HLOC(
            data = data, # data,
            batch_size = batch_size,
            epochs = count,
            hour = hour
        )


    # for predicting custom minute intervals
    # time_frame = predict_HLOC(
    #         data = data,
    #         batch_size = batch_size,
    #         epochs = count,
    #         minute = hour
    #     )


    # call price to measure
    # .all()
    time_frame.highs()
    time_frame.lows()
    # time_frame.opens()
    # time_frame.closes()
    # time_frame.opens()


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
file_name = 'predictions/{6}/{7}/{0}_{1}_{2}_{5}_{3}-{4}_new-28-prediction.csv'.format(
        localtime.tm_year,  # current year
        localtime.tm_mon,   # current month
        localtime.tm_mday,  # currnet day
        start,              # begining range for records
        (stop - 1),         # end range for records
        price_point,        # which price recod is being recorded: high, low, open, close
        traget_month,       # prediction month
        taget_day           # prediction day
        )


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
