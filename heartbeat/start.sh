#!/bin/bash

./bin/run &
envsubst < heartbeat.template.yml > heartbeat.yml
./bin/heartbeat -e -c heartbeat.yml
