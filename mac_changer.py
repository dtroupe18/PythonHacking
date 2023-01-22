#!/user/bin/env python

import re
import argparse
import subprocess


def get_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", required=True, help="Interface to change the MAC address for")
    parser.add_argument("-m", required=True, help="new MAC address")

    arguments = parser.parse_args()

    if not arguments.i:
        parser.error("[-] Please specify an interface, use --help for more info.")
    elif not arguments.m:
        parser.error("[-] Please specify a new MAC address, use --help for more info.")

    return parser.parse_args()


def change_mac(interface, new_mac):
    print("[+] Changing the MAC address for " + interface + " to " + new_mac)

    # This call could be high jacked. For example entering "eth0;ls"
    # for interface above.
    # Ref - https://knowledge-base.secureflag.com/vulnerabilities/code_injection/os_command_injection_python.html

    # subprocess.call("ifconfig " + interface + " down", shell=True)
    # subprocess.call("ifconfig " + interface + " hw ether " + new_mac, shell=True)
    # subprocess.call("ifconfig " + interface + " up", shell=True)

    subprocess.run(['ifconfig', interface, 'down'], shell=False)
    subprocess.run(['ifconfig', interface, 'hw', 'ether', new_mac], shell=False)
    subprocess.run(['ifconfig', interface, 'up'], shell=False)


def get_current_mac_address(interface):
    result = subprocess.run(['ifconfig', interface], capture_output=True, text=True)
    # REGEX helper https://pythex.org/
    current_mac_search_result = re.search(r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w', result.stdout)

    if current_mac_search_result:
        return current_mac_search_result.group(0)
    else:
        raise Exception('[-] Could not read current MAC address for interface ' + interface)


args = get_arguments()
initial_mac_address = get_current_mac_address(args.i)
print('Current MAC address ' + initial_mac_address)
change_mac(args.i, args.m)
new_mac_address = get_current_mac_address(args.i)

if new_mac_address == args.m:
    print('[+] MAC address was successfully changed to ' + new_mac_address)
else:
    print('[-] Failed to update MAC address!')



