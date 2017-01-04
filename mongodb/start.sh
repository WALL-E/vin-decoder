#!/bin/bash

role=`id -u`
if test $role -ne 0
then
    echo "运行脚本需要root权限"
    exit 1
fi

command -v systemctl
ret=$?
if test $ret -ne 0
then
    service mongod start && echo "mongdb started"
else
    systemctl start mongod.service && echo "mongdb started"
fi
