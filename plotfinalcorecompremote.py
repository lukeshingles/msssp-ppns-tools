#!/usr/bin/env python3
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import glob
from plotcommon import *

# modellist = ['m5z0006y40', 'm6z0006y24', 'm6z0006y30', 'm6z0006y35', 'm6z0006y40']

for mass in ['3', '4', '5', '6']:
    for strhe in ['24', '30', '35', '40']:
        modellist = ('m' + mass + 'z0006y' + strhe,)

        modelnumlower = -1  # not important since we only keep the final model
        modelnumupper = 999999999  # 472300

        specieslist = ['H', 'He', 'C', 'N', 'O', 'Other']

#        fig, axes = plt.subplots(len(modellist), sharex=True, figsize=(columnwidth, columnwidth*2.5), tight_layout={"pad":0.1,"h_pad":0.0,"w_pad":0.0})
        fig = plt.figure()
        ax = fig.add_axes([0.112, 0.11, 0.84, 0.85])
        mcore = [0.0 for x in modellist]
        m = 0
        # find the last bob file

        bobfilelist = glob.glob('/home/lukes/coala/z0006models-herich/' + modellist[0] + '/bob???.dat')
        print(modellist[0], bobfilelist)
        if len(bobfilelist) > 0:
            bobfilename = bobfilelist[-1]
    else:
        continue
        mtot = -1
        abundances = {}
        bobfile = open(bobfilename, 'r')
        enteredselectedmodel = False
        enteredabundancetable = False
        for line in bobfile:

            if enteredselectedmodel and enteredabundancetable:
                if line.startswith('  NEXT TINT=') or line.startswith(' LHeB > 10000.0 '):
                    enteredabundancetable = False
                    enteredselectedmodel = False
                    for n in reversed(list(range(len(abundances['H'])))):
                        if abundances['H'][n] > 0.45:
                            mcore[m] = massgrid[n]
                            break
                else:  # we can output the abundances now that we're leaving the abundancetable
                    # print line
                    row = line.split()
                    massgrid.append(((1.0 - float(row[1])) ** 3) * mtot)  # "1-X" is a weird quantity
                    if 'H' in specieslist:
                        abundances['H'].append(float(line[36:44]))
                    if 'He' in specieslist:
                        abundances['He'].append(float(line[54:63]))
                    if 'C' in specieslist:
                        abundances['C'].append(float(line[63:73]))
                    if 'N' in specieslist:
                        abundances['N'].append(float(line[74:84].rstrip('E')))  # Extra E was appearing in the bob files!
                    if 'O' in specieslist:
                        abundances['O'].append(float(line[85:95].rstrip('E')))
                    if 'Other' in specieslist:
                        abundances['Other'].append(float(line[96:103]))

            if line.startswith('  MODEL NO'):
                if not line[10:18].startswith('*'):
                    modelnumber = int(line[10:18])
                else:
                    modelnumber = modelnumupper
                mtot = float(line[22:30])
                if modelnumlower <= modelnumber <= modelnumupper:
                    enteredselectedmodel = True
                else:
                    enteredselectedmodel = False
                enteredabundancetable = False

            if line.startswith('                                        H      HE3        HE       C           N         O      OTHER'):
                enteredabundancetable = True
                massgrid = []
                for species in specieslist:
                    abundances[species] = []

        print('/'.join(bobfilename.split('/')[-2:]) + ': last NMOD={0:7d}, Mtot={1:.3f}, Mcore={2:.3f}'.format(modelnumber, mtot, mcore[m]))
        # print massgrid
        for (species, color, dashes) in zip(specieslist, abundancecolorlist, abundancedasheslist):
            ax.plot(massgrid, abundances[species], label=species, color=color, dashes=dashes, lw=2,
                    marker='None', markersize=8, markeredgewidth=0)
        print('Central C/N={0:.3f}'.format((abundances['C'][-1]/abundances['N'][-1] * 14.0/12.0)))
        print('Central C/O={0:.3f}'.format((abundances['C'][-1]/abundances['O'][-1] * 16.0/12.0)))
        print(' ')
        ax.set_xlim(xmax=max(mcore)*1.05)
        modellabel = modellist[m][1:].split('z')[0] + ' M$_\odot$, Y=0.' + modellist[m][-2:]
        ax.annotate(modellabel, xy=(0.03, 0.08),  xycoords='axes fraction', horizontalalignment='left',
                    verticalalignment='bottom', fontsize=fs-1.5)

        # ax.xaxis.set_major_locator(ticker.MultipleLocator(base=1.0))
        ax.xaxis.set_minor_locator(ticker.MultipleLocator(base=0.05))
        ax.yaxis.set_major_locator(ticker.MultipleLocator(base=0.1))
        ax.yaxis.set_minor_locator(ticker.MultipleLocator(base=0.05))
        plt.setp(plt.getp(ax, 'xticklabels'), fontsize=fsticklabel)
        plt.setp(plt.getp(ax, 'yticklabels'), fontsize=fsticklabel)
        for axis in ['top', 'bottom', 'left', 'right']:
            ax.spines[axis].set_linewidth(framewidth)
        ax.set_ylabel(r'$\mathrm{X}_i$', fontsize=fs)
        ax.set_ylim(ymin=-0.04, ymax=1.0)
        # ax.set_yticks(ax.get_yticks()[1:-2])

        # ax.set_yscale('log')

        ax.legend(loc='upper left', ncol=4, handlelength=2, numpoints=1, prop={'size': fs-2})
        ax.set_xlabel("$\mathrm{M}_\mathrm{r} \,[\mathrm{M}_\odot]$", fontsize=fs)

        fig.savefig('fig-finalcorecomp-' + modellist[0] + '.pdf', format='pdf')
        plt.close()
