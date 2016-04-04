#!/usr/bin/env python
import csv
import sys
import math
import struct
import argparse
#from collections import deque

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

def formatRow (row):
    if args.format == 'csv':
        return ",".join(row)
    elif args.format == 'tsv':
        return "\t".join(row)
    else:
        return row[0].ljust(7) + "".join(map(lambda z: z.rjust(8), row[1:]))

parser = argparse.ArgumentParser(description='Extract abundances from a nucleosynthesis model comp file.')
parser.add_argument('compfile', action='store',
                    help='model composition (.cmp) file')
parser.add_argument('species', nargs='+',
                    help='species names to be output')
parser.add_argument('-speciesfile', action='store', default='../m3z01-standard-pmz1/species.dat',
                    help='species.dat file')
parser.add_argument('--noheader', action='store_true',
                    help='don\'t output a header')
parser.add_argument('-format', action='store', default='csv',choices=['csv','tsv','fixed'],
                    help='format type (csv, tsv, fixed)')
parser.add_argument('-mass', action='store',
                    help='mass shell selection (nearest greater than)')
args = parser.parse_args()

speciesNamesDisplayed = args.species

#speciesNamesDisplayed = ('p','he4','s32','s33','s34','s36')
#speciesNamesDisplayed = "He4	C12	N14	N15	O16	O17	F19	Ne20	Ne21	Ne22	Si28	Si29	Si30	P31	S32	S33	S34	S36	Ar36	Ar38	Ar39	Ar40	Fe54	Fe55	Fe56	Fe57	Fe58".lower().split("\t")
with open(args.speciesfile, 'rb') as txtFile:
    csvReader = csv.reader(txtFile, delimiter=' ', skipinitialspace=True)
    speciesCount = int(csvReader.next()[0])
    speciesList = [()] * speciesCount
    if not args.noheader:
        print "# species file: '" + args.speciesfile + "' lists " + str(speciesCount) + " species"
    for i in range(speciesCount):
        #mass number, elm symbol, species name, neutron number
        row = csvReader.next()
        speciesList[i] = (int(row[0]), row[1], row[2], int(row[3]))

#convert species names to numbers
speciesDisplayedNumbers = map(lambda z: speciesList.index(z), filter(lambda z: z[2] in speciesNamesDisplayed, speciesList))

if isBinaryFile(args.compfile):
    if not args.noheader:
        print "# comp file: '" + args.compfile + "' (binary)"
    with open(args.compfile, mode='rb') as compfile:
        fileContent = compfile.read()
        modelNumber = struct.unpack("H", fileContent[0:2])[0]
        numMassPoints = struct.unpack("H", fileContent[2:4])[0]
        compNumSpecies = struct.unpack("H", fileContent[4:6])[0]
        massPoints = struct.unpack("f" * numMassPoints, fileContent[6:6+4*numMassPoints])
        abundances = [] * numMassPoints

        for massPointNum in range(numMassPoints):
            abundances.append([])
            for speciesNum in speciesDisplayedNumbers:
                #one is up flows, other is down flows
                abundIndex = 6 + 4 * (numMassPoints + compNumSpecies * massPointNum + speciesNum)
                abundIndex2 = 6 + 4 * (numMassPoints + compNumSpecies * (numMassPoints + massPointNum) + speciesNum)
                #average up and down flows
                abundances[-1].append(0.5 * (struct.unpack("f", fileContent[abundIndex:abundIndex+4])[0] + struct.unpack("f", fileContent[abundIndex2:abundIndex2+4])[0]))

        convindex = 6 + 4 * (numMassPoints + numMassPoints*compNumSpecies*2)
        numConvectiveBoundaries = struct.unpack("H", fileContent[convindex:convindex+2])[0]
        convectiveBoundaries = struct.unpack("f" * numConvectiveBoundaries, fileContent[convindex + 2:convindex + 2 + 4*numConvectiveBoundaries])
else:
    if not args.noheader:
        print "# comp file: '" + args.compfile + "' (text)"
    with open(args.compfile, 'rb') as txtFile:
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
    abundances = [] * numMassPoints

    for massPointNum in range(numMassPoints):
        abundances.append([])
        for speciesNum in speciesDisplayedNumbers:
            abundances[-1].append(0.5 * (float(compRaw[3 + numMassPoints + massPointNum*compNumSpecies + speciesNum]) + float(compRaw[3 + numMassPoints + (numMassPoints + massPointNum)*compNumSpecies + speciesNum])))
    numConvectiveBoundaries = int(compRaw[3 + numMassPoints + numMassPoints*compNumSpecies*2])
    convectiveBoundaries = map(float,compRaw[3 + numMassPoints + numMassPoints*compNumSpecies*2+1:][:numConvectiveBoundaries])

if not args.noheader:
    print "# model number:", modelNumber
    print "# number of mass points:", numMassPoints
    print "# comp file species count:", compNumSpecies
    print "# convective boundaries: " + ",".join(map('{0:.5f}'.format,convectiveBoundaries))
    print "# values are log10(Y)"
    print formatRow(["#mass"] + map(lambda x:speciesList[x][2],speciesDisplayedNumbers))

for massPointNum in range(numMassPoints):
    if args.mass == None or massPoints[massPointNum] >= float(args.mass):
        print formatRow(["{0:.5f}".format(massPoints[massPointNum])] + map(
            lambda z: ("-inf" if z <= 0 else '{0:.3f}'.format(math.log10(z))),abundances[massPointNum]))
        if args.mass != None:
            break
