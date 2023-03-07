"""Service and App management tools for RAP-2021."""
from subprocess import run, PIPE


def list_services_or_apps(type: str):
    pipe1 = run(['systemctl --user list-unit-files'], stdout=PIPE, shell=True)
    pipe2 = run(['grep reachy'], input=pipe1.stdout, stdout=PIPE, shell=True)
    pipe3 = run(["awk '{print $1}'"], input=pipe2.stdout, stdout=PIPE, shell=True)

    output = pipe3.stdout.decode().split('\n')
    service_list = [service for service in output if service]

    if type == 'service':
        return [srv_name.split('.service')[0] for srv_name in service_list if 'app' not in srv_name]
    if type == 'app':
        return [srv_name.split('.service')[0].split('app_')[1] for srv_name in service_list if 'app' in srv_name]


def restart_service_or_app(type: str, name: str):
    if type == 'service':
        run([f'systemctl --user restart {name}.service'], stdout=PIPE, shell=True)
    elif type == 'app':
        run([f'systemctl --user restart app_{name}.service'], stdout=PIPE, shell=True)


def stop_service_or_app(type: str, name: str):
    if type == 'service':
        run([f'systemctl --user stop {name}.service'], stdout=PIPE, shell=True)
    elif type == 'app':
        run([f'systemctl --user stop app_{name}.service'], stdout=PIPE, shell=True)


def is_service_or_app_running(type: str, name: str):
    if type == 'service':
        pipe = run([f'systemctl --user is-active {name}.service'], stdout=PIPE, shell=True)
    elif type == 'app':
        pipe = run([f'systemctl --user is-active app_{name}.service'], stdout=PIPE, shell=True)

    status = pipe.stdout.decode().split()
    if status[0] == 'active':
        return 'running'
    return 'stopped'


def get_service_or_app_status(type: str, name: str):
    if type == 'service':
        return run([f'systemctl --user status -n99999 {name}.service'], stdout=PIPE, shell=True).stdout
    elif type == 'app':
        return run([f'systemctl --user status -n99999 app_{name}.service'], stdout=PIPE, shell=True).stdout


def list_app_to_disable():
    app_list = list_services_or_apps('app')
    need_to_disable = False

    for app in app_list:
        if is_service_or_app_running('app', app) == 'running':
            need_to_disable = True

    if need_to_disable:
        return [app for app in app_list if is_service_or_app_running('app', app) == 'stopped']
    return []
