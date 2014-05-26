#!/usr/bin/env python
#-*-coding:utf-8-*-
from signal import signal, SIGTERM
from sys import exit
import atexit
from time import sleep

def cleanup():
    print "Cleanup"

if __name__ == "__main__":
    print type(atexit)
    atexit.register(cleanup)

    # Normal exit when killed
    #kill -9 时不会调用atexit 
    signal(SIGTERM, lambda signum, stack_frame: exit(1))
    
    sleep(10)
