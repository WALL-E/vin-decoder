#!/bin/bash

role=`id -u`
if test $role -ne 0
then
    echo "运行脚本需要root权限"
    exit 1
fi

command -v systemctl > /dev/null
ret=$?
if test $ret -ne 0
then
    service rabbitmq-server status
else
    systemctl status rabbitmq-server
fi
