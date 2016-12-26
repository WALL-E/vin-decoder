#!/bin/bash

role=`id -u`
if test $role -ne 0
then
    echo "运行脚本需要root权限"
    exit 1
fi

/bin/cp -f tornado.ini /etc/supervisord.d

ret=$?
if test $role -eq 0
then
    echo "copy tornado.ini to /etc/supervisord.d [ok]"
else
    echo "copy tornado.ini to /etc/supervisord.d [failed]"
fi
