#!/Users/fengtao/anaconda/bin/python -x
# -*- coding: utf-8 -*-#
''' this is docstring
#=============================================================================================
# PROGRAM      :  decode.py
# USAGE        :  Decode variables in given GRIB2 files and written to MICAPS diamond 4 file
# AUTHOR       :  Tao FENG
# FIRSTWRITTEN :  2016.10.26
# DEPENDENCY   :  numpy pyngl pynio
#=============================================================================================
'''
import os
import sys
import numpy
import Nio
import Ngl

#
#  Open the GRIB file.
#
print "Function：", sys.argv[0]
print "infilenames:"
#
# Func:writemicapsd4
def writemicapsd4(outfilename, varstring, var, lat, lon, date):
    '''Write to ascii file in MICAPS diamond 4 format.

    '''
    print 'Writing file :'+outfilename
    print 'Data :'+varstring
    yr1 = date[0: 4]
    mo1 = date[4: 6]
    dy1 = date[6: 8]
    hr1 = date[8:10]
    nx1 = len(var[0, :])
    ny1 = len(var[:, 0])
    slon = lon[0]
    elon = lon[nx1]
    slat = lat[0]
    elat = lat[ny1]
    dlon = round((elon-slon)/(nx1-1), 2)
    dlat = round((elat-slat)/(ny1-1), 2)
    interval = '1' # need preset
    nstart = '0' # need preset
    nend = '0' # need preset
    ismooth = '0' # need preset
    iheavy = '0' # need preset
    header1 = "diamond 4 " + varstring
    header2 = yr1 + ' ' + mo1 + ' ' + dy1 + ' ' +hr1 + '   0 9999' + '  ' \
            + str(dlon) + ' ' + str(dlat) + ' ' + str(slon) + ' ' + str(elon) \
            + ' ' + str(slat) + ' ' + str(elat) + '  ' +   str(nx1) + ' ' +\
            str(ny1) + ' ' + interval + ' ' + nstart + ' ' + nend + ' ' + \
            ismooth + ' ' + iheavy
    #
    #  Write a subsection of tempa to an ASCII file.
    #
    numpy.set_printoptions(threshold='nan')
    __console__ = sys.stdout
    os.system("/bin/rm -f " + outfilename)
    sys.stdout = open(outfilename, "w")
    print header1
    print header2
    for iii in range(0, nx1):
        for jjj in range(0, ny1):
            print "%8.2f" % (var[iii, jjj])
    sys.stdout = __console__

    #target = open(outfilename, 'w')
    #target.truncate()
    #target.write(header1)
    #target.write('\n')
    #target.write(header2)
    #target.write('\n')
    #print var[0,0]
    #target.write(var[:,:])
    #target.write('\n')
    #target.close()

for i in range(1, len(sys.argv)):
    infilename = sys.argv[i]
    print infilename

    #file = Nio.open_file(os.path.join(Ngl.pynglpath("data"),"grb",infilename),"r")
    infile = Nio.open_file(infilename, "r")

    names = infile.variables.keys()  #  Get the variable names
    print "\nVariable names:"      #  and print them out.
    print names

    for j in range(0, len(names)):
        if names[j] == 'lat_0' or names[j] == 'lon_0':
            continue

        #
        #  For variable in names[1], retrieve and print all attributes
        #  and their values.
        #
        print "\nThe attributes and their values for variable " + names[j] + ":"
        for attrib in infile.variables[names[j]].attributes.keys():
            t = getattr(infile.variables[names[j]], attrib)
            print "Attribute " + "'" + attrib + "' has value:", t

        #
        #  For variable in names[0], retrieve and print the dimension names.
        #
        print "\nFor variable " + names[j] + " the dimension names are:"
        print infile.variables[names[j]].dimensions

        #
        #  Get the variables.
        #

        var = infile.variables[names[j]]
        #name = names[0]
        #print name.split('_')
        varname = names[j].split('_')
        varname1 = varname[0]
        lat = infile.variables['lat_0']
        lon = infile.variables['lon_0']

        filename = infilename.split('_')
        initime = filename[8]
        yr4 = initime[0:4]
        mo2 = initime[4:6]
        dy2 = initime[6:8]
        hr2 = initime[8:10]
        fc3 = str(var.forecast_time)[1]
        outfilename = varname1.lower() +"_"+yr4 + mo2 + dy2 + hr2+"."+fc3.zfill(3)
        varstring = yr4+'年'+mo2+'月'+dy2+'日'+hr2+'时'+varname[0] +' ' + fc3.zfill(3) + '小时预报'

        writemicapsd4(outfilename, varstring, var, lat, lon, initime)

    infile.close()

Ngl.end()
