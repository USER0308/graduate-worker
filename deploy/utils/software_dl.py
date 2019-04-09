#!/usr/bin/python

from utils import log_debug, run_by_system, run_by_subprocess


    
def check_exist(check_command):
    if_exist = run_by_system(command=check_command, is_sudo=False)
    if_exist >>= 8
    return if_exist

def install(check_command, install_command):
    is_exist = check_exist(check_command)
    if is_exist == 127:
        install_log, error_log = run_by_subprocess(command=install_command,is_sudo=True)
#        log_debug('stderr is: \n')
#        for line in error_log:
#            log_debug(error_log)
#        log_debug('install logs are:\n')
#        for line in install_log:
#            print install_log

def uninstall(check_command, uninstall_command):
    is_exist = check_exist(check_command)
    if is_exist == 0:
        uninstall_result = run_by_system(command=uninstall_command, is_sudo=True)
        if uninstall_result == 0:
            print 'uninstall sucessfully'
    else:
        print 'not installed yet'

def install_curl():
    check_command = 'command -v curl'
    install_command = 'apt install -y curl'
    install(check_command, install_command)

def uninstall_curl():
    check_command = 'command -v curl'
    uninstall_command = 'apt --purge -y remove curl'
    uninstall(check_command, uninstall_command)

def install_docker():
    install_curl()  # docker depends on curl to install
    check_command = 'command -v docker'
    install_command = 'curl -sSL https://get.docker.com/ | sh;'
    install(check_command, install_command)

def uninstall_docker():
    check_command = 'command -v docker'
    uninstall_command = 'apt --purge -y remove docker-ce docker-ce-cli containerd.io'
    uninstall(check_command, uninstall_command)

def add_user_to_docker():  # need to logout/login
    get_user_command = 'whoami'
    command_log, error_log = run_by_subprocess(get_user_command, False)
    username = command_log
    log_debug(username)
    add_user_to_docker_command = 'usermod -aG docker ' + username
    command_log, error_log = run_by_subprocess(add_user_to_docker_command, True)
    log_debug(command_log)
    log_debug(error_log)

def check_user_in_docker_group():
    get_user_command = 'whoami'
    command_log, error_log = run_by_subprocess(get_user_command, False)
    username = command_log
    check_user_in_docker_group_command = 'id ' + username
    command_log, error_log = run_by_subprocess(check_user_in_docker_group_command, False)
    log_debug(command_log)
    if 'docker' in command_log:
        return True
    else:
        return False

def install_pip():
    check_command = 'command -v pip'
    install_command = 'apt install -y python-pip'
    install(check_command, install_command)

def uninstall_pip():
    check_command = 'command -v pip'
    uninstall_command = 'apt --purge -y remove python-pip'
    uninstall(check_command, uninstall_command)

def install_pydocker():
    install_pip()
    check_command = ''  ## TODO
    install_command = 'pip install docker'
    install(check_command=check_command, install_command=install_command)

def uninstall_pydocker():
    check_command = ''
    uninstall_command = 'pip uninstall -y docker'
    uninstall(check_command, uninstall_command)

def install_compose():
    install_pip()
    check_command = 'command -v docker-compose'
    install_command = 'pip install docker-compose>=1.17.0'
    install(check_command, install_command)

def uninstall_compose():
    check_command = 'command -v docker-compose'
    uninstall_command = 'pip uninstall -y docker-compose'
    uninstall(check_command, uninstall_command)

def install_all():
    install_curl()
    install_pip()
    #install_pydocker()
    install_docker()
    install_compose()

def uninstall_all():
    #uninstall_pydocker()
    uninstall_compose()
    uninstall_docker()
    uninstall_pip()
    uninstall_curl()

def download_img(tag):
    #download_img('x86_64-1.0.0')
    images = ['peer', 'orderer', 'couchdb', 'ccenv', 'javaenv', 'kafka', 'zookeeper', 'tools']
    is_sudo = True
    if check_user_in_docker_group():
        is_sudo = False
    for image in images:
        pull_command = 'docker pull hyperledger/fabric-'+image+':'+tag
        log_debug(pull_command)
        command_log, error_log = run_by_subprocess(pull_command, is_sudo)
        # deal with command_log, error_log
        change_tag_command = 'docker tag hyperledger/fabric-'+image+':'+tag+' hyperledger/fabric-'+image
        log_debug(change_tag_command)
        command_log, error_log = run_by_subprocess(change_tag_command, is_sudo)

def download_ca(tag):
    #download_ca('x86_64-1.0.0')
    pull_command = 'docker pull hyperledger/fabric-ca:'+tag
    command_log, error_log = run_by_subprocess(pull_command, True)
    # deal with command_log,error_log
    change_tag_command = 'docker tag hyperledger/fabric-ca:'+tag+' hyperledger/fabric-ca'
    run_by_subprocess(change_tag_command, True)

def download_binary():
    command = 'curl https://nexus.hyperledger.org/content/repositories/releases/org/hyperledger/fabric/hyperledger-fabric/linux-amd64-1.0.0/hyperledger-fabric-linux-amd64-1.0.0.tar.gz | tar xz'
    command_log, error_log = run_by_subprocess(command, True)
    # deal with command_log, error_log


def list_images():
    command = 'docker images | grep hyperledger*'


if __name__ == '__main__':
    a = raw_input('install or uninstall?(i/u) ')
    if a == 'u':
        pass
        uninstall_docker()
    elif a == 'i':
        install_all()
        download_img(tag='x86_64-1.0.0')
        download_ca(tag='x86_64-1.0.0')
        download_binary()
        list_images()
