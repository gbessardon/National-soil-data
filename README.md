# National-soil-data

This repository contains all the procedure and the file necessary to the procedure to convert Irish Soil Information System data (http://soils.teagasc.ie) into a SURFEX (https://www.umr-cnrm.fr/surfex/) file input.

The Irish Soil Information System data are Shapefiles (.shp) containing location of associations of soil from the sampling (or series) collected around Ireland. Unfortunately these Shapefiles do not contain sand and clay fraction however it can be found using other informations available on the 


To gain computational time it is recommended to use the gdal_translate (https://gdal.org/programs/gdal_translate.html) command:
gdal_translate -a_srs ’+proj=longlat +datum=WGS84 +no_defs’ -projwin -12 60 -2 50 [inputfile.tif] [outputfile.tif
] 
where -12 60 and -2 50 respectively the upper right and lower right points (or the most north-westerly and
south easterly points)



Create_blend.py has two functions:
-Corsendata when needed reduce the data of an higher resolution data to a lower res-
olution data. The lower resolution values are defined by the average of all the higher
resolution grid value in the coarser grid box. It assumes that the extent of both datasets
are the same.

Blendata Fills the gap in the national data using the reference dataset to fill the gap
