# -*- coding: utf-8 -*-
"""

"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import datetime
from scipy import stats

data_dir='//data/directory/' #enter your data directory
#convert date and time to total running seconds
def time_to_running_seconds(dates, times):
    datetimestrings = dates + " " + times
    timestamps = []
    for datetimestr in datetimestrings:
        timestamps.append(datetime.datetime.strptime(datetimestr,"%d/%m/%Y %H:%M:%S").timestamp())
    return np.array(timestamps)   

 
# open and plot evaporation rate data
def open_plot_and_save (filename, seperator=',', comment='#'):
    Evapdata=pd.read_csv(filename ,sep=seperator, comment='#')
    Evapdata.columns = ["Date","Time", "Weight","Units", "Comments"]
 
    x_absolute = time_to_running_seconds(Evapdata['Date'], Evapdata['Time'])
    x_relative = x_absolute - x_absolute[0]
    y = Evapdata['Weight']
    
    filepart, file_extension = os.path.splitext(filename)
    plt.plot(x_relative[:3500],y[:3500],'b-')
    plt.title(filepart)
    plt.xlabel('time $[s]$')
    plt.ylabel('weight $[g]$')
    plt.savefig(filepart+".svg")
    plt.show()
    
    y=np.array(y)
    x_relative=np.array(x_relative)
    np.savetxt(filepart+"_running_time_weight.csv", np.c_[x_relative, y], header="Time,Weight",delimiter=',',fmt='%.18g')

#calculate Evaporation rate from gravimetric data
def get_Evaporationrate (filename, seperator=',', comment='#'):
    data=pd.read_csv(filename, sep=seperator, comment=comment)
    data.columns= ["Time", "Weight"]
    x=data['Time']
    y=data['Weight']         

    slope, intercept, r_value, p_value, std_err = stats.linregress(x[10:200], y[10:200])
#    #show fit in graph with all data
#    plt.plot(x, y, 'm-', label='original data')
#    #show fit in graph with just the data fitted
    plt.plot(x[10:200], y[10:200], 'm-', label='original data')
    plt.plot(x[10:200], intercept + slope*x[10:200], 'k--', label='fitted line')
    plt.legend()
    plt.show()
    print("r-squared:", r_value**2)
    print("slope:", slope)
    print("Evaporationrate [cm/s]:", abs(slope)/4.84)#39.52cm^2 glass slides, 4cm^2 steel plates,  4.84cm^2 glass coverslip
    
open_plot_and_save(data_dir+"name.csv") #your filename
get_Evaporationrate(data_dir+"name.csv")
