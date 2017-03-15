#!/usr/bin/env python
import os
# from os import walk

print(r'This program will show and optionally delete ns????xxxxxxx.??? files where xxxxxxx is greater or equal to nmod_min')

# Fix Python 2.x.
try:
    input = raw_input
except NameError:
    pass

nmodmin = int(input("nmod_min:"))

compfilelist = []
for (dirpath, dirnames, filenames) in os.walk("./"):
    compfilelist.extend([fn for fn in filenames if ((fn[:2] == 'ns' and len(fn) == 17) and int(fn[-11:-4]) >= nmodmin)])
    break

print('\n'.join(compfilelist))

if input("Delete these files? (y/n):") == 'y':
    for filename in compfilelist:
        print('deleting ' + filename)
        os.remove(filename)
