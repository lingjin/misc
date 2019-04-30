import json

with open("../jira_config.json", "r") as json_file:
    json_data = json.load(json_file)

print(json_data)