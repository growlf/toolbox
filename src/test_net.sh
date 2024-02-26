#!/bin/bash

# File with nodes to test, one address per line
NODES_FILE=./nodes.list

# Test for color support
# check if stdout is a terminal...
if test -t 1; then

    # see if it supports colors...
    ncolors=$(tput colors)

    if test -n "$ncolors" && test $ncolors -ge 8; then
        bold="$(tput bold)"
        underline="$(tput smul)"
        standout="$(tput smso)"
        normal="$(tput sgr0)"
        black="$(tput setaf 0)"
        red="$(tput setaf 1)"
        green="$(tput setaf 2)"
        yellow="$(tput setaf 3)"
        blue="$(tput setaf 4)"
        magenta="$(tput setaf 5)"
        cyan="$(tput setaf 6)"
        white="$(tput setaf 7)"
        orange="$(tput setaf 208)"
        purple="$(tput setaf 135)"

    fi
fi

# Show the date this script was run
date

# Get the primary interface IP and device name
ip4=$(/sbin/ip route get 8.8.8.8 | awk '/src/ { print $7 }')
dev=$(/sbin/ip route get 8.8.8.8 | awk '/src/ { print $5 }')
echo "Host IP address on $dev: $ip4"

# Get external IP address
external=$(dig @resolver4.opendns.com myip.opendns.com +short)
echo "Public IP address: $external"

# Get and test acces to the default gateway
default_gateway=$(/sbin/ip route | awk '/default/ { print $3 }')
ping -c 1 "$default_gateway" > /dev/null
if [ $? -eq 0 ]; then
echo "- node $default_gateway (default gateway) is ${green}accessible${normal}"
else
echo "ERROR: default gateway ($default_gateway) is ${red}${bold}unreachable${normal}"
exit 1
fi

# Loop over supplied node addresses list if it exists
if test -f ${NODES_FILE}; then
cat ${NODES_FILE} |  while read output
do
    ping -c 1 "$output" > /dev/null
    if [ $? -eq 0 ]; then
    echo "- node $output is ${green}accessible${normal}"
    else
    echo "- node $output is ${red}${bold}unreachable${normal}"
    fi
done
fi
