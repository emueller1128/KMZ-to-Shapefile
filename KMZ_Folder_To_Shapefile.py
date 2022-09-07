# Import system modules
import arcpy
import os

# Set workspace (where all the KMLs are)
arcpy.env.workspace = "U:\Reference Materials\GIS\Python_Scripts\Testing\kmz"
arcpy.env.overwriteOutput = True

# Set local variables and location for the consolidated file geodatabase and final shapefile folder
gdb_out_location = "U:\Reference Materials\GIS\Python_Scripts\Testing\gdb"
shp_out_location = "U:\Reference Materials\GIS\Python_Scripts\Testing\shp"

# Convert all KMZ and KML files found in the current workspace
for kmz in arcpy.ListFiles('*.KM*'):
    print("CONVERTING: {0}".format(os.path.join(arcpy.env.workspace, kmz)))
    arcpy.KMLToLayer_conversion(kmz, gdb_out_location)

# Change the workspace to fGDB location
arcpy.env.workspace = gdb_out_location

# Loop through all the FileGeodatabases within the workspace
wks = arcpy.ListWorkspaces('*', 'FileGDB')

for fgdb in wks:  
    # Change the workspace to the current FileGeodatabase
    arcpy.env.workspace = fgdb
    arcpy.env.overwriteOutput = True
    # For every Featureclass inside, copy it to the shapefile folder and use the name 
    # from the original fGDB  
    feature_classes = arcpy.ListFeatureClasses('*', '', 'Placemarks')
    for fc in feature_classes:
        print("COPYING: {} FROM: {}".format(fc, fgdb))
        fcCopy = os.path.join(fgdb, 'Placemarks', fc)
        arcpy.FeatureClassToFeatureClass_conversion(
            fcCopy, shp_out_location, fgdb[fgdb.rfind(os.sep) + 1:-4])
