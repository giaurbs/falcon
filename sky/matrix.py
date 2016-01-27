#!/usr/bin/env python3

#import subprocess
#import re
#import pydoc
import time
import os
import errno
import subprocess
import socket

from ancillary import bcolors
#from ancillary import tab_replace

#variables
PATH_TO_LOG = "/var/log/syslog*"
DIR_OF_TEMPFILE = "/tmp/falcon_loganalyzer/"



def build_matrix():
	
	# memorizing fwlogwatch output in the DIR_OF_TEMPFILE
	# -s source port
	# -d destination port
	# -N resolve service
	# -t starting time
	# -z time interval
	
	
	#building filepath
	timestamp = time.strftime("%Y-%m-%d_%H:%M:%S")
	filename = "falcon.data."+timestamp+".log"
	tempfile_fullpath = DIR_OF_TEMPFILE+filename

	try:
		os.makedirs(DIR_OF_TEMPFILE)
	except OSError as exception:
			if exception.errno != errno.EEXIST:
				raise


	#building commands
	fwlog_cast = "fwlogwatch -s -d -N -t -z "+PATH_TO_LOG+" > "+tempfile_fullpath

	#casting command
	print (bcolors.GREEN+"Building temporary file..."+bcolors.ENDC)
	os.system(fwlog_cast)


	#analyzing file
	print (bcolors.GREEN+"Analyzing temporary file..."+bcolors.ENDC)

	header = ""
	body = []

	fp = open(tempfile_fullpath)
	for i, line in enumerate(fp):
		if i <= 5:
			header += line
		elif i >= 9:
			row = line.replace("\n","").split(' ')
			ip = row[8]
			geoloc = subprocess.check_output(["geoiplookup", ip]).decode('UTF-8')
			geoloc = geoloc.replace("GeoIP Country Edition: ","")
			geoloc = geoloc.replace("\n","")
			row.append(geoloc)
			body.append(row)
	fp.close()

	return [header,body]


def sort_matrix(matrix):
	sorted_matrix)=	sorted(matrix, key=lambda item: socket.inet_aton(item[0]))
	sorted_matrix = sorted(matrix, key=lambda ip: ip[8])
	return sorted_matrix
