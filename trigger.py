"""
BO_AI trigger.py
GitHub Actions をAPIで起動する
"""

import os
import requests

GITHUB_OWNER = "jv8gbf476b-ctrl"
GITHUB_REPO = "BO_AI_RUN"
WORKFLOW_FILE = "run.yml"
BRANCH = "main"


def trigger_workflow():
    token = os.environ["PAT_TOKEN"]

    url = (
        f"https://api.github.com/repos/"
        f"{GITHUB_OWNER}/{GITHUB_REPO}/actions/workflows/"
        f"{WORKFLOW_FILE}/dispatches"
    )

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    data = {
        "ref": BRANCH
    }

    response = requests.post(
        url,
        headers=headers,
        json=data,
        timeout=20,
    )

    if response.status_code == 204:
        print("✅ BO_AI_RUNを起動しました")
        return True

    print("❌ 起動失敗")
    print(response.status_code)
    print(response.text)

    return False


if __name__ == "__main__":
    trigger_workflow()
