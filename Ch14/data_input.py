import pymysql
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

conn = pymysql.connect ( host = 'localhost', user = 'surf', password = 'stormsex'
                         ,db = 'findb', charset = 'utf8')
sql = " select * from stock_price where stock_price.code = '005930'"
curs = conn.cursor()

rows = curs.execute(sql)


df = pd.read_sql(sql, con=conn)

conn.close()

df['MA_voloume'] = df['volume'].rolling(5).mean()
temp1 = df['MA_voloume']
temp2 = df['volume']
temp3 = (temp1-temp2)/ temp1

prices = df['close'].tolist()
price = df['close']
daily_return = (price / price.shift(1) - 1)
daily_return_avg = daily_return.rolling(5).mean()
daily_return_change = (daily_return - daily_return_avg )/ daily_return_avg
daily_volatility = (df['high'] - df['low'] )/ df['close']
temp_nextdr = daily_return.tolist()
temp_nextdr = temp_nextdr[1:]
temp_nextdr.insert(5697,0)

input_data = { 'date' : df['date'],
               'DReturnC' : daily_return_change.tolist(),
               'DVolumeC' : temp3.tolist(),
               'DVolatilityC' : daily_volatility.tolist(),
               'Next_D_Return' : temp_nextdr
            }

input_data = pd.DataFrame(input_data)
f_input_data = input_data[3794:]
# using data from 2010



f_input_data_truncation = f_input_data[abs(f_input_data['DReturnC']) < 20]
# truncation if Daily Return Change is over 2,000%
temp_sorting = list()
for i in f_input_data_truncation['Next_D_Return'].tolist() :
    if i > 0.02 :
        temp_sorting.append('H')
    elif i < -0.02 :
        temp_sorting.append('L')
    else:
        temp_sorting.append('N')
# sorting data by range of return    


plt.figure()
plt.plot(daily_return_change)
plt.plot(temp3)
plt.plot(daily_volatility)
plt.plot(input_data_temp['DReturnC'])
plt.show()


