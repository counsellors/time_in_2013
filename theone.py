#!/usr/bin/env python
# -*-coding:utf-8-*-

import os
import sys
import time
import random
import subprocess
import multiprocessing

lckdir = '/tmp/uRule.tmp'
myPidLck =0

def getLckDir():
    if not os.path.exists(lckdir):
        os.mkdir(lckdir)

def getLckFromPid(pid):
    if not isinstance(pid,str):
        pid = str(pid)
    path = os.path.join(lckdir,pid+'.lck')
    return path

def cleanUselessLck():
    for filename in os.list(lckdir):
        filepath = os.path.join(lckdir, filename)
        try:
            if os.path.isfile(filepath):
                os.unlink(filepath)
        except Exception, e:
            print e

def debugPopen( *popenargs, **kwargs):
    if  kwargs.has_key("stdout") :
        print "don't add stdout in debugPopen"
        return -2
    if  kwargs.has_key("stderr") :
        print "don't add stderr in debugPopen"
        return -2
    ignore = False
    if kwargs.has_key("ignorerr"):
        ignore = kwargs.pop("ignorerr")
    splitargs = None
    if type(popenargs[0]) == str  :
        if not kwargs.has_key("shell") or kwargs["shell"] != True :
            popenargs = popenargs[0].split()
            popenargs = (popenargs,)
    #print "Exec: Start to excute - %s " % str(popenargs)
    result = ''
    tmpsub = subprocess.Popen(*popenargs, stdout=subprocess.PIPE,stderr= subprocess.STDOUT,  **kwargs )
    for line in iter(tmpsub.stdout.readline, b''):
        result += line.rstrip("\n")
    #print result
    tmpret = tmpsub.wait()
    if tmpret != 0 and ignore == False :
        print "Error: returncode %s in %s " % (tmpret,popenargs)
    return tmpret

def checkSingleton():
    findSelfCmd = "ps -ef|grep \"python .*%s\""%(os.path.basename(__file__))
    while 1:
        process = subprocess.Popen(findSelfCmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        existFlag = 0
        runtimeExistFlag = 0
        for line in iter(process.stdout.readline, b''):
            #print repr(line)
            import re 
            match = re.search('.*? (\d+)', line)
            old_pid = ""
            if match:
                old_pid = match.group(1)
                if os.path.exists(getLckFromPid(old_pid)):
                    os.remove(getLckFromPid(old_pid))
                
            if line.find('grep') == -1 and old_pid != str(os.getpid()):
                print "等待上一个脚本结束"
                runtimeExistFlag += 1
        if runtimeExistFlag > 0 :
            sleeptime = random.uniform(1,2)
            time.sleep(sleeptime)
            continue
        else:
            #print "上一个脚本结束"
            break 
def runCommand(e):
    e.wait()
    if e.is_set():
        print 'get event and exit'
        exit(0)
    print "cmd 1"
    debugPopen("python atexit_v2.py")
    print "cmd 2"
    debugPopen("python atexit_v2.py")
    print "cmd 3"
    debugPopen("python atexit_v2.py")
   
def checkTerm(e, parentPid):
    while 1:
        myPidLck = getLckFromPid(parentPid)
        print 'check my pid file %s'%myPidLck
        if not os.path.exists(myPidLck):
            e.set()
            print 'checkTerm: event is set'
            break
        else:
            sleeptime = random.uniform(1,2)
            time.sleep(sleeptime)
            
if __name__ == "__main__":
    global myPid
    myPid = os.getpid()
    getLckDir()
    checkSingleton()
    #runCommand()
    myPidLck = getLckFromPid(os.getpid())
    if not os.path.exists(myPidLck):
        open(myPidLck, 'w').close() 
        print 'mk my pid file %s'%myPidLck
    e = multiprocessing.Event()
    w1 = multiprocessing.Process(name='worker', target=runCommand, args=(e,))
    w2 = multiprocessing.Process(name='monitor', target=checkTerm, args=(e,myPid))
    w2.start()
    w1.start()
    print 'main: working before new Mgr'

