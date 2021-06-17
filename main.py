from dnacentersdk import DNACenterAPI
from dotenv import load_dotenv
from datetime import date
import urllib3
import json
import os

today = date.today() # Set  data and time
todays_date = today.strftime("%m-%d-%y") # Set  data and time format 

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) # Silence the insecure warning due to SSL Certificate

def spacer():
    print("+"+"-"*60+"+")

def get_device_list():
    devices = dnac.devices.get_device_list()
    devicesuid = []
    devicesname = []
    for device in devices.response:
        if device.family != "Unified AP":
            devicesuid.append(device.id)
            devicesname.append(device.hostname)
    get_device_config_by_id(devicesuid, devicesname)
    return devicesname

def get_device_config_by_id(device_list, name_list):
    for device, hostname in zip(device_list, name_list):
        spacer()
        print("Device Hostname: {} ".format(hostname))
        print("Executing Command on {}".format(device))
        get_conf = dnac.devices.get_device_config_by_id(network_device_id=device).response
        cwd = (os.getcwd() + "/" + todays_date)
        filepath = os.path.join(cwd, hostname.replace(".", "-")) # Avoid file extension issues by removing any periods from the hostname
        if not os.path.exists(cwd):
            os.makedirs(cwd)
        with open(filepath, 'w') as file:
            file.write(get_conf)
        print("Archiving Running Configuration ... ")

    devices = ("\n".join('%01d %s' % (i, s) for i, s in enumerate(name_list, 1)))
    spacer()
    print("Folder named {} created in {}. \nRunning configuration for the following devices have been archived: \n\n{}\n".format(todays_date, os.getcwd(), devices))
    spacer()


if __name__ == '__main__':
    load_dotenv()
    username = os.getenv("DNA_CENTER_USERNAME")
    password = os.getenv("DNA_CENTER_PASSWORD")
    base_url = os.getenv("DNA_CENTER_BASE_URL")
    version = os.getenv("DNA_CENTER_VERSION")
    dnac = DNACenterAPI(username=username, password=password, base_url=base_url, version=version, verify=False)

    spacer()
    print("Auth Token: ", dnac.access_token)
    spacer()
    print("Gathering Device Info ... ")
    get_device_list()
