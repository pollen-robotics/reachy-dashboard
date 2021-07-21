import sys
import time

from subprocess import check_output, PIPE, CalledProcessError

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
    mode = get_connection_mode()
    if mode == 'Wifi':
        return {
            'mode': 'Wifi',
            'SSID': check_output(['iwgetid', '-r']).decode(sys.stdout.encoding).strip(),
        }
    elif mode == 'Hotspot':
        return {
            'mode': 'Hotspot',
            'SSID': 'Reachy-AP',
        }
    elif mode == 'Ethernet':
        return {
            'mode': 'Ethernet',
            'SSID': '',
        }
    return {
        'mode': 'None',
        'SSID': '',
    }


def get_available_wifis():
    if get_connection_mode() == 'Hotspot':
        return ['Reachy-AP']

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


def get_connection_mode():
    con_msg = check_output(['nmcli', 'con', 'show', '--active']).decode().strip()
    if not con_msg:
        return 'None'
    if 'ethernet' in con_msg:
        return 'Ethernet'
    if 'Reachy-AP' in con_msg:
        return 'Hotspot'
    return 'Wifi'


def get_connection_card_info():
    info = {}
    wlan_config = get_wlan_status()

    info['SSID'] = wlan_config['SSID']

    if wlan_config['mode'] == 'Wifi':
        info['level'] = 'success'
        info['icon'] = 'wifi'
        info['title'] = 'WiFi'
        info['message'] = 'Connected'

    elif wlan_config['mode'] == 'None':
        info['level'] = 'error'
        info['icon'] = 'signal_wifi_off'
        info['title'] = 'No connection'
        info['message'] = "No internet connection detected. Reachy's hotspot is off."

    elif wlan_config['mode'] == 'Ethernet':
        info['level'] = 'success'
        info['icon'] = 'settings_ethernet'
        info['title'] = 'Ethernet'
        info['message'] = ''

    else:
        info['level'] = 'warning'
        info['icon'] = 'wifi_tethering'
        info['title'] = 'Hotspot'
        info['message'] = "Reachy's access point is on."

    return info
