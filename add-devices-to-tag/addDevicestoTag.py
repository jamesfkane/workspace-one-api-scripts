#!/opt/relocatable-python/bin/python3

import argparse
import csv
import json
import requests
import credentials

parser = argparse.ArgumentParser()
parser.add_argument('--csv', help='path to csv with serial numbers in a single column')
args = parser.parse_args()

api_url_base = "https://domain.awmdm.com/api/mdm"

get_device_id = "{}/devices?searchby=Serialnumber&id=".format(api_url_base)

ws1_headers = credentials.ws1API

while True:
    try:
        tagID = int(input("Enter the tag ID: "))
        break
    except ValueError:
        print("Please input integer only...")
        continue

add_to_tag = "{}/tags/%s/adddevices".format(api_url_base) %(tagID)

serialnumber = []

deviceID = []


with open (args.csv, "r") as infile:
    csv_reader = csv.reader(infile)
    next(csv_reader)
    for row in csv_reader:
        serialnumber.append(row[0])

print(serialnumber)

for serial in serialnumber:
    try:
        response = requests.get(get_device_id+serial, headers=ws1_headers).json()
        deviceID.append(response['Id']['Value'])
        
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

for device in deviceID:
    payload = json.dumps({
        "BulkValues": {
            "Value": [
                device
            ]
        }
    })
    try:
        response = requests.post(add_to_tag, headers=ws1_headers, data=payload).json()
        print(response)
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)