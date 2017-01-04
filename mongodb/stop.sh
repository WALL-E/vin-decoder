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
    service mongod stop && echo "mongdb stoped"
else
    systemctl stop mongod.service && echo "mongdb stoped"
fi
