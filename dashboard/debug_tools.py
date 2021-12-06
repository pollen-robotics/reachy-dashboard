import os
from os import path

import numpy as np
import ast
from datetime import datetime

import reachy_pyluos_hal
from reachy_pyluos_hal.config import load_config

from reachy_controllers.joint_state_controller import get_reachy_model


ros_log_path = path.expanduser('~') + '/.ros/log'
host_name = os.uname().nodename


def from_datetime_to_str(dt: datetime):
    year = str(dt.year)
    month = str(dt.month)
    day = str(dt.day)
    hour = str(dt.hour)
    minute = str(dt.minute)
    second = str(dt.second)

    if len(month) == 1:
        month = '0' + month

    if len(day) == 1:
        day = '0' + day

    if len(hour) == 1:
        hour = '0' + hour

    if len(minute) == 1:
        minute = '0' + minute

    if len(second) == 1:
        second = '0' + second

    return year + '-' + month + '-' + day + '-' + hour + '-' + minute + '-' + second


def get_latest_log_folders():
    log_folders_list = [file[0] for file in os.walk(ros_log_path)][1:]
    dates = [f.split('log/')[1].split(host_name)[0] for f in log_folders_list]

    times = []

    for d in dates:
        d_int = [int(component) for component in d.split('-')[:6]]
        year, month, day, hour, min, sec = d_int
        times.append(datetime(year, month, day, hour, min, sec))

    times.sort()
    latest_date = times[-1]

    for f in log_folders_list:
        if from_datetime_to_str(latest_date) in f:
            return f

def get_required_containers(empty_values: bool = False):
    required_parts_cards = {}

    first_piece_to_part = {
        'l_shoulder_pitch': 'left_arm',
        'r_shoulder_pitch': 'right_arm',
        'neck': 'head',
    }

    fan_types = [reachy_pyluos_hal.fan.DxlFan, reachy_pyluos_hal.fan.OrbitaFan]

    config = load_config(config_name=get_reachy_model())

    for part in config:
        if empty_values:
            required_containers = []
        else:
            required_containers = {
                part_name: [value.__module__, value.id] for (part_name, value) in part.items() if type(value) not in fan_types
            }

        first_piece = list(part.keys())[0]
        required_parts_cards[first_piece_to_part[first_piece]] = required_containers

    return required_parts_cards

def get_missing_containers():
    with open(get_latest_log_folders() + '/launch.log') as log_file:
        logs = log_file.readlines()

    missing_container_msg = 'reachy_pyluos_hal.reachy.MissingContainerError'

    try:
        missing_msg = [log for log in logs if missing_container_msg in log][0]
    except IndexError:
        return get_required_containers(empty_values=True)

    str_dct = missing_msg.split('devices ')[1].split('!')[0]
    dct = ast.literal_eval(str_dct)
    return dct


def get_missing_containers_names():
    missing_names = {}

    required_containers = get_required_containers()
    missing_containers = get_missing_containers()

    for robot_part, miss_cont in list(missing_containers.items()):
        list_miss_names = []

        if miss_cont:
            for container in miss_cont:
                miss_value = [list(container.keys())[0], list(container.values())[0]]

                for cont_name, cont_value in required_containers[robot_part].items():
                    if cont_value == miss_value:
                        list_miss_names.append(cont_name)
        missing_names[robot_part] = list_miss_names
    return missing_names


def are_missing_containers():
    all_missing_containers = np.asarray(list(get_missing_containers_names().values())).flatten()
    return not np.array_equal(np.asarray(all_missing_containers).flatten(), np.array([]))

def are_all_containers_missing():
    # [len([part_name for (part_name, value) in part.items() if type(value) not in fan_types]) for part in config]  
    # output [9, 9, 3] : combien on est cense avoir de conteneurs pour chaque partie
    # [len(a[part]) for part in a] ( a = get_missing_containers_names())
    