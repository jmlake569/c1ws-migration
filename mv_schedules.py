import requests
import json
from pprint import pprint

#define Deep Security manager hostname with port and API key
DSM_HOSTNAME = "<YOUR-DSM-HOSTNAME-HERE>"
DSM_API_KEY = "<YOUR-API-KEY-HERE>"
PORT = "4119"
#define Cloud One Workload Security region
REGION = "<YOUR-CLOUD-ONE-REGION-HERE>"
C1_API_KEY = "<YOUR-API-KEY-HERE>"
#set up the Deep Security API and headers
dsmurl = f"https://{DSM_HOSTNAME}:{PORT}/api/scheduledtasks"
dsm_headers = {"api-version": "v1", "Content-Type": "application/json", "api-secret-key": DSM_API_KEY}

#setup Cloud One API and headers
c1 = f"https://workload.{REGION}.cloudone.trendmicro.com/api/scheduledtasks"
c1_headers = {"api-version": "v1", "Content-Type": "application/json", "Authorization": C1_API_KEY}

response = requests.get(dsmurl, headers=dsm_headers)
data = json.loads(response.content)

for task in data["scheduledTasks"]:
    payload = {
        "name": task["name"],
        "type": task["type"],
        "scheduleDetails": task["scheduleDetails"],
        "enabled": task["enabled"],
    }
    if "lastRunTime" in task:
        payload["lastRunTime"] = task["lastRunTime"]
    if "nextRunTime" in task:
        payload["nextRunTime"] = task["nextRunTime"]
    if task["type"] == "synchronize-cloud-account" and "synchronizeCloudAccountTaskParameters" in task:
        payload["synchronizeCloudAccountTaskParameters"] = task["synchronizeCloudAccountTaskParameters"]
    if task["type"] == "send-alert-summary" and "sendAlertSummaryTaskParameters" in task:
        payload["sendAlertSummaryTaskParameters"] = task["sendAlertSummaryTaskParameters"]
    elif task["type"] == "check-for-security-updates" and "checkForSecurityUpdatesTaskParameters" in task:
        computer_group_id = task["checkForSecurityUpdatesTaskParameters"]["computerFilter"].get("computerGroupID")
        if computer_group_id is not None:
            c1_cgep=f"https://{DSM_HOSTNAME}:{PORT}/api/computergroups/{computer_group_id}"
            response = requests.get(c1_cgep, headers=dsm_headers)
            cgdata = json.loads(response.content)
            cgname = cgdata['name']
            c1_scg=f"https://workload.{REGION}.cloudone.trendmicro.com/api/computergroups"
            response = requests.get(c1_scg, headers=c1_headers)
            search_data = json.loads(response.content)
            folder_id = None
            for group in search_data["computerGroups"]:
                if group["name"] == cgname:
                    folder_id = group["ID"]
                    break
            if folder_id is not None:
                payload["checkForSecurityUpdatesTaskParameters"] = {
                    "computerFilter": {
                        "type": "computers-in-group",
                        "computerGroupID": folder_id
                    }
                }
        else:
            payload["checkForSecurityUpdatesTaskParameters"] = task["checkForSecurityUpdatesTaskParameters"]
    elif task["type"] == "scan-for-recommendations" and "scanForRecommendationsTaskParameters" in task:
        computer_group_id = task["scanForRecommendationsTaskParameters"]["computerFilter"].get("computerGroupID")
        if computer_group_id is not None:
            c1_cgep=f"https://{DSM_HOSTNAME}:{PORT}/api/computergroups/{computer_group_id}"
            response = requests.get(c1_cgep, headers=dsm_headers)
            cgdata = json.loads(response.content)
            cgname = cgdata['name']
            c1_scg=f"https://workload.{REGION}.cloudone.trendmicro.com/api/computergroups"
            response = requests.get(c1_scg, headers=c1_headers)
            search_data = json.loads(response.content)
            folder_id = None
            for group in search_data["computerGroups"]:
                if group["name"] == cgname:
                    folder_id = group["ID"]
                    break
            if folder_id is not None:
                payload["scanForRecommendationsTaskParameters"] = {
                    "computerFilter": {
                        "type": "computers-in-group",
                        "computerGroupID": folder_id
                    }
                }
        else:
            payload["scanForRecommendationsTaskParameters"] = task["scanForRecommendationsTaskParameters"]
    elif task["type"] == "generate-report" and "generateReportTaskParameters" in task:
        payload["generateReportTaskParameters"] = task["generateReportTaskParameters"]
    elif task["type"] == "scheduled-agent-upgrade" and "scheduledAgentUpgradeTaskParameters" in task:
        payload["scheduledAgentUpgradeTaskParameters"] = task["scheduledAgentUpgradeTaskParameters"]
    elif task["type"] == "send-alert-summary" and "sendPolicyTaskParameters" in task:
        payload["sendPolicyTaskParameters"] = task["sendPolicyTaskParameters"]
    elif task["type"] == "scan-for-integrity-changes" and "scanForIntegrityChangesTaskParameters" in task:
        payload["scanForIntegrityChangesTaskParameters"] = task["scanForIntegrityChangesTaskParameters"]
    if task["type"] == "scan-for-malware" and "scanForMalwareTaskParameters" in task:
        computer_group_id = task["scanForMalwareTaskParameters"]["computerFilter"].get("computerGroupID")
        #uses the computer "computerGroupID" from the "scanForMalwareTaskParameters" to get the folder name from Deep Securtiy and then it uses the folder name to query the C1 console and retrieve the new group ID then attach that to the payload to assign the scheduled malware scan to the correct folder with the new group ID
        if computer_group_id is not None:
            c1_cgep=f"https://{DSM_HOSTNAME}:{PORT}/api/computergroups/{computer_group_id}"
            response = requests.get(c1_cgep, headers=dsm_headers)
            cgdata = json.loads(response.content)
            cgname = cgdata['name']
            c1_scg=f"https://workload.{REGION}.cloudone.trendmicro.com/api/computergroups"
            response = requests.get(c1_scg, headers=c1_headers)
            search_data = json.loads(response.content)
            folder_id = None
            for group in search_data["computerGroups"]:
                if group["name"] == cgname:
                    folder_id = group["ID"]
                    break
            if folder_id is not None:
                payload["scanForMalwareTaskParameters"] = {
                    "computerFilter": {
                        "type": "computers-in-group",
                        "computerGroupID": folder_id
                    }
                }
        else:
            payload["scanForMalwareTaskParameters"] = task["scanForMalwareTaskParameters"]
        
    # Send a POST request to create the task
    response = requests.post(c1, headers=c1_headers, json=payload)


    if response.status_code == 200:
        print(f"Task {task['name']} successfully created")
    else:
        print(f"Error creating task {task['name']}: {response.content}")
