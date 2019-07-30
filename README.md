# National-soil-data

This repository contains all the procedure and the file necessary to the procedure to convert Irish Soil Information System data (http://soils.teagasc.ie) into a SURFEX (https://www.umr-cnrm.fr/surfex/) file input.


# Requirements


numpy
shapefile
pyproj
sys
osgeo
matplotlib
mpl_toolkits

# Description


The Irish Soil Information System data are Shapefiles (.shp) containing location of associations of soil from the sampling (or series) collected around Ireland. Unfortunately these Shapefiles do not contain sand and clay fraction however it can be found using other informations available on the Irish Soil Information System website (http://soils.teagasc.ie)


The repository is divided in 4 different subfolders:
- *input_files*: contains get_all_associations.php and get_all_series specific files from the teagasc dataset and it is recommended to set the teagasc file and the reference dataset here
- *conversion_national_to_grid*: contains all the scripts used to convert the national dataset to the desired grid
- *blending*: contains all the scripts necessary to blend the national dataset with a reference dataset
- *plots*: contains different scripts to plot the data at different stages

 # How to use it
1. Reduce the size of your the international dataset around the desired area:

To gain computational time it is recommended to use the gdal_translate (https://gdal.org/programs/gdal_translate.html) command:
gdal_translate -a_srs ’+proj=longlat +datum=WGS84 +no_defs’ -projwin -12 60 -2 50 [inputfile] [outputfile.tif] 
where -12 60 and -2 50 respectively the upper right and lower right points (or the most north-westerly and
south easterly points), and store the outputfile.tif file in the input_file directory and run the scripts using it.

2. Conversion of the national data to the desired grid:


3. Blend of the national data with the reference dataset:
Here we simply fill the national dataset gap using the national dataset

Create_blend.py has two functions:
-Corsendata when needed reduce the data of an higher resolution data to a lower res-
olution data. The lower resolution values are defined by the average of all the higher
resolution grid value in the coarser grid box. It assumes that the extent of both datasets
are the same.

Blendata Fills the gap in the national data using the reference dataset to fill the gap

4. 



