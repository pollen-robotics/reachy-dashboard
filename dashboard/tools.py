import re
import sys
import time

from subprocess import check_output, Popen, PIPE, CalledProcessError, call
from threading import Thread

import subprocess


def setup_new_wifi(ssid: str, password: str) -> None:
    former_network = get_wlan_status()['SSID']
    
    if former_network == 'Reachy-AP':
        set_hotspot_state('off')
    else:
        subprocess.run(['nmcli', 'con', 'delete', former_network])
    subprocess.run(['nmcli', '-ask', 'device', 'wifi', 'connect', ssid, 'password', password])


def set_hotspot_state(state: str):
    cmd = {'on': 'up', 'off': 'down'}
    subprocess.run(['nmcli', 'con', cmd[state], 'Reachy-AP'])

def get_ip():
    process = subprocess.Popen(['ifconfig'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, _ = process.communicate()
    stdout = stdout.decode().split('wlp0s20f3')[-1]

    if get_wlan_status()['SSID'] == 'Reachy-AP':
        ip = stdout[stdout.find('inet ')+5:stdout.find('inet ')+15]
    else:
        ip = stdout[stdout.find('inet ')+5:stdout.find('inet ')+18]
    return ip

def get_wlan_status():
    try:
        ssid = check_output(['iwgetid', '-r']).decode(sys.stdout.encoding).strip()
        mode = 'DHCP'
    except CalledProcessError:
        ssid = 'Reachy-AP'
        mode = 'Hotspot'

    return {
        'mode': mode,
        'SSID': ssid,
    }

def get_available_wifis():
    process = subprocess.Popen(['nmcli', 'dev', 'wifi'], stdout=PIPE, stderr=PIPE)
    stdout, _ = process.communicate()

    net_list = []

    for network_info in stdout.decode().split('\n')[1:-1]: 
        if network_info.split('Infra')[0].split()[0] == '*': 
            net_list.append(network_info.split('Infra')[0].split()[2:]) 
        else: 
            net_list.append(network_info.split('Infra')[0].split()[1:]) 

    return list(dict.fromkeys([" ".join(net) for net in net_list]))

def halt(delay: int):
    time.sleep(delay)
    subprocess.run(['sudo', 'shutdown', 'now'])
