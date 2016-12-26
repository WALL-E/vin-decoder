#!/bin/bash

role=`id -u`
if test $role -ne 0
then
    echo "运行脚本需要root权限"
    exit 1
fi

cat <<'EOF' > /etc/yum.repos.d/mongodb-org-3.0.repo
[mongodb-org-3.0]
name=MongoDB Repository
baseurl=http://repo.mongodb.org/yum/redhat/$releasever/mongodb-org/3.0/x86_64/
gpgcheck=0
enabled=1
EOF

yum install -y supervisor.noarch
yum install -y mongodb-org
yum install -y rabbitmq-server
yum -y install python-setuptools.noarch
yum -y install python-tornado.noarch
yum -y install python-requests.noarch
yum -y install supervisor.noarch

command -v wget || yum -y install wget || exit 1

easy_install pip
pip install pymongo
pip install beautifulsoup4
pip install pika
pip install ipy
pip install ipaddress
