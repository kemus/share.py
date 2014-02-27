#!/usr/bin/python2
import sys
import threading
import errno
import random
import string
import os
import shutil
import SimpleHTTPServer
import SocketServer
import socket

def getExternalIP():
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect(('google.com', 80))
    ip = sock.getsockname()[0]
    sock.close()
    return ip
passkey=  ''.join(random.sample(string.letters+string.digits,9))

if len(sys.argv) < 2:
    print "Usage: share.py file..."
    sys.exit(1)
if not os.path.exists("serving"):
    os.mkdir("serving")
if not os.path.exists("serving/%s"%passkey):
    os.mkdir("serving/%s"%passkey)

sys.argv.pop(0)
print "Making temporary copy of files..."
while(len(sys.argv) > 0):
    name = sys.argv.pop(0)
    if not os.path.exists(name):
        print "%s does not exist!"%name
        sys.exit(2)
    dst = "serving/%s/%s"%(passkey, name)
    print "%s --> %s"%(name, dst)
    try:
        shutil.copytree(name, dst)
    except OSError as E:
        if E.errno == errno.ENOTDIR:
            shutil.copy(name, dst)
        else:
            raise

os.chdir("serving/%s"%passkey)
port = random.randint(8000,8999)
httpd = SocketServer.TCPServer(("", port), SimpleHTTPServer.SimpleHTTPRequestHandler)
print "Done!"
server=threading.Thread(target=httpd.serve_forever)
server.daemon=True
server.start()

print "Serving at http://%s:%s"%(getExternalIP(),port)

raw_input("push enter to close server\n")

print "Closing server..."
httpd.shutdown()
print "Deleting temporary files..."
os.chdir("..")
shutil.rmtree(passkey)
print "Done!"
