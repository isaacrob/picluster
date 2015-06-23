#! /usr/bin/python
import socket, click, os

@click.command()
@click.option('--hostfile',default='ipaddresses',help='which hostfile to boot with')
@click.option('--configfile',default='/home/pi/.ipython/profile_picluster/remotehosts.py',help='which config file to write')
def writehostdata(hostfile,configfile):
	file=open(hostfile,'r')
	readfile=file.read()
	splithosts=readfile.split('\n')
	file.close()
	file=open(configfile,'w')
	file.write('c = get_config()\n')
	file.write('c.SSHEngineSetLauncher.engines = {')
	reachable=[]
	print splithosts
	for host in splithosts:
		if host=='':
			break
		s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		s.settimeout(1)
		try:
			s.connect((str(host),22))
			reachable.append(str(host))
			print "reached "+str(host)
		except:
			print "could not reach "+str(host)
		s.close()
	print str(len(reachable))+" hosts reached"
	for host in reachable:
		file.write("'"+host+"':1,")
	file.write('}\n')
	file.close()

if __name__=='__main__':
	os.chdir("/home/pi")
	writehostdata()
