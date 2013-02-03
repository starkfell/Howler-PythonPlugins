#!/usr/bin/python
#
#  --- [icinga_py_check_disk] Python Script for Icinga ---
#
# Author(s):     Ryan Irujo
# Inception:     01.30.2013
# Last Modified: 02.02.2013
#
# Description:   Script that calls on the 'check_disk' Nagios Plugin and returns back the current
#                Disk Space of a particular partition on a host.
#
#
# Changes:       02.02.2013 - [R. Irujo]
#                Added check for Disk_Critical Variable to verify that it is a number.
#
#
# Command Line:  ./icinga_py_check_disk "[Critcal_Percent]" "[Disk_Path]"
# NRPE Examples: ./check_nrpe -H srv101.fabrikam.com -c icinga_py_check_disk -a "5" "/var/log"

import numbers
import re
import sys
import subprocess


# Getting Hostname of Server.
Get_Hostname = subprocess.Popen("hostname", stdout=subprocess.PIPE)
Hostname     = Get_Hostname.communicate()[0]
Hostname     = Hostname.rstrip()


#Verifying that Parameters passed to the script have values.
try:

        Disk_Critical     = int(sys.argv[1])
        Disk_Path         = sys.argv[2]


except ValueError:
        print "The [Disk_Critical] Variable must be a number!"
        exit(3)
except IndexError:
        print "Both the [Disk_Critical] and [Disk_Path] Variables are required!"
        exit(3)


# Formatting Command to return back Disk Statistics.
CheckDiskCmd = "/usr/lib64/nagios/plugins/check_disk -c {0}% -p {1}".format(Disk_Critical,Disk_Path)

# Disk Space Check
Disk_Check   = subprocess.Popen(CheckDiskCmd, stdout=subprocess.PIPE, shell=True)
Disk_Result  = Disk_Check.communicate()[0]
Disk_Result  = Disk_Result.rstrip()


# Final Results and Performance Data are calculated.
if Disk_Check.returncode > 2:
        print "There was a problem running the [check_disk] plugin on {0}".format(Hostname)
        exit(3)
elif re.search("WARNING",Disk_Result):
        print "{0}".format(Disk_Result)
        exit(1)
elif re.search("CRITICAL",Disk_Result):
        print "{0}".format(Disk_Result)
        exit(2)
elif re.search("OK",Disk_Result):
        print "{0}".format(Disk_Result)
        exit(0)


