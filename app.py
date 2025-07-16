#app.py

from fastapi import FastAPI, Request
import requests
import os

# --- 設定 ---
REDMINE_URL = os.getenv("REDMINE_URL", "<redmine-URL>")
API_KEY = os.getenv("REDMINE_API_KEY", "<YOUR_API_KEY>")
PROJECT_ID = os.getenv("REDMINE_PROJECT_ID", "<project_ID>")
TRACKER_ID = int(os.getenv("REDMINE_TRACKER_ID", 1))  # 1=Bug
OPEN_STATUS_ID = int(os.getenv("REDMINE_OPEN_STATUS_ID", 1))    # 未着手
CLOSE_STATUS_ID = int(os.getenv("REDMINE_CLOSE_STATUS_ID", 8))  # 完了

app = FastAPI()

# チケット作成
def create_redmine_issue(subject, description):
    url = f"{REDMINE_URL}/issues.json"
    headers = {"X-Redmine-API-Key": API_KEY, "Content-Type": "application/json"}
    payload = {
        "issue": {
            "project_id": PROJECT_ID,
            "tracker_id": TRACKER_ID,
            "subject": subject,
            "description": description,
            "status_id": OPEN_STATUS_ID
        }
    }
    r = requests.post(url, json=payload, headers=headers)
    if r.status_code == 201:
        return r.json()["issue"]["id"]
    else:
        print(f"Create error: {r.text}")
        return None

# チケット検索（未完了のみ）
def find_existing_issue(subject):
    url = f"{REDMINE_URL}/issues.json?project_id={PROJECT_ID}&subject=~{subject}&status_id=open"
    headers = {"X-Redmine-API-Key": API_KEY}
    r = requests.get(url, headers=headers)
    if r.status_code == 200 and r.json()["issues"]:
        return r.json()["issues"][0]
    return None

# チケットを完了に
def close_redmine_issue(issue_id):
    url = f"{REDMINE_URL}/issues/{issue_id}.json"
    headers = {"X-Redmine-API-Key": API_KEY, "Content-Type": "application/json"}
    payload = {"issue": {"status_id": CLOSE_STATUS_ID}}
    r = requests.put(url, json=payload, headers=headers)
    return r.status_code == 200

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    alerts = data.get("alerts", [])
    result = []
    for alert in alerts:
        labels = alert.get("labels", {})
        alertname = labels.get("alertname", "unknown")
        instance = labels.get("instance", "unknown")
        status = alert.get("status", "")
        subject = f"{alertname}:{instance}"
        description = alert.get("annotations", {}).get("summary", "")

        if status == "firing":
            # firing時は同じsubjectの未完了チケットがなければ新規作成
            issue = find_existing_issue(subject)
            if not issue:
                issue_id = create_redmine_issue(subject, description)
                result.append({"created": issue_id})
            else:
                result.append({"already_exists": issue["id"]})
        elif status == "resolved":
            # resolved時は同じsubjectの未完了チケットがあれば完了にする
            issue = find_existing_issue(subject)
            if issue:
                close_redmine_issue(issue["id"])
                result.append({"closed": issue["id"]})
            else:
                result.append({"no_open_issue": subject})
    return {"result": result}

