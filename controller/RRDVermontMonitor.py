# Vermont Management
# Copyright (C) 2008 University of Erlangen, Staff of Informatik 7 <limmer@cs.fau.de>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.


import os
import base64

from VermontLogger import logger


class RRDVermontMonitor:

    xpaths = None
    names = None
    interval = None
    # record every 10  60  3600 seconds a value in rrd (multiplied by "step" size -s)
    rrdintervals = (2, 12, 720)
    rrdgraphhist = (120, 1440, 43200)

    def __init__(self, xpaths, names, interval):
        self.xpaths = xpaths
        self.names = names
        self.interval = interval

    def collect_data(self, xml):
        if not os.access("rrd", os.R_OK|os.W_OK):
            os.mkdir("rrd")
        rrdfn = "rrd/db_%d_%d.rrd"
        for i in range(0, len(self.xpaths)):
            data = xml.xpath(self.xpaths[i])
            logger().info("inserting value %s for element '%s' (%s)" % (data, self.names[i], self.xpaths[i]))
            for j in range(0, len(self.rrdintervals)):
                if not os.access(rrdfn % (i, j), os.R_OK|os.W_OK):
                    os.system("rrdtool create %s -s 5 DS:s:GAUGE:%d:U:U RRA:AVERAGE:0.5:%d:10000 RRA:MIN:0.5:%d:10000 RRA:MAX:0.5:%d:10000" % (rrdfn % (i, j), self.rrdintervals[j]*5*2, self.rrdintervals[j], self.rrdintervals[j], self.rrdintervals[j]))
                os.system("rrdtool update %s N:%f " % (rrdfn % (i, j), data))
    

    def get_graph(self, idx1, idx2):
        rrdfn = "rrd/db_%d_%d.rrd" % (idx1, idx2)
        pngfn = "rrd/db_%d_%d.png" % (idx1, idx2)
        os.system("rrdtool graph %s --imgformat PNG --end now --start end-%dm DEF:ds0b=%s:s:MAX LINE1:ds0b#9999FF:\"min/max\" DEF:ds0c=%s:s:MIN LINE1:ds0c#9999FF DEF:ds0a=%s:s:AVERAGE LINE2:ds0a#0000FF:\"average\"" % (pngfn, self.rrdgraphhist[idx2], rrdfn, rrdfn, rrdfn))
        pic = open(pngfn).read()
        return base64.b64encode(pic)
        
