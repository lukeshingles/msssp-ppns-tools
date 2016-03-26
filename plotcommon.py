#!/usr/bin/env python3

import struct

dashesList = [(),(1.5,2,9,2),(5,1),(0.5,2),(4,2)]
dash_capstyleList = ['butt','butt','butt','round','butt']
colorList = ['black',(0,.8*158./255,0.6*115./255),(204./255,121./255,167./255),(213./255,94./255,0.0)]
markersList = ['s','D','o','^','v','*']
linewidth = 1.3
markersize = 4

fruitylabel = 'SCP14'
fruitylinecolor = '0.20' #or 'blue'
fruitydashes = (1,1)
fruitymarker = 'None'
fruitylinewidth = linewidth

VD09label = 'VD09'
VD09linecolor = '0.30' #or 'red'
VD09dashes = (3,1)
VD09marker = 'None'
VD09linewidth = linewidth

#surface abundances colour
abundancecolorlist = ['black',(0.0,0.5,0.7),(0.35,0.7,1.0),(0.9,0.2,0.0),(0.9,0.6,0.0),(0.0,0.6,0.5),(0.8,0.5,1.0)] #(0.95,0.9,0.25)]
#abundancedasheslist = [()]*7
abundancedasheslist = [(),(),(),(6,1),(6,1),(2.5,1),(2.5,1)]

#surface abundances B&W version
#abundancecolorlist = ['black']*4 + ['0.4']*3
#abundancedasheslist = [(),(6,1,0.7,1),(6,1),(3,1)]*2

fs = 9 # font size
fsticklabel = 8

framewidth = 1

columnwidth = 3 # in inches for figsize=(w,h)
textwidth = 6.2

singlefigsize = (columnwidth,columnwidth*0.9)
doublefigsize = (columnwidth,columnwidth*1.7)
triplefigsize = (columnwidth,columnwidth*2)     #mgisotopes, #core mass luminosity
#quadfigsize = (columnwidth,columnwidth*2.5) #core mass luminosity

doublewidefigsize = (textwidth,columnwidth)

def getVariable(filecontent, byteoffset, variablecode):
    startpos = byteoffset + 4 + (variablecode * 4)
    return struct.unpack('<f', filecontent[startpos:startpos+4])[0]
