"""Network tools for RAP-2021."""
import sys
import time

from subprocess import check_output, PIPE, Popen, run


def get_available_wifis():
    """List available wifis.

    If the hotspot is turned on, no wifi connection can be seen.
    Hotspot must be turned off to see available wifis.
    """
    if get_connection_status()['mode'] == 'Hotspot':
        return ['Reachy-AP']

    process = Popen(['nmcli', 'dev', 'wifi'], stdout=PIPE, stderr=PIPE)
    stdout, _ = process.communicate()

    net_list = []

    for network_info in stdout.decode().split('\n')[1:-1]:
        if network_info.split('Infra')[0].split()[0] == '*':
            net_list.append(network_info.split('Infra')[0].split()[2:])
        else:
            net_list.append(network_info.split('Infra')[0].split()[1:])

    return list(dict.fromkeys([" ".join(net) for net in net_list]))


def get_connection_card_info():
    """Build info dictionary depending on the connection mode used.

    This info are needed by the html page to build the card showing
    the connection information.
    """
    info = {}
    wlan_config = get_connection_status()

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
        info['message'] = "Reachy's access point is on. Turn it off to connect to wifi."

    return info


def get_connection_status():
    """Return the connection mode used.

    In case of wifi connection, also return the SSID of the connected wifi.
    """
    active_con = check_output(['nmcli', 'con', 'show', '--active']).decode().strip()
    if not active_con:
        return {
            'mode': 'None',
            'SSID': '',
        }
    if 'ethernet' in active_con:
        return {
            'mode': 'Ethernet',
            'SSID': '',
        }
    if 'Reachy-AP' in active_con:
        return {
            'mode': 'Hotspot',
            'SSID': 'Reachy-AP',
        }
    return {
            'mode': 'Wifi',
            'SSID': check_output(['iwgetid', '-r']).decode(sys.stdout.encoding).strip(),
        }


def get_ip():
    """Return ip address."""
    process = Popen(['ifconfig'], stdout=PIPE, stderr=PIPE)
    stdout, _ = process.communicate()
    stdout = stdout.decode().split('wlp0s20f3')[-1]

    connection_mode = get_connection_status()['mode']

    if connection_mode == 'Hotspot':
        ip = stdout[stdout.find('inet ')+5:stdout.find('inet ')+15]
    elif connection_mode == 'None':
        ip = []
    else:
        ip = stdout[stdout.find('inet ')+5:stdout.find('inet ')+18]
    return ip


def halt(delay: int):
    """Halt NUC computer."""
    time.sleep(delay)
    run(['sudo', 'shutdown', 'now'])


def set_hotspot_state(state: str):
    """Turn hotspot on/off.

    Args:
        state: 'on' or 'off'.
    """
    cmd = {'on': 'up', 'off': 'down'}
    run(['nmcli', 'con', cmd[state], 'Reachy-AP'])


def setup_new_wifi(ssid: str, password: str) -> None:
    """Connect to a new wifi network.

    Forget previous wifi connection and connect to a new one
    using the requested ssid and password.

    Args:
        ssid:
        password: (in plain text)
    """
    former_network = get_connection_status()['SSID']

    if former_network == 'Reachy-AP':
        set_hotspot_state('off')
    else:
        run(['nmcli', 'con', 'delete', former_network])
    run(['nmcli', '-ask', 'device', 'wifi', 'connect', ssid, 'password', password])
