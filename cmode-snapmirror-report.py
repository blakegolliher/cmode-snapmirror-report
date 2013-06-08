#!/usr/bin/python
##
#
# A simple snapmirror lag report
# Using netapp API and Python
#
##

import sys, string, os
import getpass
import datetime
import time
from math import log

sys.path.append("/var/local/netapp-manageability-sdk-5.1/lib/python/NetApp")
from NaServer import *

## Thanks internet!
## http://stackoverflow.com/questions/1094841/reusable-library-to-get-human-readable-version-of-file-size
unit_list = zip(['bytes', 'kB', 'MB', 'GB', 'TB'], [0, 0, 1, 2, 2])
def sizeof_fmt(num):
    """Human friendly file size"""
    if num > 1:
        exponent = min(int(log(num, 1024)), len(unit_list) - 1)
        quotient = float(num) / 1024**exponent
        unit, num_decimals = unit_list[exponent]
        format_string = '{:.%sf} {}' % (num_decimals)
        return format_string.format(quotient, unit)
    if num == 0:
        return '0 bytes'
    if num == 1:
        return '1 byte'

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
	if(mirror.child_get_string("relationship-progress") == None):
		rate = 0
		if(mirror.child_get_string("relationship-type") == "data_protection"):
			print "	%s -> %s : %s : Transferred %s so far. " % (mirror.child_get_string("source-location"),mirror.child_get_string("destination-location"),mirror.child_get_string("relationship-status"),sizeof_fmt(int(rate)))
			print "	State is %s" % mirror.child_get_string("mirror-state")
			print "	Snapshot in flight is %s" % mirror.child_get_string("transfer-snapshot")
	else:
		rate = mirror.child_get_string("relationship-progress")
		if(mirror.child_get_string("relationship-type") == "data_protection"):
			print "	%s -> %s : %s : Transferred %s so far. " % (mirror.child_get_string("source-location"),mirror.child_get_string("destination-location"),mirror.child_get_string("relationship-status"),sizeof_fmt(int(rate)))
			print "	State is %s" % mirror.child_get_string("mirror-state")
			print "	Snapshot in flight is %s" % mirror.child_get_string("transfer-snapshot")
