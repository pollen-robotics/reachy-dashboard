from reachy_utils.discovery import get_missing_motors_reachy, get_reachy_model
from reachy_utils.config import config_to_parts


def get_missing_modules_names():
    return get_missing_motors_reachy()


def get_required_modules():
    required_modules = {}

    reachy_model = get_reachy_model()

    full_kit_modules = {
        'right_arm': {
            'r_shoulder_pitch': ['motor', 10],
            'r_shoulder_roll': ['motor', 11],
            'r_arm_yaw': ['motor', 12],
            'r_elbow_pitch': ['motor', 13],
            'r_l_forearm_yaw': ['motor', 14],
            'r_wrist_pitch': ['motor', 15],
            'r_wrist_roll': ['motor', 16],
            'r_gripper': ['motor', 17],
        },
        'left_arm': {
            'l_shoulder_pitch': ['motor', 20],
            'l_shoulder_roll': ['motor', 21],
            'l_arm_yaw': ['motor', 22],
            'l_elbow_pitch': ['motor', 23],
            'l_l_forearm_yaw': ['motor', 24],
            'l_wrist_pitch': ['motor', 25],
            'l_wrist_roll': ['motor', 26],
            'l_gripper': ['motor', 27],
            },
        'head': {
            'r_antenna': ['motor', 30],
            'l_antenna': ['motor', 31],
            'orbita': ['motor', 70],
        }
    }

    for part in config_to_parts[reachy_model]:
        required_modules[part] = full_kit_modules[part]

    return required_modules


def are_missing_modules():
    required = get_required_modules()
    required_len = [len(required[part]) for part in required]

    missing = get_missing_motors_reachy()
    missing_len = [len(missing[part]) for part in missing]

    if required_len == missing_len:
        return 'all_missing'

    elif sum(missing_len) != 0:
        return 'some_missing'

    return 'none_missing'
