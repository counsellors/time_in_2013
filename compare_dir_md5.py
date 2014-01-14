#/usr/bin/env python

#file: comparemd5.py
#usage: <dstDir> <srcDir>

import sys, os, re
import md5
import time

class Md5Tool:
    def __init__(self):
        self.name = 'MD5TOOL'
        self.fh = None
        self.strMd5 = None
        self.recordname = 'data%s.md5' % (time.strftime("%Y_%m_%d_%H_%M_%S",time.localtime(time.time())))
        self.dc = {}

    def getMD5(self, strFile):
        try:
            #print strFile
            self.fh = open(strFile, 'rb')
            m = md5.md5()
            self.strRead = ""

            while True:
                strRead = self.fh.read(8096)
                if not strRead:
                    break
                m.update(strRead)
            self.bet = True
            self.strMd5 = m.hexdigest()
        except Exception,e:
            #print e
            self.bet = False
        finally:
            if self.fh:
                self.fh.close()
          
        return [self.bet, self.strMd5]

    def getDC(self, srcfile):
        src = self.getMD5(srcfile)
        self.dc[os.path.basename(srcfile)] = src[1]

    def record(self):
        ios = 'w'
        ntuple = sorted(self.dc.iteritems(), key = lambda item:item[0])
        for item in ntuple:
            fp = open(self.recordname, ios)
            fp.write(item[0] + ' : ' + item[1] + '\n')
            fp.close
            if ios == 'w':
                ios = 'a'

    def compare(self, dstfile, srcfile):
        dst = self.getMD5(dstfile)
        src = self.getMD5(srcfile)
        
        if dst[0] == False or src[0] == False:
            print '[-] Error: Cannt find file %s or %s' % (dstfile, srcfile)
            return -1
        
        #print 'check %s %s' % (srcfile, src[1])
        #print '--new %s %s' % (len(srcfile)*' ', dst[1])
        if dst[1] != src[1]:
            print '[-] Warning: File %s has changed, please confirm it.' % srcfile
            return -1
            
        return 1

    def diff(self, dstdir, srcdir):
        if not  os.path.isdir(dstdir) or not os.path.isdir(srcdir):
            print '[-] Error: Not dir'
        for root,dirs,files in os.walk(srcdir):
            for file in files:
                if not re.search(r'\.svn', os.path.join(root, file)):
                    #print '\t%s %s' % (root,file)
                    for droot, ddirs,dfiles in os.walk(dstdir):
                        for dfile in dfiles:
                            if file == dfile:
                                self.compare(os.path.join(droot, dfile), os.path.join(root, file))
                                print '*'*40
            
    def check(self, srcdir):

        if not os.path.isdir(srcdir):
            print '[-] Error: Not dir'
        for root,dirs,files in os.walk(srcdir):
            for file in files:
                if not re.search(r'\.svn', os.path.join(root, file)):
                    #print '\t%s %s' % (root,file)
                    self.getDC(os.path.join(root, file))

        self.record()
                    
        print '[-] Make it!'
if __name__ == '__main__':
    tips = 'Usage: %s <dstDir> <srcDir>' % sys.argv[0]
    if len(sys.argv) > 3:
        print  tips
    if len(sys.argv) == 3:
        mtool = Md5Tool()
        mtool.diff(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 2:    
        mtool = Md5Tool()
        mtool.check(sys.argv[1])


