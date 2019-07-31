# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 11:01:14 2019

@author: gbessardon
"""

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
from osgeo import gdal



def get_data(fn,maskn):
    
    gdal.UseExceptions()
    ds = gdal.Open(fn)
    data = ds.ReadAsArray()
    gt = ds.GetGeoTransform()
     
    #
    #
    xres = gt[1]
    yres = gt[5]
    #
    xmin = gt[0] 
    ymin = gt[3]
    #
    xmax = gt[0] + (xres * ds.RasterXSize)
    ymax = gt[3] + (yres * ds.RasterYSize) 
#    else:
#        xmax = gt[0] + (xres * ds.RasterXSize) 
#        ymax = gt[3] + (yres * ds.RasterYSize) 
    
 
    X=np.arange(xmin,xmax,xres)
    Y=np.arange(ymin,ymax,yres)
    Xp=X[0:min(data.shape)]
    Yp=Y[0:min(data.shape)]
    if not np.isnan(maskn):
        D=np.ma.masked_where(data==maskn,data)
    else:
        D=np.ma.masked_where(np.where(np.isnan(data)==1),data)
    
    return (Xp,Yp,D)
    
    
    
fnameclay='/home/gbessardon/python_scripts/teagasc/test_clay.tif'
(LATc,LONc,Dc)=get_data(fnameclay,0)  

fnamesand='/home/gbessardon/python_scripts/teagasc/test_sand.tif'
(LATs,LONs,Ds)=get_data(fnamesand,0)   

fig = plt.figure(figsize=(40, 20))
ax1=fig.gca()
m = Basemap(projection='tmerc', lon_0=-8, lat_0=53.5,llcrnrlon=-11.7,llcrnrlat=51.1,
            urcrnrlat=55.5,urcrnrlon=-5,resolution='c',ax=ax1)
#m.drawcountries()
#m.drawcoastlines(linewidth=.5)
m.drawmeridians(np.arange(-10,-6,2),color='k', linewidth=1.0)
m.drawparallels(np.arange(53,56,1),color='k', linewidth=1.0)
Xm,Ym=m(LATs,LONs)
c1=m.pcolormesh(Xm, Ym, Ds, cmap=plt.cm.rainbow,vmin=0,vmax=100)
cb1=m.colorbar(c1)
#cb1.ax.set_ylabel('sand fraction',fontsize=40)
cb1.ax.tick_params(labelsize=25) 
fig.savefig ('teagasc_grid_sand.png',bbox_inches='tight',transparent=True)  
#
##
fig2 = plt.figure(figsize=(40, 20))
ax2=fig2.gca()
m = Basemap(projection='tmerc', lon_0=-8, lat_0=53.5,llcrnrlon=-11.7,llcrnrlat=51.1,
            urcrnrlat=55.5,urcrnrlon=-5,resolution='c',ax=ax2)
#m.drawcountries()
#m.drawcoastlines(linewidth=.5)
m.drawmeridians(np.arange(-10,-6,2),color='k', linewidth=1.0)
m.drawparallels(np.arange(53,56,1),color='k', linewidth=1.0)
Xmc,Ymc=m(LATc,LONc)
c2=m.pcolormesh(Xmc, Ymc, Dc, cmap=plt.cm.rainbow,vmin=0,vmax=100)
cb2=m.colorbar(c2)
#cb2.ax.set_ylabel('clay fraction',fontsize=40)
cb2.ax.tick_params(labelsize=25) 

fig2.savefig ('teagasc_grid_clay.png',bbox_inches='tight',transparent=True) 

#

