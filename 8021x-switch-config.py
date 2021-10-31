#!/usr/bin/env python
import os

from datetime import datetime
from rich import print as rprint
from rich.table import Table
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result, print_title
from nornir_jinja2.plugins.tasks import template_file
from nornir_netmiko import netmiko_send_command, netmiko_send_config
from myfuncs.imp_funct import get_credentials, read_file, generate_hosts_yaml

# Generate defaults.yaml file with username and password
def generate_defaults_yaml(username, password):
    """Use user credentials to generate defaults.yaml file
    Parameters:
    username - username to SSH to the remote device
    password - password to SSH to the remote device
    Returns:
    """
    # Open (or create and open) defaults.yaml file to store
    # username/password to SSH to devices
    with open('inventory/defaults.yaml', 'w') as default_file:
        default_file.write(f'---\nusername: {username}\npassword: {password}\n')
        default_file.write('...')

def get_access_ports(task):
    # This task runs the 'show interface switchport' command and makes it machine readable through TextFSM templates
    r = task.run(
        name = "Getting switchports",
        task = netmiko_send_command,
        command_string = "show interface switchport",
        use_textfsm = True
    )

    # Create an empty list called 'access_ports' for each host, so we can store our access ports in here
    task.host['access_ports'] = []
    # Loop through all interfaces gathered in the previous task, Finds access port and saves the information to the list
    for interface in r.result:
        if interface['admin_mode'] == "static access":
            task.host['access_ports'].append(dict(interface))
    # Print out all the access ports found for the host to make it more visual
    for access_port in task.host['access_ports']:
        rprint(f"[green][{task.host.name}][/green] Interface [red]{access_port['interface']}[/red] is of type access")


# It generates the configuration using the jinja2 templates for each host or device. 
def generate_config(task, j2path, j2template):
    r = task.run(
        name = "Generating configuration with jinja2 template",
        task = template_file,
        template = j2template,
        path = j2path
    )
    task.host["config"] = r.result

# It Pushes the jinja2 templates for each host or device.
def push_config(task):
    task.run(
        name = "Push jinja2 generated configuration to host",
        task = netmiko_send_config,
        config_commands = task.host["config"].splitlines()
    )

def main():
    """
    Execution begins here
    """
    # The following lines added to make it easy for human users to read
    print('\n' + '*' * 79)
    print('\n       Network automation using NORNIR Automation Framework!!    \n')
    print('*' * 79 + '\n')

    # Get IP addresses of devices you want to connect and generate hosts.yaml file
    devices_txt = input('Please enter .txt file containing IP addresses [devices.txt]: ')\
     or 'devices.txt'
    devices = read_file(devices_txt)
    generate_hosts_yaml(devices, 'inventory/hosts.yaml')

    # Get user credentials from the user
    username, password = get_credentials()

    # Generate 'inventory/defaults.yaml' file containing user credential
    generate_defaults_yaml(username, password)

    # Set the environment variable so Python can find network-to-code templates folder
    os.environ["NET_TEXTFSM"] = "/opt/conda/lib/python3.9/site-packages/ntc_templates/templates"

    # Init Nornir with our config file - You can follow it up with a filter if needed
    nr = InitNornir(config_file="config.yaml")
    
    # Gather all access ports for our devices and print the result
    result_access = nr.run(task = get_access_ports)
    print_result(result_access, vars=["diff","exception"])

    # Generate the configuration for each host, whilst specifying our jinja2 folder and template
    result_gen_config = nr.run(task = generate_config, j2path= "templates/", j2template = "8021x_mon.j2")
    print_result(result_gen_config, vars=["diff","exception"])

    # Push the generated configuration to our hosts
    result_push_config = nr.run(task = push_config)
    print_result(result_push_config, vars=["diff","exception"])

    # Wipe out defaults.yaml file to remove  user credentials and set it as below 
    generate_defaults_yaml('cisco', 'password')

    # Wipe out hosts.yaml file to remove devices IP addresses
    devices = ['1.1.1.1', '2.2.2.2']
    generate_hosts_yaml(devices, 'inventory/hosts.yaml')
  
if __name__ == "__main__":
    # Execute main from here
    main()
    # Freeze screen until any key pressed
    input('Enter any key to exit!!!')
