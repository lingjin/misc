import json
import base64
from jira import JIRA
import re

with open("../jira_config.json", "r") as json_file:
    json_data = json.load(json_file)

jira_server_options = json_data['jira_server_options']
jira_usr = json_data['jira_usr']
jira_pass = base64.b64decode(json_data['jira_pass']).decode('ascii')

jira_obj = JIRA(jira_server_options, basic_auth=(jira_usr, jira_pass))

projects = jira_obj.projects()

print(jira_obj)