#Redmineチケットの自動Close

def close_redmine_issue(alertname, instance):
    params = {
        "key": REDMINE_API_KEY,
        "status_id": "open",
        "subject": f"{alertname}:{instance}",
        "project_id": PROJECT_ID
    }
    res = requests.get(f"{REDMINE_URL}/issues.json", params=params)
    issues = res.json().get("issues", [])
    for issue in issues:
        issue_id = issue["id"]
        data = {"issue": {"status_id": DONE_STATUS_ID}}
        headers = {
            "X-Redmine-API-Key": REDMINE_API_KEY,
            "Content-Type": "application/json",
        }
        url = f"{REDMINE_URL}/issues/{issue_id}.json"
        res2 = requests.put(url, json=data, headers=headers)
        res2.raise_for_status()


# Alertmanager APIからの受信で「resolved」判定
@app.post("/req_API")
async def receive_alert(request: Request):
    data = await request.json()
    for alert in data.get("alerts", []):
        state = alert.get("status")
        alertname = alert["labels"].get("alertname")
        instance = alert["labels"].get("instance")
        if state == "firing":
            group_and_create(alert)
        elif state == "resolved":
            close_redmine_issue(alertname, instance)
    return {"result": "ok"}
