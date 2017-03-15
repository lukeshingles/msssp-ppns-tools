#!/bin/bash

for i in {1..100}
do
    NUM=$i
    while [ ${#NUM} -ne 3 ];
    do
        NUM="0"$NUM
    done
    if [ -f "log$NUM.dat" ]
    then
        echo ""
        echo "-- log$NUM.dat --"
        cat log$NUM.dat | grep -m 1 Mass
        cat log$NUM.dat | grep -m 1 NMOD=
        tac log$NUM.dat | grep -m 1 Mass
        tac log$NUM.dat | grep -m 1 NMOD=
    fi
done
if [ -f "log.xxx" ]
then
    echo ""
    echo "-- log.xxx --"
    cat log.xxx | grep -m 1 Mass
    cat log.xxx | grep -m 1 NMOD=
    tac log.xxx | grep -m 1 Mass
    tac log.xxx | grep -m 1 NMOD=
fi
