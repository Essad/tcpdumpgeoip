#!/bin/env python

import requests
import simplejson as json
import subprocess as sub
from IPy import IP


# Elastic Search Instance
url = "http://localhost:9200/ldfmap/logs/?pipeline=geoip-info"
#tcpdump -l -v -tt -nn not arp and not udp

p = sub.Popen(('sudo', 'tcpdump', '-l', '-tt' ,'-nn', 'tcp or udp'), stdout=sub.PIPE)
for row in iter(p.stdout.readline, b''):
    #print row.rstrip()   # process here
    dump = row.rstrip().split()
    #print(dump)
    # Time is in epoch_millis

    time = dump[0].split(".")[0]
    # Extracting IP and Portnumber (TCPDump lists this as 10.0.0.1.80)
    srcipx = dump[2].split(".")
    try:
        srcip = srcipx[0] + "." + srcipx[1] + "." + srcipx[2] + "." + srcipx[3] 
    except IndexError:
        srcip = 'null'

    try:
        srcport = srcipx[4]
    except IndexError:
        srcport = 'null'


    #Doing the same for Destination
    dstipx = dump[4].split(".")
    try:
        dstip = dstipx[0] + "." + dstipx[1] + "." + dstipx[2] + "." + dstipx[3]
    except IndexError:
        dstip = 'null'

    try:
        dstport = dstipx[4]
    except IndexError:
        dstport = 'null'

    #Listing the protocol 
    try:
        proto = dump[5]
    except IndexError:
        proto = 'null'    


    # Print some verbose output
    print "DSTIP: " + dstip + " SRCIP:" + srcip 
    
    if dstip is not None:
        ip = IP(dstip)
        dst_net = ip.iptype()
        data = { 'occurred_at': time, 'dst_ip': dstip, 'src_ip': srcip, 'proto': proto, 'src_port': srcport, 'dst_port': dstport, 'dst_net': dst_net }
        headers = {'Content-type': 'application/json'}
        r = requests.post(url, data=json.dumps(data), headers=headers)

