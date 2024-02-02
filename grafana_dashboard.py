import requests
import json

 
def downloadDashboardJSON(grafana_key: str, dashboardUID: str):
    url = f"http://grafana-prod.default.svc.cluster.local:3000/api/dashboards/uid/{dashboardUID}"
    headers = {
        "Authorization": f"Bearer {grafana_key}",
        "Content-Type": "application/json",
        "accept": "application/json",
    }
    response = requests.request("GET", url, headers=headers)
    if(response.status_code == 200):
        with open("downloadDashboardJSON.json", "w") as file:
            json.dump(response.json(), file)
    
        return response.json()
    else:
        raise ValueError(f"Failed to download dashboard. Status code: {response.status_code}")

 
def mergeDashboards(dashboard_d: json, db_list: list):
    consolidated_dashboard = {
    "dashboard": {
        "annotations": {
        "list": [
            {
            "$$hashKey": "object:13",
            "builtIn": 1,
            "datasource": {
                "type": "datasource",
                "uid": "grafana"
            },
            "enable": True,
            "hide": True,
            "iconColor": "rgba(0, 211, 255, 1)",
            "name": "Annotations & Alerts",
            "target": {
                "limit": 100,
                "matchAny": False,
                "tags": [],
                "type": "dashboard"
            },
            "type": "dashboard"
            }
        ]
        },
        "description": "Telegraf Host Metrics",
        "editable": True,
        "fiscalYearStartMonth": 0,
        "gnetId": 1443,
        "graphTooltip": 0,
        "links": [],
        "liveNow": False,
        "panels": [],
        "refresh": "30s",
        "schemaVersion": 37,
        "style": "dark",
        "tags": [
        "telegraf",
        "influxdb",
        "hosts"
        ],
        "templating": {
        "list": [
            {
            "auto": True,
            "auto_count": 30,
            "auto_min": "10s",
            "current": {
                "selected": False,
                "text": "1m",
                "value": "1m"
            },
            "hide": 0,
            "name": "interval",
            "options": [
                {
                "selected": False,
                "text": "auto",
                "value": "$__auto_interval_interval"
                },
                {
                "selected": False,
                "text": "10s",
                "value": "10s"
                },
                {
                "selected": False,
                "text": "20s",
                "value": "20s"
                },
                {
                "selected": False,
                "text": "30s",
                "value": "30s"
                },
                {
                "selected": True,
                "text": "1m",
                "value": "1m"
                },
                {
                "selected": False,
                "text": "10m",
                "value": "10m"
                },
                {
                "selected": False,
                "text": "30m",
                "value": "30m"
                },
                {
                "selected": False,
                "text": "1h",
                "value": "1h"
                },
                {
                "selected": False,
                "text": "6h",
                "value": "6h"
                },
                {
                "selected": False,
                "text": "12h",
                "value": "12h"
                },
                {
                "selected": False,
                "text": "1d",
                "value": "1d"
                },
                {
                "selected": False,
                "text": "7d",
                "value": "7d"
                },
                {
                "selected": False,
                "text": "14d",
                "value": "14d"
                },
                {
                "selected": False,
                "text": "30d",
                "value": "30d"
                }
            ],
            "query": "10s,20s,30s,1m,10m,30m,1h,6h,12h,1d,7d,14d,30d",
            "refresh": 2,
            "skipUrlSync": False,
            "type": "interval"
            }
        ]
        },
        "time": {
        "from": "now-5m",
        "to": "now-30s"
        },
        "timepicker": {
        "nowDelay": "30s",
        "refresh_intervals": [
            "5s",
            "10s",
            "30s",
            "1m",
            "5m",
            "15m",
            "30m",
            "1h",
            "2h",
            "1d"
        ],
        "time_options": [
            "5m",
            "15m",
            "1h",
            "6h",
            "12h",
            "24h",
            "2d",
            "7d",
            "30d"
        ]
        },
        "timezone": "browser",
        "version": 7,
        "weekStart": ""
    },
    "folderUid": "TXJqe-0Mk",
    "overwrite": False
}
    row = {
    "collapsed": True,
    "gridPos": {
        "h": 1,
        "w": 24,
        "x": 0,
        "y": 1
    },
    "panels": [],
    "type": "row"
    }

    for db in range(len(db_list)):
        primary_row = row
        if(db == 0):
            primary_row["gridPos"]["y"] = 0

        primary_row["title"] = db_list[db]
        consolidated_dashboard["dashboard"]["panels"].append(primary_row)
         
        with open("mergedDashboard.json", "w") as fp:
            json.dump(consolidated_dashboard, fp)
        
        with open("mergedDashboard.json", "r") as file:
            consolidated_dashboard = json.load(file)


    for row in consolidated_dashboard["dashboard"]["panels"]:  
        dashboard = dashboard_d  
        for panel in dashboard["dashboard"]["panels"]:
            row["panels"].append(panel) 

    with open("mergedDashboard.json", "w") as fp:
        json.dump(consolidated_dashboard, fp)

    with open("mergedDashboard.json", "r") as file:
        consolidated_dashboard = json.load(file)

    i=0 
    for row in consolidated_dashboard["dashboard"]["panels"]:   
        tags = {
                    "key": "host",
                    "operator": "=~",
                    "value": db_list[i]
                }
        for panel in row["panels"]:
            panel["targets"][0]["tags"].append(tags)
        i+=1

    with open("mergedDashboard.json", "w") as fp:
        json.dump(consolidated_dashboard, fp)
    with open("mergedDashboard.json", "r") as file:
        consolidated_dashboard = json.load(file)

    consolidated_dashboard["dashboard"]["title"] = "Databases_consolidated_dashboard_of_{}".format(db_list[0])
    with open("mergedDashboard.json", "w") as fp:
        json.dump(consolidated_dashboard, fp)

    
    

def uploadConsolidatedDashboard(grafana_key: str) -> bool:
    url = f"http://grafana-prod.default.svc.cluster.local:3000/api/dashboards/db"
    headers = {
        "Authorization": f"Bearer {grafana_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    with open("mergedDashboard.json", "r") as file:
        consolidated_dashboard = json.load(file)

    response = requests.request("POST", url, headers=headers, json=consolidated_dashboard)
    if(response.status_code == 200):
        return True
    else:
        return False


grafana_key = 'glsa_L302nAd4qtIcthbbzEHY1Zq103lst9oI_6c9b79ae'


if __name__ == '__main__':
    
    db_list = input("Enter the database host names whose Grafana dashboards need to be consolidated. The first name should be primary database host followed by its secondary database host names. IMPORTANT: The host names should be entered in one line with single space in between\n")
    if(' ' in db_list):
        db_list = list(map(str, db_list.split(' ')))
    else:
        print("Single space is not found in the input provided. Please enter the host names as per the given instruction. Atleast two host names should be entered\n")
        exit(1)
    
    dashboardUID = "YIMEXyZ4k"
    dashboard = downloadDashboardJSON(grafana_key, dashboardUID)
    mergeDashboards(dashboard, db_list)
    if(uploadConsolidatedDashboard(grafana_key)):
        print("Successfully uploaded the consolidated dashboard for {} in Grafana\n".format(db_list[0]))
    else:
        print("Error! Couldn't upload the consolidated dashboard for {} to Grafana".format(db_list[0]))
        
   