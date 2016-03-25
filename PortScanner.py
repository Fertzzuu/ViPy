import optparse
from socket import *
from threading import *

screenLock = Semaphore(value=1)

def connScan(tgtHost, tgtPort):
	try:
		connSkt = socket(AF_INET, SOCK_STREAM)
		connSkt.connect((tgtHost, tgtPort))
		connSkt.send('Massage\r\n')				#comment these lines for disable header grabbing
		results = connSkt.recv(100)
		screenLock.acquire()
		print "[+]%d/tcp open" % tgtPort
		print "[+] " + str(results)
	except:
		screenLock.acquire()
		print "[-]%d/tcp closed" % tgtPort
	finally:
		screenLock.release()
		connSkt.close()

def portScan(tgtHost, tgtPort):
	try:
		tgtIP = gethostbyname(tgtHost)
	except:
		print "[-] Cannot resolve '%s' : Unknown host" % tgtHost
		return
	setdefaulttimeout(1)
	for tgtPort in tgtPorts:
		t = Thread(target = connScan, args = (tgtHost, int(tgtPort)))
		t.start()
		
def main():
	parser = optparse.OptionParser("usage: %prog" + " -h [target host] -p [target port]")
	
	parser.add_option('-h', dest = 'tgtPort', type = 'string', help='specify target port[s] separated by comma ')
	(options, args) = parser.parse_args()
	tgtHost = options.tgtHost
	tgtPorts = str(options.tgtPort).split(", ")
	if ((tgtHost == None) or (tgtPorts == None)):
		print parser.usage
		exit(0)	
	portScan(tgtHost, tgtPorts)
	
	
#--------------

if __name__ == "__main__":
	main()
	
	
	