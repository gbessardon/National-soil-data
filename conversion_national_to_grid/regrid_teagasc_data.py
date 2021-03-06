# -*- coding: utf-8 -*-
"""
Created on Thu May 16 09:33:08 2019

@author: gbessardon
"""


import numpy as np
import shapefile as shp
from pyproj import Proj
import sys

import teagasc_soil_series as tss
import teagasc_asso_to_series as tats
import save_tiff as st
import read_config as config

def get_filepaths(directory,string):
    file_paths = []  # List which will store all of the full filepaths.
    for root, directories, files in os.walk(directory):
        for filename in files:
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            if string in filepath:
                file_paths.append(filepath)  # Add it to the list.

    return file_paths

def read_shapefile(sf):
    #fetching the headings from the shape file
    fields = [x[0] for x in sf.fields][1:]

#fetching the records from the shape file
    records = [list(i) for i in sf.records()]
    shps = [s.points for s in sf.shapes()]
    asso_unit = [r[1] for r in records]
    Association_1 = [r[2] for r in records]
    Association_2= [r[3] for r in records]

    return fields,records,shps, Association_1,Association_2, asso_unit
    


def plt_map_fill(idi,sf,cmapname,figname) :
    fig = plt.figure()
    ax1=fig.gca()
    m = Basemap(projection='tmerc', lon_0=-8, lat_0=53.5,llcrnrlon=-11.7,llcrnrlat=51.1,
                urcrnrlat=55.5,urcrnrlon=-5,resolution='f',ax=ax1)
    m.drawcountries()
    m.drawcoastlines(linewidth=.5)
    m.drawmeridians(np.arange(-10,-6,2),color='k', linewidth=1.0)
    m.drawparallels(np.arange(53,56,1),color='k', linewidth=1.0)
    colorsmap=plt.get_cmap(cmapname,len(idi)) 
    for j,i in enumerate(idi) :
        shape_ex = sf.shape(i)
        x_lon = np.zeros((len(shape_ex.points),1))
        y_lat = np.zeros((len(shape_ex.points),1))
        for ip in range(len(shape_ex.points)):
            x_lon[ip] = shape_ex.points[ip][0]
            y_lat[ip] = shape_ex.points[ip][1]
        lons,lats=pnyc(x_lon,y_lat,inverse=True)
        X,Y=m(lons,lats)
        plt.fill(X,Y,color=colorsmap(j))
    plt.savefig(figname)    
    return
    
    
def remove_duplicates(lista):
    seen = set()
    uniq = []
    ind=[]
    for i,x in enumerate(lista):
        if x not in seen:
            uniq.append(x)
            seen.add(x)
            ind.append(i)            
            
            #uniq=np.array(uniq)       
    return uniq,seen,ind
    

    
def putonthegrid(x_ind,y_ind,var,Val):
    #x_ind, y_ind values of the closest indices 
    #var the associated variable at the given points 
    #Val the gridded variable
    #look for unique x_ind values
    uniqx,seenx,idx=remove_duplicates(x_ind)
    for ux in uniqx:
        #looking for uniq corresponding y values
        tempx=np.where(ux==x_ind)[0]
        coresy=y_ind[tempx]
        uniqy,seenx,idx=remove_duplicates(coresy)
        for uy in uniqy:
            if np.isnan(Val[ux,uy]):
                Val[ux,uy]=var
            else:
                oldval=Val[ux,uy]
                A=np.array([oldval,var])
                if len(A[~np.isnan(A)])>0:
                    Val[ux,uy]=np.mean(A[~np.isnan(A)])
    
    return(Val)
    
def generate_grid(lonmin,lonmax,latmin,latmax,Pix):
    Upper_Left = np.array([lonmin,latmax])
    Lower_Right= np.array([lonmax,latmin])
    Pixel_Size = np.array([Pix,-Pix])

    xres = Pixel_Size[0]    
    yres = Pixel_Size[1]

    xmin = Upper_Left[0] 
    ymin = Lower_Right[1]


    xmax = Lower_Right[0] 
    ymax = Upper_Left[1]

    if xres>0:
        X=np.arange(xmin,xmax,xres)
    else:
        X=np.arange(xmax,xmin,xres)
    
    if yres<0:
        Y=np.arange(ymax,ymin,yres)
    else:
        Y=np.arange(ymin,ymax,yres)
        
    return(X,Y)





#########################MAIN##################################################

fn='config.cfg'
(Shp_name,Fasso,Fse,lonmin,lonmax,latmin,latmax,projection,ellipse,lat0,lon0,
 x0,y0,k0,Pix,fnsand,fnclay,nodata)=config.readconf(fn)

#check configuration
if lonmin>=lonmax:
    sys.exit("ERROR min longitude>= max longitude")
if latmin>=latmax:
    sys.exit("ERROR min latgitude>= max latgitude")

#read the shapefile
sf=shp.Reader(Shp_name)    
fields,records,shps,  Association_1,Association_2, asso_unit= read_shapefile(sf)
#generates a function to convert the prjected data (needs a function to read it in the Readme.txt)
pnyc = Proj(proj=projection,ellps=ellipse,lat_0=lat0,lon_0=lon0, x_0=x0, y_0=y0, k_0=k0)
#+a 	Semimajor radius of the ellipsoid axis
#+axis 	Axis orientation
#+b 	Semiminor radius of the ellipsoid axis
#+ellps 	Ellipsoid name (see proj -le)
#+k 	Scaling factor (deprecated)
#+k_0 	Scaling factor
#+lat_0 	Latitude of origin
#+lon_0 	Central meridian
#+lon_wrap 	Center longitude to use for wrapping (see below)
#+over 	Allow longitude output outside -180 to 180 range, disables wrapping (see below)
#+pm 	Alternate prime meridian (typically a city name, see below)
#+proj 	Projection name (see proj -l)
#+units 	meters, US survey feet, etc.
#+vunits 	vertical units.
#+x_0 	False easting
#+y_0 	False northing



#get the series corresponding to the association name
natIDass,placeID,corres_asso=tats.getasso_serie(Fasso)            
#get the clay,sand, silt fraction in the series
natID,sand,clay,silt=tss.siltclaysand_series(Fse)

#associate the clay, silt, with place and association
sandass=np.zeros(natIDass.shape)*np.nan
clayass=np.zeros(natIDass.shape)*np.nan
#siltass=np.zeros(natIDass.shape)*np.nan
for i,n in enumerate(natIDass):
    indice=np.where(n==natID)[0]
    if len(indice)>0:
        sandass[i]=sand[indice[0]]
        clayass[i]=clay[indice[0]]
#        siltass[i]=silt[indice[0]]
clayshp=np.zeros(np.array(asso_unit).shape)*np.nan
sandshp=np.zeros(np.array(asso_unit).shape)*np.nan
#siltshp=np.zeros(np.array(asso_unit).shape)*np.nan
for i,c in enumerate(corres_asso):
    ind=np.where(c==np.array(asso_unit))
    clayshp[ind]=clayass[i]
    sandshp[ind]=sandass[i]


###############################################################################
#################### REGRID POINTS ############################################
###############################################################################


(X,Y)=generate_grid(lonmin,lonmax,latmin,latmax,Pix)

Sand=np.zeros((X.shape[0],Y.shape[0]))*np.nan    
Clay=np.zeros((X.shape[0],Y.shape[0]))*np.nan  
for j,_ in enumerate(Association_2) :
    shape_ex = sf.shape(j)
    x_lon = np.zeros(len(shape_ex.points))
    y_lat = np.zeros(len(shape_ex.points))
    for ip in range(len(shape_ex.points)):
        x_lon[ip] = shape_ex.points[ip][0]
        y_lat[ip] = shape_ex.points[ip][1]
    lons,lats=pnyc(x_lon,y_lat,inverse=True)
    x_ind = np.zeros(len(shape_ex.points))
    y_ind = np.zeros(len(shape_ex.points))
    #search for the closest value to find in the grid        
    for k,l in enumerate(lons):
        x_ind[k]=int(np.argmin(np.abs(l-X)))
        y_ind[k]=int(np.argmin(np.abs(lats[k]-Y)))    
    
    Sand=putonthegrid(x_ind,y_ind,sandshp[j],Sand)
    Clay=putonthegrid(x_ind,y_ind,clayshp[j],Clay)
    
st.Savetiff(Sand.T,X,Y,fnsand,nodata)
st.Savetiff(Clay.T,X,Y,fnclay,nodata)


                
        
        
