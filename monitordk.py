#!/usr/bin/python

import os
import json
import docker
from deploy.utils.utils import log_debug, run_by_system, run_by_subprocess

def get_os_info():
    command = """uname -mo"""
    command_log, error_log = run_by_subprocess(command, False)
    os_type = command_log

    client = docker.from_env()
    active_containers = client.containers.list()
    all_containers = client.containers.list(all=True)

    command = """docker -v"""
    command_log, error_log = run_by_subprocess(command, False)
    command_log = command_log.split(' ')
    command_log = command_log[2]
    command_log = command_log[:-1]
    version = command_log
    info = {
        'os': os_type,
        'activeContainer': len(active_containers),
        'totalContainer': len(all_containers),
        'dockerVersion': version,
        'ip': '192.168.10.100',
        'domainName': '192.168.10.100'
    }
    return json.dumps(info)
    
def get_docker_info():
    command = """ docker ps | sed -n '2,$p' | awk  -F '  +' '{print $1 "\t" $2 "\t" $3 "\t" $4 "\t" $5 "\t" $NF}' """
    command_log, error_log = run_by_subprocess(command, False)
    docker_status = command_log
    print(docker_status)
    return docker_status


if __name__ == '__main__':
    get_os_info()
