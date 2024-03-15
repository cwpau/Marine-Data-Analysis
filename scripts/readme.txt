1) Database preparation with pure python and mysql codes:
    i) /Users/wilsoncwpau/Library/CloudStorage/OneDrive-3vj4cv/PycharmProjects/Marine_NimWanRoad/datacleaning.py-> cleaned_XXXX.csv

    ii) /Users/wilsoncwpau/Library/CloudStorage/OneDrive-3vj4cv/PycharmProjects/Marine_NimWanRoad/readcsv_to_mysql.py->read csv and import into SQL database
        (data after 2021-12-16 dropped since raw data formatting is wrong)
    
    iii) /Users/wilsoncwpau/Library/CloudStorage/OneDrive-3vj4cv/PycharmProjects/Marine_NimWanRoad/sqlexport_process.py->export from sql to create individual csvs for each date between start and end database

2) work in QGIS
    i) /Users/wilsoncwpau/Library/CloudStorage/OneDrive-3vj4cv/QGIS_Marine/qgis_script_ref/trial.py
        run the script in parts (QGIS may freeze if run everything at once, better to perform steps 1-3 and 4-5 separately)
    csvs of intersections should be produced
    ii) 