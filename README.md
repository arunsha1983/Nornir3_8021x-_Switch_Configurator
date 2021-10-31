# Nornir 8021x Switch Configurator
Automate 802.1x Cisco Switch Configuration using Nornir Automation Framework

Author: Arun Shankaralingam

Github: https://github.com/arunsha1983/dot1x-Switch-Configurator

# Nornir 8021x Switch Configurator Use Case

- Each device in device.txt we will gather switch port details with TextFSM parsing and Filter only the access ports
- After gathering access ports will generate a configuration for each device using the jinja2 template
- Push the generated DOT1X configuration to each device that is Global and Interface level configurations (Only to Access Ports)

## Overview of the files
This script is built around Nornir 3.1 and with various plugins. For ease of use, I have used the Meheretab Mengistu MyFunction module to get a username and password to generate it in the inventory defaults.yaml file.

1. Inventory ==> It contains all the Files needed for the Nornir ######### Do NOT MODIFY #########
    - defaults.yaml   ---> can be left empty, but must be present as a file 
    - groups.yaml     ---> is used to group your hosts and provide platform info (used for authentication)
    - hosts.yaml      ---> is used to put in the hosts you want to run the scripts against in yaml format
2. myfuncs ==> A package of functions written by Meheretab Mengistu to create Nornir Inventory Files automatically based on devices.txt. ######### Do NOT MODIFY #########
    - imp_funct.py ---> Multiple common functions to create a username and password and hosts for the Inventory files easily.
3. templates ==> This folder contains the jinja2 template file used for switch global and interface 802.1x configurations.
4. 8021x-switch-config.py ==> Python Script created for this Nornir 8021x Switch Configurator
    - generate_defaults_yaml ---> Generate defaults.yaml file with username and password
    - get_access_ports ---> This task runs the 'show interface switch port command and makes it machine-readable through TextFSM templates. Prints the access ports.
    - generate_config ---> It generates the configuration using the jinja2 templates for each host or device.
    - push_config ---> It Pushes the jinja2 templates for each host or device.
    - main --> It is the mail function written to run the above tasks  
5. config.yaml ==> A configuration file is used to indicate the location of the inventory files as well as the plugin type being utilized for the Nornir Initiation
5. devices.txt ==> This file contains the IP addresses of network switches.
6. Nornir.log ==> Nornir log File 
7. requirement.txt ==> It provides all the dependencies installed for this script to work
 

## Built With
Please use NORNIR Version 3.1 and Python Version must be at least v3.6.8
Following Packets, Modules and Requirements are needed and all other dependencies are in the 'requirements.txt'
    
    nornir==3.1.1
    nornir-jinja2==0.2.0
    nornir-netmiko==0.1.2
    nornir-utils==0.1.2
    ntc-templates==2.3.2
    paramiko==2.8.0
    
For more information see ---> https://github.com/nornir-automation/nornir

# Running the Nornir 8021x Switch Configurator

There are several options for running this Nornir 8021x Switch Configurator the preferred option is as below

1. Pull the docker image and run it in your computer/server docker container. It is best as it will contain all dependencies and work without any issues.
2. Clone the Github Repository and run the code on a computer/server with Python Virtual Environment. Install requirements.txt then run the python script

If you are cloning the Github repository to your Python virtual Environment use the `pip3 freeze -r requirements.txt` to install all the dependencies.

Note: As always, **test** your changes to a demo host in a lab environment **before** using it in a production environment.

### Run the Docker

**Pre-requesites**

1. Docker installed in Windows or Linux machine
2. Basic knowledge on Dockers - https://www.youtube.com/watch?v=zJ6WbK9zFpI 

**Step 1 - Download the docker image to your machine**

`docker pull arunsha/dot1x-switch-configurator:latest`

**Step 2 - Run the Docker image in your machine**

Command will run the docker image dot1x-switch-configurator. It Exposes port 2022 for outside and uses port 22 inside the container.

`docker run -p 2002:22 dot1x-switch-configurator`

**Step 3 - SSH to your Docker Machine using your favorite tool**

SSH into your Docker running machine using port 2022 to login into the dot1x-switch-configurator use below credentials.

Username : `test`
Password : `test`

See image here ![image](https://user-images.githubusercontent.com/60428178/139592667-696419f0-dd90-4348-b765-4cce55155a8e.png)

**Step 4 - Update your Device list**

`nano devices.txt` --> Update your Targeted switch Device IP addresses
`Ctrl+O` --> To Save the device.txt file
`Ctrl+X` --> To exit the Nano editor

See image here ![image](https://user-images.githubusercontent.com/60428178/139592698-d09136d4-7f14-41eb-a6da-f3c4f6f98ec0.png)

**Step 5 - Change the jinja2 template to the configuration you want**

The current jinja2 template file located at _templates/8021x_mon.j2_is an example. You can update the file with your configurations or create a new jinja2 file.

`cd templates/`  --> To get to the tempaltes folder
`nano 8021x_mon.j2` --> Update the Existing Jinja2 template for Global and Interface configurations
`Ctrl+O` --> To Save the 8021x_mon.j2 file
`Ctrl+X` --> To exit the Nano editor

Your Interface access port configuration should be inserted between `interface {{i['interface']}}` and `!`. If your have changed the template's name or are using a new jinja2 template file, alter the name at line_97_ next to _j2template=_:
` result_gen_config = nr.run(task = generate_config, j2path= "templates/", j2template = "8021x_mon.j2")`

See image here ![image](https://user-images.githubusercontent.com/60428178/139592864-50e4e86f-2a07-4cc0-bd0b-bcb8ba518dbe.png)

**Step 6 - Run the script**

You should be ready to run the script now for your devices. To run the script you simply enter:

`python3 8021x-switch-config.py`

The script will prompt you for the users to confirm that they updated the devices.txt file and ask for the username and password to execute the script. See the output result for the script in the image here. ![image](https://user-images.githubusercontent.com/60428178/139593524-e94a9403-5528-4d2c-b68e-4b68803ce150.png)

Switch Configuration results:

![image](https://user-images.githubusercontent.com/60428178/139593450-d90584b4-58d8-4300-a58b-3d4cf81ae27d.png)

## Learning
Nornir Related Learning

 [nornir.tech](https://nornir.tech) or [nornir-automation](https://github.com/nornir-automation/nornir/)

Related DevNet Sandbox:

[IOS XE on Catalyst 9000](https://devnetsandbox.cisco.com/RM/Diagram/Index/98d5a0fb-1b92-4b5b-abf6-a91e0ddba241?diagramType=Topology)

Python introduction Learning Labs:

[Intro Python: Part 1](https://developer.cisco.com/learning/lab/intro-python-part1/step/1)

[Intro Python - Part 2](https://developer.cisco.com/learning/lab/intro-python-part2/step/1)

Get to know jinja2 templating:

[NAPALM with Templates](https://developer.cisco.com/learning/lab/napalm_with_templates/step/1)

Related solutions on DevNet Ecosystem Exchange:

[Nornir 3 Filtering Demo](https://developer.cisco.com/codeexchange/github/repo/writememe/nornir-filtering-demo)

[Nornir3_802.1x_configuration](https://github.com/nouse4it/Nornir3_802.1x_configuration)
