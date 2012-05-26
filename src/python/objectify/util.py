#!/usr/bin/python2
from subprocess import *

def myrun(args):
    """Return stdout and stderr combined along with an exit code (errorcode, stdout)"""
    p = Popen(" ".join(args), shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT)#, close_fds=True)
    output = p.stdout.read()
    retval = p.wait()

    return retval, output

def writefile(filename, data):
   f = open(filename, "w")
   f.write(data)
   f.close()
