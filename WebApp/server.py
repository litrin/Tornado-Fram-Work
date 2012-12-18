#!/usr/bin/env python

from lib.config import CFG
import os
from core.server import service

def getPorts():
    sPort = CFG.getOption('service', 'ports')
    lPortList = []
    for port in sPort.split(','):
        try:
            lPortList.append(int(port))
        except:
            pass

    return lPortList

def start():
    map(service, getPorts())
    print "Server start OK!"

if __name__ == "__main__":
    #if os.fork() ==0: start()
    #else: exit()
    start()
