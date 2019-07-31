# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 13:28:24 2019

@author: gbessardon
"""
from osgeo import gdal
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np


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
    
gdal.UseExceptions()
fname = '/home/gbessardon/SOILGRID/soilgrid_sand_ireland.tif' 
(Xs,Ys,datasand)=get_data(fname,0)
fclay = '/home/gbessardon/SOILGRID/soilgrid_clay_ireland.tif' 
(Xc,Yc,dataclay)=get_data(fclay,0)


fnbc='/home/gbessardon/python_scripts/teagasc/Soilgrid_blend_clay.tif'
(Xbc,Ybc,databc)=get_data(fnbc,255)
fnbs='/home/gbessardon/python_scripts/teagasc/Soilgrid_blend_sand.tif'
(Xbs,Ybs,databs)=get_data(fnbs,255)

fig = plt.figure(figsize=(40, 20))
ax1=fig.gca()
m = Basemap(projection='tmerc', lon_0=-8, lat_0=53.5,llcrnrlon=-11.7,llcrnrlat=51.1,
            urcrnrlat=55.5,urcrnrlon=-5,resolution='c',ax=ax1)
m.drawmeridians(np.arange(-15,-5,2),color='k', linewidth=1.0)
m.drawparallels(np.arange(50,60,1),color='k', linewidth=1.0)
Xm,Ym=m(Xc,Yc)
c1=m.pcolormesh(Xm, Ym, databc, cmap=plt.cm.rainbow,vmin=0,vmax=100)
cb1=m.colorbar(c1)
cb1.ax.tick_params(labelsize=25) 
fig.savefig ('teagasc_blend_clay.png',bbox_inches='tight',transparent=True)  

fig2 = plt.figure(figsize=(40, 20))
ax2=fig2.gca()
m = Basemap(projection='tmerc', lon_0=-8, lat_0=53.5,llcrnrlon=-11.7,llcrnrlat=51.1,
            urcrnrlat=55.5,urcrnrlon=-5,resolution='c',ax=ax2)

m.drawmeridians(np.arange(-15,-5,2),color='k', linewidth=1.0)
m.drawparallels(np.arange(50,60,1),color='k', linewidth=1.0)
Xm,Ym=m(Xc,Yc)
c2=m.pcolormesh(Xm, Ym, dataclay, cmap=plt.cm.rainbow,vmin=0,vmax=100)
cb2=m.colorbar(c2)
cb2.ax.tick_params(labelsize=25)
fig2.savefig('Soilgrid_clay_rainbow.png',bbox_inches='tight',transparent=True)


fig3 = plt.figure(figsize=(40, 20))
ax3=fig3.gca()
m = Basemap(projection='tmerc', lon_0=-8, lat_0=53.5,llcrnrlon=-11.7,llcrnrlat=51.1,
            urcrnrlat=55.5,urcrnrlon=-5,resolution='c',ax=ax3)
m.drawmeridians(np.arange(-15,-5,2),color='k', linewidth=1.0)
m.drawparallels(np.arange(50,60,1),color='k', linewidth=1.0)
Xm,Ym=m(Xs,Ys)
c3=m.pcolormesh(Xm, Ym, databs, cmap=plt.cm.rainbow,vmin=0,vmax=100)
cb3=m.colorbar(c3)
cb3.ax.tick_params(labelsize=25) 
fig3.savefig ('teagasc_blend_sand.png',bbox_inches='tight',transparent=True)  

fig4 = plt.figure(figsize=(40, 20))
ax4=fig4.gca()
m = Basemap(projection='tmerc', lon_0=-8, lat_0=53.5,llcrnrlon=-11.7,llcrnrlat=51.1,
            urcrnrlat=55.5,urcrnrlon=-5,resolution='c',ax=ax4)

m.drawmeridians(np.arange(-15,-5,2),color='k', linewidth=1.0)
m.drawparallels(np.arange(50,60,1),color='k', linewidth=1.0)
Xm,Ym=m(Xs,Ys)
c4=m.pcolormesh(Xm, Ym, datasand, cmap=plt.cm.rainbow,vmin=0,vmax=100)
cb4=m.colorbar(c4)
cb4.ax.tick_params(labelsize=25)
fig4.savefig('Soilgrid_sand_rainbow.png',bbox_inches='tight',transparent=True)



