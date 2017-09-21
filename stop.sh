#!/usr/bin/env bash

# Stop CarGuard API
if pgrep -f toopath/bin/python &> /dev/null ; then pkill -f toopath/bin/python; fi