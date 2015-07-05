#!/bin/bash
ps aux|fgrep "process.py" |fgrep -v grep |awk '{print $2;}'|xargs kill -3
