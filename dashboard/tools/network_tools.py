"""Network tools for RAP-2021."""
import sys
import time
from serial import Serial

from subprocess import CalledProcessError, check_output, PIPE, Popen, run

from serial.serialutil import SerialException


class NetworkTools:
    def __init__(
            self,
            port: str = '/dev/arduino',
            baudrate: int = 9600,
            timeout: float = 0.01) -> None:

        try:
            self.ser_ip_display = Serial(port=port, baudrate=baudrate, timeout=timeout)
            print(f'Connected to ip displayer board on {port}')
        except SerialException:
            print(f'Could not connect to ip displayer board on {port}')
            pass

    def display_ip(self, ip: str):
        """Display Reachy's IP address on LCD screen."""
        try:
            self.ser_ip_display.write(bytes('<' + ip + '>\n', 'utf8'))
        except:
            pass

    def get_available_wifis(self):
        """List available wifis.

        If the hotspot is turned on, no wifi connection can be seen.
        Hotspot must be turned off to see available wifis.
        """
        if self.get_connection_status()['mode'] == 'Hotspot':
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

    def get_connection_card_info(self):
        """Build info dictionary depending on the connection mode used.

        This info are needed by the html page to build the card showing
        the connection information.
        """
        info = {}
        wlan_config = self.get_connection_status()

        info['SSID'] = wlan_config['SSID']

        if wlan_config['mode'] == 'Wifi':
            info['level'] = 'success'
            info['title'] = 'WiFi'
            info['message'] = 'Connected'

        elif wlan_config['mode'] == 'None':
            info['level'] = 'error'
            info['title'] = 'No connection'
            info['message'] = "Reachy is not connected to any network. Reachy's hotspot is off."

        elif wlan_config['mode'] == 'Ethernet':
            info['level'] = 'success'
            info['title'] = 'Ethernet'
            info['message'] = ''

        else:
            info['level'] = 'warning'
            info['title'] = 'Hotspot'
            info['message'] = "Reachy's access point is on."

        return info

    def get_connection_status(self):
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
        try:
            ssid = check_output(['iwgetid', '-r']).decode(sys.stdout.encoding).strip()
            return {
                'mode': 'Wifi',
                'SSID': ssid,
            }
        except CalledProcessError:
            return {
                'mode': 'Failed_wifi',
                'SSID': '',
            }

    def get_ip(self):
        """Return ip address."""
        connection_mode = self.get_connection_status()['mode']

        process = Popen(['ifconfig'], stdout=PIPE, stderr=PIPE)
        stdout, _ = process.communicate()
        stdout = [part for part in stdout.decode().split()]

        ip_dic = {
            'Hotspot': '10.42.0.1',
            'None': [],
            'Wifi': stdout[[i for (i, p) in enumerate(stdout) if p == 'wlp0s20f3:'][0] + 5],
            'Ethernet': stdout[5]
        }
        return ip_dic[connection_mode]

    def halt(self, delay: int):
        """Halt NUC computer."""
        time.sleep(delay)
        run(['sudo', 'shutdown', 'now'])

    def set_hotspot_state(self, state: str):
        """Turn hotspot on/off.

        Args:
            state: 'on' or 'off'.
        """
        cmd = {'on': 'up', 'off': 'down'}
        run(['nmcli', 'con', cmd[state], 'Reachy-AP'])
        time.sleep(5.0)
        self.display_ip(self.get_ip())

    def setup_new_wifi(self, ssid: str, password: str) -> None:
        """Connect to a new wifi network.

        Forget previous wifi connection and connect to a new one
        using the requested ssid and password.

        Args:
            ssid:
            password: (in plain text)
        """
        former_connection = self.get_connection_status()

        if former_connection['SSID'] == 'Reachy-AP':
            self.set_hotspot_state('off')
        elif former_connection['mode'] == 'Wifi' or former_connection['mode'] == 'Ethernet':
            run(['nmcli', 'con', 'delete', former_connection['SSID']])

        try:
            check_output(['nmcli', 'connection', 'add', 'type', 'wifi', 'ifname', 'wlp0s20f3', 'ssid', ssid, 'con-name', ssid,
                          '+802-11-wireless-security.key-mgmt', 'WPA-PSK', '+802-11-wireless-security.psk', password])
        except CalledProcessError:
            run(['nmcli', 'con', 'delete', ssid])
            self.set_hotspot_state('on')
            return

        time.sleep(4.0)
        if self.get_connection_status()['mode'] == 'Failed_wifi':
            run(['nmcli', 'con', 'delete', ssid])
            self.set_hotspot_state('on')
        self.display_ip(self.get_ip())
