import urllib.request, json 
with urllib.request.urlopen("https://www.pland.gov.hk/pland_en/info_serv/digital_planning_data/Metadata/OZP_PLAN_GML.json") as url:
    ozp_json_list = json.loads(url.read().decode())
    
for ozp in ozp_json_list:
    print(ozp["GML_LINK"])
    urllib.request.urlretrieve(ozp["GML_LINK"], ozp["NAME_ENG"]+".zip")
