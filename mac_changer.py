#!/user/bin/env python

import subprocess
import argparse


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
    subprocess.call("ifconfig " + interface + " down", shell=True)
    subprocess.call("ifconfig " + interface + " hw ether " + new_mac, shell=True)
    subprocess.call("ifconfig " + interface + " up", shell=True)


args = get_arguments()
change_mac(args.i, args.m)
