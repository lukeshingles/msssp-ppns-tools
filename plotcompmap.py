#!/usr/bin/env python
import csv
import math
import struct
import numpy as np
import matplotlib.pyplot as plt
#from matplotlib.mlab import griddata
from scipy.interpolate import griddata
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

nmodstart = 3100
nmodend   = 4600
speciesNamesDisplayed = ('p','he4','c13','ba138')
#modelfolder = "/Volumes/Seagate 2TB/coala/z0006models-herich/320species/m3z0006y24alpha0s320/"
modelfolder = "/Users/lukes/Downloads/m3z0006y24alpha0s320/"

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

fig = plt.figure(figsize=(12,7))
ax = fig.add_axes([0.10, 0.00, 0.85, 0.97])
fs = 18

xList = []
yList = []
zList = []
z2List = []
mhcorelistnmod = []
mhcorelistmass = []
mhecorelistnmod = []
mhecorelistmass = []
envelopeczinnernmod = []
envelopeczinnermass = []
iscvnzonenmod = []
iscvnzoneinner = []
iscvnzoneouter = []

compfilelist = []
for (dirpath, dirnames, filenames) in walk(modelfolder + "comp/"):
    compfilelist.extend(filter(lambda fn: fn[:2]=='ns' and fn[-4:]=='.cmp' and int(fn[-11:-4]) >= nmodstart and int(fn[-11:-4]) <= nmodend, filenames))
    break

for compfilename in compfilelist:
    if isBinaryFile(dirpath + compfilename):
        print "\n==>comp file (bin): '" + compfilename
        with open(dirpath + compfilename, mode='rb') as compfile:
            fileContent = compfile.read()
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
                abundances[massPointNum][s] = (massnumber * 0.5 * (float(compRaw[3 + numMassPoints + massPointNum*compNumSpecies + speciesDisplayedNumbers[s]]) + float(compRaw[3 + numMassPoints + (numMassPoints + massPointNum)*compNumSpecies + speciesDisplayedNumbers[s]])))
        numConvectiveBoundaries = int(compRaw[3 + numMassPoints + numMassPoints*compNumSpecies*2])
        convectiveBoundaries = map(float,compRaw[3 + numMassPoints + numMassPoints*compNumSpecies*2+1:][:numConvectiveBoundaries])
        convectiveBoundaries = zip(convectiveBoundaries[0::2], convectiveBoundaries[1::2])

    modelNumber = int(compfile[-11:-4]) #overwrite value from the file with number from filename

    print "# model number:", modelNumber
    print "# number of mass points:", numMassPoints
    print "# comp file species count:", compNumSpecies
    print "# convective boundaries: [" + "][".join(['%.5f, %.5f' % (cvz[0],cvz[1]) for cvz in convectiveBoundaries]) + "]"
    #print "# values are mass fraction"
    #print ",".join(["#mass"]+map(lambda x:speciesList[x][2],speciesDisplayedNumbers))

    for massPointNum in range(numMassPoints):
        if abundances[massPointNum][1] >= 0.45 and (abundances[massPointNum-1][1] < 0.45 or massPointNum == 0):
            mhecorelistnmod.append(modelNumber)
            mhecorelistmass.append(massPoints[massPointNum])
        if abundances[massPointNum][0] >= 0.50 and (abundances[massPointNum-1][0] < 0.50 or massPointNum == 0):
            mhcorelistnmod.append(modelNumber)
            mhcorelistmass.append(massPoints[massPointNum])

        #print ", ".join(["%.5f" % massPoints[massPointNum]] + map(lambda z: '%.3f' % z,abundances[massPointNum]))
        xList.append(modelNumber)
        yList.append(massPoints[massPointNum])
        zList.append(math.log10(max(1e-4,abundances[massPointNum][2])))
        z2List.append(math.log10(max(1e-8,abundances[massPointNum][3])))

        iscvnzonenmod.append(modelNumber)
        iscvnzoneinner.append(0.0)
        iscvnzoneouter.append(0.0)

        for cvz in convectiveBoundaries:
            if cvz[1] > 38.0: #envelope convection zone
                envelopeczinnernmod.append(modelNumber)
                envelopeczinnermass.append(cvz[0])
            else:
                if (cvz[1]-cvz[0]) > 1e-4:
                    if iscvnzoneinner[-1] == 0.0:
                        iscvnzoneinner[-1] = cvz[0]
                        iscvnzoneouter[-1] = cvz[1]
                    else:
                        if cvz[1] > iscvnzoneouter[-1]:
                            iscvnzoneouter[-1] = cvz[1]

yMax = max(envelopeczinnermass)
xi, yi = np.mgrid[min(xList):max(xList):200j,min(mhecorelistmass)*0.9995:yMax:100j]
print "Interpolating..."

zi = griddata((np.array(xList),np.array(yList)),np.array(zList),(xi,yi), method='nearest')
zi2 = griddata((np.array(xList),np.array(yList)),np.array(z2List),(xi,yi), method='nearest')

cdict = plt.cm.autumn._segmentdata.copy()
#cdict['red'] =  ((0.00, 1.0, 1.0),
#                 (1.00, 0.2, 0.2))
#cdict['green'] =((0.00, 0.0, 0.0),
#                 (1.00, 0.0, 0.0))
#cdict['blue'] =((0.00, 0.0, 0.0),
#                 (1.00, 0.0, 0.0))
cdict['alpha'] =  ((0.00, 0.0, 0.0),
                   (0.15, 0.0, 1.0),
#                   (0.50, 1.0, 1.0),
#                   (0.75, 1.0, 1.0),
                   (1.00, 1.0, 1.0))
plt.register_cmap(name='Cmapoverlay', data=cdict)

cdict = plt.cm.Greens._segmentdata.copy()
cdict['red'] =  ((0.00, 0.0, 0.0),
                 (1.00, 0.0, 0.0))
cdict['green']= ((0.00, 0.267, 0.267),
                 (1.00, 0.267, 0.267))
cdict['blue'] = ((0.00, 0.106, 0.106),
                 (1.00, 0.106, 0.106))
cdict['alpha'] =  ((0.00, 0.0, 0.0),
                   (0.08, 0.0, 0.0),
#                   (0.50, 1.0, 1.0),
#                   (0.75, 1.0, 1.0),
                   (1.00, 1.0, 1.0))
plt.register_cmap(name='Cmapoverlay2', data=cdict)

print "Plotting..."
#ax.pcolormesh(xi,yi,zi, cmap=plt.cm.hsv, vmin=0.0)

cf = ax.contourf(xi, yi, zi, cmap='Cmapoverlay')
cf2 = ax.contourf(xi, yi, zi2, cmap='Cmapoverlay2')

x = plt.colorbar(cf, label="X(C-13)", orientation='horizontal', pad=0.02)
x.ax.invert_xaxis()
x2 = plt.colorbar(cf2, label="X(Ba-138)", orientation='horizontal',pad=0.13)
x2.ax.invert_xaxis()


plt.fill_between(envelopeczinnernmod, envelopeczinnermass, [yMax] * len(envelopeczinnermass), facecolor=(55.0/255,101.0/255,186.0/255), lw=0)

startindex = -1
for i in range(len(iscvnzonenmod)):
    if (iscvnzoneinner[i] == 0.0 and iscvnzoneouter[i] == 0.0): #or i == len(iscvnzonenmod)-1:
        if startindex != -1:
            plt.fill_between(iscvnzonenmod[startindex:i], iscvnzoneinner[startindex:i], iscvnzoneouter[startindex:i], facecolor=(55.0/255,101.0/255,186.0/255), lw=0)
            startindex = -1
    else:
        if startindex == -1:
            startindex = i


ax.plot(mhecorelistnmod, mhecorelistmass, color='black', linestyle='--',markersize=7, markeredgewidth=0, marker='None', lw=2)
ax.plot(mhcorelistnmod, mhcorelistmass, color='black', linestyle='-',markersize=7, markeredgewidth=0, marker='None', lw=2)

plt.setp(plt.getp(plt.gca(), 'xticklabels'), fontsize=fs-2)
plt.setp(plt.getp(plt.gca(), 'yticklabels'), fontsize=fs-2)
ax.set_ylabel('M / M$_\odot$', labelpad=12, fontsize=fs)
ax.set_xlabel("model number", labelpad=12, fontsize=fs)
fig.savefig('plotcompmap.pdf',format='pdf')
plt.close()
