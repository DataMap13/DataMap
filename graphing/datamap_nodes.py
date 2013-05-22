#!/usr/bin/python

class DF3Node:

    def __init__(self, node_id, window_num, num_packets):
        self.node_id = node_id
        self.window_num = window_num
        self.num_packets = num_packets
 
    def merge(self, not_self):
        self.num_packets += self.num_packets

    def __eq__(self, not_self):
        if self.node_id == not_self.node_id and self.window_num == not_self.window_num:
            return True
        return False


'''
DrexelGuest data. Shouldn't be used for dragonfly3 data (gotten via airodump) because all we have is volume information for that network. See DF3Node.
'''
class DGNode:

    '''
    other than 'window_size', which is the length in seconds that this node will compile data for, 
    everything comes directly from the row returned from the database. 
    '''
    def __init__(self, window_size, node_id, firstSwitchedMillis, srcIP, destIP, srcPort, destPort, protocol, num_packets, num_bytes, tcpControlBits):
        self.node_id = node_id
        self.startMillis = firstSwitchedMillis
        self.endMillis = self.startMillis + window_size # we CANNOT merge any nodes with this node that have a 'startMillis' greater than OR equal to this node's endMillis. 
        self.srcIPs = set()
        self.destIPs = set()
        self.srcPorts = set()
        self.destPorts = set()
        self.protocols = set()
        self.srcIPs.add(srcIP)
        self.destIPs.add(destIP)
        self.srcPorts.add(srcPort)
        self.destPort.add(destPort)
        self.protocols.add(protocols)
        self.num_packets = num_packets
        self.num_bytes = num_bytes
        self.tcpControlBits = tcpControlBits
 
    def merge(self, not_self):
        self.srcIPs.update(not_self.srcIPs)
        self.destIPs.update(not_self.destIPs)
        self.srcPorts.update(not_self.srcPorts)
        self.destPort.update(not_self.destPorts)
        self.protocols.update(not_self.protocols)
        self.num_packets += not_self.num_packets
        self.num_bytes += not_self.num_bytes
        self.tcpControlBits += not_self.tcpControlBits

    def __eq__(self, not_self):
        if self.node_id == not_self.node_id and self.startMillis <=  not_self.startMillis and self.endMillis > not_self.startMillis :
            return True
        return False

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


if __name__ == '__main__':
    df3nodes = []
    df3nodes.append(DF3Node(1,0,5))
    df3nodes.append(DF3Node(2,2,5))
    df3nodes.append(DF3Node(3,0,5))

    print DF3Node(1,0,8) in df3nodes

