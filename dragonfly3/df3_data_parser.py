#!/usr/bin/python
import time
import os
import MySQLdb as mdb
import sys

sys.path.append("/bin")
from datamap_daemon_common import *

'''
README: to use:
You must have the mysql package for Python installed:

$ sudo apt-get install python-mysqldb

Then, create the 'mon' interface:

$ echo s3tt0p! | sudo -S airmon-ng start wlan0

Before starting df3_data_parser.py, be sure to delete (or rename) any old files that were made by airodump-ng.

Then, start df3_data_parser.py:

$ ./df3_data_parser.py cap-01.csv _python_01 &

Finaly, start airodump:

$ screen -S airdump -d -m `echo s3tt0p! | sudo -S airodump-ng -t OPN -t WPA2 -w ./cap  mon0 > /dev/null 2>&1 &`


When satisfied, stop df3_data_parser.py, and then stop screen:

screen -x airdump

This program will write to the database after each time it reads from the csv file.

Andrew W.E. McDonald
'''


''' class to hold the information from each data line
'''
class Entry:
    '''
    note that 'millis_time' will be the time recorded immediately prior to the read that was done from the csv file.
    The input values will be stored in a list.
    '''
    def __init__(self,station_mac, power, num_packets, bssid, probed_essids, millis_time):
        self.entry = [station_mac, power, num_packets, bssid, probed_essids, millis_time]

    def replace_num_packets(self, new_num_packets):
        self.entry[2] = new_num_packets
        return self

'''
instructions
'''
def usage():
    return "usage: "+sys.argv[0]+" <csv filename> [<table name>] [<window size>]\n\nwhere:\n<csv filename> (mandatory) is the name of the csv file to read (and path if not in current directory).\n\n<table name> (optional) is what you would like to name the table that is created in the database. If a table exists with the chosen name, data will be appended to it. If this parameter is not supplied, the default -- '_python_' -- will be used. Table name must not be wholly made up of numbers.\n\n<window size> (optional -- default is 1 second) is the number of seconds to wait between reading the csv file. Effectively, this is your window size in seconds."


#################################### Initialization #################################
#####################################################################################
num_args = len(sys.argv)
if num_args < 2 or num_args > 4:
    print usage()
    exit()
elif num_args == 2:
    table_name = "_python_"
    window_size = 1
elif num_args == 3:
    try:
        window_size = float(sys.argv[2])
        table_name = "_python_"
    except ValueError:
        # then we know that this should be the table name instead
        table_name = sys.argv[2]
        window_size = 1
elif num_args == 4:
    try:
        window_size = float(sys.argv[2])
        table_name = sys.argv[3] 
    except ValueError:
        # then we check to see if it's the other way around
        table_name = sys.argv[2]
        try:
            window_size = float(sys.argv[3])
        except ValueError:
            print usage()
            exit()

if ".csv" not in sys.argv[1]:
    print usage()
    exit()

read_file = sys.argv[1]

addr = get_config("server_addr")
user = get_config("db_username")
passwd = get_config("db_password")
schema = get_config("db_name")
target_network = get_config("wpa2_essid")
window_num = 0
cant_open = True
is_initial = True


##### wait until the file we are trying to read exists ######
#print os.path.exists(read_file)
while (cant_open):
    try:
        file_to_read = open(read_file,'r')
        cant_open = False
    except IOError:
        #print "couldn't open file... trying again in one second."
        time.sleep(1)


##### connect to db ######
# TODO  put in try/except, and write to output file if can't write to db.
con = mdb.connect(addr, user, passwd, schema);

#### create table ####
with con:
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS "+table_name+"(Window_Num INT, Station_MAC CHAR(17), Power INT, Num_Packets INT, BSSID CHAR(17), Probed_ESSIDs VARCHAR(256), Millis_Time DOUBLE)")



#################################### Begin loop to read entire csv every "window_size" seconds #################################
################################################################################################################################
while True:
    line = file_to_read.readline() 
    while not "Station MAC" in line: #we don't care about anything before that line 
        read_time = time.time()*1000 # go from seconds to milliseconds
        line = file_to_read.readline()

    # break up by comma, create dictionary. When the loop above exits, 'line' will contain the following:
    # Station MAC, First time seen, Last time seen, Power, # packets, BSSID, Probed ESSIDs
    # Then we take that, and strip whitespace and put it into a list.
    if is_initial:
        key_list = [key.strip() for key in line.split(',')]
    # we want elements 0,3,4,5,6
    # we'll check element 6 of the data lines for "dragonfly3". If that is present, then we keep that line.

    this_windows_entries = []
    line = file_to_read.readline()
    while not line.__eq__(''):
        data_list = [data.strip() for data in line.split(',')]
        probed_essids = ""
        try:
            probed_essids = data_list[6]
        except IndexError:
            pass
        if target_network in probed_essids: # make sure 'dragonfly3' (in this case) is in "Probed ESSIDs"
            new_entry = Entry(data_list[0], data_list[3], data_list[4], data_list[5], data_list[6], read_time)
            this_windows_entries.append(new_entry)
        line = file_to_read.readline()

    this_windows_mac_address_dictionary = {} # create a mapping between the current window's (which will be the last windows next time around)  mac addresses and # of packets so we don't have to run an O(n^2) operation next time around
    for this_entry in this_windows_entries: # we also want to do this with the total number of packets (not the calculated delta)
        this_windows_mac_address_dictionary[this_entry.entry[0]] = int(this_entry.entry[2])
    if not is_initial:
        # we need to subtract the new "# packets" field from the last window's "# packets" field to get the deltas -- but we need to make sure that the MAC addresses match
        i = 0
        for this_entry in this_windows_entries:
            try: # we can't be sure that an access point we just saw was seen last time around -- better check and be safe
                prev_num_packets = last_windows_mac_address_dictionary[this_entry.entry[0]]
                print "last packets: %s vs. current packets: %s -- for AP: %s" % (str(prev_num_packets),str(this_entry.entry[2]),str(this_entry.entry[0]))
                delta_packets = int(this_entry.entry[2]) - prev_num_packets
                this_windows_entries[i] = this_entry.replace_num_packets(str(delta_packets))
            except KeyError:
                pass # if there isn't a previous value, then we just keep the same number.
    last_windows_mac_address_dictionary = this_windows_mac_address_dictionary
    is_initial = False

    with con:
        for this_entry in this_windows_entries:
            cur = con.cursor()
            #sql_query = "INSERT INTO "+table_name+"(Window_Num, Station_MAC, Power, Num_Packets, BSSID, Probed_ESSIDs, Millis_Time) \
            #    VALUES("+str(window_num)+", '"+this_entry.entry[0]+"', "+this_entry.entry[1]+", "+this_entry.entry[2]+", '"+this_entry.entry[3]+"', \
            #    '"+this_entry.entry[4]+"', '"+str(this_entry.entry[5])+"')"
            #print sql_query
            cur.execute("INSERT INTO "+table_name+"(Window_Num, Station_MAC, Power, Num_Packets, BSSID, Probed_ESSIDs, Millis_Time) \
                VALUES("+str(window_num)+", '"+this_entry.entry[0]+"', "+this_entry.entry[1]+", "+this_entry.entry[2]+", '"+this_entry.entry[3]+"', \
                '"+this_entry.entry[4]+"', '"+str(this_entry.entry[5])+"')")
    file_to_read.seek(0)
    window_num += 1
    time.sleep(window_size)
    


file_to_read.close()




