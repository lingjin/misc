import json
import base64
from jira import JIRA
import re

JIRA_CONFIG_FILE = '../jira_config.json'
JIRA_SERVER_OPTIONS = 'jira_server_options'
JIRA_USR = 'jira_usr'
JIRA_PASS = 'jira_pass'

def init_jira_from_json():
    with open(JIRA_CONFIG_FILE, 'r') as json_file:
        json_data = json.load(json_file)

    jira_server_options = json_data[JIRA_SERVER_OPTIONS]
    jira_usr = json_data[JIRA_USR]
    jira_pass = base64.b64decode(json_data[JIRA_PASS]).decode('ascii')
    jira = JIRA(jira_server_options, basic_auth=(jira_usr, jira_pass))

    return jira

if __name__ == "__main__":
    jira = init_jira_from_json()
    projects = jira.projects()
    print(projects)