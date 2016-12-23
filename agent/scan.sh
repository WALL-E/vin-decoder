#!/bin/bash

cd tcping && make clean && make

cd ..
cat "./agent.list" | while read LINE
do
    echo $LINE

    IP=`echo -n $LINE|cut -d: -f1`
    PORT=`echo -n $LINE|cut -d: -f2`
    #echo "IP:"$IP
    #echo "PORT:"$PORT

    ./tcping/tcping -p $PORT -t 3 -c 1 $IP 1>/dev/null 2>/dev/null
    ret=$$

    if test $ret -eq 0 
    then
        echo $IP":"$PORT
    fi
done
