#!/bin/bash

role=`id -u`
if test $role -ne 0
then
    echo "运行脚本需要root权限"
    exit 1
fi

cd `dirname $0`

./install.sh

command -v systemctl
ret=$?
if test $ret -ne 0
then
    service supervisord start && echo "supervisord started"
else
    systemctl start supervisord && echo "supervisord started"
fi
