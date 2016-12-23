#!/bin/bash

role=`id -u`
if test $role -ne 0
then
    echo "运行脚本需要root权限"
    exit 1
fi

yum install python-setuptools.noarch

command -v wget || yum -y install wget || exit 1

easy_install pip
pip install pymongo
pip install beautifulsoup4

