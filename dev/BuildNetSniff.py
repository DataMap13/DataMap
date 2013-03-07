'''
Created on Oct 17, 2012

@author: Andrew W.E. McDonald
'''
import subprocess
import os

def build_NetSniff(build_dir):
    try:
        print os.getcwd()
        os.chdir(build_dir)
        print os.getcwd()
        subprocess.call("./configure")
        print "configured"
        subprocess.call("make")
        print "made"
        subprocess.call("make install")
    except:
        print "build NetSniff failed"
        
        
        
build_NetSniff("../lib/netsniff")
