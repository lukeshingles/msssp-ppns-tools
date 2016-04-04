#!/usr/bin/env python
import csv
import struct
import numpy as np
import matplotlib.pyplot as plt
from os import walk

def isBinaryFile (filename):
    fin = open(filename, 'rb')
    try:
        CHUNKSIZE = 1024
        while 1:
            chunk = fin.read(CHUNKSIZE)
            if '\0' in chunk: # found null byte
                return True
            if len(chunk) < CHUNKSIZE:
                break # done
    finally:
        fin.close()
    return False

#nmodstart = 304320
#nmodend   = 306000
nmodstart = -1
nmodend = 999999999

speciesNamesDisplayed = ('p','he4','c13','n14','pb208')
#modelfolder = "/Volumes/Seagate 2TB/coala/z0006models-herich/320species/m6z0006y35a0s320/"
modelfolder = "m6y35comp/"

speciesfile = modelfolder + "species.dat"

with open(speciesfile, 'rb') as txtFile:
    csvReader = csv.reader(txtFile, delimiter=' ', skipinitialspace=True)
    speciesCount = int(csvReader.next()[0])
    speciesList = [()] * speciesCount
    print "# species file: '" + speciesfile + "' lists " + str(speciesCount) + " species"
    for i in range(speciesCount):
        #mass number, elm symbol, species name, neutron number
        row = csvReader.next()
        speciesList[i] = (int(row[0]), row[1], row[2], int(row[3]))

#convert species names to numbers
speciesDisplayedNumbers = map(lambda z: speciesList.index(z), filter(lambda z: z[2] in speciesNamesDisplayed, speciesList))

fs = 18

compfilelist = []
for (dirpath, dirnames, filenames) in walk(modelfolder + "comp/"):
    compfilelist.extend(filter(lambda fn: fn[:2]=='ns' and fn[-4:]=='.cmp' and int(fn[-11:-4]) >= nmodstart and int(fn[-11:-4]) <= nmodend, filenames))
    break

for compfilename in compfilelist:
    if isBinaryFile(dirpath + compfilename):
        print "\n==>comp file (bin): '" + compfilename
        with open(dirpath + compfilename, mode='rb') as fcomp:
            fileContent = fcomp.read()
            #model number is wrong for some reason
            modelNumber = struct.unpack("<H", fileContent[0:2])[0]
            numMassPoints = struct.unpack("<H", fileContent[2:4])[0]
            compNumSpecies = struct.unpack("<H", fileContent[4:6])[0]
            massPoints = struct.unpack("f" * numMassPoints, fileContent[6:6+4*numMassPoints])
            abundances = np.zeros((numMassPoints,len(speciesDisplayedNumbers)))

            for massPointNum in range(numMassPoints):
                for s in range(len(speciesDisplayedNumbers)):
                    #one is up flows, other is down flows
                    abundIndex = 6 + 4 * (numMassPoints + compNumSpecies * massPointNum + speciesDisplayedNumbers[s])
                    abundIndex2 = 6 + 4 * (numMassPoints + compNumSpecies * (numMassPoints + massPointNum) + speciesDisplayedNumbers[s])
                    massnumber = speciesList[speciesDisplayedNumbers[s]][0]
                    #average up and down flows and multiply by mass number to get mass fraction
                    abundances[massPointNum][s] = (massnumber * 0.5 * (struct.unpack("<f", fileContent[abundIndex:abundIndex+4])[0] + struct.unpack("f", fileContent[abundIndex2:abundIndex2+4])[0]))

            convindex = 6 + 4 * (numMassPoints + numMassPoints*compNumSpecies*2)
            numConvectiveBoundaries = struct.unpack("H", fileContent[convindex:convindex+2])[0]
            convectiveBoundaries = struct.unpack("f" * numConvectiveBoundaries, fileContent[convindex + 2:convindex + 2 + 4*numConvectiveBoundaries])
            convectiveBoundaries = zip(convectiveBoundaries[0::2], convectiveBoundaries[1::2])
    else:
        print "\n==>comp file (text): " + compfilename
        with open(dirpath + compfilename, 'rb') as txtFile:
            csvReader = csv.reader(txtFile, delimiter=' ', skipinitialspace=True)

            compRaw = []
            for row in csvReader:
                for col in row:
                    if col != '':
                        compRaw.append(col)
        modelNumber = int(compRaw[0])
        numMassPoints = int(compRaw[1])
        compNumSpecies = int(compRaw[2])
        massPoints = map(float, compRaw[3:3+int(compRaw[1])])
        abundances = np.zeros((numMassPoints,len(speciesDisplayedNumbers)))

        for massPointNum in range(numMassPoints):
            for s in range(len(speciesDisplayedNumbers)):
                massnumber = speciesList[speciesDisplayedNumbers[s]][0]
                abundances[massPointNum][s] = (massnumber * 0.5 * (float(compRaw[3 + numMassPoints + massPointNum*compNumSpecies + speciesDisplayedNumbers[s]])
                                               + float(compRaw[3 + numMassPoints + (numMassPoints + massPointNum)*compNumSpecies + speciesDisplayedNumbers[s]])))
        numConvectiveBoundaries = int(compRaw[3 + numMassPoints + numMassPoints*compNumSpecies*2])
        convectiveBoundaries = map(float,compRaw[3 + numMassPoints + numMassPoints*compNumSpecies*2+1:][:numConvectiveBoundaries])
        convectiveBoundaries = zip(convectiveBoundaries[0::2], convectiveBoundaries[1::2])

    modelNumber = int(compfilename[-11:-4]) #overwrite value from the file with number from filename

    print "# model number:", modelNumber
    print "# number of mass points:", numMassPoints
    print "# comp file species count:", compNumSpecies
    print "# convective boundaries: [" + "][".join(['{0:.5f}, {1:.5f}'.format(cvz[0], cvz[1]) for cvz in convectiveBoundaries]) + "]"
    #print "# values are mass fraction"
    #print ",".join(["#mass"]+map(lambda x:speciesList[x][2],speciesDisplayedNumbers))

    fig = plt.figure(figsize=(12,7))
    ax = fig.add_axes([0.10, 0.10, 0.85, 0.85])

    for cvz in convectiveBoundaries:
        #plt.bar(cvz[0], 1, width=cvz[1]-cvz[0], bottom=10**-24, color='1.0',lw=1,alpha=1, hatch="//", edgecolor='0.4')
        plt.bar(cvz[0], 1, width=cvz[1]-cvz[0], bottom=10**-24,lw=0, alpha=1.0, color="0.85", edgecolor='black', linewidth=3)

    colorList = ['black','red','green','blue','orange']
    for s in range(len(speciesDisplayedNumbers)):
        ax.plot(massPoints, [massShell[s] for massShell in abundances], color=colorList[s], label=speciesNamesDisplayed[s], lw=1.5)

    ax.set_yscale('log')
    ax.legend(loc=4,ncol=1,handlelength=1.5,frameon=False,numpoints=1,prop={'size':fs-4})
    ax.set_xlim(xmin=1.164,xmax=1.166)
    ax.set_ylim(ymin=1e-20)
    plt.setp(plt.getp(ax, 'xticklabels'), fontsize=fs-2)
    plt.setp(plt.getp(ax, 'yticklabels'), fontsize=fs-2)
    ax.set_ylabel('Mass fraction', labelpad=12, fontsize=fs)
    ax.set_xlabel("M / M$_\odot$", labelpad=12, fontsize=fs)
    outfile = 'm6y35comp/pdf/' + compfilename + '.pdf'
    print "writing " + outfile
    fig.savefig(outfile,format='pdf')
    plt.close()
