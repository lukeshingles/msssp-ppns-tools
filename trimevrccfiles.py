#!/usr/bin/env python
import os
import struct

evfilenum = []
evnmodstart = []
evnmodend = []

print "file".rjust(10), "start".rjust(10), "end".rjust(10)

for n in range(0,100):
    filename = "ev%03d.dat" % n
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
        print "WARNING: ev%03d.dat starts before ev%03d.dat!" % (evfilenum[n],evfilenum[n-1])
    elif evnmodend[n-1] >= evnmodstart[n]:
        print "ev%03d.dat overlaps with ev%03d.dat" % (evfilenum[n-1],evfilenum[n])
        if os.path.isfile("ev%03dtrim.dat" % evfilenum[n-1]):
            print "- deleting existing file ev%03dtrim.dat" % evfilenum[n-1]
            os.system("rm ev%03dtrim.dat" % evfilenum[n-1])
        print "- trimming ev%03d.dat to end at %d" % (evfilenum[n-1],evnmodstart[n]-1)
        os.system("echo 'ev%03d.dat\nev%03dtrim.dat\n0\n" % (evfilenum[n-1],evfilenum[n-1]) + str(evnmodstart[n]-1) + "' | selectp > /dev/null")

        if os.path.isfile("rcc%03dtrim.dat" % evfilenum[n-1]):
            print "- deleting existing file rcc%03dtrim.dat" % evfilenum[n-1]
            os.system("rm rcc%03dtrim.dat" % evfilenum[n-1])
        print "- trimming rcc%03d.dat to end at %d" % (evfilenum[n-1],evnmodstart[n]-1)
        os.system("echo 'rcc%03d.dat\nrcc%03dtrim.dat\n0\n" % (evfilenum[n-1],evfilenum[n-1]) + str(evnmodstart[n]-1) + "' | rccselect > /dev/null")
