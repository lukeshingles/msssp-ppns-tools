#!/usr/bin/env python
import csv
modellist = ('m3z01-standard-pmz1','m3z01-c13an-nacrelow','m3z01-c13an-nacrehigh','m3z01-ne22an-il10low','m3z01-ne22an-il10med','m3z01-ne22an-il10high','m3z01-ne22an-il10high-x600','m3z01-kd02-pmz1','m3z01-ths8-pmz0','m3z01-ths8-pmz1','m3z01-ths8-pmz1+ext','m3z01-ths8-pmz5','m3z01-ths8-pmz10')
outelements = ('ne','mg','si','s','p','cl','ar')

maxmodelnamechars = max(map(len,modellist))
print "#log epsilon final surface abundances"
print "#modelname".ljust(maxmodelnamechars) + "\t\t" + "\t".join(map(lambda x: x.ljust(5), outelements)) + "\tC/O\tC12/C13" #\tMg24/25\tMg24/26"
for modeldir in modellist:
    with open(modeldir + "/surfabund.dat", 'rb') as txtFile:
        csvReader = csv.reader(txtFile, delimiter=' ', skipinitialspace=True)
        while not " ".join(csvReader.next()).startswith("# Final abundances"):
            pass
        
        outrow = ["!"] * len(outelements)
        for row in csvReader:
            if row[0] in outelements:
                outrow[outelements.index(row[0])] = ("%0.3f" % float(row[2])).ljust(5)
            if row[0:2] == ["#","C/O"]:
                outrow.append("%0.3f" % float(row[3][:-1])) #C/O
                outrow.append("%0.3f" % float(row[6][:-1])) #c12/c13
                #if row[0:2] == ["#","mg24/mg25"]:
                #outrow.append("%0.3f  " % float(row[3][:-1])) #mg24/mg25
                    #outrow.append("%0.3f" % float(row[6])) #mg24/mg26
        print modeldir.ljust(maxmodelnamechars) + "\t\t" + "\t".join(outrow)
