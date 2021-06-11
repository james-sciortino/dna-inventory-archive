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
    cmd_run(devicesuid, devicesname)

def cmd_run(device_list, name_list):
    for device, hostname in zip(device_list, name_list):
        print("Getting running config on {}".format(hostname))
        run_cmd = dnac.command_runner.run_read_only_commands_on_devices(commands=["show ip int br"],deviceUuids=[device], name=hostname)
        print("Task started! Task ID is {}".format(run_cmd.response.taskId))
        task_info = dnac.task.get_task_by_id(run_cmd.response.taskId)
        task_progress = task_info.response.progress
        print("Task Status : {}".format(task_progress))
        while task_progress == 'CLI Runner request creation':
            task_progress = dnac.task.get_task_by_id(run_cmd.response.taskId).response.progress
        task_progress = json.loads(task_progress)

        cmd_output = dnac.file.download_a_file_by_fileid(task_progress['fileId'], save_file=True)
        print("Saving config for device ... \n")

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