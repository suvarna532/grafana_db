import requests
import json


def searchDashboard(grafana_key: str, dashboardName:str) -> str:
    url = f"http://43.204.119.250:3000/api/search?query={dashboardName}"
    headers = {
        "Authorization": f"Bearer {grafana_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    response = requests.request("GET", url, headers=headers)
    #response = requests.get(url, headers=headers)
    #with open("searchDashboard.json", "w") as file:
        #json.dump(response.json(), file) 
        #file.write(response.text) 
    return response.json()[0]['uid']   

def downloadDashboardJSON(grafana_key: str, dashboardUID: str, json_file: str):
    url = f"http://43.204.119.250:3000/api/dashboards/uid/{dashboardUID}"
    headers = {
        "Authorization": f"Bearer {grafana_key}",
        "Content-Type": "application/json",
        "accept": "application/json",
    }
    response = requests.request("GET", url, headers=headers)
    with open('{}.json'.format(json_file), "w") as file:
        json.dump(response.json(), file)

def addRowToPrimary(primaryDBName: str):
    with open("primary.json", 'r+') as fp:
        primary_data = json.load(fp)
        primary_data['dashboard']['panels'].insert(0, {'type': "row", 'title': "Primary DB {}".format(primaryDBName)})
        primary_data['dashboard']['title'] = 'Consolidated Dashboard for {}'.format(primaryDBName)
        primary_data['dashboard'].pop("uid")
        fp.seek(0)
        json.dump(primary_data, fp, indent = 2)

    
def mergeDashboards(secondary_file: str, secondaryDBName: str):
    with open(secondary_file, 'r') as fp_s:
        secondary_data = json.load(fp_s)
    with open("primary.json", 'r+') as fp:
        primary_data = json.load(fp)
        primary_data['dashboard']['panels'].append({'type': "row", 'title': "Secondary DB {}".format(secondaryDBName)})
        for panel in secondary_data['dashboard']['panels']:
            primary_data['dashboard']['panels'].append(panel)
        fp.seek(0)
        json.dump(primary_data, fp, indent = 2)
        consolidated_file = primary_data['dashboard']
    with open("consolidated_dashboard.json", "w+") as np:
        np.seek(0)
        json.dump(consolidated_file, np)

def uploadConsolidatedDashboard(grafana_key: str, primaryDBName: str) -> bool:
    url = f"http://43.204.119.250:3000/api/dashboards/db"
    headers = {
        "Authorization": f"Bearer {grafana_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    with open("consolidated_dashboard.json", "r") as fp:
        data_file = json.load(fp)
    data = {
  "dashboard": {
    "title": "Consolidated-Dashboard For {}".format(primaryDBName),
    "panels": data_file['panels']
  },
  "overwrite": True,
}
    response = requests.request("POST", url, headers=headers, json=data)
    if(response.status_code == 200):
        return True
    else:
        return False


       
# GLOBAL VARIABLES
# TODO: Change to corresponding bearer ID
#Prod Env Key
#grafana_key = 'glsa_GTQiH7o8Zzzfe4vNVe1U3XZwe50qLxbb_a4dd48e6'
#Test Env Key
grafana_key = 'glsa_zuzXUBr6FpB6Cq1f4BzePQ0TkHozWzwI_b0738eae'

if __name__ == '__main__':
    
    primaryDBName = input("Enter the primary DB dashboard Name\n")
    secondaryDBName = input("Enter the secondary DB dashboard Name\n")
    choice = input("Are there more secondary DB dashboards to add? (y/n)\n")
    secondaryDBName_list = []
    if(choice in ['Y','y','Yes','yes','YES']):
        input_secondaryDBNames = input("Enter the remaining secondary DB dashboards names each separated by space and at the end press Enter:\n")
        secondaryDBName_list = list(map(str, input_secondaryDBNames.split()))
    elif(choice in ['N','n','NO','No','no']):
        pass
    else:
        print("Entered wrong choice. Hence existing...\n")
        exit(1)
        
    dashboardUID = searchDashboard(grafana_key, primaryDBName)
    downloadDashboardJSON(grafana_key, dashboardUID, "primary")
    addRowToPrimary(primaryDBName)
    dashboardUID = searchDashboard(grafana_key, secondaryDBName)
    downloadDashboardJSON(grafana_key, dashboardUID, "secondary")
    mergeDashboards("secondary.json", secondaryDBName)
    if(len(secondaryDBName_list) != 0):
        for db in secondaryDBName_list:
            dashboardUID = searchDashboard(grafana_key, db)
            json_file = "secondary-{}".format(secondaryDBName_list.index(db)+1)
            downloadDashboardJSON(grafana_key, dashboardUID, json_file)
            mergeDashboards(json_file, secondaryDBName)
            
    if(uploadConsolidatedDashboard(grafana_key, "primary-host")):
        print("Successfully uploaded the consolidated dashboard for {} in Grafana\n".format(primaryDBName))
    else:
        print("Error! Couldn't upload the consolidated dashboard for {} to Grafana".format(primaryDBName))
        

