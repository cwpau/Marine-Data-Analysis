import os
import glob
import processing
from qgis.core import QgsProject
from os.path import dirname
from os.path import basename

rootPath = QgsProject.instance().homePath()
OZPMapDirectory = os.path.join(rootPath, 'OZPs')
print('Base Folder: ' + OZPMapDirectory)

# Load all gml
layernames_list = glob.glob(OZPMapDirectory + '/**/Plan GIS Data GML/PLAN_SCHEME_AREA.gml', recursive=True)
    
print(layernames_list)
input_param = { 'CRS' : QgsCoordinateReferenceSystem('EPSG:2326'), 
'LAYERS' : layernames_list, 
'OUTPUT' : 'TEMPORARY_OUTPUT' }

processing.runAndLoadResults('qgis:mergevectorlayers', input_param)


