#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import sys

addr = "129.25.28.81"
user = "datamap13"
passwd = "seniordesign13"
schema = "network_data"

con = mdb.connect(addr, user, passwd, schema);

for i in range(0,5):
    with con:

        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS \
            _python_(Id INT PRIMARY KEY AUTO_INCREMENT, BSSID VARCHAR(25), Volume INT, Start_Time INT, End_Time INT)")
        cur.execute("INSERT INTO _python_(BSSID,Volume, Start_Time, End_Time) VALUES('be:0f:fa:ab:08:12',10,0,3)")
