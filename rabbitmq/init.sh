#!/bin/bash

rabbitmqctl list_users | grep guest && rabbitmqctl delete_user guest
rabbitmqctl list_users | grep admin || rabbitmqctl add_user admin admin

rabbitmqctl set_user_tags admin administrator
rabbitmqctl clear_permissions -p / admin
rabbitmqctl set_permissions -p / admin '.*' '.*' '.*'
