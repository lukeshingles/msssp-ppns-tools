#!/bin/bash

for i in {1..100}
do
    NUM=$i
#      while [ ${#NUM} -ne 3 ];
#      do
#        NUM="0"$NUM
#      done
    if [ -f "out.$NUM" ]
    then
        echo ""
        echo "-- out.$NUM --"

        cat out.$NUM | grep -m 1 .srf
        echo "..."
        tac out.$NUM | grep -m 1 .nsm
    fi
done
if [ -f "out" ]
then
    echo ""
    echo "-- out --"

    cat out | grep -m 1 .srf
    echo "..."
    tac out | grep -m 1 .nsm
fi
