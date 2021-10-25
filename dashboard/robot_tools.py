import os
import yaml

from subprocess import check_output

from reachy_pyluos_hal.discovery import identify_luos_containers, find_gate

DEFAULT_MODEL = 'full_kit'
DEFAULT_CARDS = 'camera'

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

def identify_boards():
    with open('~/.boards.yaml') as f:
        board_config_file = yaml.load(f, Loader=yaml.FullLoader)
        if 'boards' not in board_config_file:
            board_config = DEFAULT_CARDS
        board_config = board_config_file['boards']

    with open(os.path.abspath('..')+'/boards/configs/'+board_config+'.yaml') as f: 
        required_boards = yaml.load(f, Loader=yaml.FullLoader)

    for board in required_boards:
        check_output()    


def check_missing_motors():
    port, found, missing = find_gate()
    return