__author__ = 'sean.mcfall'

# test to create a table/feature layer through arcpy

import arcpy
arcpy.env.overwriteOutput = 1
arcpy.env.workspace = "in_memory"

rivers = "C:\\Users\\Sean.McFall\\Documents\\SH\\Washington\\wa_rivers_UnsplitLine.shp"

# fclass = "C:/Data/Municipal.gdb/Hospitals"
# fieldnames = [f.name for f in arcpy.ListFields(fclass)]

fieldnames = [f.name for f in arcpy.ListFields(rivers)]

print fieldnames