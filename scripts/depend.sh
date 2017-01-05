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

yum install -y mongodb-org

rpm --import https://www.rabbitmq.com/rabbitmq-release-signing-key.asc
yum -y install rabbitmq-server

command -v wget || yum -y install wget || exit 1
command -v curl || yum -y install curl || exit 1
command -v netstat || yum -y install net-tools || exit 1
command -v lsof || yum -y install lsof || exit 1

command -v python2.7 || curl https://raw.githubusercontent.com/WALL-E/static/master/setup/redhat/install_python27|bash

pip2.7 install http://oerp142a4.bkt.clouddn.com/pymongo-3.4.0.tar.gz
pip2.7 install http://oerp142a4.bkt.clouddn.com/beautifulsoup4-4.5.3.tar.gz
pip2.7 install http://oerp142a4.bkt.clouddn.com/pylint-1.6.4.tar.gz
pip2.7 install http://oerp142a4.bkt.clouddn.com/requests-2.12.4.tar.gz
pip2.7 install http://oerp142a4.bkt.clouddn.com/supervisor-3.3.1.tar.gz
pip2.7 install http://oerp142a4.bkt.clouddn.com/certifi-2016.9.26.tar.gz
pip2.7 install http://oerp142a4.bkt.clouddn.com/tornado-4.4.2.tar.gz
pip2.7 install http://oerp142a4.bkt.clouddn.com/pika-0.10.0.tar.gz
pip2.7 install http://oerp142a4.bkt.clouddn.com/IPy-0.83.tar.gz
pip2.7 install http://oerp142a4.bkt.clouddn.com/ipaddress-1.0.17.tar.gz
