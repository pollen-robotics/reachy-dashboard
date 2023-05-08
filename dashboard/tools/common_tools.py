from subprocess import CalledProcessError, check_output, PIPE, Popen, run


def shutdown():
    run(['shutdown', '-h'])
    print('Received shutdown order. Power off in one minute.')