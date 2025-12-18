import json
import os

ls = os.listdir("backend/actions_templates/")

dic_actions = {}
for l in ls:
    if "json" in l:
        with open(f"backend/actions_templates/{l}") as f:
            dic_actions[os.path.splitext(l)[0]] = json.load(f)
