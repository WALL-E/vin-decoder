#!/bin/bash

rabbitmq-server -detached
rabbitmqctl start_app
rabbitmq-plugins enable rabbitmq_management
