from dnacentersdk import DNACenterAPI
from dotenv import load_dotenv
from datetime import date
import urllib3
import json
import os

today = date.today() # Set  data and time
todays_date = today.strftime("%m-%d-%y") # Set  data and time format 

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) # Silence the insecure warning due to SSL Certificate

def get_device_list():
    devices = dnac.devices.get_device_list()
    devicesuid = []
    devicesname = []
    for device in devices.response:
        if device.family != "Unified AP":
            devicesuid.append(device.id)
            devicesname.append(device.hostname)
    get_device_config_by_id(devicesuid, devicesname)

def get_device_config_by_id(device_list, name_list):
    for device, hostname in zip(device_list, name_list):
        print("Device Hostname: {} ".format(hostname))
        print("Executing Command on {}".format(device))
        get_conf = dnac.devices.get_device_config_by_id(network_device_id=device).response
        cwd = (os.getcwd() + "/" + todays_date)
        filepath = os.path.join(cwd, hostname.replace(".", "-")) # Avoid file extension issues by removing any periods from the hostname
        if not os.path.exists(cwd):
            os.makedirs(cwd)
        with open(filepath, 'w') as file:
            file.write(get_conf)
        print("Archiving Running Configuration ... \n")

if __name__ == '__main__':
    load_dotenv()
    username = os.getenv("DNA_CENTER_USERNAME")
    password = os.getenv("DNA_CENTER_PASSWORD")
    base_url = os.getenv("DNA_CENTER_BASE_URL")
    version = os.getenv("DNA_CENTER_VERSION")
    dnac = DNACenterAPI(username=username, password=password, base_url=base_url, version=version, verify=False)

    print("Auth Token: ", dnac.access_token)
    print("Gathering Device Info ... \n")
    get_device_list()