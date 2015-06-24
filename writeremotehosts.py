#! /usr/bin/python
import socket, click, os, paramiko
from subprocess import call

@click.command()
@click.option('--hostfile',default='ipaddresses',help='which hostfile to boot with')
@click.option('--configfile',default='/home/pi/.ipython/profile_picluster/remotehosts.py',help='which config file to write')
@click.option('--controller_ip',default='10.40.3.12',help='ip of the cluster controller')
def writehostdata(hostfile,configfile,controller_ip):
	file=open(hostfile,'r')
	readfile=file.read()
	splithosts=readfile.split('\n')
	file.close()
	file=open(configfile,'w')
	file.write('c = get_config()\n')
	file.write("c.LocalControllerLauncher.controller_args=['--log-to-file','--log-level=20','--ip="+controller_ip+"']\n")
	file.write('c.SSHEngineSetLauncher.engines = {')
	reachable=[]
	print splithosts
	for host in splithosts:
		if host=='':
			break
		if str(host)==controller_ip:
			continue
		s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		s.settimeout(1)
		try:
			s.connect((str(host),22))
			reachable.append(str(host))
			print "reached "+str(host)
			s.close()
		except:
			print "could not reach "+str(host)
			s.close()
			continue
		if call(['ssh','-oBatchMode=yes',str(host),"'date'"])==255:
			sshhost='pi@'+str(host)
			c=paramiko.SSHClient()
			c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			c.connect(str(host),username='pi',password='raspberry')
			c.exec_command('sudo chmod 777 /home/pi/.ssh/authorized_keys')
			call(['ssh-copy-id','-i','/home/pi/.ssh/id_rsa',sshhost])
			c.exec_command('sudo chmod 755 /home/pi/.ssh/authorized_keys')
			c.close()
			print 'established passwordless ssh to '+str(host)
	print str(len(reachable))+" hosts reached"
	for host in reachable:
		file.write("'"+host+"':1,")
	file.write('}\n')
	file.close()

if __name__=='__main__':
	#os.chdir("/home/pi")
	writehostdata()
