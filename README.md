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
1. Reduce the size of the reference dataset around the desired area:

To gain computational time it is recommended to use the gdal_translate (https://gdal.org/programs/gdal_translate.html) command:
gdal_translate -a_srs ’+proj=longlat +datum=WGS84 +no_defs’ -projwin -12 60 -2 50 [inputfile] [outputfile.tif] 
where -12 60 and -2 50 respectively the upper right and lower right points (or the most north-westerly and
south easterly points), and store the outputfile.tif file in the input_file directory and run the scripts using it.

2. Download the national dataset 
Choose on of the (.shp) files available in http://soils.teagasc.ie and store it in the input files directory

3. Conversion of the national data to the desired grid:
run the file conversion_national_to_grid/regrid_teagasc_data.py with the parameters set in conversion_national_to_grid/config.cfg.

4. Blend of the national data with the reference dataset:
run the file blending/read_config_blending.py with parameter set in blending/config_blending.cfg.


5. Merge the newly created blend into the new dataset :
gdal_merge.py -o [outputfile] -co COMPRESS=DEFLATE [file1] [file2]}} can merge 2 dataset at different coordinates with [file2] data covering [data1] when they overlap. -co COMPRESS=DEFLATE defines the compression format

6. If needed convert the tif file to dir: 
gdal_translate -of EHdr -ot Byte [input.tif] [output.dir] allows to create the .dir file input for SURFEX. Before running it in SURFEX or HARMONIE the corresponding output.hdr file needs to be created as follow:
one coment line
nodata: 0 
north: [HDR_NORTH]
south: [HDR_SOUTH]
west:  [HDR_WEST]
east:  [HDR_EAST]
rows:  [HDR_ROWS]
cols:  [HDR_COLS]
recordtype: recordtype: integer 8 bits



