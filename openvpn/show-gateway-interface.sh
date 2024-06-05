#!/bin/sh
DEFAULT_GW=`ip route show | grep -o 'default via [0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}' | awk '{print $3}'`
DEFAULT_DEV=`ip route show | grep -o 'default via [0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\} dev [^ ]*' | awk '{print $5}'`
ip route delete default via $5
ip route add default via $DEFAULT_GW dev $DEFAULT_DEV
