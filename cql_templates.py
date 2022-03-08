cql_input = '''
library Retrieve
using FHIR version '4.0.0'
include FHIRHelpers version '4.0.0'

codesystem icd10: 'http://fhir.de/CodeSystem/bfarm/icd-10-gm'
codesystem loinc: 'http://loinc.org'
codesystem ops: 'http://fhir.de/CodeSystem/bfarm/ops'

context Patient

define InInitialPopulation:
  Patient.gender = 'female' and
  exists [Condition: Code 'C50.1' from icd10] and
  exists [Procedure: Code '8-523.00' from ops] and
  exists from [Observation: Code '718-7' from loinc] O
    where O.value as Quantity > 6 'g/dL'
'''


library_template = '''{
  "resourceType": "Library",
  "url": "urn:uuid:a2b9f4b4-5d5b-46bd-a9fd-35f024c852fa",
  "status": "active",
  "type" : {
    "coding" : [
      {
        "system": "http://terminology.hl7.org/CodeSystem/library-type",
        "code" : "logic-library"
      }
    ]
  },
  "content": [
    {
      "contentType": "text/cql",
      "data": "CmxpYnJhcnkgUmV0cmlldmUKdXNpbmcgRkhJUiB2ZXJzaW9uICc0LjAuMCcKaW5jbHVkZSBGSElSSGVscGVycyB2ZXJzaW9uICc0LjAuMCcKCmNvbnRleHQgUGF0aWVudAoKY29kZXN5c3RlbSBsb2luYzogJ2h0dHA6Ly9sb2luYy5vcmcnCmNvZGVzeXN0ZW0gYWRtaW5nZW5kZXI6ICdodHRwOi8vaGw3Lm9yZy9maGlyL2FkbWluaXN0cmF0aXZlLWdlbmRlcicKCmRlZmluZSBJbkluaXRpYWxQb3B1bGF0aW9uOgogIGV4aXN0cyhmcm9tIFtPYnNlcnZhdGlvbjogQ29kZSAnNzY2ODktOScgZnJvbSBsb2luY10gTwogICAgd2hlcmUgTy52YWx1ZS5jb2RpbmcgY29udGFpbnMgQ29kZSAnZmVtYWxlJyBmcm9tIGFkbWluZ2VuZGVyCg=="
    }
  ]
}'''


measure_template = '''{
  "resourceType": "Measure",
  "url": "urn:uuid:49f4c7de-3320-4208-8e60-ecc0d8824e08",
  "status": "active",
  "library": "urn:uuid:a2b9f4b4-5d5b-46bd-a9fd-35f024c852fa",
  "scoring": {
    "coding": [
      {
        "system": "http://terminology.hl7.org/CodeSystem/measure-scoring",
        "code": "cohort"
      }
    ]
  },
  "group": [
    {
      "population": [
        {
          "code": {
            "coding": [
              {
                "system": "http://terminology.hl7.org/CodeSystem/measure-population",
                "code": "initial-population"
              }
            ]
          },
          "criteria": {
            "language": "text/cql",
            "expression": "InInitialPopulation"
          }
        }
      ]
    }
  ]
}'''