# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 09:22:17 2019

@author: gbessardon
"""
def readconf(fn):
    text = open(fn,'r')
    nodata=255
    for t in text:
        if not t.startswith('#'):
            a=t.split('=')
            if len(a)>1:
                if 'Longitude_min' in a[0]:
                    lonmin=float(a[1])
                if 'Latitude_max' in a[0]:
                    latmax=float(a[1])
                if 'Longitude_max' in a[0]:
                    lonmax=float(a[1])
                if 'Latitude_min' in a[0]:
                    latmin=float(a[1]) 
                if  'Pixel_Size' in a[0]:
                    Pix=float(a[1])
                if 'Shapefile_name' in a[0]:
                    Shp_name=a[1].split('\n')[0]
                if 'filename_association' in a[0]:
                    Fasso=a[1].split('\n')[0]
                if 'file_series' in a[0]:
                    Fse=a[1].split('\n')[0]
                if 'proj' in a[0]:
                    projection=a[1]
                if 'ellps' in a[0]:
                    ellipse=a[1].split('\n')[0]                
                if 'lat_0' in a[0]:
                    lat0=float(a[1])
                if 'lon_0' in a[0]:
                    lon0=float(a[1])
                if 'x_0' in a[0]:
                    x0=float(a[1])
                if 'y_0' in a[0]:
                    y0=float(a[1])
                if 'k_0' in a[0]:
                    k0=float(a[1])
                if 'Outsand' in a[0]:
                    fnsand=a[1].split('\n')[0]
                if 'Outclay' in a[0]:
                    fnclay=a[1].split('\n')[0]
                if 'Nodata' in a[0]:
                    nodata=float(a[1])

    return(Shp_name,Fasso,Fse,lonmin,lonmax,latmin,latmax,projection,ellipse,lat0,
           lon0,x0,y0,k0,Pix,fnsand,fnclay,nodata)
