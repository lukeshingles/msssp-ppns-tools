#!/bin/bash

if [ -f "seq.xxx" ]
then
  for i in {1..100}
    do
      NUM=$i
      while [ ${#NUM} -ne 3 ];
      do
        NUM="0"$NUM
      done
      if [ -f "seq$NUM.dat" ]
      then
	echo "seq$NUM.dat found, skipping."
      else
	mv -v bob.xxx  bob$NUM.dat
	mv -v ev.xxx   ev$NUM.dat
	mv -v last.xxx last$NUM.dat
	mv -v log.xxx  log$NUM.dat
	mv -v rcc.xxx  rcc$NUM.dat
	mv -v seq.xxx  seq$NUM.dat
	break
      fi
    done
else
  echo "seq.xxx not found, stopping."
fi
