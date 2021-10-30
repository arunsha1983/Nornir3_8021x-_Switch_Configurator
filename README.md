# Nornir 8021x Switch Configurator
Automate 802.1x Cisco Switch Configuration using Nornir Automation Framework

Author: Arun Shankaralingam
Github : https://github.com/arunsha1983/Nornir3_8021x-_Switch_Configurator

# Nornir 8021x Switch Configurator Use Case

- Each device in device.txt we will gather switchport details with TextFSM and Filter only the access ports
- After gathering access ports will generate configuration for each device using jinja2 template
- Push the generated configuration to each device that is Global and Interface configutions(Only Access Ports)

## Overview of the files
This script is built around Nornir 3.1 and with various plugins. For ease of use i have used Meheretab Mengistu MyFunction module to get username and password to generate it in the inventory defaults.yaml file.

1. Inventory ==> It contains all the Files needed for the Nornir ######### Do NOT MODIFY #########
    - defaults.yaml   ---> can be left empty, but must be present as a file 
    - groups.yaml     ---> is used to group your hosts an provide a plattform info (used for authentication)
    - hosts.yaml      ---> is used to put in the hosts you want to run the scripts against in yaml format
2. myfuncs ==> A package of functions written by Meheretab Mengistu to create Nornir Inventory Files automatically based on devices.txt. ######### Do NOT MODIFY #########
    - imp_funct.py ---> Multiple common functions to create a username and password and hosts for the Inventory files easily.
3. templates ==> This folder contains jinja2 template file used for switch global and interface 802.1x configurations.
4. 8021x-switch-config.py ==> Python Scipt used for this Nornir 8021x Switch Configurator
    - generate_defaults_yaml ---> Generate defaults.yaml file with username and password
    - get_access_ports ---> This task runs the 'show interface switchport' command and makes it machine readable through TextFSM templates.Prints the access ports.
    - generate_config ---> It generates the configuration using the jinja2 templates for each host or device.
    - push_config ---> It Pushes the jinja2 templates for each host or device.
    - main --> It is the mail function written to run the above tasks  
5. config.yaml ==> A configuration file is used to indicate the location of the inventory files as well as the plugin type being utilized for the Nornir
5. devices.txt ==> This file contians the IP addresses of network equipments you need to SSH.
6. Nornir.log ==> Nornir log File 
7. requirement.txt ==> It provides all the depencies installed for this script to work
 

## Built With
Pleae use NORNIR Version 3.1 and Python Version must be at least v3.6.8
Following Packtes, Modules and Requirements are needed:
    
    nornir==3.1.1
    nornir-jinja2==0.2.0
    nornir-netmiko==0.1.2
    nornir-utils==0.1.2
    ntc-templates==2.3.2
    paramiko==2.8.0
    
For more informations see ---> https://github.com/nornir-automation/nornir

If you are using the code in a Python virtual Environment use the "pip3 freeze -r requirements.txt" to install all the dependencies.

# Running the Nornir 8021x Switch Configurator

There are several options for running this Nornir 8021x Switch Configurator the preferred option is as below

1. Pull the docker image  and run it in your computer/server docker container. It is best as it will contains all dependencies and work without any issues.
2. Clone the Github Repository and running the code on a computer/server with Python Virtual Environment.

### Run the Docker

**Pre-requesites**

1. Docker installed in Windows or Linux machine
2. Basic knowledge on Dockers - https://www.youtube.com/watch?v=zJ6WbK9zFpI 


**Step 1 - Download the repository**

Choose a path of your liking and clone the GitHub repositoy in this path:
`git clone https://github.com/brammeskens/nornir_config_access_ports.git`

**Step 2 - Create your Python virtual environment**

It's generally cleaner to use Python virtual environments as each virtual environment has its own Python binary and independent packages. So we will create one:
`python3 -m venv nornir_config_access_ports`

**Step 3 - Activate your Python virutal environment**

After the creation of the virtual environment, we should activate it so we can actually make use of it:
```
cd nornir_config_access_ports
source bin/activate
```

**Step 4 - Install the dependencies**

Let's install the dependencies with the requirements.txt file from the repo:
`pip3 install -r requirements`

**Step 5 - Create your Nornir 3 inventory**

General usage of Nornir is required. Please see [nornir.tech](https://nornir.tech) or [nornir-automation](https://github.com/nornir-automation/nornir/). Example files have already been supplied at the _inventory_ folder. Alter these files to match your environment:
```
inventory/defaults.yaml
inventory/groups.yaml
inventory/hosts.yaml
```

**Step 6 - Filter your Nornir 3 inventory to your liking**

It's a good idea to start small and not run your script on your whole inventory. That's where Nornir 3's filtering comes into play. In case you would like to filter your hosts based on their parent group, you may want to add the following code after Nornir initialization (line _54_):
`nr = nr.filter(F(has_parent_group='afg'))`
For further Nornir 3 filtering examples and practice see [Nornir 3 Filtering Demo](https://developer.cisco.com/codeexchange/github/repo/writememe/nornir-filtering-demo).

**Step 7 - Change the jinja2 template to the configuration you want**

Alter the jinja2 template file located at _templates/8021x_mon.j2_ or create a new jinja2 file to your liking in the folder. In our example _8021x_mon.j2_ file you will find a general part of the configuration we want to send to the host (change it as needed). Next you will find a section to generate the specific configuration to the access ports:
```
{% for i in host["access_ports"] %}
interface {{i['interface']}}
authentication event fail action next-method
authentication event server dead action authorize
authentication event server dead action authorize voice
authentication event server alive action reinitialize
authentication host-mode multi-domain
authentication open
authentication order dot1x mab
authentication priority dot1x mab
authentication port-control auto
authentication periodic
authentication timer reauthenticate server
authentication violation replace
mab
dot1x pae authenticator
dot1x timeout tx-period 8
spanning-tree portfast
!
{% endfor %}
```
Your custom access port configuration should be inserted between `interface {{i['interface']}}` and `!`. If your have changed the template's name or are using a new jinja2 template file, alter the name at line _64_ next to _j2template=_:
`    result_gen_config = nr.run(task = generate_config, j2path= "templates/", j2template = "8021x_mon.j2")`

**Step 8 - Run the script**

You should be ready to run the script now. If you feel uncertain about the _push_config_ task, we advise you to comment out lines _68_ and _69_ by inserting _#_ at the beginning of the line before you run the script. To run the script you simply enter:
`python3 config_access_ports.py`
The script will prompt you for the user's (defined in _inventory/defaults.yaml_) password and will run the following tasks by default:
```
get_access_ports
generate_config
push_config
```

As always, **test** your changes to a demo host in a lab environment **before** actually using it in a production environment.



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

