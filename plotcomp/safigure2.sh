#!/bin/sh

../getmodelabundances.py ../m3z01-ths8-pmz1/comp/ns125_0006940.cmp p c13 n14 > m3z01-ths8pmz1-0006940.csv
./plotpmz.py m3z01-ths8pmz1-0006940.csv
rm m3z01-ths8pmz1-0006940.csv
../getmodelabundances.py ../m3z01-ths8-pmz1/comp/ns125_0007184.cmp p c13 n14 > m3z01-ths8pmz1-0007184.csv
./plotpmz.py m3z01-ths8pmz1-0007184.csv
rm m3z01-ths8pmz1-0007184.csv