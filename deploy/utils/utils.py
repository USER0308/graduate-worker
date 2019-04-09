import os
import subprocess
from deploy.config.config import debug, sudo_password

def log_debug(message):
    if debug == True:
        print message

def run_by_system(command, is_sudo):
    if is_sudo:
        status_code = os.system('echo %s|sudo -S %s' % (sudo_password,command))
        return status_code
    else:
        status_code = os.system(command)
        return status_code

def run_by_subprocess(command, is_sudo):
    log_debug('running command')
#    log_debug(command)
#    log_debug(is_sudo)
    command_log = ''
    error_log = ''
    if is_sudo:
        command = 'echo %s|sudo -S %s' % (sudo_password,command)
    log_debug(command)
    d = subprocess.Popen(command,
                        stdin=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        universal_newlines=True,
                        shell=True)
    while True:
        if d.poll() == None:
            output = d.stdout.readline()
            command_log += output
            #log_debug(output.strip())
            #error = d.stderr.readline()
            #error_log += error
        else:
            break
    log_debug('command_log is:')
    log_debug(command_log)
#    log_debug('error_log is:')
#    log_debug(error_log)
    return command_log,error_log