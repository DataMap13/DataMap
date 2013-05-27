#!/usr/bin/python
# -*- coding: utf-8 -*-


import MySQLdb as mdb
import gc
import matplotlib 
from pylab import *
import time
import sys
import numpy as np
from datamap_nodes import DF3Node, DGNode
import Tkinter as Tk 

matplotlib.use('TkAgg') # needed????

ion() # turn on interactive mode
show() # show the window
'''
Database rows:
=====================
for df3 data: [Node_id, Window_Num, Station_MAC, Power, Num_Packets, BSSID, Proved_ESSIDs, Millis_Time]
    -> important indices: 0 -> node_id, 1 -> window_num, 4 -> num_packets, 7 -> millis_time

will have one line per node, and will plot by window_num on x-axsis, taking sum of packets that node saw. Also can graph amount of traffic though each access point if we want.
=====================
for drexel guest data: [nodeId, latitude, longitude, firstSwitchedMillis, srcIP, dstIP, srcPort, dstPort, proto, pkts, bytes, tcpControlBits]
    -> important indices: 0 -> node_id, 3 -> firstSwitchedMillis, 4 -> srcIP, 5 -> dstIP, 6 -> srcPort, 7 -> dstPort, 8 -> proto, 9 -> num_packets, 10 -> bytes, 11 - tcpControlBits 

will have one figure per node, showing: # distinct sourceIPs, # distinct destintationIPs, # distinct source ports, # distinct dest ports, # distinct protocols, number of packets, number of bytes, and number of tcp control bits -- each plotted in their own subplots, one data point per time window

can also plot average volume 
'''

addr = "129.25.28.81" # NOTE to someone that can explain this to me: why can't we connect via 127.0.0.1?
user = "datamap13"
passwd = "seniordesign13"
schema = "network_data"


gc.collect() # garbage collect to make sure any previous connections to the db were dealt with properly.
connection = mdb.connect(addr, user, passwd, schema);

#query = "select * from "+table_name+" limit "+str(num_rows) # from start of tabl
#query_2 = "select * from myTable limit 5,18446744073709551615" # to get all rows after n'th row, use large number

dg_table_name = "network_data.h_20130508_20_1" 
table_name = "network_data.dragonfly3_20130508"
num_rows = 100 
num_collection_nodes = 5
df3_max_data_points = 10#50 # on graph
dg_max_data_points = df3_max_data_points
df3_current_data_points = 0 # on graph
dg_current_data_points = 0
start = 0
dg_start = 0
window_size = 1 # seconds. this window size determines the granularity
correlation_window_size = 30 # start with using 30 windows (30 seconds).
num_windows_to_get = 30
num_dg_windows_to_get = 30
window_range = [0,df3_max_data_points]
dg_window_range = [0,dg_max_data_points]

__absolute_window_number = 0 # Don't touch this. Ever. This is 'absolute' with respect to a single correlation window.

keep_graphing = True
not_enough_data = True
df3_data = [] # dragonfly 3 data
df3_nodes = []
dg_data = [] # drexel guest data
dg_nodes = []
df3_windows = [] # will be a list of df3_nodes 
dg_windows = []
df3_data_per_node = [] 
dg_data_per_node = []
df3_pre_corr_lists = []
dg_pre_corr_lists = []
df3_correlations = []
dg_correlations = []
while keep_graphing:
    __absolute_window_number = -1
    for current_window_number in range(0, num_windows_to_get):
        __absolute_window_number += 1 
        df3_data = [] # clear previous data
        df3_data_per_node = []
        not_enough_data = True 
        while not_enough_data:
            with connection:
                # get data from db 
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
                # this checks to see if the data we got is all from the same time window. 
                if ((df3_data[0][7]+1000) > df3_data[len(df3_data)-1][7]): 
                    print "previous query did not return all necessary data -- querying again..."
                    continue # if it is, then we want to query again to try to get all of the data for the window we're about to graph
                not_enough_data = False
            
        # parse data
        num_entries = len(df3_data)
        current_window_start = df3_data[0][7]
        current_window_end = current_window_start + 1000
        df3_nodes = []
        for i in range(0, num_entries):
            try:
                if (current_window_end <= df3_data[i][7]):
                    break # once we've gotten all info for the current window, we move on to graphing the data
            except IndexError:
                break
            this_data = df3_data.pop(0) # if we are still in the current window (which we will be if we get here), remove the first entry
            # need to adjust 'i' and 'num_entries' to account for removing an element -- all others shift forward
            num_entries -= 1
            i -= 1
            temp_node = DF3Node(this_data[0], window_size, this_data[4], this_data[7], __absolute_window_number)
            # check to see if we already have this node, by checking the node_id and window range (see __eq__ method in DF3Node)
            if temp_node in df3_nodes:
                location = df3_nodes.index(temp_node)
                #print "node number",temp_node.node_id," had ",df3_nodes[location].num_packets," packets prior to merge, and ",
                df3_nodes[location].merge(temp_node)
                #print df3_nodes[location].num_packets," after the merge. temp_node had ",temp_node.num_packets," packets."
            else:
                df3_nodes.append(temp_node)

        df3_windows.append(df3_nodes)

    '''
    #########################################################
    ====================== NOW GRAB DG DATA =================
    #########################################################
    '''

    __absolute_window_number = -1
    for current_window_number in range(0, num_dg_windows_to_get):
        __absolute_window_number += 1 
        dg_data = [] # clear previous data
        dg_data_per_node = []
        not_enough_data = True 
        while not_enough_data:
            with connection:
                # get data from db 
                the_dg_cursor = connection.cursor()
                query = "select * from "+dg_table_name+" limit "+str(dg_start)+","+str(num_rows) # ask for data
                num_rows_retrieved = the_dg_cursor.execute(query)
                dg_start += num_rows_retrieved # update starting index for next query
                print "retrieved '"+str(num_rows_retrieved)+"' from "+dg_table_name
                dg_data += the_dg_cursor.fetchall() # append new data to current data
                if (num_rows_retrieved < num_rows): # if there isn't enough data in the database, then we'll take a nap and try again in 'window_size' seconds.
                    print "not enough data to graph -- will try again in "+str(window_size)+" seconds..."
                    time.sleep(window_size)
                    continue
                # FOR DG GRAPHING:
                # this checks to see if the data we got is all from the same time window. 
                if ((dg_data[0][3]+1000) > dg_data[len(dg_data)-1][3]): 
                    print "previous query did not return all necessary data -- querying again..."
                    continue # if it is, then we want to query again to try to get all of the data for the window we're about to graph
                not_enough_data = False
            
        # parse data
        num_entries = len(dg_data)
        current_window_start = dg_data[0][3]
        current_window_end = current_window_start + 1000
        dg_nodes = []
        for i in range(0, num_entries):
            try:
                if (current_window_end <= dg_data[i][3]):
                    break # once we've gotten all info for the current window, we move on to graphing the data
            except IndexError:
                break
            this_data = dg_data.pop(0) # if we are still in the current window (which we will be if we get here), remove the first entry
            # need to adjust 'i' and 'num_entries' to account for removing an element -- all others shift forward
            num_entries -= 1
            i -= 1
            temp_node = DGNode(window_size, this_data[0], this_data[3], this_data[4], this_data[5],this_data[6],this_data[7],this_data[8],this_data[9],this_data[10], this_data[11],  __absolute_window_number)
            # check to see if we already have this node, by checking the node_id and window range (see __eq__ method in DGNode)
            if temp_node in dg_nodes:
                location = dg_nodes.index(temp_node)
                #print "node number",temp_node.node_id," had ",df3_nodes[location].num_packets," packets prior to merge, and ",
                dg_nodes[location].merge(temp_node)
                #print df3_nodes[location].num_packets," after the merge. temp_node had ",temp_node.num_packets," packets."
            else:
                dg_nodes.append(temp_node)

        dg_windows.append(dg_nodes)

    '''   
    ##################################
    =========== consolidate =========

        first, df3
    #################################
    '''

    # Now we need to take 'df3_windows' and create one vector (actually dictionary to allow us to keep track of missing windows for nodes) per collection node (all 'node' instances that have the same 'node_id').
    for i in range(0, num_collection_nodes): # need to initialize the dictionaries 
        df3_data_per_node.append({})

    for df3_window in df3_windows:
        for node in df3_window:
            df3_data_per_node[node.node_id][node.absolute_window_number] = node.num_packets

    # Next we input '0' for any window that we don't have information from a collection node for, and turn the dictionaries into lists
    df3_pre_corr_lists = []
    for i in range(0, num_collection_nodes): # need to initialize the lists 
        df3_pre_corr_lists.append([])
    current_node_id = -1
    for node in df3_data_per_node:
        current_node_id += 1 # in the above step, the indidces of the dictionaries in the list was the same as the node_id
        for i in range(0,correlation_window_size): 
            try:
                df3_pre_corr_lists[current_node_id].append(node[i])
            except KeyError:
                # this means that there wasn't a window for this node at this time. So, we set the value to '0'... if we didn't it would be hard to calculate the correlation between nodes.
                df3_pre_corr_lists[current_node_id].append(0)


    ####################### TEST PRINT START ######################
    print "lists pre-correlation:"
    i = 0
    for node in df3_pre_corr_lists:
        print "node #"+str(i)+": "+str(node)
        i += 1
    ####################### TEST PRINT END ######################

    # Then we use numpy.corrcoef([vector_1, vector_2, vector_3, etc.]) which will return a correlation matrix.
    # This matrix has columns 'vector_1', 'vector_2', 'vector_3', etc. in that order, and has rows in the same order starting with 'vector_1' at top.
    #       This means that in the returned matrix, [0,0] will have a correlation of '1' because it is 'vector_1' measured against itself.
    #           HOWEVER, if any of the the input vectors had only 1 distinct number (all '0', all '1', etc.) then that will cause 'NaN' to be returned.
    current_corrs = np.corrcoef(df3_pre_corr_lists)
    print current_corrs

    # To fix this, we must run numpy.nan_2_num(correlation_matrix). This will 'fix' the issues. NOTE that I don't know how it does this, nor how good an idea it is to use this function. I just know that it removes the 'nan' from the correlation matrix.
    no_nan_corrs = np.nan_to_num(current_corrs)
    print no_nan_corrs

    # After getting the correlation matrix and fixing it, we find the average correlation between a node and all other nodes, for each node. Once we have that, we plot.
    i = 0
    corrs_to_plot = []
    current_total_corr = 0
    for node in no_nan_corrs: # each row will contain the correlation values for node 'i'
        print "node: "+str(node)
        j = 0
        current_total_corr = 0
        for this_corr in node: # each column will contain the correlation between node 'i' and node 'j'
            print "this_corr: "+str(this_corr)
            if i == j: # don't get the correlation between a node and itself.
                j += 1
                continue
            current_total_corr += this_corr
            j += 1
        corrs_to_plot.append(current_total_corr/j)
        i += 1

    df3_correlations.append(corrs_to_plot)
    print "df3_correlations: "+str(df3_correlations)
    df3_corrs_transposed = []
    num_df3_corrs = len(df3_correlations)
    for i in range(0,num_collection_nodes):
        temp = []
        for j in range(0,num_df3_corrs):
            temp.append(df3_correlations[j][i])
        df3_corrs_transposed.append(temp)
    print "df3_corrs_transposed: "+str(df3_corrs_transposed)
    x_vals = arange(0,len(df3_correlations), 1)
    print "x_vals: "+str(x_vals)



    '''   
    ##################################
    =========== consolidate =========

    ========== now dg ===============
    #################################
    '''

    # Now we need to take 'dg_windows' and create one vector (actually dictionary to allow us to keep track of missing windows for nodes) per collection node (all 'node' instances that have the same 'node_id').
    for i in range(0, num_collection_nodes): # need to initialize the dictionaries 
        dg_data_per_node.append({})

    for dg_window in dg_windows:
        for node in dg_window:
            dg_data_per_node[node.node_id][node.absolute_window_number] = [len(node.srcIPs), len(node.destIPs), len(node.srcPorts), len(node.destPorts), len(node.protocols), node.num_packets, node.num_bytes, node.tcpControlBits]

    # Next we input '0' for any window that we don't have information from a collection node for, and turn the dictionaries into lists
    dg_pre_corr_lists = []
    for i in range(0, num_collection_nodes): # need to initialize the lists 
        dg_pre_corr_lists.append([0,0,0,0,0,0,0,0])
    current_node_id = -1
    for node in dg_data_per_node:
        current_node_id += 1 # in the above step, the indidces of the dictionaries in the list was the same as the node_id
        for i in range(0,correlation_window_size): 
            try:
                t = dg_pre_corr_lists[current_node_id]
                n = node[i]
                p = [ t[0]+n[0], t[1]+n[1],t[2]+n[2],t[3]+n[3],t[4]+n[4],t[5]+n[5],t[6]+n[6],t[7]+n[7] ]
                dg_pre_corr_lists[current_node_id] = p
            except KeyError:
                # this means that there wasn't a window for this node at this time. So, we skip it 
                pass
                #dg_pre_corr_lists[current_node_id] = [0,0,0,0,0,0,0,0]


    ####################### TEST PRINT START ######################
    print "lists pre-correlation (FOR DREXELGUEST):"
    i = 0
    for node in dg_pre_corr_lists:
        print "node #"+str(i)+": "+str(node)
        i += 1
    ####################### TEST PRINT END ######################

    # Then we use numpy.corrcoef([vector_1, vector_2, vector_3, etc.]) which will return a correlation matrix.
    # This matrix has columns 'vector_1', 'vector_2', 'vector_3', etc. in that order, and has rows in the same order starting with 'vector_1' at top.
    #       This means that in the returned matrix, [0,0] will have a correlation of '1' because it is 'vector_1' measured against itself.
    #           HOWEVER, if any of the the input vectors had only 1 distinct number (all '0', all '1', etc.) then that will cause 'NaN' to be returned.
    current_dg_corrs = np.corrcoef(dg_pre_corr_lists)
    print "DREXELGUEST correlations: "+str(current_dg_corrs)

    # To fix this, we must run numpy.nan_2_num(correlation_matrix). This will 'fix' the issues. NOTE that I don't know how it does this, nor how good an idea it is to use this function. I just know that it removes the 'nan' from the correlation matrix.
    no_nan_dg_corrs = np.nan_to_num(current_dg_corrs)
    print no_nan_dg_corrs

    # After getting the correlation matrix and fixing it, we find the average correlation between a node and all other nodes, for each node. Once we have that, we plot.
    i = 0
    dg_corrs_to_plot = []
    current_total_corr = 0
    for node in no_nan_dg_corrs: # each row will contain the correlation values for node 'i'
        print "node: "+str(node)
        j = 0
        current_total_corr = 0
        for this_corr in node: # each column will contain the correlation between node 'i' and node 'j'
            print "this_corr: "+str(this_corr)
            if i == j: # don't get the correlation between a node and itself.
                j += 1
                continue
            current_total_corr += this_corr
            j += 1
        dg_corrs_to_plot.append(current_total_corr/j)
        i += 1

    dg_correlations.append(dg_corrs_to_plot)
    print "dg_correlations: "+str(dg_correlations)
    dg_corrs_transposed = []
    num_dg_corrs = len(dg_correlations)
    for i in range(0,num_collection_nodes):
        temp = []
        for j in range(0,num_dg_corrs):
            temp.append(dg_correlations[j][i])
        dg_corrs_transposed.append(temp)
    print "dg_corrs_transposed: "+str(dg_corrs_transposed)
    dg_x_vals = arange(0,len(dg_correlations), 1)
    print "dg_x_vals: "+str(dg_x_vals)




    '''
    ##########################
    ====== update plots ======
    ##########################
    '''

    # update plot
    clf()
    df3_plot_axes = subplot(211)
    df3_plot_axes.set_autoscalex_on(False)
    df3_plot_axes.set_xlim(window_range[0],window_range[1])
    #df3_plot_axes.set_xlim([0,10])
    df3_plot_axes.set_autoscaley_on(False)
    df3_plot_axes.set_ylim([-1,1])
    ###################### NOTE: this plot statement will have to be manually updated depending upon the number of collection nodes
    l = plot(x_vals,df3_corrs_transposed[0], '-', x_vals, df3_corrs_transposed[1], '-', x_vals,df3_corrs_transposed[2], '-', x_vals, df3_corrs_transposed[3], '-', x_vals, df3_corrs_transposed[4],'-')
    grid(True)
    title('DataMap - Average Node Correlation')
    ylabel('Damped oscillation')


    dg_plot_axes = subplot(212)
    dg_plot_axes.set_autoscalex_on(False)
    dg_plot_axes.set_xlim(dg_window_range[0],dg_window_range[1])
    #df3_plot_axes.set_xlim([0,10])
    dg_plot_axes.set_autoscaley_on(False)
    dg_plot_axes.set_ylim([-1,1])
    ###################### NOTE: this plot statement will have to be manually updated depending upon the number of collection nodes
    m = plot(dg_x_vals,dg_corrs_transposed[0], '-', dg_x_vals, dg_corrs_transposed[1], '-', dg_x_vals, dg_corrs_transposed[2], '-', dg_x_vals, dg_corrs_transposed[3], '-', dg_x_vals, dg_corrs_transposed[4],'-')
    grid(True)

    xlabel('Window Number (1 Window = '+str(window_size)+' Second(s))')
    ylabel('Correlation Value')
    draw()
    #time.sleep(.5)
    #raw_input()

    df3_current_data_points += 1
    dg_current_data_points += 1
    # Once we update the plot, we MUST make sure to pop the first value off of the 'df3_correlations' list: df3_correlations.pop(0)
    # And do the same with df3_windows
    df3_windows.pop(0)
    dg_windows.pop(0)
    if df3_current_data_points > df3_max_data_points:
        window_range[0] += 1
        window_range[1] += 1
       #df3_correlations.pop(0)
        df3_current_data_points -= 1
    if dg_current_data_points > dg_max_data_points:
        dg_window_range[0] += 1
        dg_window_range[1] += 1
        dg_current_data_points -= 1


        # Then we loop back around, and grab one more window. This is done by setting 'num_windows_to_get' to '1', so that the data-gathering loop only executes one time. Alternatively, if we want to wait longer between correlation values, the num_windws_to_get could be left alone (default is '30' at the time of this comment), or set somehwere in the middle.

    num_windows_to_get = 1
    num_dg_windows_to_get = 1



connection.close()

