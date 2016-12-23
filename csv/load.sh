#!/bin/bash

mongoimport -h 127.0.0.1:27017 \
-d "vin" \
-c "year" \
-f "code,year" \
--type=csv --file=./year.csv

mongoimport -h 127.0.0.1:27017 \
-d "vin" \
-c "wmi" \
-f "wmi,manufacturer" \
--type=csv --file=./wmi.csv

