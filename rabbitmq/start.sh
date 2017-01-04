#!/bin/bash

role=`id -u`
if test $role -ne 0
then
    echo "运行脚本需要root权限"
    exit 1
fi

cd `dirname $0`

command -v systemctl
ret=$?
if test $ret -ne 0
then
    service rabbitmq-server start && echo "rabbitmq-server started"
else
    systemctl start rabbitmq-server && echo "rabbitmq-server started"
fi

./init.sh
