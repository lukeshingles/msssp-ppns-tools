#!/usr/bin/env python
import matplotlib.pyplot as plt
#from matplotlib.lines import Line2D
from matplotlib.patches import PathPatch
import csv
#import sys
#import itertools
import argparse

parser = argparse.ArgumentParser(description='Plot model composition csv file output by getmodelabundances.py.')
parser.add_argument('compfile', action='store',
                    help='model composition (.csv) file')
parser.add_argument('-xmin',type=float,
                    help='minimum x value')
parser.add_argument('-xmax',type=float,
                    help='minimum x value')
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
    plt.bar(convectiveBoundaries[i], 1, width=convectiveBoundaries[i+1]-convectiveBoundaries[i], bottom=10**-8.5,lw=0, alpha=0.5, color="0.65", edgecolor='black', linewidth=5)
    #p = ax.fill_between((convectiveBoundaries[i],convectiveBoundaries[i+1]), (1,1), 10**-8.5, color='0.9',lw=0)
    #for path in p.get_paths():
    #    p1 = PathPatch(path, fc="white", hatch="/", edgecolor='green')
    #    ax.add_patch(p1)
        #p1.set_zorder(p.get_zorder())
    #    p1.set_zorder(-1)

for i in range(len(abundArray)):
    lineDashes = [(),(9,2),(),(9,2),(4,2),(2,2)][(i)%6]
    lineColor = [(1.0,0.0,0.0),(1.0,0.0,0.0),'0','0','0','0'][(i)%6]

    plt.plot(massArray, abundArray[i], color=lineColor, marker='None', markersize=0, linewidth=3, dashes=lineDashes, markeredgewidth=0, label=headerRow[1+i])

plt.legend(loc=0, handlelength=2)

fs = 16.5
plt.setp(plt.getp(plt.gca(), 'xticklabels'), fontsize=fs)
plt.setp(plt.getp(plt.gca(), 'yticklabels'), fontsize=fs)

#ax.set_title("$^{13}$C pocket", y=1.04)
ax.set_yscale('log')
ax.set_ylabel('Molar fraction Y', labelpad=8, fontsize=fs)
ax.set_xlabel("Mass coordinate / M$_\odot$", labelpad=8, fontsize=fs)
ax.set_xlim(min(massArray),max(massArray))
ax.set_xlim(args.xmin,args.xmax)
#ax.set_ylim(min(filter(lambda x:x != float('-inf'), abundArray[0])),max(abundArray[0]))
#ax.set_ylim(min(abundArray),max(abundArray))
#ax.set_ylim(-8.5,0)
ax.set_ylim(10 ** -8.3,1)
fig.savefig(args.compfile[:-4]+'.pdf',format='pdf')
plt.close()
