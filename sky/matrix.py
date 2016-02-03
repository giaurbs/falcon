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
DIR_OF_TEMPFILE = "./tmp/"



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

	# initializing header and body of my matrix
	# it looks like this [ header, 
	#		       body [
	#			      row1[field1, field2, ... , fieldn], 
	#			      row2[field1, field2, ... , fieldn], 
	#			      ...,
	#		 	      rown[field1, field2, ... , fieldn] 
	#			      ]

	header = ""
	body = []

	#reading temporary file
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

			# making nice the action -> getting rid of ] closing bracked and removing [UFW in the array
			row[5] = row[5].replace("]","")
			del row[4]

			# adding the line to the body
			body.append(row)
	fp.close()
	
	#cleaning temporary files
#	os.remove(DIR_OF_TEMPFILE+"*")
#	os.remove("/opt/falcon/sky/tmp/*")
	#returning the matrix
	return [header,body]


# WIP
#def sort_matrix(matrix):
#	sorted_matrix)=	sorted(matrix, key=lambda item: socket.inet_aton(item[0]))
#	sorted_matrix = sorted(matrix, key=lambda ip: ip[8])
#	return sorted_matrix
