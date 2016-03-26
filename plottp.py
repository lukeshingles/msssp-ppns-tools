#!/usr/bin/env python
import sys
#import numpy as np
import matplotlib.pyplot as plt

for mode in range(1+5):

    fig = plt.figure()
    ax = fig.add_axes([0.15, 0.13, 0.82, 0.85])
    fs = 19


    modellist = ['m3z0006y40','m4z0006y30']

    xValues = []
    yValues = []
    for i in range(len(modellist)):
        tpdata = []
        headers = []
        fpulse = open('marmot_backup/evoln_code/' + modellist[i] + '/pulse.dat','rb')
        for line in fpulse.readlines():
            row = line.split()
            if row[0].startswith("#"):
                headers = [row[0][1:]] + row[1:] #remove leading hash character
                print headers
            elif len(headers) == 0:
                sys.exit("ERROR: No header row found (starts with #)")
            else:
                # if first thermal pulse, or a non-duplicate one
                if len(tpdata) == 0 or tpdata[-1]['pulse'] != row[0]:
                    tpdata.append(dict(zip(headers,row)))
                else:
                    print modellist[i] + ": Ignoring duplicate of pulse " + row[0]

        # new set of x,y coords
        xValues.append([])
        yValues.append([])

        if mode == 0:
            ax.set_ylabel('Mcore [M$_\odot$]', labelpad=12, fontsize=fs)
            for pulse in tpdata:
                xValues[-1].append(int(pulse['pulse']))
                yValues[-1].append(float(pulse['Mcore']))
        elif mode == 1:
            ax.set_ylabel('Mcore increase [M$_\odot$]', labelpad=12, fontsize=fs)
            prevMcore = -1.02
            for pulse in tpdata:
                if prevMcore >= 0.0:
                    xValues[-1].append(int(pulse['pulse']))
                    yValues[-1].append(float(pulse['Mcore'])-prevMcore)
                prevMcore = float(pulse['Mcore'])
        elif mode == 2:
            ax.set_ylabel('DUP efficiency $\lambda$', labelpad=12, fontsize=fs)
            for pulse in tpdata:
                xValues[-1].append(int(pulse['pulse']))
                yValues[-1].append(float(pulse['lambda']))
        elif mode == 3:
            ax.set_ylabel('interpulse period [yr]', labelpad=12, fontsize=fs)
            for pulse in tpdata:
                xValues[-1].append(int(pulse['pulse']))
                yValues[-1].append(float(pulse['interpulse']))
        elif mode == 4:
            ax.set_ylabel('Cumulative TDU Mass [M$_\odot$]', labelpad=12, fontsize=fs)
            for pulse in tpdata:
                xValues[-1].append(int(pulse['pulse']))
                if len(yValues[-1]) == 0:
                    yValues[-1].append(float(pulse['Ddredge']))
                else:
                    yValues[-1].append(yValues[-1][-1] + float(pulse['Ddredge']))
        elif mode == 5:
            ax.set_ylabel('DMh', labelpad=12, fontsize=fs)
            for pulse in tpdata:
                xValues[-1].append(int(pulse['pulse']))
                yValues[-1].append(float(pulse['DMh']))


    #ax.yaxis.grid(color='gray', linestyle='dotted')
    #ax.set_axisbelow(True)

    colorList = ('black','blue','red','purple','orange')
    linestyleList = ['-','--','-.',':']

    #print xValues
    #print yValues
    for n in range(len(modellist)):
        ax.plot(xValues[n], yValues[n], color=colorList[n % len(colorList)], marker='x', markersize=2, markeredgewidth=0,lw=1.5,linestyle=linestyleList[0*n % len(linestyleList)], label=modellist[n])


    ax.legend(loc=4,handlelength=1,frameon=False,numpoints=1)

    #plt.setp(plt.getp(plt.gca(), 'xticklabels'), fontsize=fs-2)
    #plt.setp(plt.getp(plt.gca(), 'yticklabels'), fontsize=fs-2)

    ax.set_xlabel('Thermal pulse number', labelpad=12, fontsize=fs)

    #ax.set_xlim(xmin=35)
    #ax.set_xlim(xmax=85)

    #ax.set_yscale('log')

    #ax.set_ylim(ymin=-5.5)
    #ax.set_ylim(ymax=1)

    outfilenames = ['plot-mcore.pdf','plot-mcoreincrease.pdf','plot-lambda.pdf','plot-interpulse.pdf','plot-tdumass.pdf','plot-dmh.pdf']
    print "Writing file: " + outfilenames[mode]
    fig.savefig(outfilenames[mode],format='pdf')
    #fig.savefig('plot-deltamcore.pdf',format='pdf')
    #fig.savefig('plot-lambda.pdf',format='pdf')
    #fig.savefig('plot-interpulse.pdf',format='pdf')
    plt.close()
