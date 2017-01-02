# RabbitMQ

## Web UI
开启管理页面功能

```shell
 rabbitmq-plugins enable rabbitmq_management
```

http://localhost:15672/


## 常用命令

* 启动
  * rabbitmq-server -detached
  * rabbitmqctl start\_app

* 关闭
  * rabbitmqctl stop\_app
  * rabbitmqctl stop

* 添加管理员
  * rabbitmqctl add\_user admin admin
  * rabbitmqctl change\_password admin admin
  * rabbitmqctl set\_user\_tags admin administrator

* 权限
  * rabbitmqctl list\_user\_permissions admin
  * rabbitmqctl set\_permissions -p / admin '.\*' '.\*' '.\*'
  * rabbitmqctl clear\_permissions -p / admin
