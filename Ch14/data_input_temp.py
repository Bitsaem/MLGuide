import pymysql
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname('Ch6'))))
from Ch14 import som
from mpl_toolkits.mplot3d import Axes3D

conn = pymysql.connect ( host = 'localhost', user = 'mfe_dongwuk', password = 'aazz'
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

#plt.plot(daily_return_change)

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


#set up som_anlaysis

nNodesEdge = 20
temp = f_input_data_truncation.ix[:,'DReturnC':'DVolumeC']
data = temp.values
# chanage dataframe to numpy array

net = som.som(nNodesEdge,nNodesEdge,data,usePCA=0)
step = 0.2

# Train the network for 0 iterations (to get the position of the nodes)
"""
net.somtrain(data,0)
pl.figure(1)
for i in range(net.x*net.y):
    neighbours = np.where(net.mapDist[i,:]<=step)

    t = np.zeros((np.shape(neighbours)[1]*2,np.shape(net.weights)[0]))
    t[::2,:] = np.tile(net.weights[:,i],(np.shape(neighbours)[1],1))
    t[1::2,:] = np.transpose(net.weights[:,neighbours[0][:]])
    pl.plot(t[:,0],t[:,1],'g-')
pl.axis('off')

pl.figure(2)

net.somtrain(data,5)
for i in range(net.x*net.y):
    neighbours = np.where(net.mapDist[i,:]<=step)

    t = np.zeros((np.shape(neighbours)[1]*2,np.shape(net.weights)[0]))
    t[::2,:] = np.tile(net.weights[:,i],(np.shape(neighbours)[1],1))
    t[1::2,:] = np.transpose(net.weights[:,neighbours[0][:]])
    pl.plot(t[:,0],t[:,1],'g-')
pl.axis('off')
"""
net.somtrain(data,100)
"""
pl.figure(3)
pl.plot(data[:,0],data[:,1],'.')
for i in range(net.x*net.y):
    neighbours = np.where(net.mapDist[i,:]<=step)
    #print neighbours
    #n = tile(net.weights[:,i],(shape(neighbours)[1],1))
    t = np.zeros((np.shape(neighbours)[1]*2,np.shape(net.weights)[0]))
    t[::2,:] = np.tile(net.weights[:,i],(np.shape(neighbours)[1],1))
    t[1::2,:] = np.transpose(net.weights[:,neighbours[0][:]])
    pl.plot(t[:,0],t[:,1],'g-')

"""

z_H = np.zeros(400)
z_L = np.zeros(400)
z_N = np.zeros(400)
for i in range(1794):
        result = net.somfwd(data[i,:])
        neuron_index = result[0]
        if temp_sorting[i] == 'H' :
            z_H[neuron_index] += 1
        elif temp_sorting[i] == 'L' :
             z_L[neuron_index] += 1
        else :
            z_N[neuron_index] += 1
            

fig = plt.figure()
ax = fig.add_subplot(111, projection = "3d")

ax.set_xlabel("x")
ax.set_ylabel("y") 
ax.set_zlabel("z")
ax.set_xlim3d(0,100)
ax.set_ylim3d(0,100) 
xpos = list()
ypos = list()
for i in range(20) :
    for j in range (20):
        xpos.append(4*j + 2) 
        ypos.append(4*i + 2)

dx = 2*np.ones(400)
dy = 2*np.ones(400)
dz = [z_H,z_L,z_N]
zpos = np.zeros(400)   # the starting zpos for each bar
colors = ['r', 'b', 'g', 'y']
for i in range(2):
    ax.bar3d(xpos, ypos, zpos, dx, dy, dz[i], color=colors[i])
    zpos += dz[i]    # add the height of each bar to know where to start the next

plt.gca().invert_xaxis()
plt.show()
