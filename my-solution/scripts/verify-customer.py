#!/usr/bin/env python3
import json

import datetime
def validate(date_text):
        try:
            datetime.date.fromisoformat(date_text)
        except ValueError:
            raise ValueError("Incorrect date format")

with open("customer_data.json", "r") as file:
    customerData = json.load(file)

try:
    customerData["customer_motto"]
except NameError:
    if type(customerData["customer_motto"]) == str:
        pass
    else:
        print("Invalid data type: customer_motto")
        exit(1)
else:
    print("Empty field: customer_motto")
    exit(1)

try:
    customerData["created_date"]
except NameError:
    if validate(customerData["created_date"]):
        pass
    else:
        print("Invalid data type: created_date")
        exit(1)
else:
    print("Empty field: created_date")
    exit(1)