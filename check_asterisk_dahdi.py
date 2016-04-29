#!/usr/bin/python

# Script:       check_asterisk_dahdi.py                                         
# Author:       Haris Buchal blog.axiomdynamics.com                             
# Description:  Plugin for Nagios (and forks) to check status for DAHDI cards
#		on Asterisk server. It uses dahdi_scan command and parses the  
#		output for status on each card found. It requires python 2.6+.
#		THIS SOFTWARE COMES WITH ABSOLUTELY NO WARRANTY
# License:      GPLv2
# Version:	1.0	                                                          
# 20160429      Created plugin                   

import subprocess
import sys
import os

CMD="/usr/sbin/dahdi_scan"

#Nagios exit codes
STATE_OK=0
STATE_WARNING=1              
STATE_CRITICAL=2        
STATE_UNKNOWN=3         

if not (os.path.isfile(CMD) and os.access(CMD,os.X_OK)):
        print "Unknown: ",CMD," not found"
        sys.exit(STATE_UNKNOWN)
	
cmd = subprocess.Popen([CMD], 
	stdout=subprocess.PIPE, 
	stderr=subprocess.PIPE)
try:
	result = cmd.communicate()
except OSError, e:
	print >>sys.stderr, "Execution failed:",e
	sys.exit(STATE_UNKNOWN)

if result[1] == "": # external cmd returned no error
	output = result[0]

        if output == "" or len(output) <=0:
		print "Warning: No cards found"
		sys.exit(STATE_WARNING)
 
	dhdi_output = output.splitlines()
        
	# get starting index for each span. spans start at [1],[2]...
        dhdi_cards_found = [i for i, x in enumerate(dhdi_output) if x.startswith('[')] 
        
	# normalize raw output using indexes
        dhdi_cards = []

	cid = 0
	dhdi_cards_count = len(dhdi_cards_found)
	while cid < dhdi_cards_count:
		if cid == dhdi_cards_count - 1:	#last card so cut all to the end
			str_idx = dhdi_cards_found[cid]
			dhdi_cards.append( dhdi_output[str_idx:] )
			break
		
		str_idx = dhdi_cards_found[cid]
		end_idx = dhdi_cards_found[cid + 1] - 1

		dhdi_cards.append( dhdi_output[str_idx:end_idx] )
		cid = cid + 1
	
     	# outpout normalized in list so now we look for cards with issues if any
	problem_ddhi_cards = [] 

	for c in dhdi_cards:
		if "active=yes" not in c[1] or "alarms=OK" not in c[2]:
			problem_ddhi_cards.append(c)

	if len(problem_ddhi_cards) > 0:
		for pc in problem_ddhi_cards:  
			print "Critical:",pc[0],pc[1],pc[2],pc[3],pc[4],pc[5],pc[6]
		sys.exit(STATE_CRITICAL)
	else:
		for oc in dhdi_cards:
			print "OK:",oc[0],oc[1],oc[2],oc[3],oc[4],oc[5],oc[6]
		sys.exit(STATE_OK)
else:
	print "Command",ocmd,"returned error:",result[1]
	sys.exit(STATE_UNKNOWN)
