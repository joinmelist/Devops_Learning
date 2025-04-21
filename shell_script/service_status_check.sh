#!/bin/bash
<< comment

Information :- this script checking service file status and restart service if service stop 
version :- 0.3

comment

function status_check(){
#name=$(systemctl | grep running | grep $1 | gawk -e '{print $4}')
#name=$(systemctl |gawk  '$1 == "websocket.socket" && $4 == "running" {print $4}')
name=$(systemctl is-active "$1" 2>/dev/null)
echo "service checking name :- $1"
if [[ "$?" -eq 0 ]] && [[ $name == "active" ]];
then
        echo "*************** service is running **************"

else
        echo "############################ restart service script ############################"
	echo "systemctl restart $1"
	systemctl restart "$1"
	#status_check $1
	#systemctl status "$1"
	if [[ "$?" -eq 0 ]];
	then
		echo "restart comand not working...."
		echo "Send ADMIN Email "
	fi
fi
}

#status_check $1

list=("cross_market_websocket.service" "cross_market_websocket.socket" "websocket.service" "websocket.socket")
for i in ${list[@]}
do
        echo "$i status checking..."
        status_check $i

done

