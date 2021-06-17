[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/james-sciortino/dna-get-interface-report)

# DNA-Config-Archive-Tool.py

*This code is for the Cisco DNA Center platform and has been tested on all IOS-XE platforms supported by DNA Center, including routers, switches and wireless controllers.*
**Note that AireOS wireless controllers are not supported, because they do not run IOS-XE**

---

# Purpose
**The purpose of this code is to give network engineers a programmatic tool to archive IOS-XE configurations on a daily basis.**

Note:
- This code leverages the DNA Center SDK.
- This code utilizes three DNA Center APIs: 'Get Token', 'Get Device by ID' and 'Get Device Config by ID'.
- Each time this code is run, a folder titled with today's date will be created at the root of your working directory; configurations will be stored within this folder.

# Intended Audience
**This code is intended for network engineers who manage DNA Center, Catalyst switches, and wish to archive all of their IOS-XE configs for any reason!**

For example, imagine the following:
- You have a switch managed by DNA Center.
- The switch fails, and boots without a running configuration.
- You want to restore the running configuration on the switch, but first you need its latest backup.

**Schedule this code to run on a daily basis to generate a backup for your entire DNA Center inventory (exclusing wireless access points).**

# How This Code Works
This code intends to accomplish the following tasks:
1. Call the DNA Center API **Authentication API** with your DNA Center IP address, username, and password to generate an auth-x token for subsequent API calls.
2. Call the DNA Center API **Get device list** to identify all Device UUIDs and hostnames, excluding wireless access points.
3. Call the DNA Center API **Get device config by id**, and pass in the uuid of each device, to iterate through all devices and copy their running config to memory
4. If a folder titled with today's date doesn't already exist at the root of your working, directory, then it will be created.
5. For each device, create a config file titled with the device's hostname, within the folder titled with today's date.
6. To avoid any file extension errors (for example, to avoid create .inc files), any period (".") will be replaced with a hyphen ("-")

# Prerequesites
1. Admin access to a DNA Center appliance, reachable over TCP/443
2. Catalyst switches and routers managed in the DNA Center Inventory.
3. [Python](https://www.python.org/downloads/) installed on your local machine.
4. [pip](https://packaging.python.org/tutorials/installing-packages/) is installed for Python
5. [dnacentersdk](https://dnacentersdk.readthedocs.io/en/latest/index.html) is installed for Python

# Installation Steps

**Bash / Ubuntu / Linux**
1. Clone this repository from a bash terminal:
```console
git clone https://github.com/james-sciortino/dna-get-interface-report.git
```
2. Navigate into the directory:
```console
cd dna-get-interface-report
```
3. Update [config.py](config.py) with your DNA Center information, including: FQDN or management IP address of the DNA Enterprise VIP, port, and credentials. Be sure to update the variable **DNA_SWITCHES** with a *comma-seperated Python list of hostnames for each Catalyst Switch you want to report on.*
```console
nano config.py
```
4. Install the required dependencies specified in [requirements.txt](requirements.txt) from the <dna-get-interface-report> folder:
```console
pip3 install -r requirements.txt 
```
5. Run the code from your cloned git repository:
```console
python main.py
```

# Tutorial

Imagine you have a building on your Campus LAN which the business plans to expand with new users, new cubicles, new Access Points, etc. 

Your manager tasks you with generating a report of *existing* active interfaces on the *existing* switches in the building, to better understand how many new switches are required.
    - The generated report will detail how many *access* ports are used, how many *module* (or, *uplink*) interfaces are used, and how many interfaces are currently available.
    - You will be presented with a PrettyTable in your Bash or PowerShell terminal with this report
    - A.CSV file will be generated with this report, and can be shared with management. 

In the the example below, tThe goal is to scan three Cisco Catalyst switches: Two Catalyst 9300 Series Switches, and one Catalyst 9400 Series Switch. 

```
$ python .\main.py
+------------------------------------------------------------+
Auth Token:  eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2MDJjMGUyODE0NzEwYTIyZDFmN2UxNzIiLCJhdXRoU291cmNlIjoiaW50ZXJuYWwiLCJ0ZW5hbnROYW1lIjoiVE5UMCIsInJvbGVzIjpbIjYwMmJlYmU1MTQ3MTBhMDBjOThmYTQwOSJdLCJ0ZW5hbnRJZCI6IjYwMmJlYmU1MTQ3MTBhMDBjOThmYTQwMiIsImV4cCI6MTYyMzg5NjAwNCwiaWF0IjoxNjIzODkyNDA0LCJqdGkiOiI5MDRjOWNiNi0xZWQzLTQzZDYtYTM5YS1mZTQ3OGU2ZGExOTUiLCJ1c2VybmFtZSI6ImRldm5ldHVzZXIifQ.jPvAA2WGWUVtD3z8g97StSwvkThMxR3uWA0HjIr2CLF1F0cd4eto522lVRuDcNl7xlJYnE0kX-0FxzirLJQi33QdDlOp9ZvLaRdtHv3jmnOw_vpJTKA1It93Kz2ANxqS4KhjJKUR25rw5LgibKmAOC22MnZZXZuw3-CtKpRK1fJN4ooBaome7Ix-ZsOuVcV6HTjGZHd1Qb0IuRK7BoyYYGkouMF1ne7lbbBd8SlcBLzJdC-yt0FRGcdrgf7Kfpunw6ZMyNlVsVTcUQr9tsWo_yxkO4bXsZ61jaA4p5efc2J3GP3VJlJKWHgHVXSU4fabp99Tilg3JKos53s7FFJuiA
+------------------------------------------------------------+
Gathering Device Info ...
+------------------------------------------------------------+
Device Hostname: asr1001-x.abc.inc 
Executing Command on 6aad2ec7-d1d0-4605-bf32-f62266c5f53e
Archiving Running Configuration ... 
+------------------------------------------------------------+
Device Hostname: cs3850.abc.inc
Executing Command on 5d6dd65b-eb43-4e28-bd31-e6b0730b2ac5
Archiving Running Configuration ... 
+------------------------------------------------------------+
Folder named 06-16-21 created in <built-in function getcwd>.
 Running configuration for the following devices have been archived:

1 asr1001-x.abc.inc
2 cs3850.abc.inc

+------------------------------------------------------------+
```

# FAQ 
1. What is the purpose of each file?
    - [.env](.env) - Contains DNA Center info, including DNA Center FQDN, username and password.
    - [main.py](main.py) - Primary code. This is the file you execute to run this code. 

2. How do I properly modify [.env](.env) with the appropriate information? 
    - **DNA_CENTER_BASE_URL** = **IP address** or **FQDN** of your DNA Center's Enterprise VIP**
    - **DNA_CENTER_USERNAME** =  **Username** with **SUPER-ADMIN-ROLE** permissons on your DNA Center controller.
    - **DNA_CENTER_PASSWORD** = **Password** of your **Username** with **SUPER-ADMIN-ROLE** permissons on your DNA Center controller.
    - **DNA_CENTER_VERSION** = The version of DNA Center you are currently using. Needed for the dnacentersdk. If you're unsure, leave this at **2.1.1**
    - **DNA_CENTER_DEBUG** =  Do not modify. Leave this set to **False**
    - **DNA_CENTER_SINGLE_REQUEST_TIMEOUT=** = Do not modify. Leave this set to **60**. 
    - **DNA_CENTER_WAIT_ON_RATE_LIMIT** = Do not modify. Leave this set to **True**. 

# Authors
Please contact me with questions or comments.
- James Sciortino - james.sciortino@outlook.com

# License
This project is licensed under the terms of the MIT License.