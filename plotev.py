#!/usr/bin/env python
import csv
import sys
import os
import math
import struct
import matplotlib.pyplot as plt
import argparse

def evcode(string):
    value = int(string)
    if value < 1 or value > 64:
        msg = "%r is not between 1 and 64." % string
        raise argparse.ArgumentTypeError(msg)
    return value

parser = argparse.ArgumentParser(description='Plot ev files from Mount Stromlo Stellar Structure code and save as evplot.pdf.')
parser.add_argument('-listcodes', dest='listcodes', action='store_true',
                    default=False, help='List variable code labels 1-64')
parser.add_argument('-logscalex', dest='logscalex', action='store_true',
                    default=False, help='Use a log scale on the x-axis')
parser.add_argument('-logscaley', dest='logscaley', action='store_true',
                    default=False, help='Use a log scale on the y-axis')
parser.add_argument('-xcode', metavar='N', type=evcode, default=1,
                    help='x value variable number 1-64 (default 1)')
parser.add_argument('-ycode', metavar='N', type=evcode, default=59,
                    help='y value variable number 1-64 (default 59)')
parser.add_argument('-xmin', metavar='N', type=float,
                    help='min x value on plot')
parser.add_argument('-xmax', metavar='N', type=float,
                    help='max x value on plot')
parser.add_argument('-ymin', metavar='N', type=float,
                    help='min y value on plot')
parser.add_argument('-ymax', metavar='N', type=float,
                    help='max y value on plot')
parser.add_argument('-every', metavar='N', type=int, default=50,
                    help='plot every N models')
parser.add_argument('infiles', metavar='file', type=str, nargs='*',
                    help='one or more ev files')

args = parser.parse_args()

labels = ['Time (in years)',                                             
'Convective Core Mass Fraction',
'Maximum Temperature',
'Density at Tmax',
'Mass H-exhausted Core [Msun]',
'Mass of Temperature Maximum',
'Inner Edge of Convective Envelope [Msun]',
'Intershell Convective Region, Outer Edge',
'Intershell Convective Region, Inner Edge',
'Mass of He-exhausted Core [Msun]',
'Radius/Rsun',
'Central Density',
'Central Temperature',
'Central Pressure',
'Luminosity [L/Lsun]',
'H Burning Luminosity',
'He Burning Luminosity',
'C Burning Luminosity',
'Gravitational Luminosity',
'Neutrino Luminosity',
'Log10( Effective temperature [K] )',
'Central He4',
'Central C12',
'He4 at Tmax',
'C12 at Tmax',
'Central O16',
'Mass at Bottom of H Shell',
'Bottom H Shell Radius/Rsun',
'Bottom H Shell Temperature',
'Bottom H Shell Density',
'Middle H Shell Radius/Rsun',
'Middle H Shell Temperature [K]',
'Middle H Shell Density',
'Mass at Top of H Shell',
'Top H Shell Radius/Rsun',
'Top H Shell Temperature',
'Top H Shell Density',
'Mass at Bottom of He Shell',
'Bottom He Shell Radius/Rsun',
'Bottom He Shell Temperature [K]',
'Bottom He Shell Density',
'Middle He Shell Radius/Rsun',
'Middle He Shell Temperature [K]',
'Middle He Shell Density',
'Mass at Top of He Shell',
'Top He Shell Radius/Rsun',
'Top He Shell Temperature',
'Top He Shell Density',
'T at Base of Intershell Zone',
'Rho at Base of Intershell Zone',
'Intershell Convective Region: Centre',
'T at Centre of Intershell Zone',
'Rho at Centre of Intershell Zone',
'T at Top of Intershell Zone',
'Rho at Top of Intershell Zone',
'Max Eps(H)',
'T at Max Eps(H)',
'Rho at Max Eps(H)',
'T Base of Convective Envelope [K]',
'Total Mass/Msun',
'Mdot',
'Period [days]',
'Vexp',
'Mbol']

if args.listcodes:
    labelList = map(lambda x,y:str(x+1).rjust(2) + "\t" + y,range(len(labels)),labels)
    print "Variable codes:"
    print "\n".join(labelList)

if len(args.infiles) == 0:
    print "No ev files specified. Use -h to list command-line options."
else:
    print "Plotting " + labels[args.ycode-1] + " vs. " + labels[args.xcode-1]

    seriesLabels = map(lambda x:x[-20:], args.infiles)

    listX = []
    listY = []
    for filename in args.infiles:
        listX.append([])
        listY.append([])
        with open(filename, mode='rb') as file:
            print 'Processing ' + filename + "..."
            fileContent = file.read()
            print 'Starting Mass: ',struct.unpack("d", fileContent[4:12])[0]

            #b is the byte number
            for b in range(20,len(fileContent)-4,268*args.every): #every n models
                #modelNumbers.append(struct.unpack("i", fileContent[b:b+4])[0])
                if args.xcode == 1:
                    #listX[-1].append([struct.unpack("d", fileContent[b+4:b+12])[0]]) #time
                    if len(listX[-1]) == 0:
                        listX[-1].append(0.0e0)
                    else:
                        listX[-1].append(struct.unpack("d", fileContent[b+4:b+12])[0] - struct.unpack("d", fileContent[20+4:20+12])[0]) #time minus begining time
                else:
                    listX[-1].append(struct.unpack("f", fileContent[b+12+(args.xcode-2)*4:b+16+(args.xcode-2)*4])[0])
                if args.ycode == 1:
                    listY[-1].append([struct.unpack("d", fileContent[b+4:b+12])[0]]) #time
                else:
                    listY[-1].append(struct.unpack("f", fileContent[b+12+(args.ycode-2)*4:b+16+(args.ycode-2)*4])[0])

    fig = plt.figure()
    ax = fig.add_axes([0.15, 0.11, 0.80, 0.85])

    ax.yaxis.grid(color='gray', linestyle='dotted')
    #ax.set_axisbelow(True)

    lineColors = ('black','blue','red','purple','orange')
    for n in range(len(listX)):
        ax.plot(listX[n], listY[n], color=lineColors[n % len(lineColors)], marker='None', markersize=0, markeredgewidth=0,lw=0.5,linestyle='-',label=seriesLabels[n])

    ax.set_xlabel(labels[args.xcode-1], labelpad=12)
    ax.set_ylabel(labels[args.ycode-1], labelpad=12)

    if args.logscalex:
        ax.set_xscale('log')
    if args.logscaley:
        ax.set_yscale('log')

    if not args.xmin is None:
        ax.set_xlim(xmin=float(args.xmin))
    if not args.xmax is None:
        ax.set_xlim(xmax=float(args.xmax))
    if not args.ymin is None:
        ax.set_ylim(ymin=float(args.ymin))
    if not args.ymax is None:
        ax.set_ylim(ymax=float(args.ymax))

        #ax.set_xlim(1000,100000)
        #plt.xlim(1000,100000)
        #fig.xlim(1000,100000)

    plt.locator_params(axis = 'y', nbins = 30)
    ax.legend(loc=4,handlelength=1,frameon=False,numpoints=1,prop={'size':12})

    fig.savefig('plotev.pdf',format='pdf')
    plt.close()

