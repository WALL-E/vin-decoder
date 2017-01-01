#!/bin/bash

pgrep beam >> /dev/null || rabbitmq-server -detached
rabbitmqctl start_app
rabbitmq-plugins enable rabbitmq_management
