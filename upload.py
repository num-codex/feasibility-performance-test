import os
import requests

folder_to_load = "data-perf-codex-small"


for file in os.listdir(folder_to_load):
    if file.endswith(".ndjson"):
        filepath = os.path.join(f'./{folder_to_load}', file)

        with open(filepath) as fp:
            Lines = fp.readlines()
            print("loading file:" + filepath)
            for line in Lines:
                headers = {'Content-Type': "application/fhir+json"}
                payload = line
                resp = requests.post("http://localhost:8081/fhir", data=line, headers=headers)
