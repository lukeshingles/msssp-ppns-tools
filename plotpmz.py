#!/usr/bin/env python
import matplotlib.pyplot as plt
#from matplotlib.lines import Line2D
import csv
import argparse

parser = argparse.ArgumentParser(description='Plot model composition csv file output by getmodelabundances.py.')
parser.add_argument('compfile', action='store',
                    help='model composition (.csv) file')
args = parser.parse_args()

massArray = []
abundArray = []

fig = plt.figure()
ax = fig.add_axes([0.112, 0.11, 0.84, 0.85])
convectiveBoundaries = []

csvReader = csv.reader(open(args.compfile,'rb'), delimiter=',', skipinitialspace=True)
for row in csvReader:
    if not row[0].startswith("#"):
        massArray.append(float(row[0]))

        for i in range(0,len(row)-1):
            newAbund = 10 ** float(row[i+1])
            if i == len(abundArray):
                abundArray.append([newAbund]) #create new column for the species
            else:
                abundArray[i].append(newAbund)

    elif row[0].startswith("# convective boundaries: "):
        convectiveBoundaries = [float(row[0][25:])] + map(float,row[1:])
    elif row[0] == '#mass':
        headerRow = row

print convectiveBoundaries
for i in range(0,len(convectiveBoundaries),2):
    #plt.bar(convectiveBoundaries[i], 10**8.5, width=convectiveBoundaries[i+1]-convectiveBoundaries[i], bottom=10**-8.5, color='1.0',lw=0,alpha=1, hatch="//", edgecolor='0.4')
    plt.bar(convectiveBoundaries[i], 1, width=convectiveBoundaries[i+1]-convectiveBoundaries[i], bottom=10**-8.5,lw=0, alpha=0.5, color="0.65", edgecolor='black', linewidth=5)

for i in range(len(abundArray)):
    lineColor = ['0','r','b','y'][i%4]
    lineDashes = [(),(15,2),(3,2),(0.2,6),(4,2)][i%4]

    plt.plot(massArray, abundArray[i], color=lineColor, marker='o', markersize=0, lw=3, dashes=lineDashes, markeredgewidth=0, label=headerRow[1+i])

plt.legend(loc=4, handlelength=2)

fs = 16.5
plt.setp(plt.getp(plt.gca(), 'xticklabels'), fontsize=fs)
plt.setp(plt.getp(plt.gca(), 'yticklabels'), fontsize=fs)

#ax.set_title("$^{13}$C pocket", y=1.04)
ax.set_yscale('log')
ax.set_ylabel('Molar fraction Y', labelpad=8, fontsize=fs)
ax.set_xlabel("Mass coordinate / M$_\odot$", labelpad=8, fontsize=fs)
ax.set_xlim(min(massArray),max(massArray))
ax.set_xlim(0.628,0.6335)
#ax.set_ylim(min(filter(lambda x:x != float('-inf'), abundArray[0])),max(abundArray[0]))
#ax.set_ylim(min(abundArray),max(abundArray))
#ax.set_ylim(-8.5,0)
ax.set_ylim(10 ** -8.5,1)
fig.savefig(args.compfile[:-4]+'.pdf',format='pdf')
plt.close()
