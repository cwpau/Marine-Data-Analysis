import os,sys

# Select the Study Zone layer
layers = QgsProject.instance().mapLayersByName('Study Zone')
StudyZoneExtent = layers[0].extent()

rootPath = QgsProject.instance().homePath()
TPUMapDirectory = os.path.join(rootPath, 'TPU')

# Get the OZP Boundary within Study Zone
input_param = {'INPUT': TPUMapDirectory+'/2016BC_TPU_SB_VC.gml',
'EXTENT': StudyZoneExtent,
'CLIP': False,
'OUTPUT': TPUMapDirectory+'/TPUSelected.gml'}
result = processing.runAndLoadResults('qgis:extractbyextent', input_param)
