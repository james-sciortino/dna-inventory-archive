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
+---------------------------------------------+
Geting DNA Auth Token ...
Your token is [shown here]
+---------------------------------------------+
Searching DNA Center Inventory for the following switches: ['switch1', 'switch2', 'switch3']...
Detailed interface output stored in flash memory
+---------------------------------------------+
Creating .CSV Template...
Generating detailed report for each switch..
+---------------------------------------------+
+--------------------------------------+-----------------+-----------------+-----------------+----------------+------------------+-------------+
|       Switch Name      |   Switch Model  | UP Access Ports | UP Module Ports | Total UP Ports | Total DOWN Ports | Total Ports |
+--------------------------------------+-----------------+-----------------+-----------------+----------------+------------------+-------------+
|         switch1        |      C9410R     |        3        |        1        |       4        |        54        |      58     |
|         switch2        | C9300L-48UXG-4X |        3        |        0        |       3        |        49        |      52     |
|         switch3        | C9300L-48UXG-4X |        3        |        0        |       3        |        49        |      52     |
+--------------------------------------+-----------------+-----------------+-----------------+----------------+------------------+-------------+
+---------------------------------------------+
Generating .CSV Report...
CSV report created in working directory: port-report-06-02-21.csv
```

# FAQ 
1. What is the purpose of each file?
    - [config.py](config.py) - Contains DNA Center info and API calls, as strings.
    - [main.py](main.py) - Primary code. This is the file you execute to run this code. 

2. Does this code use NETCONF, RESTCONF, or both?

    - This code leverages **RESTCONF** APIs and **YANG** data models only. **NETCONF** is not used.

3. How do I enable RESTCONF on my Catalyst switches?
    - These API calls are not sent directly to your Catalyst switches. Instead, each API GET request is sent to the DNA Center controller only. 
    -  DNA Center is the central management server for all of these switches, and it already has the interface information we need!

4. How do I properly modify [config.py](config.py) with the appropriate information? 


- **DNA_FQDN ** = **IP address** or **FQDN** of your DNA Center's Enterprise VIP**
- **DNA_PORT** = Port used for **RESTCONF** API calls on DNA. Default is **443**
- **DNA_USER** =  **Username** with **SUPER-ADMIN-ROLE** permissons on your DNA Center controller.
- **DNA_PASS** = **Password** of your **Username** with **SUPER-ADMIN-ROLE** permissons on your DNA Center controller.
- **DNA_SWITCHES** = A comma-seperated list of Catalyst switch **hostnames** *that you want to include in your report.
    - This variable is a Python list, and each **hostname** is a string. 
    - For example, if you want a report on three switches - named switch1, switch2 and switch3 - the **DNA_SWITCHES** variable would be equal to *["switch1", "switch2", "switch3"]*

*NOTE: Do not modify any of the API calls below the line **# DNA API Calls*** in [config.py](config.py)

# Authors
Please contact me with questions or comments.
- James Sciortino - james.sciortino@outlook.com

# License
This project is licensed under the terms of the MIT License.