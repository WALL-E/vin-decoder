#!/bin/bash

role=`id -u`
if test $role -ne 0
then
    echo "运行脚本需要root权限"
    exit 1
fi

mongodb/stop.sh
rabbitmq/stop.sh
supervisor/stop.sh

