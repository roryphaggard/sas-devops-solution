#!/usr/bin/env python3
from simple_salesforce import Salesforce
import sys
import json
import yaml
import retry
from kubernetes import config, dynamic
from kubernetes.client import api_client

customerName = sys.argv[1]
customerUUID = sys.argv[2]

sf = Salesforce(username='myemail@example.com', consumer_key='XYZ', privatekey_file='filename.key')

@retry(stop_max_attempt_number=3)
def get_status_code():
    statusCode = sf.get.status_code
    if statusCode == 200:
      customerData = sf.query_all("SELECT Id, customer_name, customer_motto, created_date, custom_data FROM Contact WHERE Id = customerUUID AND customer_name = 'customerName'")
      return customerData
    elif statusCode == [401,503,504]:
      statusMessage = sf.get.RequestException
      print("Error retrieving data from CRM:", statusMessage)
      exit(1)
    elif statusCode == [403,500,502]:
      statusMessage = sf.get.RequestException
      print("Error retrieving data from CRM:", statusMessage)
      exit(1)

customerMotto = customerData["customer_motto"]

with open("customer_data.json","w") as json_file:
    json.dump(customerData)

client = dynamic.DynamicClient(
    api_client.ApiClient(configuration=config.load_kube_config())
)
api = client.resources.get(api_version="v1", kind="ConfigMap")
configmapName = "http-payload"
configmapManifest = {
    "kind": "ConfigMap",
    "apiVersion": "v1",
    "metadata": {
        "name": configmapName,
        "labels": {
            "customerName": "customerUUID",
        },
    },
    "data": {
        "index.html": '{"Welcome companyName, companyMotto"}'
    },
}

with open("http-payload.yaml","w") as yaml_file:
    yaml.dump(configmapManifest)