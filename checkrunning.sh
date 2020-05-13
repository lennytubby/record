#!/bin/bash
#
# 1 - program to mointor
while true; do
    my_array=()
    while IFS= read -r line; do
        my_array+=( "$line" )
    done < <( ps aux | grep $1 )
    if [ ${#my_array[@]} -gt 3 ]; then 
	    echo true
	    sleep 5m
    else 
	    echo false
	    `./sendMail.sh "Record.py crashed" "!" lennart@slusny.de`
	    break
    fi
done
