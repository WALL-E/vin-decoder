#!/bin/bash

role=`id -u`
if test $role -ne 0
then
    echo "运行脚本需要root权限"
    exit 1
fi

cd `dirname $0`

/bin/cp -f vin-decoder.ini /etc/supervisord.d

ret=$?
if test $role -eq 0
then
    echo "copy vin-decoder.ini to /etc/supervisord.d [ok]"
else
    echo "copy vin-decoder.ini to /etc/supervisord.d [failed]"
fi
