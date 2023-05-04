# Reachy Dashboard

Web page developed to give an overview of the state of your Reachy (which motors are detected, what services are running, what are the motors temperatures…) as well as giving you the possiblity to access quickly some features (changing a robot’s part compliance for example).

This tool has been thought to help you start easier with the robot and facilitate quick debugging.

## Installing RAP on Reachy

Clone the repo and install the python dependencies.
```bash
cd ~/dev
git clone https://github.com/pollen-robotics/reachy-dashboard.git
cd reachy-dashboard
pip3 install -e .
```
Create a hotspot connection.
```bash
nmcli dev wifi hotspot ifname wlp0s20f3 con-name Reachy-AP ssid Reachy-AP password "Reachy-AP"
```

## Accessing the dashboard
To start the dashboard:
```bash
cd ~/dev/reachy-dashboard/dashboard
python3 server.py
```
After that, the dashboard can be accessed locally at http://127.0.0.1:3972 or from any device connected on the same as network as Reachy
at http://<Reachy'ip>:3972.

By default, if Reachy was connected to any wifi network, Reachy's hotspot will be activated. You can connect to the wifi *Reachy-AP* and Reachy will get the static IP 10.42.0.1. The dahsboard can thus be accessed at http://10.42.0.1:3972.

Otherwise, Reachy's IP address can be read on the LCD displayed attached to the robot.

## Using the dashboard

Check out the [dashboard documentation page](https://docs.pollen-robotics.com/dashboard/introduction/introduction/) to learn what you can do with it!

## Display Reachy's IP address

A Notion page explaining the hardware needed and how to use it to display Reachy's IP address on a LCD screen is available
[here](https://pollen-robotics.notion.site/IP-address-display-7bbfb240aa654248ad8f10bd8b1602ba).

---
