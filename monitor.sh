#!/usr/bin/bash
#
# Some extended monitoring functionality; Tested on Amazon Linux 2
#                        _ _             
#  _ __ ___   ___  _ __ (_) |_ ___  _ __ 
# | '_ ` _ \ / _ \| '_ \| | __/ _ \| '__|
# | | | | | | (_) | | | | | || (_) | |   
# |_| |_| |_|\___/|_| |_|_|\__\___/|_|   
#

sleep 5

INSTANCE_ID=$(curl -s http://169.254.169.254/latest/meta-data/instance-id)
MEMORYUSAGE=$(free -m | awk 'NR==2{printf "%.2f%%", $3*100/$2 }')
PROCESSES=$(expr $(ps -A | grep -c .) - 1)
HTTPD_PROCESSES=$(ps -A | grep -c httpd)
PROC=$(uname -p)
KERNEL=$(uname -svr)
ARCH=$(uname -m)
echo "<----------------->"
echo "Instance running at: $(date +%d)/$(date +%m)/$(date +%y) $(date +"%T")"
echo "Processor:  $PROC"
echo "Kernel Version: $KERNEL"
echo "Architecture: $ARCH"
echo "Instance ID: $INSTANCE_ID"
echo "Memory utilisation: $MEMORYUSAGE"
echo "No of processes: $PROCESSES"

if [ $HTTPD_PROCESSES -ge 1 ]
    then
        echo "Web server is running"
    else
        echo "Web server is NOT running"
fi

echo '<----------------->'