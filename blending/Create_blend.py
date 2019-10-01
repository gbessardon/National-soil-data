
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
import save_tiff as st
import read_config_blending as rcb
import Corsendata as cor
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
    
    return (Xp,Yp,D,xres,yres)
    
    
def Blenddata(dataclay,datasand,dataclayt,datasandt,noref):
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
                
    Clayblend_mask=np.ma.masked_where(Clayblend==noref,Clayblend)
    Sandblend_mask=np.ma.masked_where(Sandblend==noref,Sandblend)
    return (Clayblend_mask,Sandblend_mask)


#read_the_configuration_file
fn='config_blending.cfg'
(Sand_ref,Clay_ref,Sand_nat,Clay_nat,noref,nonat,fnsand,fnclay)=rcb.readconf(fn)



# Get the data    
gdal.UseExceptions() 
(Xrefs,Yrefs,sandref,xresref,yresref)=get_data(Sand_ref,nonat) 
(Xrefc,Yrefc,clayref,xresref,yresref)=get_data(Clay_ref,noref)

(Xnats,Ynats,sandnat,xresnat,yresnat)=get_data(Sand_nat,nonat) 
(Xnatc,Ynatc,claynat,xresnat,yresnat)=get_data(Clay_nat,nonat)

if (xresref!=xresnat) or (yresref!=yresnat):
	sandnat,claynat=cor.Coarsendata(claynat,sandnat,clayref,sandref)


(Clayblend_mask,Sandblend_mask)=Blenddata(clayref,sandref,claynat,sandnat,noref)

st.Savetiff(Clayblend_mask,Xrefc,Yrefc,fnclay,noref) 
st.Savetiff(Sandblend_mask,Xrefs,Yrefs,fnsand,noref)   

