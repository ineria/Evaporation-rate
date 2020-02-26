# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 16:53:59 2019

@author: ms01106
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import datetime
from scipy import stats
import glob
import matplotlib.cm
import re
import scipy.constants as const

data_dir='//surrey.ac.uk/Research/Malin_Schulz_PhDproject/Experimental/Evaporation rate/'
files= sorted(glob.glob(data_dir+'*LinkamWarmstage_*.csv'))

        
#convert date and time to total running seconds
def time_to_running_seconds(dates, times):
    datetimestrings = dates + " " + times
    timestamps = []
    for datetimestr in datetimestrings:
        timestamps.append(datetime.datetime.strptime(datetimestr,"%d/%m/%Y %H:%M:%S").timestamp())
    return np.array(timestamps) 

for i, filename in enumerate(files):
    
    name=os.path.basename(filename)
    name,ext=os.path.splitext(name)
    
    color= matplotlib.cm.get_cmap('rainbow')(i/len(files))
    
    Evapdata=pd.read_csv(filename ,sep=',', comment='#')
     
    if len(Evapdata.columns) == 5:               #data recorded with Sartorius balance  
        Evapdata.columns = ["Date","Time", "Weight","Units", "Comments"]
        x_absolute = time_to_running_seconds(Evapdata['Date'], Evapdata['Time'])
        x = (x_absolute - x_absolute[0])[:33000]
        y = Evapdata['Weight'][:33000]
        a=5000                                  #cut-off for linear regression
        
    else: 
        if len(Evapdata.columns) == 2:          #data recorded manually
            Evapdata.columns = ["Time", "Weight"]
            x = Evapdata['Time']
            y = Evapdata['Weight']
            a=72                                #cut-off for linear regression
            
    slope, intercept, r_value, p_value, std_err = stats.linregress(x[:a], y[:a])
            
    
    if "steel" in filename:
        area=4
    if "glass" in filename: 
        area=4.84
    if "petridish" in filename:
        area=const.pi*(2.25**2)

    print(re.sub('Evaporationrate_gravimetric_60_static_', '',name)+" Evaporationrate [nm/s]:", (abs(slope)/area)*1e7)
    plt.plot(x,y,color=color,label=re.sub('Evaporationrate_gravimetric_60_static_', '',name))
    plt.plot(x[:a],intercept+slope*x[:a],'k--',label='_None_')
    plt.xlabel('time [s]')
    plt.ylabel('weight [g]')
    plt.legend(bbox_to_anchor=(1.01, 0.5),loc=6,fancybox=True, framealpha=0)

    
