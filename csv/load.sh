#!/bin/bash

mongoimport -h 127.0.0.1:27017 \
-d "vin" \
-c "wmi" \
-f "wmicode,manufacturer" \
--type=csv --file=./wmi.csv

