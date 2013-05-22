#!/usr/bin/python
# -*- coding: utf-8 -*-


import MySQLdb as mdb
import gc
import matplotlib
from pylab import *
import time
import sys


'''
ion() # turn on interactive mode
X = np.linspace(-np.pi, np.pi, 256, endpoint=True)
C,S = np.cos(X), np.sin(X)
#show(block=False)
show()
fig = figure()
for i in range(1,11):
    clf()
    plot(X,C*i)
    plot(X,S*i)
    fig.canvas.draw()
    time.sleep(1)
'''



'''
Database rows:
=====================
for df3 data: [Node_id, Window_Num, Station_MAC, Power, Num_Packets, BSSID, Proved_ESSIDs, Millis_Time]
    -> important indices: 0 -> node_id, 1 -> window_num, 4 -> num_packets, 5 -> millis_time

will have one line per node, and will plot by window_num on x-axsis, taking sum of packets that node saw. Also can graph amount of traffic though each access point if we want.
=====================
for drexel guest data: [nodeId, latitude, longitude, firstSwitchedMillis, srcIP, dstIP, srcPort, dstPort, proto, pkts, bytes, tcpControlBits]
    -> important indices: 0 -> node_id, 3 -> firstSwitchedMillis, 4 -> srcIP, 5 -> dstIP, 6 -> srcPort, 7 -> dstPort, 8 -> proto, 9 -> num_packets, 10 -> bytes, 11 - tcpControlBits 

will have one figure per node, showing: # distinct sourceIPs, # distinct destintationIPs, # distinct source ports, # distinct dest ports, # distinct protocols, number of packets, number of bytes, and number of tcp control bits -- each plotted in their own subplots, one data point per time window

can also plot average volume 

'''

class DF3Node:

    def __init__(self, node_id, window_num, num_packets):

    def merge(self, not_self):
        self.num_packets += self.num_packets

    def __eq__(self, not_self):
        if self.node_id == not_self.node_id and self.window_num == not_self.window_num:
            return True
        return False


addr = "129.25.28.81" # NOTE to someone that can explain this to me: why can't we connect via 127.0.0.1?
user = "datamap13"
passwd = "seniordesign13"
schema = "network_data"


gc.collect() # garbage collect to make sure any previous connections to the db were dealt with properly.
connection = mdb.connect(addr, user, passwd, schema);

#query = "select * from "+table_name+" limit "+str(num_rows) # from start of tabl
#query_2 = "select * from myTable limit 5,18446744073709551615" # to get all rows after n'th row, use large number

table_name = "network_data.h_20130516_19_0"
table_name = "network_data.dragonfly3_20130508"
num_rows = 100
start = 0
window_size = 1 # seconds

keep_graphing = True
df3_data = [] # dragonfly 3 data
dg_data = [] # drexel guest data
while keep_graphing:
    with connection:
        the_cursor = connection.cursor()
        query = "select * from "+table_name+" limit "+str(start)+","+str(num_rows) # ask for data
        num_rows_retrieved = the_cursor.execute(query)
        start += num_rows_retrieved # update starting index for next query
        print "retrieved '"+str(num_rows_retrieved)+"' from "+table_name
        df3_data += the_cursor.fetchall() # append new data to current data
        if (num_rows_retrieved < num_rows): # if there isn't enough data in the database, then we'll take a nap and try again in 'window_size' seconds.
            print "not enough data to graph -- will try again in "+str(window_size)+" seconds..."
            time.sleep(window_size)
            continue
        # FOR DF3 GRAPHING:
        if (df3_data[0][1] == df3_data[len(df3_data)-1][1]): # this checks to see if the data we got is all from the same window
            print "previous query did not return all necessary data -- querying again..."
            continue # if it is, then we want to query again to try to get all of the data for the window we're about to graph
            
    num_entries = len(data)
    current_window = data[0][1]
    for i in range(0, num_entries):
        if (current_window != df3_data[i][1]):
            break # once we've gotten all info for the current window, we move on to graphing the data
        this_data = df3_data.pop(0) # if we are still in the current window (which we will be if we get here), remove the first entry
        temp_node = DF3Node(this_data[0], this_data[1], this_data[4])
        # check to see if we already have this node, by checking the node_id and window_num (see __eq__ method in DF3Node)




    print "Current data:"
    for row in df3_data:
        print row
    print

connection.close()
