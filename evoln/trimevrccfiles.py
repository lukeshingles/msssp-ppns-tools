#!/usr/bin/env python
import os
import struct

evfilenum = []
evnmodstart = []
evnmodend = []

print "file".rjust(10), "start".rjust(10), "end".rjust(10)

for n in range(0,100):
    filename = "ev{0:03d}.dat".format(n)
    if os.path.isfile(filename):
        modelNumbers = []
        with open(filename, mode='rb') as evfile:
            fileContent = evfile.read()
            #print 'Mass: ',struct.unpack("d", fileContent[4:12])[0]

            #b is the byte number
            for b in range(20,len(fileContent)-4,268):
                modelNumbers.append(struct.unpack("i", fileContent[b:b+4])[0])

        evfilenum.append(n)
        evnmodstart.append(modelNumbers[0])
        evnmodend.append(modelNumbers[-1])
        print filename.rjust(10), str(modelNumbers[0]).rjust(10), str(modelNumbers[-1]).rjust(10)

for n in range(1,len(evfilenum)):
    if evnmodstart[n] <= evnmodstart[n-1]:
        print "WARNING: ev{0:03d}.dat starts before ev{1:03d}.dat!".format(evfilenum[n], evfilenum[n-1])
    elif evnmodend[n-1] >= evnmodstart[n]:
        print "ev{0:03d}.dat overlaps with ev{1:03d}.dat".format(evfilenum[n-1], evfilenum[n])
        if os.path.isfile("ev{0:03d}trim.dat".format(evfilenum[n-1])):
            print "- deleting existing file ev{0:03d}trim.dat".format(evfilenum[n-1])
            os.system("rm ev{0:03d}trim.dat".format(evfilenum[n-1]))
        print "- trimming ev{0:03d}.dat to end at {1:d}".format(evfilenum[n-1], evnmodstart[n]-1)
        os.system("echo 'ev{0:03d}.dat\nev{1:03d}trim.dat\n0\n".format(evfilenum[n-1], evfilenum[n-1]) + str(evnmodstart[n]-1) + "' | selectp > /dev/null")

        if os.path.isfile("rcc{0:03d}trim.dat".format(evfilenum[n-1])):
            print "- deleting existing file rcc{0:03d}trim.dat".format(evfilenum[n-1])
            os.system("rm rcc{0:03d}trim.dat".format(evfilenum[n-1]))
        print "- trimming rcc{0:03d}.dat to end at {1:d}".format(evfilenum[n-1], evnmodstart[n]-1)
        os.system("echo 'rcc{0:03d}.dat\nrcc{1:03d}trim.dat\n0\n".format(evfilenum[n-1], evfilenum[n-1]) + str(evnmodstart[n]-1) + "' | rccselect > /dev/null")
