import base64

import json

import os

import requests
 
GITHUB_TOKEN = os.environ["GH_TOKEN"]

REPO = "appsec-scans/cxone-demo-1"

BRANCH = "main"

NEW_BRANCH = "add-appsec-workflow"

WORKFLOW_PATH = ".github/workflows/appsec.yaml"

WORKFLOW_FILE = "appsec.yaml"
 
headers = {

    "Authorization": f"token {GITHUB_TOKEN}",

    "Accept": "application/vnd.github.v3+json",

}
 
def file_exists():

    url = f"https://api.github.com/repos/{REPO}/contents/{WORKFLOW_PATH}?ref={BRANCH}"

    r = requests.get(url, headers=headers)

    return r.status_code == 200
 
def create_branch():

    url = f"https://api.github.com/repos/{REPO}/git/ref/heads/{BRANCH}"

    base_sha = requests.get(url, headers=headers).json()["object"]["sha"]
 
    url = f"https://api.github.com/repos/{REPO}/git/refs"

    data = {

        "ref": f"refs/heads/{NEW_BRANCH}",

        "sha": base_sha,

    }

    r = requests.post(url, headers=headers, json=data)

    r.raise_for_status()
 
def commit_file():

    with open(WORKFLOW_FILE, "rb") as f:

        content = base64.b64encode(f.read()).decode()
 
    url = f"https://api.github.com/repos/{REPO}/contents/{WORKFLOW_PATH}"

    data = {

        "message": "Add AppSec workflow",

        "content": content,

        "branch": NEW_BRANCH,

    }

    r = requests.put(url, headers=headers, json=data)

    r.raise_for_status()
 
def create_pull_request():

    url = f"https://api.github.com/repos/{REPO}/pulls"

    data = {

        "title": "Add AppSec GitHub Workflow",

        "head": NEW_BRANCH,

        "base": BRANCH,

        "body": (

            "### 🛡️ AppSec Workflow Added\n\n"

            "This PR adds the Checkmarx AppSec workflow.\n\n"

            "**Note for developers**: Please add your protected branches to the `push` and `pull_request` triggers "

            "in the workflow (`.github/workflows/appsec.yaml`) to ensure AppSec scans run for your branches."

        )

    }

    r = requests.post(url, headers=headers, json=data)

    r.raise_for_status()
 
def main():

    if file_exists():

        print("Workflow file already exists. No action taken.")

        return

    create_branch()

    commit_file()

    create_pull_request()

    print("Pull request created successfully.")
 
if __name__ == "__main__":

    main()
 
