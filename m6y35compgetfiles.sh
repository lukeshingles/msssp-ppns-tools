#!/bin/sh

scp marmot:~/marmot/m6z0006y35a0s320/ns320_03047??.cmp m6y35comp/comp/
#scp marmot:~/marmot/m6z0006y35a0s320/ns320_0304???.cmp m6y35comp/
#rsync -avhL --include='final*.dat' --include='yields.dat' --include='surfabund.dat' --include="m*z0006y*/" --exclude='*' --exclude='arrow' --exclude='comp' --exclude='nsmodel' mosura:~/coala/z0006models-herich/320species/ ppns320species/
