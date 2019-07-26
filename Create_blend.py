
# -*- coding: utf-8 -*-
"""
Created on Tue May 21 10:26:20 2019

@author: gbessardon
"""



from osgeo import gdal
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
from pyproj import Proj
from scipy.interpolate import griddata
import multiprocessing as mp
import save_tiff as st

#plt.switch_backend('agg')

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
    
    
def Coarsendata(dataclayt,datasandt,dataclayh,datasandh):
    #"data"-t data from teagasc i.e national database to be coarsed
    #"data"-h data from hswd or the reference database
    # This scripts assume that both spatial extent are the same 
    fa=dataclayt.shape[0]/dataclayh.shape[0]
    # 255 is a random value where the mask is applied
    dataclaytcoarse=255*np.ones(dataclayh.shape)
    datasandtcoarse=255*np.ones(datasandh.shape)
    for i in range(1,dataclayh.shape[0]):
        for j in range(1,dataclayh.shape[1]):
    #        if not np.ma.is_masked(dataclayh[i,j]): #mask the sea by using HWSD masks
                if not np.ma.is_masked(np.ma.mean(dataclayt[i*fa-fa:i*fa+fa,j*fa-fa:j*fa+fa])):
                    #np.ma.mean excludes masked values unlike np.mean
                    dataclaytcoarse[i,j]=np.ma.mean(dataclayt[i*fa-fa:i*fa+fa,j*fa-fa:j*fa+fa]) 
                    datasandtcoarse[i,j]=np.ma.mean(datasandt[i*fa-fa:i*fa+fa,j*fa-fa:j*fa+fa])       
                    
    dataclaytcoarse_m=np.ma.masked_where(dataclaytcoarse==255,dataclaytcoarse)
    datasandtcoarse_m=np.ma.masked_where(datasandtcoarse==255,datasandtcoarse)
    return(dataclaytcoarse_m,datasandtcoarse_m)

def Blenddata(dataclay,datasand,dataclayt,datasandt):
    #"data"-t data from teagasc i.e national database to be coarsed
    #"data"-h data from hswd or the reference database
    Clayblend=255*np.ones(dataclayt.shape)
    Sandblend=255*np.ones(datasandt.shape)
    for i in range(dataclayt.shape[0]):
        for j in range(dataclayt.shape[1]):
            if np.ma.is_masked(dataclayt[i,j]):
                if not np.ma.is_masked(dataclay[i,j]):
                    Clayblend[i,j]=dataclay[i,j]
                    Sandblend[i,j]=datasand[i,j]                    
            else:
                Clayblend[i,j]=dataclayt[i,j]
                Sandblend[i,j]=datasandt[i,j]
                
    Clayblend_mask=np.ma.masked_where(Clayblend==255,Clayblend)
    Sandblend_mask=np.ma.masked_where(Sandblend==255,Sandblend)
    return (Clayblend_mask,Sandblend_mask)



# Get the data    
gdal.UseExceptions()
fname = '/home/gbessardon/SOILGRID/soilgrid_sand_ireland.tif' 
(Xp,Yp,datasand)=get_data(fname,0)
fclay = '/home/gbessardon/SOILGRID/soilgrid_clay_ireland.tif' 
(Xc,Yc,dataclay)=get_data(fclay,0)

fnamet = '/home/gbessardon/python_scripts/teagasc/test_sand.tif' 
(Xpt,Ypt,datasandt)=get_data(fnamet,0)
fclayt = '/home/gbessardon/python_scripts/teagasc/test_clay.tif' 
(Xct,Yct,dataclayt)=get_data(fclayt,0)

(Clayblend_mask,Sandblend_mask)=Blenddata(dataclay,datasand,dataclayt,datasandt)

st.Savetiff(Clayblend_mask,Xc,Yc,'Soilgrid_blend_clay.tif',0) 
st.Savetiff(Sandblend_mask,Xc,Yc,'Soilgrid_blend_sand.tif',0)   
#print('ok1')

print('ok')

fig = plt.figure(figsize=(40, 40))
ax1=fig.add_subplot(131)
m = Basemap(projection='merc',llcrnrlon=np.min(Xc),llcrnrlat=np.min(Yc),
            urcrnrlat=np.max(Yc),urcrnrlon=np.max(Xc),resolution='c',ax=ax1)
m.drawcountries()
m.drawcoastlines(linewidth=.5)
m.drawmeridians(np.arange(-15,-5,2),color='k', linewidth=1.0)
m.drawparallels(np.arange(50,60,1),color='k', linewidth=1.0)
Xm,Ym=m(Xc,Yc)
c1=m.pcolormesh(Xm, Ym, Clayblend_mask, cmap=plt.cm.afmhot,vmin=0,vmax=50)
ax1.set_title('Clay blend Teagasc SOILGRID')

ax2=fig.add_subplot(132)
m = Basemap(projection='merc',llcrnrlon=np.min(Xct),llcrnrlat=np.min(Yct),
            urcrnrlat=np.max(Yct),urcrnrlon=np.max(Xct),resolution='c',ax=ax2)
m.drawcountries()
m.drawcoastlines(linewidth=.5)
m.drawmeridians(np.arange(-15,-5,2),color='k', linewidth=1.0)
m.drawparallels(np.arange(50,60,1),color='k', linewidth=1.0)
Xm,Ym=m(Xct,Yct)
c1=m.pcolormesh(Xm, Ym, dataclayt, cmap=plt.cm.afmhot,vmin=0,vmax=50)
ax2.set_title('Clay Teagasc')


ax3=fig.add_subplot(133)
m = Basemap(projection='merc',llcrnrlon=np.min(Xc),llcrnrlat=np.min(Yc),
            urcrnrlat=np.max(Yc),urcrnrlon=np.max(Xc),resolution='c',ax=ax3)
m.drawcountries()
m.drawcoastlines(linewidth=.5)
m.drawmeridians(np.arange(-15,-5,2),color='k', linewidth=1.0)
m.drawparallels(np.arange(50,60,1),color='k', linewidth=1.0)
Xm,Ym=m(Xc,Yc)
c1=m.pcolormesh(Xm, Ym, dataclay, cmap=plt.cm.afmhot,vmin=0,vmax=50)
ax3.set_title('Clay SOILGRID')
#
fig.savefig('Blend_SOILGRID_teagasc.png')



fnameh = '/home/gbessardon/HWSD_v2/SAND_HWSD_v2_Ireland.tif' 
(Xph,Yph,datasandh)=get_data(fnameh,255)
fclayh = '/home/gbessardon/HWSD_v2/CLAY_HWSD_v2_Ireland.tif' 
(Xch,Ych,dataclayh)=get_data(fclayh,255)


dataclaytcoarse_m,datasandtcoarse_m=Coarsendata(dataclayt,datasandt,dataclayh,datasandh)
(Clayblend_mask2,Sandblend_mask2)=Blenddata(dataclayh,datasandh,dataclaytcoarse_m,datasandtcoarse_m)

fig = plt.figure(figsize=(40, 40))
ax1=fig.add_subplot(131)
m = Basemap(projection='merc',llcrnrlon=np.min(Xch),llcrnrlat=np.min(Ych),
            urcrnrlat=np.max(Ych),urcrnrlon=np.max(Xch),resolution='c',ax=ax1)
m.drawcountries()
m.drawcoastlines(linewidth=.5)
m.drawmeridians(np.arange(-15,-5,2),color='k', linewidth=1.0)
m.drawparallels(np.arange(50,60,1),color='k', linewidth=1.0)
Xm,Ym=m(Xch,Ych)
c1=m.pcolormesh(Xm, Ym, Clayblend_mask2, cmap=plt.cm.afmhot,vmin=0,vmax=50)
ax1.set_title('Clay blend Teagasc coarse HWSD')
#
#
ax2=fig.add_subplot(132)
m = Basemap(projection='merc',llcrnrlon=np.min(Xch),llcrnrlat=np.min(Ych),
            urcrnrlat=np.max(Ych),urcrnrlon=np.max(Xch),resolution='c',ax=ax2)
m.drawcountries()
m.drawcoastlines(linewidth=.5)
m.drawmeridians(np.arange(-15,-5,2),color='k', linewidth=1.0)
m.drawparallels(np.arange(50,60,1),color='k', linewidth=1.0)
Xm,Ym=m(Xch,Ych)
c1=m.pcolormesh(Xm, Ym, dataclaytcoarse_m, cmap=plt.cm.afmhot,vmin=0,vmax=50)
ax2.set_title('Clay Teagasc coarse')


ax3=fig.add_subplot(133)
m = Basemap(projection='merc',llcrnrlon=np.min(Xch),llcrnrlat=np.min(Ych),
            urcrnrlat=np.max(Ych),urcrnrlon=np.max(Xch),resolution='c',ax=ax3)
m.drawcountries()
m.drawcoastlines(linewidth=.5)
m.drawmeridians(np.arange(-15,-5,2),color='k', linewidth=1.0)
m.drawparallels(np.arange(50,60,1),color='k', linewidth=1.0)
Xm,Ym=m(Xch,Ych)
c1=m.pcolormesh(Xm, Ym, dataclayh, cmap=plt.cm.afmhot,vmin=0,vmax=50)
ax3.set_title('Clay HWSD')

fig.savefig('Blend_HWSD_teagasc.png')

st.Savetiff(Clayblend_mask2,Xch,Ych,'HWSD_blend_clay_test.tif',255) 
st.Savetiff(Sandblend_mask2,Xch,Ych,'HWSD_blend_sand_test.tif',255)

