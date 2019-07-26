# -*- coding: utf-8 -*-
"""
Created on Tue May 21 08:46:48 2019

@author: gbessardon
"""

from osgeo import gdal
from osgeo import osr
import numpy as np

def Savetiff(Var,X,Y,fn,nodata):


    #  Initialize the Image Size
    image_size = (len(X),len(Y))
    
    #  Choose some Geographic Transform (Around Lake Tahoe)
    lat = [np.nanmin(Y),np.nanmax(Y)]
    lon = [np.nanmin(X),np.nanmax(X)]
    
    
    # set geotransform
    nx = image_size[0]
    ny = image_size[1]
    xmin, ymin, xmax, ymax = [min(lon), min(lat), max(lon), max(lat)]
    xres = (xmax - xmin) / float(nx)
    yres = (ymax - ymin) / float(ny)
    geotransform = (xmin, xres, 0, ymax, 0, -yres)
    
    # create the 3-band raster file
    dst_ds = gdal.GetDriverByName('GTiff').Create(fn, nx, ny, 1, gdal.GDT_Byte, options = [ 'COMPRESS=DEFLATE' ] )
    
    dst_ds.SetGeoTransform(geotransform)    # specify coords
    srs = osr.SpatialReference()            # establish encoding
    srs.ImportFromEPSG(3857)                # WGS84 lat/long
    dst_ds.SetProjection(srs.ExportToWkt()) # export coords to file
    dst_ds.GetRasterBand(1).WriteArray(Var.astype(np.float32))   # write r-band to the raster
    b = dst_ds.GetRasterBand(1)
    b.SetNoDataValue(nodata)
    #dst_ds.GetRasterBand(2).WriteArray(Clay.astype(np.float32))   # write g-band to the raster
    #dst_ds.GetRasterBand(3).WriteArray(Silt.astype(np.float32))   # write b-band to the raster
    dst_ds.FlushCache()                     # write to disk
    dst_ds = None

    return