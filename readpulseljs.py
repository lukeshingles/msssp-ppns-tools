#!/usr/bin/env python

import sys
import math

tpdata = []
headers = []
with open('pulse.dat','rb') as file:
    for line in file.readlines():
        row = line.split()
        if row[0].startswith("#"):
            headers = [row[0][1:]] + row[1:] #remove leading hash character
        elif len(headers) == 0:
            sys.exit("ERROR: No header row found (starts with #)")
        else:
            # first thermal pulse, or a new one
            if len(tpdata) == 0 or tpdata[-1]['pulse'] != row[0]:
                tpdata.append(dict(zip(headers,row)))
            else:
                print "Duplicate pulse " + row[0]

print "Variables: " + ", ".join(headers) + "\n"

pulseCount = int(tpdata[-1]['pulse'])

print "Pulse count: ",pulseCount,", last TP number: ", len(tpdata)

totalMDU = 0.0e0
HBBpulsecount = 0
TeffSum = 0.0
TeffValCount = 0
ListInterpulsePeriod = []
ListIscvnTime = []
MaxLambda = -1
MaxMHecsh = -1
MaxTbce = -1
MaxTHeShell = -1
MaxTHShell = -1
for pulse in tpdata[1:]:
    if float(pulse['Teff']) != 99999:
        TeffSum += float(pulse['Teff'])
        TeffValCount += 1
    
    if float(pulse['THeshell']) > MaxTHeShell:
        MaxTHeShell = float(pulse['THeshell'])

    if float(pulse['THshell']) > MaxTHShell:
        MaxTHShell = float(pulse['THshell'])

    if float(pulse['Tbce']) > MaxTbce:
        MaxTbce = float(pulse['Tbce'])

    if float(pulse['M_csh']) > MaxMHecsh:
        MaxMHecsh = float(pulse['M_csh'])

    if float(pulse['lambda']) > MaxLambda and float(pulse['lambda']) < 1.00:
        MaxLambda = float(pulse['lambda'])

    if float(pulse['t_csh']) != 0.:
        ListIscvnTime.append(float(pulse['t_csh']))
    if float(pulse['interpulse']) != 0.:
        ListInterpulsePeriod.append(float(pulse['interpulse']))
 
    totalMDU += float(pulse['Ddredge'])
    if float(pulse['Tbce']) > 5e7:
         HBBpulsecount += 1

avgInterpulsePeriod = reduce(lambda x, y: x + y, ListInterpulsePeriod) / len(ListInterpulsePeriod)
stdevInterpulsePeriod = math.sqrt(reduce(lambda x, y: x + y, map(lambda z: (z-avgInterpulsePeriod)**2, ListInterpulsePeriod)) / len(ListInterpulsePeriod))

avgIscvnTime = reduce(lambda x, y: x + y, ListIscvnTime) / len(ListIscvnTime)
stdevIscvnTime = math.sqrt(reduce(lambda x, y: x + y, map(lambda z: (z-avgIscvnTime)**2, ListIscvnTime)) / len(ListIscvnTime))
print "Pulses with Tbce>50 MK: %d" % HBBpulsecount + " out of %d" % pulseCount
print "Mcore at 1st TP: %.3f" % float(tpdata[1]['Mcore'])
print "Total mass dredged up: %.5e" % totalMDU
print "Max lambda: %.2f" % MaxLambda
print "Max THeshell: %.2e" % MaxTHeShell
print "Max THshell: %.2e" % MaxTHShell
print "Max Mpdcz: %.4f" % MaxMHecsh
print "Max Tbce: %.2e" % MaxTbce
print "Avg interpulse period: %.2f +/- %.2f yrs" % (avgInterpulsePeriod, stdevInterpulsePeriod)
print "Avg iscvn time: %.2f +/- %.2f yrs" % (avgIscvnTime, stdevIscvnTime)
print "Avg Teff: %d" % (TeffSum/TeffValCount)

