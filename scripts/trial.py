
# export PYTHONPATH=/</Applications/QGIS.app>/Contents/Resources/python
import pandas
import os
import csv
from qgis.core import QgsVectorLayer
from qgis import processing
from PyQt5.QtCore import QVariant



#### 1) assume I have generated files from all days betwwen 2021-11-01 and 2021-12-15
#### filename format: 2021-11-11_dropped.csv
# import layer
def step1_import(date):
    param = ["UTF-8", ",","Longitude", "Latitude", "epsg:4326"]
    destination = f"file:///Users/wilsoncwpau/Library/CloudStorage/OneDrive-3vj4cv/QGIS_Marine/data/{date}_dropped.csv?encoding={param[0]}&delimiter={param[1]}&xField={param[2]}&yField={param[3]}&crs={param[4]}"

    # get the reference of the layer tree
    root = QgsProject.instance().layerTreeRoot()
    #find desired group
    mygroup = root.findGroup("data")
    #create layer object
    mylayer = QgsVectorLayer(destination, date, "delimitedtext")
    #add csv data to map
    if not mylayer.isValid():
        print("Failed to load")
    else:
        QgsProject.instance().addMapLayer(mylayer, False)   #False stands for no auto load
        mygroup.addLayer(mylayer)

    ####OK

def step2_topath(date):
    # get the reference of the layer tree
    root = QgsProject.instance().layerTreeRoot()
    #### 2) create path by path to points
    print(date)
    params = {'INPUT':f'delimitedtext://file:///Users/wilsoncwpau/Library/CloudStorage/OneDrive-3vj4cv/QGIS_Marine/data/{date}_dropped.csv?encoding=UTF-8&delimiter=,&xField=Longitude&yField=Latitude&crs=epsg:4326','CLOSE_PATH':False,'ORDER_EXPRESSION':'"Master Update Time"','NATURAL_SORT':False,'GROUP_EXPRESSION':'"overall_tn"','OUTPUT':f'/Users/wilsoncwpau/Library/CloudStorage/OneDrive-3vj4cv/QGIS_Marine/data/paths/{date}_path.gpkg'}
    check = {'INPUT':'delimitedtext://file:///Users/wilsoncwpau/Library/CloudStorage/OneDrive-3vj4cv/QGIS_Marine/data/2021-10-31_dropped.csv?encoding=UTF-8&delimiter=,&xField=Longitude&yField=Latitude&crs=epsg:4326','CLOSE_PATH':False,'ORDER_EXPRESSION':'"Master Update Time"','NATURAL_SORT':False,'GROUP_EXPRESSION':'"overall_tn"','OUTPUT':'/Users/wilsoncwpau/Library/CloudStorage/OneDrive-3vj4cv/QGIS_Marine/data/paths/2021-10-31_path.gpkg'}
    print("parameters are ", params==check)
    print(params)
    print(check)
    processing.run("native:pointstopath", params)

    # path_destination = QgsProject.instance().readPath("./")+f"/data/paths/{date}_path.gpkg|layername={date}_path"
    path_destination = f"/Users/wilsoncwpau/Library/CloudStorage/OneDrive-3vj4cv/QGIS_Marine/data/paths/{date}_path.gpkg|layername={date}_path"
    mygroup = root.findGroup("path")
    mylayer = QgsVectorLayer(path_destination, f"{date}_path", "ogr")
    if not mylayer.isValid():
        print("Failed to load")
    else:
        QgsProject.instance().addMapLayer(mylayer, False)   #False stands for no auto load
        mygroup.addLayer(mylayer)

    ####OK

def step3_joinedpath(date):
    # get the reference of the layer tree
    root = QgsProject.instance().layerTreeRoot()
    #create joined path layer so that attributes are passed to path from points
    #### 3) Join Attributes by field value
    params = {'INPUT':f'/Users/wilsoncwpau/Library/CloudStorage/OneDrive-3vj4cv/QGIS_Marine/data/paths/{date}_path.gpkg|layername={date}_path','FIELD':'overall_tn','INPUT_2':f'delimitedtext://file:///Users/wilsoncwpau/Library/CloudStorage/OneDrive-3vj4cv/QGIS_Marine/data/{date}_dropped.csv?encoding=UTF-8&delimiter=,&xField=Longitude&yField=Latitude&crs=epsg:4326','FIELD_2':'overall_tn',\
    'FIELDS_TO_COPY':['Track ID','Vessel Type Number','Ship Type_Length','Ship Type_Num'],'METHOD':1,'DISCARD_NONMATCHING':False,'PREFIX':'',\
    'OUTPUT':f'/Users/wilsoncwpau/Library/CloudStorage/OneDrive-3vj4cv/QGIS_Marine/data/paths/joined{date}_path.gpkg'}
    processing.run("native:joinattributestable", params)
    print(params)
    path_destination = f"/Users/wilsoncwpau/Library/CloudStorage/OneDrive-3vj4cv/QGIS_Marine/data/paths/joined{date}_path.gpkg|layername=joined{date}_path"
    mygroup = root.findGroup("joined_path")
    mylayer = QgsVectorLayer(path_destination, f"joined{date}_path", "ogr")
    if not mylayer.isValid():
        print("Failed to load")
    else:
        QgsProject.instance().addMapLayer(mylayer, False)   #False stands for no auto load
        mygroup.addLayer(mylayer)


# #### optional 4 styling (NOT OK yet)


# # colorstyle = QgsExpression('if("Ship Type_Length" = "SC", color_rgb(255,255,0), if("Ship Type_Length" = "RTV", color_rgb(0, 255, 0), if("Ship Type_Length" = "LF", color_rgb(0, 0, 255), color_rgb(255, 0, 0))))')
# # single_symbol = mylayer.renderer()
# # symbol = single_symbol.symbol()


# ###ref: https://gis.stackexchange.com/questions/366133/how-to-change-a-line-symbol-layer-type-using-pyqgis

# ### step 1: set line type?
# # We apply the recipe to QgsSingleSymbolRenderer ("Single Symbol")
# simpleMarkerSymbolLayer = QgsSimpleMarkerSymbolLayer()
# simpleMarkerSymbolLayer.setShape(QgsSimpleMarkerSymbolLayer.Arrow)
# property = QgsProperty()
# property.setExpressionString("45 * 2")
# property.setActive(True)
# simpleMarkerSymbolLayer.setDataDefinedProperty(QgsSymbolLayer.PropertyAngle, property)

# ### step 2: set line color?
# propertyColor = QgsProperty()
# propertyColor.setExpressionString('if("Ship Type_Length" = "SC", color_rgb(255,255,0), if("Ship Type_Length" = "RTV", color_rgb(0, 255, 0), if("Ship Type_Length" = "LF", color_rgb(0, 0, 255), color_rgb(255, 0, 0))))')
# propertyColor.setActive(True)
# simpleMarkerSymbolLayer.setDataDefinedProperty(QgsSymbolLayer.PropertyFillColor, propertyColor)

# markerSymbol = QgsMarkerSymbol([simpleMarkerSymbolLayer])
# # markerSymbol.setAngle(90.0) # Commented as we already set dynamically angle from an expression

# markerLineSymbolLayer = QgsMarkerLineSymbolLayer()
# # markerLineSymbolLayer.setColor(propertyColor.asExpression())
# markerLineSymbolLayer.setSubSymbol(markerSymbol)
# lineSymbol = QgsLineSymbol([markerLineSymbolLayer])
# mylayer.renderer().setSymbol(lineSymbol)

# # Convert to rule based renderer ("Single Symbol" to "Rule-based")
# # If not required, just comment below two lines and keep the last line
# newRenderer = QgsRuleBasedRenderer.convertFromRenderer(mylayer.renderer())
# mylayer.setRenderer(newRenderer)

# mylayer.triggerRepaint()

#### 5) import gate1, gate2 and trash to produce the intersections
# get the reference of the layer tree
# path_destination = QgsProject.instance().readPath("./")+f"/data/paths/{date}_path.gpkg|layername={date}_path"
###Do i need to add?
def addgate():
    root = QgsProject.instance().layerTreeRoot()
    for gate in ["Gate1", "Gate2", "GateSTV"]:
        gate_destination = f"/Users/wilsoncwpau/Library/CloudStorage/OneDrive-3vj4cv/QGIS_Marine/{gate}.gpkg|layername={gate}"
        mygroup = root.findGroup("Gates")
        mylayer = QgsVectorLayer(gate_destination, f"{gate}", "ogr")
        if not mylayer.isValid():
            print("Failed to load")
        else:
            QgsProject.instance().addMapLayer(mylayer, False)   #False stands for no auto load
            mygroup.addLayer(mylayer)


####OK 2022-12-16 step1-3, proceed to intersect, 
# applying overlay_nearest to a new field in intersect to get nearest time for gate 1,2

def step4_lineintersect(date, gate):
    # get the reference of the layer tree
    root = QgsProject.instance().layerTreeRoot()
    #create joined path layer so that attributes are passed to path from points
    #### 4) Line intersections
    params = {'INPUT':QgsProcessingFeatureSourceDefinition(f'/Users/wilsoncwpau/Library/CloudStorage/OneDrive-3vj4cv/QGIS_Marine/data/paths/joined{date}_path.gpkg|layername=joined{date}_path', selectedFeaturesOnly=False, featureLimit=-1, flags=QgsProcessingFeatureSourceDefinition.FlagOverrideDefaultGeometryCheck, geometryCheck=QgsFeatureRequest.GeometrySkipInvalid),'INTERSECT':f'/Users/wilsoncwpau/Library/CloudStorage/OneDrive-3vj4cv/QGIS_Marine/{gate}.gpkg|layername={gate}','INPUT_FIELDS':[],'INTERSECT_FIELDS':[],'INTERSECT_FIELDS_PREFIX':'','OUTPUT':f'/Users/wilsoncwpau/Library/CloudStorage/OneDrive-3vj4cv/QGIS_Marine/data/intersects/int_{date}_{gate}.gpkg'}
    
    processing.run("native:lineintersections", params)

    print(params)
    int_destination = f'/Users/wilsoncwpau/Library/CloudStorage/OneDrive-3vj4cv/QGIS_Marine/data/intersects/int_{date}_{gate}.gpkg'
    mygroup = root.findGroup("intersections")
    mylayer = QgsVectorLayer(int_destination, f"int_{date}_{gate}", "ogr")  #input path, name, ogr
    if not mylayer.isValid():
        print("Failed to load")
    else:
        QgsProject.instance().addMapLayer(mylayer, False)   #False stands for no auto load
        mygroup.addLayer(mylayer)

def step5_addexpression(date, gate):
    #get layer
    layername = f'int_{date}_{gate}'
    layer = QgsProject.instance().mapLayersByName(layername)

    if len(layer)==1:
        layer = QgsProject.instance().mapLayersByName(layername)[0]
        #add new field
        layer_provider = layer.dataProvider()
        layer_provider.addAttributes([QgsField("Nearest", QVariant.String)])
        layer.updateFields()
        #idx = layer.IndexFromName('Nearest1111')
        #set up context for excecuting expressions
        context = QgsExpressionContext()
        context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(layer))

        #Expression
        formula = f'array_to_string(overlay_nearest(\'{date}\', expression:="Master Update Time", filter:= "overall_tn" = attribute(\'overall_tn\')))'
        expression = QgsExpression(formula)
        #expression.prepare(layer.pendingFields())

        #calculate new field
        with edit(layer):
            for f in layer.getFeatures():
                context.setFeature(f)
                f["Nearest"] = expression.evaluate(context)
                layer.updateFeature(f)
        print(date, gate, "_Done")
    else:
        print(layername)


# if __name__ == "__main__": #does not work in qgis
#generate a list of days in between the two dates
datelist = pandas.date_range(start='2021-10-31', end='2021-12-15', freq='d').to_list()
datelist = [d.strftime('%Y-%m-%d') for d in datelist]
for date in datelist:
    step1_import(date)

    print(date)
    step2_topath(date)

    step3_joinedpath(date)
addgate()
for date in datelist:
    for gate in ["Gate1", "Gate2", "GateSTV"]:
        step4_lineintersect(date, gate)
        step5_addexpression(date, gate)


#export to CSV; step 5 stopped somewhere in between but still ok

#https://gis.stackexchange.com/questions/373784/exporting-layers-as-csv-files-using-pyqgis
for date in datelist:
    for gate in ["Gate1", "Gate2", "GateSTV"]:

        output_path = f"/Users/wilsoncwpau/Library/CloudStorage/OneDrive-3vj4cv/QGIS_Marine/data/csvs/int_{date}__{gate}.csv"
        layername = f'int_{date}_{gate}'
        layer = QgsProject.instance().mapLayersByName(layername)[0]
        QgsVectorFileWriter.writeAsVectorFormat(layer, output_path, "utf-8", driverName= "CSV", layerOptions = ['GEOMETRY=AS_XYZ'])

###OK DONE
###End of QGIS script