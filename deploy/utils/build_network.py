#!/usr/bin/python

import os
import docker
from utils import log_debug, run_by_system, run_by_subprocess





def prepare():  # check the path and config file and binary if exists
    if not os.path.exists('./bin/'):
        log_debug('bin path not exist, maybe you should download binary first')
    if not os.path.exists('./bin/cryptogen'):
        log_debug('bin/cryptogen not exist, maybe you should download binary first')
    if not os.path.exists('./bin/configtxgen'):
        log_debug('bin/configtxgen not exist, maybe you should download binary first')
    if os.path.isfile('./bin/'):
        log_debug('./bin/ is a file')
    if not os.path.isfile('./bin/cryptogen'):
        log_debug('bin/cryptogen file is a path, maybe you should download binary first')
    if not os.path.isfile('./bin/configtxgen'):
        log_debug('bin/configtxgen is a path, maybe you should download binary first')


#    if not os.path.exists('./tempOrgtempOrder'):
#        log_debug('./tempOrgtempOrder path not exist, creating')
#        os.mkdir('./tempOrgtempOrder')
    if not os.path.exists('./configtx.yaml'):
        log_debug('./configtx.yaml not exist, maybe you should generate it first')
    if not os.path.exists('./docker-compose.yaml'):
        log_debug('./docker-compose.yaml not exist, maybe you should generate it first')
    if not os.path.exists('./crypto-config.yaml'):
        log_debug('./crypto-config.yaml not exist, maybe you should generate it first')
    if not os.path.isfile('./configtx.yaml'):
        log_debug('./configtx.yaml is not a file')
    if not os.path.isfile('./crypto-config.yaml'):
        log_debug('./crypto-config.yaml is not a file')
    if not os.path.isfile('./docker-compose.yaml'):
        log_debug('./docker-compose.yaml is not a file')
    if not os.path.exists('./channel-artifacts/'):
        log_debug('./channel-artifacts/ is not exist, creating')
        os.mkdir('./channel-artifacts/')
    if not os.path.exists('./crypto-config/'):
        log_debug('./crypto-config/ is not exist, creating')
        os.mkdir('./crypto-config/')
    if not os.path.exists('./chaincode/'):
        log_debug('./chaincode/ is not exist, creating')
        os.mkdir('./chaincode/')
    if not os.path.exists('./scripts/'):
        log_debug('./scripts/ is not exist, creating')
        os.mkdir('./scripts/')



def env():
    """export FABRIC_CFG_PATH=${PWD}"""

def clean_config():
    command = """rm -fr ./channel-artifacts/*"""
    run_by_system(command, True)
    command = """rm -fr ./crypto-config/*"""
    run_by_system(command, True)

def crypto_material_gen():  ## output normally
    command = """./bin/cryptogen generate --config=./crypto-config.yaml"""
    command_log, error_log = run_by_subprocess(command, False)
    # log_debug(command_log)
    # log_debug(error_log)

def orderer_genesis_block_gen():  ## no output...
    current_path = os.getcwd()
#    log_debug('current path is:')
#    log_debug(current_path)
    env = 'FABRIC_CFG_PATH=' + current_path + ' '
    command = env + """./bin/configtxgen -profile OrdererGenesis -outputBlock ./channel-artifacts/genesis.block"""
    command_log, error_log = run_by_subprocess(command, False)
    # log_debug(command_log)
    # log_debug(error_log)

def channel_config_trans_gen():  ## no output...
    current_path = os.getcwd()
    env = 'FABRIC_CFG_PATH=' + current_path + ' '
    command = env + """./bin/configtxgen -profile Channel -outputCreateChannelTx ./channel-artifacts/channel.tx -channelID mychannel"""
    command_log, error_log = run_by_subprocess(command, False)
    # log_debug(command_log)
    # log_debug(error_log)

def anchor_peer_config_gen(org_num=2):  ## no output...
    current_path = os.getcwd()
    env = 'FABRIC_CFG_PATH=' + current_path + ' '
    command = env + """./bin/configtxgen -profile Channel -outputAnchorPeersUpdate ./channel-artifacts/OrgXMSPanchors.tx -channelID mychannel -asOrg OrgXMSP"""
    for i in range(1, org_num+1):
        command = command.replace('rgX', 'rg'+str(i))
        command_log, error_log = run_by_subprocess(command, False)
    # log_debug(command_log)
    # log_debug(error_log)


def create_channel(orderer_num=1):
#    command = ''
#    if orderer_num == 1:
#        command = """docker exec cli peer channel create -o orderer.example.com:7050 -c mychannel -f ./channel-artifacts/channel.tx"""
#    elif orderer_num > 1:
#        command = """docker exec cli peer channel create -t 20 -o orderer1.example.com:7050 -c mychannel -f ./channel-artifacts/channel.tx"""
    #    print 'running command ' + command
    #print 'outthere, command is ' + command
#    command_log, error_log = run_by_subprocess(command, False)
#    log_debug(command_log)
#    log_debug(error_log)

    client = docker.from_env()
    cli = client.containers.get('cli')
    command = """peer channel create -o orderer.example.com:7050 -c mychannel -f ./channel-artifacts/channel.tx"""
    if orderer_num > 1:
        command = """peer channel create -t 20 -o orderer1.example.com:7050 -c mychannel -f ./channel-artifacts/channel.tx"""
    exit_code, output = cli.exec_run(cmd=command)
    print exit_code, output
    return exit_code, output

def join_peer(peer_num=2,org_num=2):
    ## make all peer join (01,02,11,12)
#    peer_address_env = """-e CORE_PEER_ADDRESS=peerX.orgY.example.com:7051 """
#    cert_file_env = """-e CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/orgY.example.com/peerX.orgY.example.com/tls/ca.crt """
#    msp_path_env = """-e CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/orgY.example.com/users/Admin@orgY.example.com/msp """
#    msp_id_env = """-e CORE_PEER_LOCALMSPID="OrgYMSP" """
#    for x in range(0,peer_num):  # each org has x peers
#        for y in range(1,org_num+1):  # total y orgs
#            env1 = peer_address_env.replace('peerX', ('peer'+str(x)))
#            env1 = env1.replace('rgY', ('rg'+str(y)))

#            env2 = cert_file_env.replace('peerX', ('peer'+str(x)))
#            env2 = cert_file_env.replace('rgY', ('rg'+str(y)))

#            env3 = msp_path_env.replace('peerX', ('peer'+str(x)))
#            env3 = msp_path_env.replace('rgY', ('rg'+str(y)))
            
 #           env4 = msp_id_env.replace('rgY', ('rg'+str(y)))
            
 #           command = """docker exec """ + env1 + env2 + env3 + env4 + """ cli peer channel join -b mychannel.block"""
 #           command_log, error_log = run_by_subprocess(command, False)


    client = docker.from_env()
    cli = client.containers.get('cli')
    peer_address_env = """CORE_PEER_ADDRESS=peerX.orgY.example.com:7051"""
    cert_file_env = """CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/orgY.example.com/peerX.orgY.example.com/tls/ca.crt"""
    msp_path_env = """CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/orgY.example.com/users/Admin@orgY.example.com/msp"""
    msp_id_env = 'CORE_PEER_LOCALMSPID=OrgYMSP'
    results = []
    for x in range(0,peer_num):  # each org has x peers
        for y in range(1,org_num+1):  # total y orgs
            env1 = peer_address_env.replace('peerX', ('peer'+str(x)))
            env1 = env1.replace('rgY', ('rg'+str(y)))

            env2 = cert_file_env.replace('peerX', ('peer'+str(x)))
            env2 = cert_file_env.replace('rgY', ('rg'+str(y)))

            env3 = msp_path_env.replace('peerX', ('peer'+str(x)))
            env3 = msp_path_env.replace('rgY', ('rg'+str(y)))
            
            env4 = msp_id_env.replace('rgY', ('rg'+str(y)))
            command = """peer channel join -b mychannel.block"""
            exit_code, output = cli.exec_run(cmd=command, environment=[env1, env2, env3, env4])
            results.append([exit_code, output])
    return results


def install_chaincode(peer_num=2, org_num=2):
    # check chaincode file exist
    files = os.listdir('./chaincode/')
    if len(files) < 1:
        print 'no chaincode file exists'
        return [[1, 'no chaincode file exists']]
    ## make all peer install chaincode
#    peer_address_env = """-e CORE_PEER_ADDRESS=peerX.orgY.example.com:7051 """
#    cert_file_env = """-e CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/orgY.example.com/peerX.orgY.example.com/tls/ca.crt """
#    msp_path_env = """-e CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/orgY.example.com/users/Admin@orgY.example.com/msp """
#    msp_id_env = """-e CORE_PEER_LOCALMSPID="OrgYMSP" """
#    for x in range(0,peer_num):  # each org has x peers
#        for y in range(1,org_num+1):  # total y orgs
#            env1 = peer_address_env.replace('peerX', ('peer'+str(x)))
#            env1 = env1.replace('rgY', ('rg'+str(y)))

#            env2 = cert_file_env.replace('peerX', ('peer'+str(x)))
#            env2 = cert_file_env.replace('rgY', ('rg'+str(y)))

#            env3 = msp_path_env.replace('peerX', ('peer'+str(x)))
#            env3 = msp_path_env.replace('rgY', ('rg'+str(y)))
            
#            env4 = msp_id_env.replace('rgY', ('rg'+str(y)))
            
#            command = """docker exec """ + env1 + env2 + env3 + env4 + """ cli peer chaincode install -n mycc -v 1.0 -p github.com/hyperledger/fabric/examples/chaincode/go/"""
 #           command_log, error_log = run_by_subprocess(command, False)

    client = docker.from_env()
    cli = client.containers.get('cli')
    peer_address_env = """CORE_PEER_ADDRESS=peerX.orgY.example.com:7051"""
    cert_file_env = """CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/orgY.example.com/peerX.orgY.example.com/tls/ca.crt"""
    msp_path_env = """CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/orgY.example.com/users/Admin@orgY.example.com/msp"""
    msp_id_env = 'CORE_PEER_LOCALMSPID=OrgYMSP'
    results = []
    for x in range(0,peer_num):  # each org has x peers
        for y in range(1,org_num+1):  # total y orgs
            env1 = peer_address_env.replace('peerX', ('peer'+str(x)))
            env1 = env1.replace('rgY', ('rg'+str(y)))

            env2 = cert_file_env.replace('peerX', ('peer'+str(x)))
            env2 = cert_file_env.replace('rgY', ('rg'+str(y)))

            env3 = msp_path_env.replace('peerX', ('peer'+str(x)))
            env3 = msp_path_env.replace('rgY', ('rg'+str(y)))
            
            env4 = msp_id_env.replace('rgY', ('rg'+str(y)))
            
            command = """peer chaincode install -n mycc -v 1.0 -p github.com/hyperledger/fabric/examples/chaincode/go/"""
            exit_code, output = cli.exec_run(cmd=command, environment=[env1, env2, env3, env4])
            results.append([exit_code, output])
    return results



def instantiate_chaincode(orderer_num=1):
    # check chaincode if exist
    
    ##make chaincode instantiate once
#    command = r'''docker exec cli peer chaincode instantiate -o orderer.example.com:7050 -C mychannel -n mycc -v 1.0 -c '{"Args":["init","a","100","b","200"]}' -P "OR ('Org1MSP.member','Org2MSP.member')" '''
#    if orderer_num > 1:
#        command = r'''docker exec cli peer chaincode instantiate -o orderer1.example.com:7050 -C mychannel -n mycc -v 1.0 -c '{"Args":["init","a","100","b","200"]}' -P "OR ('Org1MSP.member','Org2MSP.member')" '''
#    command_log, error_log = run_by_subprocess(command, False)


    command = r'''peer chaincode instantiate -o orderer.example.com:7050 -C mychannel -n mycc -v 1.0 -c '{"Args":["init","a","100","b","200"]}' -P "OR ('Org1MSP.member','Org2MSP.member')" '''
    if orderer_num > 1:
        command = r'''peer chaincode instantiate -o orderer1.example.com:7050 -C mychannel -n mycc -v 1.0 -c '{"Args":["init","a","100","b","200"]}' -P "OR ('Org1MSP.member','Org2MSP.member')" '''
    client = docker.from_env()
    cli = client.containers.get('cli')
    exit_code, output = cli.exec_run(cmd=command)
    return exit_code, output

def invoke_chaincode():
    pass

def query_chaincode():
#    command = r'''docker exec cli peer chaincode query -C mychannel -n mycc -v 1.0 -c '{"Args":["query","a"]}' '''
#    command_log, error_log = run_by_subprocess(command, False)
#    log_debug(command_log)
#    log_debug(error_log)
#    command_log = command_log.strip()
#    error_log = error_log.strip()
#    if error_log:
#        return command_log, error_log
#    return command_log, ''

    client = docker.from_env()
    cli = client.containers.get('cli')
    command = r'''peer chaincode query -C mychannel -n mycc -v 1.0 -c '{"Args":["query","a"]}' '''
    exit_code, output = cli.exec_run(cmd=command)
    return exit_code, output
def yaml_up():
    command = """CHANNEL_NAME=mychannel TIMEOUT=60 docker-compose -f docker-compose.yaml up -d"""
    command_log, error_log = run_by_subprocess(command, False)
#    log_debug(command_log)
#    log_debug(error_log)

def network_up():
    #yaml_up()

    #create_channel()

    join_peer()

    install_chaincode()

    instantiate_chaincode()


def network_restart():
    command = """docker stop $(docker ps -q)"""
    run_by_system(command, False)
    command = """docker rm $(docker ps -aq)"""
    run_by_system(command, False)
    p = './crypto-config/peerOrganizations/org1.example.com/ca/org1.example.com-cert.pem'
    if os.path.exists(p):
        os.remove(p)
    p = './crypto-config/peerOrganizations/org2.example.com/ca/org2.example.com-cert.pem'
    if os.path.exists(p):
        os.remove(p)
    network_up()

def network_clean():
    command = """docker stop $(docker ps -q)"""
    run_by_system(command, False)
    command = """docker rm $(docker ps -aq)"""
    run_by_system(command, False)
    clean_config()

def generate():
    crypto_material_gen()
    orderer_genesis_block_gen()
    channel_config_trans_gen()
    anchor_peer_config_gen()

if __name__ == '__main__':
    a = raw_input('generate(1) or up(2) or clean(3) or restart(4) cleanAll(5)?')
    if a == '1':
        generate()
    elif a == '2':
        network_up()
    elif a == '3':
        prepare()
        clean_config()
    elif a == '4':
        network_restart()
    elif a == '5':
        network_clean()
