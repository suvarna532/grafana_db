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
        with open("downloadDashboardJSON_mysql.json", "w") as file:
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
        "description": "This dashboard provides basic performance metrics for mysql/mariadb. Uses telegraf built-in plugin",
        "editable": True,
        "fiscalYearStartMonth": 0,
        "gnetId": 1443,
        "graphTooltip": 0,
        "id": None,
        "links": [],
        "liveNow": False,
        "panels": [],
        "refresh": "30s",
        "schemaVersion": 37,
        "style": "dark",
        "tags": [
        "telegraf",
        "influxdb",
        "hosts",
        "mysql"
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
    "folderUid": "fe339166-aa7b-4a7b-8225-7f3006dc07ee",
    "overwrite": True
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
         
        with open("mergedDashboard_mysql.json", "w") as fp:
            json.dump(consolidated_dashboard, fp)
        
        with open("mergedDashboard_mysql.json", "r") as file:
            consolidated_dashboard = json.load(file)


    for row in consolidated_dashboard["dashboard"]["panels"]:  
        dashboard = dashboard_d  
        for panel in dashboard["dashboard"]["panels"]:
            if(("type" in panel) and (panel["type"] == "row")):
              pass
            else:
              row["panels"].append(panel) 

    with open("mergedDashboard_mysql.json", "w") as fp:
        json.dump(consolidated_dashboard, fp)

    with open("mergedDashboard_mysql.json", "r") as file:
        consolidated_dashboard = json.load(file)

    i=0 
    for row in consolidated_dashboard["dashboard"]["panels"]:   
        for panel in row["panels"]:
            for target in panel["targets"]:
                if("query" in target):
                  target["query"] = target["query"].replace("=~", "=")
                  target["query"] = target["query"].replace("/^$host$/", f"'{db_list[i]}'")
                  target["query"] = target["query"].replace("/$host$/", f"'{db_list[i]}'")
                  if("tags" in target and len(target["tags"]) != 0 ):
                      target["tags"].pop(0)
                else:
                  if("tags" in target):
                      if(len(target["tags"]) != 0):
                          target["tags"][0]["operator"] = "="
                          target["tags"][0]["value"] = f"{db_list[i]}"
        i+=1

    with open("mergedDashboard_mysql.json", "w") as fp:
        json.dump(consolidated_dashboard, fp)
    with open("mergedDashboard_mysql.json", "r") as file:
        consolidated_dashboard = json.load(file)
    
    db_name = db_list[0].split('-')[:3]
    db_name = '-'.join(db_name)
    consolidated_dashboard["dashboard"]["title"] = "{}".format(db_name)
    with open("mergedDashboard_mysql.json", "w") as fp:
        json.dump(consolidated_dashboard, fp)



def uploadConsolidatedDashboard(grafana_key: str) -> bool:
    url = f"http://grafana-prod.default.svc.cluster.local:3000/api/dashboards/db"
    headers = {
        "Authorization": f"Bearer {grafana_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    with open("mergedDashboard_mysql.json", "r") as file:
        consolidated_dashboard = json.load(file)

    response = requests.request("POST", url, headers=headers, json=consolidated_dashboard)
    if(response.status_code == 200):
        return True
    else:
        return False


grafana_key = 'glsa_L302nAd4qtIcthbbzEHY1Zq103lst9oI_6c9b79ae'


if __name__ == '__main__':

    number = input("Enter the count of the database names (Primary+Replicas)\n")
    if(int(number) < 2):
        print("Atleast 2 database names are required. Primary Database followed by Replica(s)")
        exit(1)
    print("Enter the database names whose Grafana dashboards need to be consolidated. The first name should be primary database followed by its secondary or replica database names. IMPORTANT: The DB names should be entered in line by line by pressing enter\n")
    db_list = []
    for db in range(int(number)):
        db_list.append(input().strip())
 
    dashboardUID = "kH7HzUZVk"
    dashboard = downloadDashboardJSON(grafana_key, dashboardUID)
    mergeDashboards(dashboard, db_list)
    if(uploadConsolidatedDashboard(grafana_key)):
        print("Successfully uploaded the consolidated dashboard for {} in Grafana\n".format(db_list[0]))
    else:
        print("Error! Couldn't upload the consolidated dashboard for {} to Grafana".format(db_list[0]))
        

