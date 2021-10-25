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

def identify_cards():
    with open('~/.boards.yaml') as f:
        card_config = yaml.load(f, Loader=yaml.FullLoader)
        if 'boards' not in card_config:
            required_cards = DEFAULT_CARDS
        required_cards = card_config['boards']

    with open(os.path.abspath('..')+'/boards/configs/'+required_cards+'.yaml') as f: 
        config = yaml.load(f, Loader=yaml.FullLoader) 
    check_output()    


def check_missing_motors():
    port, found, missing = find_gate()
    return