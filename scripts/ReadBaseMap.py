import os
import glob
from qgis.core import QgsProject
from os.path import dirname
from os.path import basename

rootPath = QgsProject.instance().homePath()
BaseMapDirectory = os.path.join(rootPath, 'BaseMap')

# Load Spot Height
for filename in glob.glob(BaseMapDirectory + '/**/Layers/Relief/SpotHeight.gml', recursive=True):
    layername =  basename(dirname(dirname(dirname(filename)))) + ' SpotHeight'
    iface.addVectorLayer(filename, os.path.basename(layername), "ogr")

# Load Contour
for filename in glob.glob(BaseMapDirectory + '/**/Layers/Relief/Contour.gml', recursive=True):
    layername =  basename(dirname(dirname(dirname(filename)))) + ' Contour'
    iface.addVectorLayer(filename, os.path.basename(layername), "ogr")

# Load Contour
for filename in glob.glob(BaseMapDirectory + '/**/Layers/Relief/BMSslope*.gml', recursive=True):
    layername =  basename(dirname(dirname(dirname(filename)))) + ' BMSslope'
    iface.addVectorLayer(filename, os.path.basename(layername), "ogr")

# Load Building
for filename in glob.glob(BaseMapDirectory + '/**/Layers/Buildings/Building.gml', recursive=True):
    layername =  basename(dirname(dirname(dirname(filename)))) + ' Building'
    iface.addVectorLayer(filename, os.path.basename(layername), "ogr")
    
# Load Building Structure Polygon
for filename in glob.glob(BaseMapDirectory + '/**/Layers/Buildings/BuiltStructurePolygon.gml', recursive=True):
    layername =  basename(dirname(dirname(dirname(filename)))) + ' BuiltStructurePolygon'
    iface.addVectorLayer(filename, os.path.basename(layername), "ogr")
    
# Load Pedestrian shape Line
for filename in glob.glob(BaseMapDirectory + '/**/Layers/Transportation/CartoPedLine.gml', recursive=True):
    layername =  basename(dirname(dirname(dirname(filename)))) + ' CartoPedLine'
    iface.addVectorLayer(filename, os.path.basename(layername), "ogr")

# Load Transportation shape Line
for filename in glob.glob(BaseMapDirectory + '/**/Layers/Transportation/CartoTransLine.gml', recursive=True):
    layername =  basename(dirname(dirname(dirname(filename)))) + ' CartoTransLine'
    iface.addVectorLayer(filename, os.path.basename(layername), "ogr")
    
# Load Street Center Line
for filename in glob.glob(BaseMapDirectory + '/**/Layers/Transportation/StreetCenterLines.gml', recursive=True):
    layername =  basename(dirname(dirname(dirname(filename)))) + ' StreetCenterLines'
    iface.addVectorLayer(filename, os.path.basename(layername), "ogr")

# Load Transport Polygon
for filename in glob.glob(BaseMapDirectory + '/**/Layers/Transportation/TransportPolygon.gml', recursive=True):
    layername =  basename(dirname(dirname(dirname(filename)))) + ' TransportPolygon'
    iface.addVectorLayer(filename, os.path.basename(layername), "ogr")