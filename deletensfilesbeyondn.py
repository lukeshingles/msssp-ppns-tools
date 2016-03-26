#!/usr/bin/env python
import os
#from os import walk

print r'This program will show and optionally delete ns????xxxxxxx.??? files where xxxxxxx is greater or equal to nmod_min'

nmodmin = int(raw_input("nmod_min:"))

compfilelist = []
for (dirpath, dirnames, filenames) in os.walk("./"):
    compfilelist.extend(filter(lambda fn: ((fn[:2]=='ns' and len(fn)==17) and int(fn[-11:-4]) >= nmodmin), filenames))
    break

print '\n'.join(compfilelist)

if raw_input("Delete these files? (y/n):")=='y':
    for filename in compfilelist:
        print 'deleting ' + filename
        os.remove(filename)
