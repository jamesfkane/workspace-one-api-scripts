#!/opt/relocatable-python/bin/python3

import argparse
import json
import time
import requests
import credentials

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--tag", type=int, required=True, action="store", help='input tag ID (from the WS1 URL) of devices to cutover from Teem/EventBoard to Zoom Rooms.')
args = parser.parse_args()

tagID = args.tag

print(tagID)

api_url_base = "https://domain.awmdm.com/api/mdm"

get_device_id = "{}/devices?searchby=DeviceId&id=".format(api_url_base)

remove_asam_eb_profile = "{}/profiles/40671/remove".format(api_url_base)

install_sam_zr_profile = "{}/profiles/53133/install".format(api_url_base)

remove_sam_zr_profile = "{}/profiles/53133/remove".format(api_url_base)

install_asam_zr_profile = "{}/profiles/45614/install".format(api_url_base)

query_ws1_url = "{}/devices/commands?command=DeviceQuery&searchBy=DeviceId&id=".format(api_url_base)

get_tag_devices = "{}/tags/%s/devices".format(api_url_base) %(tagID)

add_zrct_device_tag = "{}/tags/14386/adddevices".format(api_url_base)

remove_zrct_device_tag = "{}/tags/14386/removedevices".format(api_url_base)

add_zrc_device_tag = "{}/tags/14387/adddevices".format(api_url_base)

ws1_headers = credentials.ws1API

results = []

response = requests.get(get_tag_devices, headers=ws1_headers).json()
for device in response['Device']:
    results.append(str(device['DeviceId']))

def deviceQuery(results):
    for device in results:
        response = requests.post(query_ws1_url+device, headers=ws1_headers)
        print(device,response)

def removeEbASAM(results):
    for device in results:
        payload = json.dumps({
            "DeviceId": device
        })
        response = requests.post(remove_asam_eb_profile, headers=ws1_headers, data=payload)
        print(device,response)

def installZrcSAM(results):
    for device in results:
        payload = json.dumps({
            "DeviceId": device
        })
        response = requests.post(install_sam_zr_profile, headers=ws1_headers, data=payload)
        print(device,response)

def removeZrcSAM(results):
    for device in results:
        payload = json.dumps({
            "DeviceId": device
        })
        response = requests.post(remove_sam_zr_profile, headers=ws1_headers, data=payload)
        print(device,response)

def installZrcASAM(results):
    for device in results:
        payload = json.dumps({
            "DeviceId": device
        })
        response = requests.post(install_asam_zr_profile, headers=ws1_headers, data=payload)
        print(device,response)

def addZRCTDeviceTag(results):
    for device in results:
        payload = json.dumps({
        "BulkValues": {
            "Value": [
                device
            ]
        }
        })
        response = requests.post(add_zrct_device_tag, headers=ws1_headers, data=payload)
        print(device,response)

def removeZRCTDeviceTag(results):
    for device in results:    
        payload = json.dumps({
        "BulkValues": {
            "Value": [
                device
            ]
        }
        })
        response = requests.post(remove_zrct_device_tag, headers=ws1_headers, data=payload)
        print(device,response)     

def addZRCDeviceTag(results):
    for device in results:
        payload = json.dumps({
        "BulkValues": {
            "Value": [
                device
            ]
        }
        })
        response = requests.post(add_zrc_device_tag, headers=ws1_headers, data=payload)
        print(device,response)

# Remove ASAM profile for EventBoard
print("Removing EventBoard ASAM profile...")
removeEbASAM(results)

# Query all devices
print("Querying devices...")
deviceQuery(results)

# Add Zoom Rooms Controller - Temporary tag
print("Installing Zoom Rooms Controller - Temporary device tag...")
addZRCTDeviceTag(results)

# Query all devices
print("Querying devices...")
deviceQuery(results)

# Sleep 30 seconds
print('Sleeping 30 seconds...')
time.sleep(30)

# Install Zoom Rooms Controller SAM profile
print("Installing Zoom Rooms Controller SAM Profile...")
installZrcSAM(results)

# Query all devices
print("Querying devices...")
deviceQuery(results)

# Sleep 60 seconds
print('Sleeping 30 seconds...')
time.sleep(30)

# Remove Zoom Rooms Controller SAM profile
print("Removing Zoom Rooms Controller SAM profile...")
removeZrcSAM(results)

# Remove Zoom Rooms Controller - Temporary tag
print("Removing Zoom Rooms Controller - Temporary device tag...")
removeZRCTDeviceTag(results)

# Query all devices
print("Querying devices...")
deviceQuery(results)

# Sleep 30 seconds
print('Sleeping 30 seconds...')
time.sleep(30)

# Add Zoom Rooms Controller tag
print("Installing Zoom Rooms Controller device tag...")
addZRCDeviceTag(results)

# Query all devices
print("Querying devices...")
deviceQuery(results)

# Install Zoom Rooms Controller ASAM profile
print("Installing Zoom Rooms Controller ASAM Profile...")
installZrcASAM(results)

# Query all devices
print("Querying devices...")
deviceQuery(results)

# Sleep 30 seconds
print('Sleeping 30 seconds...')
time.sleep(30)

print("Cutover complete.")