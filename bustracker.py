# -*- coding: utf-8 -*-
"""
DoubleMap Bus Tracker
Created on Tue May 16 19:14:28 2017
@author: chris
"""

from doublemap import DoubleMap
import time
import datetime
from copy import deepcopy
import os.path
import csv

class BusTracker:
    '''
        This class tracks buses associated with a given DoubleMap network. It 
        records the timestamp at which each bus' "last stop" changes, 
        corresponding to the bus making a stop. This data is written to a
        comma-separated value file that can be specified by the user.
    '''
    
    def __init__(self, networkName, outputFile='bus_data.csv', verbose=False):
        '''
            Constructor initializes the tracker by reading in the name and 
            collecting the different route numbers.
            Params: string networkName (example: 'northwestern')
                    string outputFile (example: 'bus_data.csv')
                    boolean verbose (example: True)
        '''
        self.network = networkName
        self.tracker = DoubleMap(networkName)
        self.outputFile = outputFile
        self.verbose = verbose
        self.last_stops = {}
    
        # Update all route information
        self.update_stops()
        self.update_routes()
        self.update_buses()
        
        # Create file if none exists
        if not os.path.isfile(outputFile):
            with open(outputFile, 'w') as datafile:
                datafile.write(','.join(['utc_time', 
                                         'timestamp', 
                                         'route_id', 
                                         'route_name', 
                                         'stop_id', 
                                         'stop_name', 
                                         'stop_lat', 
                                         'stop_lon', 
                                         'bus_id', 
                                         'bus_name']))
                datafile.write('\n')
        
    def update_stops(self):
        ''' Update stop information '''
        if self.verbose: print('Getting stops')
        self.stops = self.tracker.stops
        self.stop_ids = list(self.stops.keys())
        if self.verbose: print(self.stop_ids)
        
    def update_routes(self):
        ''' Update the list of routes '''
        if self.verbose: print('Getting routes')
        self.routes = self.tracker.routes
        self.route_ids = list(self.routes.keys())
        if self.verbose: 
            for route in self.route_ids:
                print(self.routes[route]['name'] + ' is route ' + str(route))
        
    def update_buses(self):
        ''' Update the list of buses '''
        if self.verbose: print('Updating list of buses')
        self.buses = self.tracker.buses
        self.bus_ids = list(self.buses.keys())
        for bus in self.bus_ids:
            self.last_stops[bus] = self.buses[bus]['lastStop']
            if self.verbose: print(self.buses[bus]['name'] + ' is on route ' + 
                str(self.buses[bus]['route']) + ' with id ' + str(bus) + 
                ' and last stop was ' + str(self.buses[bus]['lastStop']))
                
    def record_stop(self, bus_id, stop_id):
        ''' Record the stop in the output file '''
        utc_time = int(time.time())
        dt = datetime.datetime.fromtimestamp(utc_time)
        time_str = dt.strftime('%Y-%m-%d %H:%M:%S')

        to_print = [utc_time, # UTC
                    time_str, # Human-readable timestamp
                    self.network, 
                    self.buses[bus_id]['route'], # Route ID
                    self.routes[self.buses[bus_id]['route']]['name'], # Route name
                    stop_id, # Stop ID
                    self.stops[stop_id]['name'], # Stop name
                    self.stops[stop_id]['lat'],  # Stop latitude
                    self.stops[stop_id]['lon'], # Stop longitude
                    bus_id, # Bus ID
                    self.buses[bus_id]['name']] # Bus name
        if self.verbose: print(to_print)
            
        with open(self.outputFile, 'a') as of:
            writer = csv.writer(of)
            writer.writerow(to_print)
                          
    def track(self):
        '''
            Start tracking the buses. Start by logging the current 'last stop'
            of all the buses, then continually check to see whether the has
            changed.
        '''
        while(True):
            previous_stops = deepcopy(self.last_stops)
            self.update_buses()
            for bus_id in previous_stops:
                if bus_id in self.last_stops and previous_stops[bus_id] != self.last_stops[bus_id]:
                    self.record_stop(bus_id, self.last_stops[bus_id])
                
            time.sleep(5)
        
    
def main():
    ''' Standalone run function '''
    tracker = BusTracker('northwestern', verbose=False)
    tracker.track()

if __name__ == '__main__':
    main()