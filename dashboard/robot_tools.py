import os
import yaml

from reachy_pyluos_hal.discovery import identify_luos_containers, find_gate

DEFAULT_MODEL = 'full_kit'

def identify_model():
    model = os.getenv('REACHY_MODEL')
    if not model:
        config_file = os.getenv('REACHY_CONFIG_FILE', default=os.path.expanduser('~/.reachy.yaml'))
        if not os.path.exists(config_file):
            model = DEFAULT_MODEL

        with open(config_file) as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            if 'model' not in config:
                model = DEFAULT_MODEL

        model = config['model']
    return model

def check_missing_motors():
    port, found, missing = find_gate()
    return