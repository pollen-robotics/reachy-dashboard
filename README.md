# Reachy Access Point

Manages the access point and wifi connection of Reachy version 2021 equipped with a NUC computer running Ubuntu 20.04. Useful to configure Reachy and connect it to a wifi network without having to plug a computer screen, mouse and keyboard...

## Installing RAP on Reachy

Clone the repo and install the python dependencies. You can do this in a [virtual environment](https://pollen-robotics.notion.site/Install-virtualenvwrapper-on-Ubuntu20-04-6ab4212c7300426abfdd39856e26efdc).
```bash
cd ~/dev
git clone https://github.com/pollen-robotics/RAP-2021.git
cd RAP-2021
pip3 install -e .
```
Create a hotspot connection.
```bash
nmcli dev wifi hotspot ifname wlp0s20f3 con-name Reachy-AP ssid Reachy-AP password "Reachy-AP"
```

## Accessing the dashboard
To start RAP:
```bash
cd ~/dev/RAP-2021/dashboard
python3 server.py
```
After that, the dashboard can be accessed locally at http://127.0.0.1:3972 or from any device connected on the same as network as Reachy
at http://<Reachy'ip>:3972.

By default, if Reachy was connected to any wifi network, Reachy's hotspot will be activated. You can connect to the wifi *Reachy-AP* and Reachy will get the static IP 10.42.0.1. The dahsboard can thus be accessed at http://10.42.0.1:3972.

Otherwise, Reachy's IP address can be read on the LCD displayed attached to the robot.

## Using the dashboard

For now, the dahsboard has only one page to handle wifi connection and activate/deactivate Reachy's hotspot. More features are coming.

## Display Reachy's IP address

A Notion page explaining the hardware needed and how to use it to display Reachy's IP address on a LCD screen is available
[here](https://pollen-robotics.notion.site/IP-address-display-7bbfb240aa654248ad8f10bd8b1602ba).

---
