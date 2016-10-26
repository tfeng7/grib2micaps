#!/Users/fengtao/anaconda/bin/python -x
# -*- coding: utf-8 -*-#
#=============================================================================================
# PROGRAM      :  decode.py
# USAGE        :  Decode variables in given GRIB2 files and written to MICAPS diamond 4 file
# AUTHOR       :  Tao FENG
# FIRSTWRITTEN :  2016.10.26
# DEPENDENCY   :  numpy pyngl pynio
#=============================================================================================
import numpy,types,os,sys 
import Nio,Ngl

#
#  Open the GRIB file.
#
#infilename = "/Users/fengtao/Working/DMDM/Z_NWGD_C_BABJ_20160922010326_P_RFFC_SCMOC-TMIN_201609220800_00000.GRB2"
print "Function：", sys.argv[0]
print "infilenames:"
#
# Func:writemicapsd4
def writemicapsd4(outfilename,varstring,var,lat,lon,date):
    '''Write to ascii file in MICAPS diamond 4 format.
    
    '''
    print 'Writing file :'+outfilename
    print 'Data :'+varstring
    yr4   = date[0: 4]
    mo2   = date[4: 6]
    dy2   = date[6: 8]
    hr2   = date[8:10]
    nx    = len(var[0,:])
    ny    = len(var[:,0])
    slon    = lon[0]
    elon    = lon[nx]
    slat    = lat[0]
    elat    = lat[ny]
    dlon    = round((elon-slon)/(nx-1),2)
    dlat    = round((elat-slat)/(ny-1),2)
    interval= '1' # need preset
    nstart  = '0' # need preset
    nend    = '0' # need preset
    ismooth = '0' # need preset
    iheavy  = '0' # need preset
    header1 = "diamond 4 " + varstring
    header2 = yr4 + ' ' + mo2 + ' ' + dy2 + ' ' +hr2 + '   0 9999' + '  ' + str(dlon) + ' ' + str(dlat) + ' ' + str(slon) + ' ' + str(elon) + ' ' + str(slat) + ' ' + str(elat) + '  ' +   str(nx) + ' ' +   str(ny) + ' ' + interval + ' ' + nstart + ' ' + nend + ' ' + ismooth + ' ' + iheavy
    #
    #  Write a subsection of tempa to an ASCII file.
    #
    numpy.set_printoptions(threshold='nan')
    __console__=sys.stdout
    os.system("/bin/rm -f " + outfilename)
    sys.stdout = open(outfilename,"w")
    print header1
    print header2
    for i in range(0,nx):
        for j in range(0,ny):
            print "%8.2f" % (var[i,j])
    sys.stdout =__console__

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
    infilename=sys.argv[i]
    print infilename

    #file = Nio.open_file(os.path.join(Ngl.pynglpath("data"),"grb",infilename),"r")
    file = Nio.open_file(infilename,"r")
    
    names = file.variables.keys()  #  Get the variable names
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
        for attrib in file.variables[names[j]].attributes.keys():
            t = getattr(file.variables[names[j]],attrib)
            print "Attribute " + "'" + attrib + "' has value:", t
        
        #
        #  For variable in names[0], retrieve and print the dimension names.
        #
        print "\nFor variable " + names[j] + " the dimension names are:"
        print file.variables[names[j]].dimensions
        
        #
        #  Get the variables.
        #
        
        var = file.variables[names[j]]
        #name = names[0]
        #print name.split('_')
        varname = names[j].split('_') 
        varname1= varname[0]
        lat = file.variables['lat_0']
        lon = file.variables['lon_0']
    
        filename= infilename.split('_') 
        initime = filename[8]
        yr4=initime[0:4]
        mo2=initime[4:6]
        dy2=initime[6:8]
        hr2=initime[8:10]
        fc3=str(var.forecast_time)[1]
        outfilename= varname1.lower() +"_"+yr4 + mo2 + dy2 + hr2+"."+fc3.zfill(3)
        varstring =  yr4+'年'+mo2+'月'+dy2+'日'+hr2+'时'+varname[0] +' ' + fc3.zfill(3) + '小时预报'
        
        writemicapsd4(outfilename,varstring,var,lat,lon,initime)
    
    file.close()
        
Ngl.end()
