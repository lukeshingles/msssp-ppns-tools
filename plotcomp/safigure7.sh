#!/bin/sh

../getmodelabundances.py ../m3z01-ths8-pmz1/comp/ns125_0073610.cmp p he4 s32 s33 s34 s36 > m3z01-ths8pmz1-0073610.csv
./plotcomposition.py m3z01-ths8pmz1-0073610.csv -xmin 0.645 -xmax 0.685
rm m3z01-ths8pmz1-0073610.csv