#!/usr/bin/python
##
# Blake Golliher - blakegolliher@gmail.com
#
# A simple snapmirror lag report
# Using netapp API and Python
#
##

import sys, string, os
import getpass
import datetime
import time
from datetime import datetime, timedelta

sys.path.append("/var/local/netapp-manageability-sdk-5.1/lib/python/NetApp")
from NaServer import *

password = getpass.getpass()

filer_name = sys.argv[1]

filer = NaServer(filer_name,1,6)
filer.set_admin_user('admin', password)
cmd = NaElement("snapmirror-get-iter")
ret = filer.invoke_elem(cmd)

if(ret.results_status() == "failed"):
  	print "%s failed." % filer_name
	print(ret.results_reason() + "\n")
	sys.exit(2)

if(ret.child_get_int("num-records") == "0"):
	print "%s failed." % filer_name
	print "no snapmirror records found.\n"
	sys.exit(2)

smlist = dict()
smlist = ret.child_get('attributes-list')

print "\nData Protection Snapmirror Relationships for %s : " % filer_name
for mirror in smlist.children_get():
	type = mirror.child_get_string("relationship-type")
	if type == "data_protection":
		type = mirror.child_get_string("relationship-type")
		rate = mirror.child_get_string("relationship-progress")
		sourcelocation = mirror.child_get_string("source-location")
		destlocation = mirror.child_get_string("destination-location")
		print "	%s -> %s : %s : Transferred %s so far. " % (sourcelocation,destlocation,type,rate)
		print "	State is %s" % mirror.child_get_string("mirror-state")
		print "	Type is	: %s" % type
		print "	Snapshot in flight is %s" % mirror.child_get_string("transfer-snapshot")
		print "	Snapmirror lag is %s" % mirror.child_get_string("lag-time")
