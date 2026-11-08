#!/usr/bin/env python3
from simple_salesforce import Salesforce

sf = Salesforce(username='myemail@example.com', consumer_key='XYZ', privatekey_file='filename.key')
with open("customer_data.json", "r") as file:
    customerData = json.load(file)

recipient = customerData["customer_name"]
uuid = customerData["Id"]
url = ("https://example.com/u/" + uuid)
message = ("Your new webapp is now available at: " + url)

sf.Communicate(recipient,uuid,message)