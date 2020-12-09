#!/bin/bash
#
# 1 - program to mointor
while true; do
    my_array=()
    while IFS= read -r line; do
        my_array+=( "$line" )
    done < <( ps aux | grep $1 )
    dt=$(date '+%d/%m/%Y %H:%M:%S')
    if [ ${#my_array[@]} -gt 3 ]; then 
	    echo true "$dt"
	    sleep 5m
    else 
	    echo false "$dt"
	    `./sendMail.sh "$1""crashed" "!" lennart@slusny.de`
	    break
    fi
done
