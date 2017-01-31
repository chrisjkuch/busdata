# -*- coding: utf-8 -*-
"""
bus_data_tracker.py

This scraper takes data from the Northwestern Intercampus shuttle route
and collects information about when each shuttle stops at each stop.
All the information is written to a csv file.
"""


from doublemap import DoubleMap # imports Travis Cunn's python doublemap API
from time import strftime, sleep # import function to print time how we want\
from datetime import datetime

def writeStop(name, route_id, bus_id, stop_id):
    # Before we check in, we need to make sure the bus hasn't gone out of service
    # to avoid getting a KeyError
    if(route_id in tracker.routes.keys() and bus_id in tracker.buses.keys()):
        routeName = tracker.route_info(route_id)[u'name']
        busName = tracker.bus_info(bus_id)[u'name']
        stopName = tracker.stop_info(stop_id)[u'name']
        nowTime = datetime.time(datetime.now())
        secondsSinceMidnight = nowTime.hour * 3600 + nowTime.minute * 60 + nowTime.second
        dataStr = ','.join([str(route_id), routeName, str(bus_id), busName, \
                    str(stop_id), stopName, str(secondsSinceMidnight), str(datetime.now())])
        datafile = open(name, 'a')    
        datafile.write(dataStr + '\n')
        datafile.close()
        stopfile = open('stop_data/' + stopName.replace('/','-').replace(' ','_') + '.csv', 'a')
        stopfile.write(str(secondsSinceMidnight)+'\n')
        stopfile.close()


tracker = DoubleMap('northwestern') # Initiates tracker
filename = 'intercampus_data.csv'

route = 48 # Intercampus shuttle route number or route number of interest

# get the buses that are out there
# keep track of current bus ids and the last stops they made
last_stops = {} 
last_bus_ids = []

i = 0
while(True):
    try:
        new_bus_ids = []
        for bus_id, bus_info in tracker.buses.iteritems(): # gives tuples of (bus_id, bus_info_dict)
            if(bus_info[u'route'] == route): # for buses on our route
                if(bus_id not in last_bus_ids): # if the bus is newly added
                    last_stops[bus_id] = bus_info[u'lastStop'] # record its last stop
                new_bus_ids.append(bus_id) # add the bus to the next iteration
                justStopped = bus_info[u'lastStop']
                if(last_stops[bus_id] != justStopped and i > 0):
                    print('Bus ' + str(bus_id)+ ' just stopped at ' + tracker.stop_info(justStopped)[u'name'] + ' at ' + strftime('%H:%M'))
                    writeStop(filename, route, bus_id, justStopped)
                    last_stops[bus_id] = justStopped
                    
        last_bus_ids = new_bus_ids # add newly added buses, remove deleted buses 
        print(i)
        i = i + 1
    except:
        pass
    sleep(10)
    
