#!/usr/bin/python

class DF3Node:

    def __init__(self, node_id, window_size, num_packets, startMillis, absolute_window_number):
        self.node_id = node_id
        self.startMillis = startMillis
        self.endMillis = startMillis + (window_size*1000)
        self.num_packets = num_packets
        self.absolute_window_number = absolute_window_number


    def merge(self, not_self, differentiate_between_windows=True):
        self.num_packets += not_self.num_packets
        if differentiate_between_windows and (not_self.absolute_window_number != self.absolute_window_number):
            print "Bad bad bad... self == "+str(self.win)+" != not_self "+str(not_self.win)

    '''
    When trying to combine different windows, 'differentiate_between_windows' should be false.
    When trying to create separate windows (based upon time), 'differentiate_between_windows' need not be called,
    but if it is, it should be 'True' (which it is by default).
    '''
    def __eq__(self, not_self, differentiate_between_windows=True):
        if (differentiate_between_windows):
            if self.node_id == not_self.node_id and self.startMillis <=  not_self.startMillis and self.endMillis > not_self.startMillis :
                return True
            else:
                return False
        else:
            if self.node_id == not_self.node_id:
                return True
            else:
                return False

    def __str__(self):
        return "[ node_id => "+str(self.node_id)+", num_packets => "+str(self.num_packets)+", startMillis => "+str(self.startMillis)+", endMillis => "+str(self.endMillis)+"]"

   


'''
DrexelGuest data. Shouldn't be used for dragonfly3 data (gotten via airodump) because all we have is volume information for that network. See DF3Node.
'''
class DGNode:

    '''
    other than 'window_size', which is the length in seconds that this node will compile data for, 
    everything comes directly from the row returned from the database. 
    '''
    def __init__(self, window_size, node_id, firstSwitchedMillis, srcIP, destIP, srcPort, destPort, protocol, num_packets, num_bytes, tcpControlBits, absolute_window_number):
        self.node_id = node_id
        self.startMillis = firstSwitchedMillis
        self.endMillis = self.startMillis + (window_size * 1000) # we CANNOT merge any nodes with this node that have a 'startMillis' greater than OR equal to this node's endMillis. 
        self.srcIPs = set()
        self.destIPs = set()
        self.srcPorts = set()
        self.destPorts = set()
        self.protocols = set()
        self.srcIPs.add(srcIP)
        self.destIPs.add(destIP)
        self.srcPorts.add(srcPort)
        self.destPorts.add(destPort)
        self.protocols.add(protocol)
        self.num_packets = num_packets
        self.num_bytes = num_bytes
        self.tcpControlBits = tcpControlBits
        self.absolute_window_number = absolute_window_number
 
    def merge(self, not_self):
        self.srcIPs.update(not_self.srcIPs)
        self.destIPs.update(not_self.destIPs)
        self.srcPorts.update(not_self.srcPorts)
        self.destPorts.update(not_self.destPorts)
        self.protocols.update(not_self.protocols)
        self.num_packets += not_self.num_packets
        self.num_bytes += not_self.num_bytes
        self.tcpControlBits += not_self.tcpControlBits

    '''
    When trying to combine different windows, 'differentiate_between_windows' should be false.
    When trying to create separate windows (based upon time), 'differentiate_between_windows' need not be called,
    but if it is, it should be 'True' (which it is by default).
    '''
    def __eq__(self, not_self, differentiate_between_windows=True):
        if (differentiate_between_windows):
            if self.node_id == not_self.node_id and self.startMillis <=  not_self.startMillis and self.endMillis > not_self.startMillis :
                return True
            return False
        else:
            if self.node_id == not_self.node_id:
                return True
            return False
        return False

    def __str__(self):
        return "[ node_id => "+str(self.node_id)+", startMillis => "+str(self.startMillis)+", endMillis => "+str(self.endMillis)+", srcIPs => "+str(self.srcIPs)+", destIPs => "+str(self.destIPs)+", srcPorts => "+str(self.srcPorts)+", destPorts => "+str(self.destPorts)+", protocols => "+str(self.protocols)+", num_packets => "+str(self.num_packets)+", total bytes => "+str(self.num_bytes)+", num_tcpControlBits "+str(self.num_tcpControlBits)+"]"

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

'''
a NodeList holds w
'''
class NodeList:

    def __init__(self):
        self.nodes = []

    def add(self,node):
        self.nodes.append(node)


'''
a Network holds a list of NodeLists.
'''
class Network:    
    
    def __init__(self):
        pass


if __name__ == '__main__':
    df3nodes = []
    df3nodes.append(DF3Node(1,0,5))
    df3nodes.append(DF3Node(2,2,5))
    df3nodes.append(DF3Node(3,0,5))

    print DF3Node(1,0,8) in df3nodes

