# -*- coding: utf-8 -*-
"""
Created on Fri May 10 14:16:23 2019

@author: gbessardon
"""


from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import shapefile as shp
from pyproj import Proj

import teagasc_soil_series as tss
import teagasc_asso_to_series as tats

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
#    url = [r[6] for r in records]
#    shape_ex=[sf.shape(i) for i in range(0,len(shps))]
##converting shapefile data into pandas dataframe
#    df = pd.DataFrame(columns=fields, data=records)
#
##assigning the coordinates
#    df = df.assign(coords=shps)
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
    for x in lista:
        if x not in seen:
            uniq.append(x)
            seen.add(x)
    uniq=np.array(uniq)       
    return uniq,seen
    

fn='/home/gbessardon/national_soils/SOIL_SISNationalSoils_shp/Data/SOIL_SISNationalSoils_Shp/SOIL_SISNationalSoils.shp'
#read the shapefile
sf=shp.Reader(fn)    
fields,records,shps,  Association_1,Association_2, asso_unit= read_shapefile(sf)
indices=np.arange(0,50)
#generates a function to convert the prjected data (needs a function to read it in the Readme.txt)
pnyc = Proj(proj='tmerc',ellps='GRS80',lat_0=53.5,lon_0=-8, x_0=200000, y_0=250000, k_0=1.000035)
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
#plt_map_fill(indices,sf,'terrain','map_soil_epa_database.jpg',(40,60) )
uniq,seen=remove_duplicates(asso_unit)
idi=np.where(np.array(Association_1)=='Elton')[0]
idi2=np.where(np.array(Association_2)=='Elton')[0]
#plt_map_fill(idi,sf,plt.cm.jet_r,'test.png')


#get the series corresponding to the association name
fnass='/home/gbessardon/national_soils/get_all_associations.php'
natIDass,placeID,corres_asso=tats.getasso_serie(fnass)            
#get the clay,sand, silt fraction in the series
fseries='/home/gbessardon/national_soils/get_all_series.php'
natID,sand,clay,silt=tss.siltclaysand_series(fseries)

#associate the clay, silt, with place and association
sandass=np.zeros(natIDass.shape)*np.nan
clayass=np.zeros(natIDass.shape)*np.nan
siltass=np.zeros(natIDass.shape)*np.nan
for i,n in enumerate(natIDass):
    indice=np.where(n==natID)[0]
    if len(indice)>0:
        sandass[i]=sand[indice[0]]
        clayass[i]=clay[indice[0]]
        siltass[i]=silt[indice[0]]

clayshp=np.zeros(np.array(asso_unit).shape)*np.nan
sandshp=np.zeros(np.array(asso_unit).shape)*np.nan
siltshp=np.zeros(np.array(asso_unit).shape)*np.nan
for i,c in enumerate(corres_asso):
    ind=np.where(c==np.array(asso_unit))
    clayshp[ind]=clayass[i]
    sandshp[ind]=sandass[i]
    siltshp[ind]=siltass[i]



fig = plt.figure()
ax1=fig.gca()
m = Basemap(projection='tmerc', lon_0=-8, lat_0=53.5,llcrnrlon=-11.7,llcrnrlat=51.1,
            urcrnrlat=55.5,urcrnrlon=-5,resolution='c',ax=ax1)
m.drawcountries()
m.drawcoastlines(linewidth=.5)
m.drawmeridians(np.arange(-10,-6,2),color='k', linewidth=1.0)
m.drawparallels(np.arange(53,56,1),color='k', linewidth=1.0)
colorsmap=plt.get_cmap(plt.cm.afmhot) 
for j,_ in enumerate(Association_2) :
    shape_ex = sf.shape(j)
    x_lon = np.zeros((len(shape_ex.points),1))
    y_lat = np.zeros((len(shape_ex.points),1))
    for ip in range(len(shape_ex.points)):
        x_lon[ip] = shape_ex.points[ip][0]
        y_lat[ip] = shape_ex.points[ip][1]
    lons,lats=pnyc(x_lon,y_lat,inverse=True)
    X,Y=m(lons,lats)
    if not np.isnan(clayshp[j]):
        plt.fill(X,Y,color=colorsmap(int(np.round(2.55*clayshp[j]))))
    else:
        plt.fill(X,Y,color=colorsmap(0))
fig.savefig('teagasc_clay_test.png')    

fig = plt.figure()
ax1=fig.gca()
m = Basemap(projection='tmerc', lon_0=-8, lat_0=53.5,llcrnrlon=-11.7,llcrnrlat=51.1,
            urcrnrlat=55.5,urcrnrlon=-5,resolution='c',ax=ax1)
m.drawcountries()
m.drawcoastlines(linewidth=.5)
m.drawmeridians(np.arange(-10,-6,2),color='k', linewidth=1.0)
m.drawparallels(np.arange(53,56,1),color='k', linewidth=1.0)
colorsmap=plt.get_cmap(plt.cm.afmhot) 
for j,_ in enumerate(Association_2) :
    shape_ex = sf.shape(j)
    x_lon = np.zeros((len(shape_ex.points),1))
    y_lat = np.zeros((len(shape_ex.points),1))
    for ip in range(len(shape_ex.points)):
        x_lon[ip] = shape_ex.points[ip][0]
        y_lat[ip] = shape_ex.points[ip][1]
    lons,lats=pnyc(x_lon,y_lat,inverse=True)
    X,Y=m(lons,lats)
    if not np.isnan(clayshp[j]):
        plt.fill(X,Y,color=colorsmap(int(np.round(2.55*sandshp[j]))))
    else:
        plt.fill(X,Y,color=colorsmap(0))
fig.savefig('teagasc_sand_test.png')  

fig = plt.figure()
ax1=fig.gca()
m = Basemap(projection='tmerc', lon_0=-8, lat_0=53.5,llcrnrlon=-11.7,llcrnrlat=51.1,
            urcrnrlat=55.5,urcrnrlon=-5,resolution='c',ax=ax1)
m.drawcountries()
m.drawcoastlines(linewidth=.5)
m.drawmeridians(np.arange(-10,-6,2),color='k', linewidth=1.0)
m.drawparallels(np.arange(53,56,1),color='k', linewidth=1.0)
colorsmap=plt.get_cmap(plt.cm.afmhot) 
for j,_ in enumerate(Association_2) :
    shape_ex = sf.shape(j)
    x_lon = np.zeros((len(shape_ex.points),1))
    y_lat = np.zeros((len(shape_ex.points),1))
    for ip in range(len(shape_ex.points)):
        x_lon[ip] = shape_ex.points[ip][0]
        y_lat[ip] = shape_ex.points[ip][1]
    lons,lats=pnyc(x_lon,y_lat,inverse=True)
    X,Y=m(lons,lats)
    if not np.isnan(clayshp[j]):
        plt.fill(X,Y,color=colorsmap(int(np.round(2.55*siltshp[j]))))
    else:
        plt.fill(X,Y,color=colorsmap(0))
fig.savefig('teagasc_silt_test.png')  


