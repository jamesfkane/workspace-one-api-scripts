#!/opt/relocatable-python/bin/python3

import argparse
import json
import csv
import time
import requests
import credentials

parser = argparse.ArgumentParser()
parser.add_argument('--csv', help='path to csv with serial numbers in a single column')
args = parser.parse_args()

api_url_base = "https://domain.awmdm.com/api"

get_device_id = "{}/mdm/devices?searchby=Serialnumber&id=".format(api_url_base)

remove_asam_profile = "{}/mdm/profiles/40671/remove".format(api_url_base)

install_asam_profile = "{}/mdm/profiles/40671/install".format(api_url_base)

remove_sam_settings_profile = "{}/mdm/profiles/51372/remove".format(api_url_base)

install_sam_settings_profile = "{}/mdm/profiles/51372/install".format(api_url_base)

remove_sam_eb_profile = "{}/mdm/profiles/51371/remove".format(api_url_base)

install_sam_eb_profile = "{}/mdm/profiles/51371/install".format(api_url_base)

query_ws1_url = "{}/mdm/devices/commands?command=DeviceQuery&searchBy=Serialnumber&id=".format(api_url_base)

add_device_tag = "{}/mdm/tags/14212/adddevices".format(api_url_base)

remove_device_tag = "{}/mdm/tags/14212/removedevices".format(api_url_base)

update_app = "{}/mam/apps/purchased/50173/install".format(api_url_base)

ws1_headers = credentials.ws1API

results = []

with open (args.csv, "r") as infile:
    csv_reader = csv.reader(infile)
    next(csv_reader)
    for row in csv_reader:
        results.append(row[0])

def deviceQuery(results):
    for lines in results:
        response = requests.post(query_ws1_url+lines, headers=ws1_headers)
        print(lines,response)

def installEbASAM(results):
    for lines in results:
        payload = json.dumps({
            "SerialNumber": lines
        })
        response = requests.post(install_asam_profile, headers=ws1_headers, data=payload)
        print(lines,response)

def removeEbASAM(results):
    for lines in results:
        payload = json.dumps({
            "SerialNumber": lines
        })
        response = requests.post(remove_asam_profile, headers=ws1_headers, data=payload)
        print(lines,response)

def addDeviceTag(results):
    for lines in results:
        response = requests.get(get_device_id+lines, headers=ws1_headers).json()
        payload = json.dumps({
        "BulkValues": {
            "Value": [
                response['Id']['Value']
            ]
        }
        })
        response = requests.post(add_device_tag, headers=ws1_headers, data=payload)
        print(lines,response)

def removeDeviceTag(results):
    for lines in results:
        response = requests.get(get_device_id+lines, headers=ws1_headers).json()    
        payload = json.dumps({
        "BulkValues": {
            "Value": [
                response['Id']['Value']
            ]
        }
        })
        response = requests.post(remove_device_tag, headers=ws1_headers, data=payload)
        print(lines,response)     

def installSettingsSAM(results):
    for lines in results:
        payload = json.dumps({
            "SerialNumber": lines
        })
        response = requests.post(install_sam_settings_profile, headers=ws1_headers, data=payload)
        print(lines,response)

def removeSettingsSAM(results):
    for lines in results:
        payload = json.dumps({
            "SerialNumber": lines
        })
        response = requests.post(remove_sam_settings_profile, headers=ws1_headers, data=payload)
        print(lines,response)

def installEbSAM(results):
    for lines in results:
        payload = json.dumps({
            "SerialNumber": lines
        })
        response = requests.post(install_sam_eb_profile, headers=ws1_headers, data=payload)
        print(lines,response)

def removeEbSAM(results):
    for lines in results:
        payload = json.dumps({
            "SerialNumber": lines
        })
        response = requests.post(remove_sam_eb_profile, headers=ws1_headers, data=payload)
        print(lines,response)

def eventboardAppUpdate(results):
    for lines in results:
        payload = json.dumps({
            "SerialNumber": lines
        })
        response = requests.post(update_app, headers=ws1_headers, data=payload)
        print(lines,response)

# Remove ASAM profile for EventBoard
print("Removing ASAM profile...")
removeEbASAM(results)

# Query all devices
print("Querying devices...")
deviceQuery(results)

# Add "Update" device tag so SAM profiles are available
print("Adding Update tag...")
addDeviceTag(results)

# Query all devices
print("Querying devices...")
deviceQuery(results)

# Sleep 60 seconds
print('Sleeping 30 seconds...')
time.sleep(30)

# Force push Settings SAM profile
print("Installing Settings SAM profile...")
installSettingsSAM(results)

# Query all devices
print("Querying devices...")
deviceQuery(results)

# Sleep 30 seconds
print('Sleeping 30 seconds...')
time.sleep(30)

# Push EventBoard update
print("Pushing EventBoard update...")
eventboardAppUpdate(results)

# Query all devices
print("Querying devices...")
deviceQuery(results)

# Sleep 300 seconds
print('Sleeping 300 seconds...')
time.sleep(300)

# Remove Settings SAM profile
print("Removing Settings SAM profile...")
removeSettingsSAM(results)

# Sleep 30 seconds
print("Sleeping 30 seconds...")
time.sleep(30)

# Query devices
print("Querying devices...")
deviceQuery(results)

# Sleep 30 seconds
print("Sleeping 30 seconds...")
time.sleep(30)

# Install SAM EB Profile
print("Installing EventBoard SAM profile...")
installEbSAM(results)

# Query devices
print("Querying devices...")
deviceQuery(results)

# Sleep 30 seconds
print("Sleeping 30 seconds...")
time.sleep(30)

# Remove SAM EB Profile
print("Removing EventBoard SAM Profile...")
removeEbSAM(results)

# Query devices
print("Querying devices...")
deviceQuery(results)

# Sleep 60 seconds
print('Sleeping 60 seconds...')
time.sleep(60)

# Remove Update device tag
print("Removing Update device tag...")
removeDeviceTag(results)

# Query devices
print("Querying devices...")
deviceQuery(results)

# Sleep 30 seconds
print("Sleeping 30 seconds...")
time.sleep(30)

# Apply ASAM profile
print("Re-apply ASAM profile")
installEbASAM(results)

print("Updates complete.")