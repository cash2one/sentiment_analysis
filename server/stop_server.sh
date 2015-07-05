#!/bin/bash

if [ $# -ne 1 ]
then
    cat <<EOF
    Usage:         $0 port|all
    Example:       $0 8080
EOF
    exit
fi

if [ $1 = all ]
then
  ps aux|fgrep "server.py" |fgrep -v grep |awk '{print $2;}'|xargs kill -3
else
   ps aux|fgrep "server.py $1 " |fgrep -v grep |awk '{print $2;}'|xargs kill -3
fi    
   exit
