# -*- coding: utf-8 -*-
"""
Created on Mon May 13 09:46:38 2019

@author: gbessardon
"""
import requests
import numpy as np
def getnatID(fn):
# open the series file and save the lines only containing live soil datasets

    lista=open(fn,'r')  
    saveline=[]
    for l in lista:
        h=l.split('}')
        for line in h:
            if 'LIVE' in line:
                saveline.append(line)
#            saveline.append(line)
                
    # split the lines to get the national ID identifiers
    natID=[]
    for s in saveline:
        h=s.split(',')
        temporary=h[1].split(':')
        natID.append(temporary[1][1:len(temporary[1])-1])
        
    return (natID)
    
    
def remove_duplicates(lista):
    seen = set()
    uniq = []
    ind=[]
    for i,x in enumerate(lista):
        if x not in seen:
            uniq.append(x)
            seen.add(x)
            ind.append(i)
    uniq=np.array(uniq)
    ind=np.array(ind)       
    return uniq,seen,ind
    

#
def weightedsoilavg0100(depthup,depthdown,values,maxidepth):
    weigthedavg=np.nan  
#    print('Allen')
    if len(depthup)>0:       
        uniq,seen,ind=remove_duplicates(depthup)        
        sumi=0
        totalthickness=0
        UP=np.array(depthup)[ind]
        DOWN=np.array(depthdown)[ind]
        VAR=np.array(values)[ind]
        if len(UP)>1:
            if max(DOWN)>maxidepth:
                maxind=np.min(np.where(np.array(DOWN)>=maxidepth))+1
            else:
                maxind=len(DOWN)
            totalthickness=0
            for i in np.arange(0,maxind):
                if i==0:
                    thickness=DOWN[i]-UP[i]
                    variable=VAR[i+1]+VAR[i]
                else:
                    if i==maxind-1:
                        if DOWN[i]<=maxidepth: 
                                thickness=DOWN[i]-UP[i]
                                variable=2*VAR[i]
                        else: 
                                thickness=maxidepth-UP[i]
                                variable=2*VAR[i]
                    else:
                        if DOWN[i]<=maxidepth: 
                                thickness=DOWN[i]-UP[i]
                                variable=VAR[i+1]+VAR[i]
                        else: 
                                thickness=maxidepth-UP[i]
                                variable=2*VAR[i]   
                totalthickness=totalthickness+thickness
                sumi=sumi+(variable*thickness) 
        else:
            totalthickness=maxidepth-UP[0]
            variable=2*VAR[0]
            sumi=sumi+(variable*totalthickness)
        b=totalthickness
        a=0
        weigthedavg=sumi/(2.0*(b-a))

    return (weigthedavg)
#        

    

def siltclaysand_series(fnass):
    natID=getnatID(fnass)
    maxidepth=100.0
    sandid=[]
    siltid=[]
    clayid=[]  
    #open the series files and get the different layer data 
    for n in natID:
            url='http://gis.teagasc.ie/soils/get_series_full.php?series_code='+n

            r = requests.get(url)
            f=r.content   
            h=f.split('{')
            temp=h[1:len(h)]
            depthup=[]
            depthdown=[]
            sandlayer=[]
            claylayer=[]
            siltlayer=[]
    #divide the teagasc file in smaller chuncks to get the depths
            if len(temp)>1:
               for t in temp:
                   if "DepthTo" in t:
                       for tt in t.split(','):
                           if  ("Depth" in tt.split(':')[0]) and ("To" not in tt.split(':')[0]):
                               if not tt.split(':')[1]=='null':
                                    depthup.append(float(tt.split(':')[1]))
                               else:
                                    depthup.append(maxidepth+10)
                           if "DepthTo" in tt.split(':')[0]:
                               if not tt.split(':')[1]=='null':
                                    depthdown.append(float(tt.split(':')[1]))
                               else:
                                    depthdown.append(maxidepth+10)
                           if "Sand" in tt.split(':')[0]:
                               if not tt.split(':')[1]=='null':
                                    sandlayer.append(float(tt.split(':')[1]))
                               else:
                                    sandlayer.append(0.0)
                           if "Clay" in tt.split(':')[0]:
                               if not tt.split(':')[1]=='null':
                                    claylayer.append(float(tt.split(':')[1]))
                               else:
                                    claylayer.append(0.0)
                           if "Silt" in tt.split(':')[0]:
                                if not tt.split(':')[1]=='null':
                                    siltlayer.append(float(tt.split(':')[1]))  
                                else:
                                    siltlayer.append(0.0)
            sand=weightedsoilavg0100(depthup,depthdown,sandlayer,maxidepth)
            clay=weightedsoilavg0100(depthup,depthdown,claylayer,maxidepth)
            silt=weightedsoilavg0100(depthup,depthdown,siltlayer,maxidepth)
            sandid.append(sand)
            clayid.append(clay)
            siltid.append(silt)

        
    return(np.array(natID),np.array(sandid),np.array(clayid),np.array(siltid))
