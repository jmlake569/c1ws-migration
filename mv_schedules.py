import requests
import json
from pprint import pprint

# Set up the Deep Security API and headers
ds = "URL:PORT/api/scheduledtasks"
ds_headers = {"api-version": "v1", "Content-Type": "application/json", "api-secret-key": "<API_KEY_HERE>"}

#setup Cloud One API and headers
c1 = "https://workload.trend-us-1.cloudone.trendmicro.com/api/scheduledtasks"
c1_headers = {"api-version": "v1", "Content-Type": "application/json", "Authorization": "ApiKey <API_KEY_HERE"}

response = requests.get(ds, headers=ds_headers)
data = json.loads(response.content)

response = requests.get(ds, headers=ds_headers)
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
    elif task["type"] == "check-for-security-updates" and "sendAlertSummaryTaskParameters" in task:
        payload["sendAlertSummaryTaskParameters"] = task["sendAlertSummaryTaskParameters"]
    elif task["type"] == "scan-for-recommendations" and "scanForRecommendationsTaskParameters" in task:
        payload["scanForRecommendationsTaskParameters"] = task["scanForRecommendationsTaskParameters"]
    elif task["type"] == "generate-report" and "generateReportTaskParameters" in task:
        payload["generateReportTaskParameters"] = task["generateReportTaskParameters"]
    elif task["type"] == "scheduled-agent-upgrade" and "scheduledAgentUpgradeTaskParameters" in task:
        payload["scheduledAgentUpgradeTaskParameters"] = task["scheduledAgentUpgradeTaskParameters"]
    elif task["type"] == "send-alert-summary" and "sendPolicyTaskParameters" in task:
        payload["sendPolicyTaskParameters"] = task["sendPolicyTaskParameters"]
    elif task["type"] == "scan-for-integrity-changes" and "scanForIntegrityChangesTaskParameters" in task:
        payload["scanForIntegrityChangesTaskParameters"] = task["scanForIntegrityChangesTaskParameters"]
    elif task["type"] == "scan-for-malware" and "scanForMalwareTaskParameters" in task:
        payload["scanForMalwareTaskParameters"] = task["scanForMalwareTaskParameters"]
    
    print(payload)
    # Send a POST request to create the task
    #response = requests.post(c1, headers=c1_headers, json=payload)

    if response.status_code == 200:
        print(f"Task {task['name']} successfully created")
    else:
        print(f"Error creating task {task['name']}: {response.content}")
