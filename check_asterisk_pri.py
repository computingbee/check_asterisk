#!/usr/bin/python
import subprocess
import sys
import os

CMD="/usr/sbin/asterisk"
CMD_ARG1="-x"
CMD_ARG1_VAL="pri show spans"

#Nagios exit codes
STATE_OK=0      
STATE_WARNING=1        
STATE_CRITICAL=2        
STATE_UNKNOWN=3         
	
if not (os.path.isfile(CMD) and os.access(CMD,os.X_OK)):
	print "Unknown: ",CMD," not found"
	sys.exit(STATE_UNKNOWN)

cmd = subprocess.Popen([CMD, CMD_ARG1, CMD_ARG1_VAL], 
	stdout=subprocess.PIPE, 
	stderr=subprocess.PIPE)
try:
	result = cmd.communicate()
except OSError, e:
	print >>sys.stderr, "Execution failed:",e
	sys.exit(STATE_UNKNOWN)

if result[1] == "": # no error
	output = result[0]

	if output == "" or len(output) <=0:
        	print "Warning: No PRI spans present"
 		sys.exit(STATE_WARNING)

	pri_spans = output.splitlines()

	problem_pri_span = []

	for i in pri_spans:
		pri_span = i.split(':')
		pri_span_status = pri_span[1].strip()
		if "Up,Active" not in "".join(pri_span_status.split()):
			problem_pri_span.append(i)

	if len(problem_pri_span) > 0:
		for i in problem_pri_span:
			print "Critical:",i
		sys.exit(STATE_CRITICAL)
	else:
		for i in pri_spans:
			print "OK:",i
		sys.exit(STATE_OK)
else:
	print "Command",ocmd,"returned error:",result[1]
	sys.exit(STATE_UNKNOWN)
