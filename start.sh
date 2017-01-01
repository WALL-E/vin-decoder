#!/bin/bash

role=`id -u`
if test $role -ne 0
then
    echo "运行脚本需要root权限"
    exit 1
fi

cd `dirname $0`

mongodb/start.sh
rabbitmq/start.sh

sleep 5

supervisor/install.sh
supervisor/start.sh

