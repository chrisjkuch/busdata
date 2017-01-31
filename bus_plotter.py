# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 17:28:01 2016

@author: chris
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as md
import numpy as np
import datetime as dt


def dayTimeToDateTime(fltime):
    hours = int(fltime * 24)
    minutes = int(fltime * 24 * 60 - hours * 60)
    seconds = 0 #int(fltime * 24 * 3600 - hours * 60 * 60 - minutes * 60)
    return(dt.datetime(2016,8,1,hours,minutes,seconds))

def setSameDay(dt_obj):
    return(dt.datetime(2016,8,1,dt_obj.hour,dt_obj.minute,dt_obj.second))    

# Temporary: Pick the stop we are interested in
stop = u'Sherman/Foster'
etoc = pd.read_csv('evanstontochicago.csv')
ctoe = pd.read_csv('chicagotoevanston.csv')

# Get the x-coordinates of vertical lines marking scheduled times


# Read the log data from the spreadsheet
busdata = pd.read_csv('test.csv')
bd = busdata[[u'Stop Name', u'Time']]
bd[u'Time'] = bd[u'Time'].astype('datetime64').apply(lambda x: md.date2num(setSameDay(x)))

groupedstops = bd.groupby(u'Stop Name')
curStop = bd.groupby(u'Stop Name').groups[stop]

times = bd.iloc[curStop, 1]
#times = times.apply(lambda x: md.date2num(setSameDay(x)))

# Set up the histogram
fig = plt.figure()
my_bins = md.date2num(dt.datetime(2016,8,1,0,0,0)) + np.linspace(6,24,(18*60)+1)/24.
hfmt = md.DateFormatter('%H:%M')
thisroute = etoc
thesestops = list(thisroute.columns.values)
nplots = len(thesestops)
i = 1
all_axes = []
for stop in thesestops:
    if(i > 1):
        fig.add_subplot(nplots, 1, i, sharex=all_axes[0], sharey=all_axes[0])
    else:
        fig.add_subplot(nplots, 1, 1)
    i += 1
    curStop = groupedstops.groups[stop]
    curTimes = bd.iloc[curStop, 1]
    ax = curTimes.plot.hist(bins=my_bins)
    ax2 = curTimes[-1:].plot.hist(bins=my_bins)
    all_axes.append(ax)
    #nboundsched = etoc[stop].apply(lambda x: md.date2num(dayTimeToDateTime(x)))
    cursched = thisroute[stop].apply(lambda x: md.date2num(dayTimeToDateTime(x)))
    top = 6
    #y1n = [0] * len(nboundsched)
    #y2n = [top] * len(nboundsched)
    y1 = [0] * len(cursched)
    y2 = [top] * len(cursched)
    plt.vlines(cursched, y1, y2)
    ax.xaxis.set_major_locator(md.HourLocator())
    ax.xaxis.set_major_formatter(hfmt)
    ax.yaxis.set_ticks([])
    ax.yaxis.set_label_position('right')
    plt.ylabel(stop, rotation=0)
#stopdata = scheduledata[stop].apply(lambda x: md.date2num(dayTimeToDateTime(x)))
#y1 = [0] * len(stopdata)
#y2 = [2] * len(stopdata)
    
plt.xticks(rotation=45)
plt.xlim([md.date2num(dt.datetime(2016,8,1,6,0,0)), md.date2num(dt.datetime(2016,8,1,23,59,0))])
plt.gcf().subplots_adjust(hspace=0)
plt.show()