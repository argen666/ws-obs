#!/bin/bash
c=10
while true;
do
#echo 1
cvlc rtsp://192.168.16.127/stream --sout=file/ts:camera_1_$(date +"%Y%m%d%H%M%S")_"$c".mp4 --stop-time=10 vlc://quit
retval="$?"
if [ "$retval" == "1" ]; then
sleep 1
else
sleep 1
fi
let "c+=10" 
done
