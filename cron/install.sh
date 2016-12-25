#!/bin/bash

role=`id -u`
if test $role -ne 0
then
    echo "运行脚本需要root权限"
    exit 1
fi

/bin/cp -f crontab.txt /var/spool/cron/root

ret=$?
if test $role -eq 0
then
    chmod 600 /var/spool/cron/root
    echo "copy crontab.txt to /var/spool/cron/root [ok]"
else
    echo "copy crontab.txt to /var/spool/cron/root [failed]"
fi
