from calendar import c
import os
from pyrsistent import v
import requests
import time
import json
import base64
import uuid
import csv
from threading import Thread

def execute_cql(query_number, fhir_server_url, cql_input):

    start = time.time()
    cql_base64 = base64.b64encode(cql_input.encode('ascii'))
    lib_uuid = f'urn:uuid:{str(uuid.uuid4())}'
    measure_uuid = f'urn:uuid:{str(uuid.uuid4())}'
    lib = json.loads(library_template)
    lib['url'] = lib_uuid
    lib['content'][0]['data'] = cql_base64.decode('ascii')

    measure = json.loads(measure_template)
    measure['url'] = measure_uuid
    measure['library'] = lib_uuid
    headers = {'Content-Type': "application/fhir+json"}
    resp = requests.post(f'{fhir_server_url}/Library', data=json.dumps(lib), headers=headers)
    resp = requests.post(f'{fhir_server_url}/Measure', data=json.dumps(measure), headers=headers)
    resp = requests.get(f'{fhir_server_url}/Measure/$evaluate-measure?measure={measure_uuid}&periodStart=2000&periodEnd=2030')
    end = time.time()

    return {"query_number": query_number,
            "query_exec_type": "cql",
            "time_taken_seconds": end - start,
            "n_resources_found": resp.json()['group'][0]['population'][0]['count']}

def execute_flare(query_number, flare_exec_url, sq):
    start = time.time()

    headers = {
        "Content-Type": "application/sq+json"}

    resp = requests.post(f'{flare_exec_url}', data=sq, headers=headers)
    end = time.time()
    return {"query_number": query_number,
            "query_exec_type": "flare",
            "time_taken_seconds": end - start, "n_resources_found": resp.json()}


exec(open('cql_templates.py').read())


def exec_perf_tests():
    fhir_server_url = "http://localhost:8081/fhir"
    perf_results = []

    for file in os.listdir("cql-queries"):

        if file.endswith(".txt"):
            filepath = os.path.join("./cql-queries", file)

            with open(filepath) as cql_file:
                cql_input = cql_file.read()
                
                execute_cql(file, fhir_server_url, cql_input)
                for index in range(0, 10):
                    perf_result = execute_cql(file, fhir_server_url, cql_input)
                    perf_result['iteration'] = index
                    perf_results.append(perf_result)

    perf_results_header = ["iteration", "query_number", "query_exec_type", "time_taken_seconds", "n_resources_found"]

    with open('performance_results-cql.csv', 'a') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=perf_results_header, delimiter=";")
        # writer.writeheader()
        writer.writerows(perf_results)


exec_perf_tests()

concurrent = 0
for index in range(0, 10):
    for i in range(concurrent):
        t = Thread(target=exec_perf_tests(index))
        t.daemon = False
        t.start()
