#!/bin/bash

mongoimport -h 127.0.0.1:27017 \
-d "vin" \
-c "year" \
-f "code,year" \
--type=csv --file=./year.csv

mongoimport -h 127.0.0.1:27017 \
-d "vin" \
-c "wmi-from-offline" \
-f "WMI,Manufacturer" \
--type=csv --file=./wmi-from-offline.csv

