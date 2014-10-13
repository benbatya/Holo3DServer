#!/usr/bin/env python
import sys
import os.path
import os

# Set up the software for a ubuntu 14.04 server.
# Requires eth0 be pointing to the outside and
# eth1 be connected to the camera's network

TEST_EXEC = False
def myExec(cmd):
	print("executing '" + cmd + "'")
	if(TEST_EXEC is not True): os.system(cmd)

def installSysFile(dirname, fname):
	fullpath = dirname + "/" + fname
	bakfile = fullpath + ".orig"

	# don't copy over the original file if it exists already
	if (os.path.exists(fname) is not True): 
		cmd = "sudo cp " + fullpath + " " + bakfile
		myExec(cmd)
	else:
		print("Backup file '" + bakfile + "' exists already. Not overriding it.")
 
	# copy over the system file
	cmd = "sudo cp " + fname + " " + fullpath
	myExec(cmd)


if __name__ == "__main__":
	
	# Stop ubuntu's network-manager
	myExec("sudo stop network-manager");

	# install interfaces
	installSysFile("/etc/network", "interfaces")

	# restart eth0
	myExec("sudo ifdown eth0");
	myExec("sudo ifup eth0");

	# install dhcpd.conf
	installSysFile("/etc/dhcp", "dhcpd.conf")

	# install isc-dhcp-server
	installSysFile("/etc/default", "isc-dhcp-server")

	# restart eth1
	myExec("sudo ifdown eth1")
	myExec("sudo ifup eth1")

	# restart the isc-dhcp-server
	myExec("sudo service isc-dhcp-server restart")
	
