import sys
import subprocess
import xml.etree.ElementTree as ET
import os
from termcolor import colored
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import re
from contextlib import contextmanager
import copy
from itertools import permutations, islice
import nmap_classes


def banner():
    print(colored("""\
	
	
 $$$$$$\  $$\                                     $$\   $$\                                   
$$  __$$\ $$ |                                    $$$\  $$ |                                  
$$ /  \__|$$ | $$$$$$\   $$$$$$\  $$$$$$$\        $$$$\ $$ |$$$$$$\$$$$\   $$$$$$\   $$$$$$\  
$$ |      $$ |$$  __$$\  \____$$\ $$  __$$\       $$ $$\$$ |$$  _$$  _$$\  \____$$\ $$  __$$\  """,'red',attrs=['bold']), end=' ')
    print(colored("    Colourful Nmap Parser",'white'))
    print(colored("""\
$$ |      $$ |$$$$$$$$ | $$$$$$$ |$$ |  $$ |      $$ \$$$$ |$$ / $$ / $$ | $$$$$$$ |$$ /  $$ | """,'white',attrs=['bold']), end=' ')
    print(colored("    Designed For Kali Linux",'white'))
    print(colored("""\
$$ |  $$\ $$ |$$   ____|$$  __$$ |$$ |  $$ |      $$ |\$$$ |$$ | $$ | $$ |$$  __$$ |$$ |  $$ | """,'blue',attrs=['bold']), end=' ')
    print(colored("    Author: Chance Bowers",'green'))
    print(colored("""\
\$$$$$$  |$$ |\$$$$$$$\ \$$$$$$$ |$$ |  $$ |      $$ | \$$ |$$ | $$ | $$ |\$$$$$$$ |$$$$$$$  | """,'red',attrs=['bold']), end=' ')
    print(colored("    glitchingreality.github.io",'white', attrs=['underline']))
    print(colored("""\
 \______/ \__| \_______| \_______|\__|  \__|      \__|  \__|\__| \__| \__| \_______|$$  ____/ 
                                                                                    $$ |      
                                                                                    $$ |      
                                                                                    \__|     """,'red',attrs=['bold']))


from termcolor import colored

def colorful_banner():
    word = "Colorful Nmap Parser"

    for letter in word:
        # Assign a unique color to each letter
        if letter.lower() == 'c':
            print(colored(letter, 'red', attrs=['bold']), end=' ')
        elif letter.lower() == 'o':
            print(colored(letter, 'green', attrs=['bold']), end=' ')
        elif letter.lower() == 'l':
            print(colored(letter, 'yellow', attrs=['bold']), end=' ')
        elif letter.lower() == 'o':
            print(colored(letter, 'blue', attrs=['bold']), end=' ')
        elif letter.lower() == 'r':
            print(colored(letter, 'magenta', attrs=['bold']), end=' ')
        elif letter.lower() == 'f':
            print(colored(letter, 'cyan', attrs=['bold']), end=' ')
        elif letter.lower() == 'u':
            print(colored(letter, 'cyan', attrs=['bold']), end=' ')
        elif letter.lower() == 'n':
            print(colored(letter, 'red', attrs=['bold']), end=' ')
        elif letter.lower() == 'p':
            print(colored(letter, 'cyan', attrs=['bold']), end=' ')
        elif letter.lower() == 'a':
            print(colored(letter, 'yellow', attrs=['bold']), end=' ')
        elif letter.lower() == 'm':
            print(colored(letter, 'green', attrs=['bold']), end=' ')
        else:
            # Handle spaces or other characters
            print(letter, end=' ')

    print()  # Add a newline at the end

# Call the colorful_banner function
colorful_banner()

def launch_nmap():
    banner()
    path = os.path.dirname(os.path.realpath(__file__))
    res_folder = path + "/results/"
    try:
        os.makedirs(os.path.dirname(res_folder))
    except Exception as e:
        pass
    params = " -oA '" + res_folder + "nmap_scan'"
    nmap_command = input("Please Enter Nmap Command: ")
    nmap_output = subprocess.check_output(nmap_command + params, shell=True)  # run the command in the terminal
    nmap_parser(res_folder)
    display_original_nmap(nmap_output)

def nmap_parser(path):
    target_file = path + "nmap_scan.xml"
    tree = ET.parse(target_file)
    root = tree.getroot()
    host_details = []

    # Get scripts
    for hosts in root.iter('host'):
        host_os = ""
        for addresses in hosts.iter('address'):
            address = addresses.get('addr')
            hostname = address
            break

        for os in hosts.iter('osmatch'):
            host_os = os.get('name')
        host = nmap_classes.Host_Details(hostname, host_os)
        for port in hosts.iter('port'):
            protocol = port.get('protocol')
            portid = port.get('portid')
            for state in port.iter('state'):
                status = state.get('state')
            for service in port.iter('service'):
                name = service.get('name')
                product = service.get('product')
                if product is not None and "httpd" in product:
                    product = product.strip("httpd")
                    product = product.strip()
                version = service.get('version')
                extra_info = service.get('extrainfo')
                tunnel = service.get('tunnel')
                host_services = nmap_classes.Scan_Information(protocol, portid, status, name, product, version,
                                                               extra_info, tunnel)
                for script in port.iter('script'):
                    script_id = script.get('id')
                    script_output = script.get('output')
                    script_information = nmap_classes.Script_Information(script_id, script_output)
                    host_services.script_info.append(script_information)
                host.scan_information.append(host_services)
        host_details.append(host)

    for host in host_details:
        print(colored("\n{}: {} {}".format('Host', host.hostname, host.host_os), 'green', attrs=['bold']), end=' ')
        for service in host.scan_information:
            script_signal = 0
            print(colored("\n{: <8} {: <8} {: <8} {: <15} {: <15} {: <3}".format("PORT", "STATE", "SERVICE", "VERSION", "EXTRA INFO", "SSL"), 'cyan'))
            if service.version is not None:
                print(colored("{: <8} {: <8} {: <8} {: <15} {: <15} {: <3}".format(
                    service.port + "/" + service.protocol if service.port else '',
                    service.state if service.state else '',
                    service.service if service.service else '',
                    "{} {}".format(service.product, service.version) if service.product and service.version else service.product,
                    service.extra_info if service.extra_info else '',
                    service.tunnel if service.tunnel else ''
                ), 'yellow'))
            else:
                print(colored("{: <8} {: <8} {: <8} {: <15} {: <15} {: <3}".format(
                    service.port + "/" + service.protocol if service.port else '',
                    service.state if service.state else '',
                    service.service if service.service else '',
                    "{} {}".format(service.product, service.version) if service.product and service.version else service.product,
                    service.extra_info if service.extra_info else '',
                    service.tunnel if service.tunnel else ''
                ), 'yellow'))

            for script in service.script_info:
                script.script_name = script.script_name.strip()
                output = script.script_output.splitlines()
                while '' in output:
                    output.remove('')
                print(colored("\tScript ID:", 'magenta'), end=' ')
                print(colored("{} ".format(script.script_name), 'white'))
                for line in output:
                    print(colored("\t\t    | {}".format(line.strip()), 'white'))
                print("\n", end=' ')

@contextmanager
def custom_redirection(fileobj):
    old = sys.stdout
    sys.stdout = fileobj
    try:
        yield fileobj
    finally:
        sys.stdout = old

def display_original_nmap(nmap_output):
    PIPE_PATH = "/tmp/my_pipe"
    if not os.path.exists(PIPE_PATH):
        os.mkfifo(PIPE_PATH)

    subprocess.Popen(['qterminal', '--tab', '--', '/bin/bash', '-c', 'tail -n +1 --follow {0}'.format(PIPE_PATH)])  # Will write all output to this terminal
    with open(PIPE_PATH, "w") as p:
        with custom_redirection(p):
            print(nmap_output)

launch_nmap()
