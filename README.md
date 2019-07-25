# National-soil-data

This repository contains all the procedure and the file necessary to the procedure to convert Irish Soil Information System data (http://soils.teagasc.ie) into a SURFEX (https://www.umr-cnrm.fr/surfex/) file input.




To gain computational time it is recommended to use the gdal_translate (https://gdal.org/programs/gdal_translate.html) command:
gdal_translate -a_srs ’+proj=longlat +datum=WGS84 +no_defs’ -projwin -12 60 -2 50 [inputfile.tif] [outputfile.tif
] 
where -12 60 and -2 50 respectively the upper right and lower right points (or the most north-westerly and
south easterly points)
