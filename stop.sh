#!/usr/bin/env bash

# Stop TooPath API
PID_FILE=~/toopath-api/toopath.pid
if pgrep -F $PID_FILE; then pkill -F $PID_FILE; fi