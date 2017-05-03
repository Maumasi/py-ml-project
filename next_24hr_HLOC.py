from predict_HLOC import *
from lab_chart import *
import time
import csv
# from time import sleep

# 1 hour data: gives the range of each line
data = 'data/EURUSD_h1_current_27.csv'

# 1 minute data
#data = 'data/EURUSD_Candlestick_1_m_ASK_05.01.2015-27.04.2017.csv'

# 5 min data
# data = 'data/EURUSD_5min_pred_27.csv'

# case study day 1 for: May 1st
# data = 'data/case_study/EURUSD_h1_case_study_D1_for_2017_5_1.csv'

# arrays used to record to ouput CSV file
times = []
highs = []
lows = []
opens = []
closes = []

# define the iteration range for recording records
# also used with naming the ouput CSV file
price_point = 'close'
traget_month = 'May'
taget_day = 1
# target range
start = 1  # start iteration
stop = 20   # stop iteration



# Methods finished being called
# .all() 
# .highs()
# .lows()
# .opens()
# .closes()


# only accurate up to 13 (1pm)
for time_ref in range(start, stop):
    # for 1hr records
    batch_size = 50 # + (time_ref * 50) #(50 - ((time_ref * 5) + (int(time_ref / 2))))
    
    #for 1min records
    #batch_size = 350
    
    print('Time round: {0}'.format(time_ref))
    print('Batch size: {0}'.format(batch_size))
    count = (20 * time_ref)
    hour = time_ref
    min_5 = (time_ref * 5)


    # for predicting custom hour intervals
    time_frame = predict_HLOC(
            data = data,
            batch_size = batch_size,
            epochs = 50, # count,
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
    time_frame.highs()
    #time_frame.lows()
    #time_frame.opens()
    #time_frame.closes()


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
file_name = 'predictions/{6}/{7}/{0}_{1}_{2}_{5}_{3}-{4}_demo-prediction.csv'.format(
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
