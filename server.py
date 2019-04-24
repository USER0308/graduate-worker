# encoding: utf-8
#!/usr/bin/python

import socket
import time
import docker
from deploy.utils import build_network, software_dl, template, utils
from monitor import Monitor

def install_software(conn):
    print('install software...')
    conn.sendall(bytes('install software...', encoding='utf-8'))
    time.sleep(2)
    # software_dl.install_all()
    conn.sendall(bytes('installing curl...', encoding='utf-8'))
    install_log, error_log = software_dl.install_curl()
    conn.sendall(bytes(install_log, encoding='utf-8'))
    time.sleep(2)
    conn.sendall(bytes('installing pip...', encoding='utf-8'))
    install_log, error_log = software_dl.install_pip()
    conn.sendall(bytes(install_log, encoding='utf-8'))
    time.sleep(2)
    conn.sendall(bytes('install docker by pip...', encoding='utf-8'))
    install_log, error_log = software_dl.install_pydocker()
    conn.sendall(bytes(install_log, encoding='utf-8'))
    time.sleep(2)
    conn.sendall(bytes('installing docker...', encoding='utf-8'))
    install_log, error_log = software_dl.install_docker()
    conn.sendall(bytes(install_log, encoding='utf-8'))
    time.sleep(2)
    conn.sendall(bytes('installing docker-compose...', encoding='utf-8'))
    install_log, error_log = software_dl.install_compose()
    conn.sendall(bytes(install_log, encoding='utf-8'))
    time.sleep(2)

def pull_image(conn):
    print('pull images...')
    conn.sendall(bytes('pull images [peer, orderer, couchdb, ccenv, javaenv, kafka, zookeeper, tools] with tag "x86_64-1.0.0" ...', encoding='utf-8'))
    software_dl.download_img(tag='x86_64-1.0.0')
    time.sleep(2)
    conn.sendall(bytes('pull images ca with tag "x86_64-1.0.0"... ', encoding='utf-8'))
    software_dl.download_ca(tag='x86_64-1.0.0')
    time.sleep(2)

def download_binary(conn):
    print('download binary...')
    conn.sendall(bytes('download binary from https://nexus.hyperledger.org...', encoding='utf-8'))
    install_log, error_log = software_dl.download_binary()
    conn.sendall(bytes(install_log, encoding='utf-8'))
    time.sleep(2)

def generate_config(conn):
    print('generate config...')
    conn.sendall(bytes('generate crypto-config...', encoding='utf-8'))
    template.crypto_config_gen(orderer_num=1, org_num=2, peer_num=2, couchdb_num=0, ca_num=0)
    time.sleep(2)
    conn.sendall(bytes('generate configtx...', encoding='utf-8'))
    template.configtx_gen(orderer_num=1, org_num=2, peer_num=2, couchdb_num=0, ca_num=0)
    time.sleep(2)
    conn.sendall(bytes('generate docker-compose.yaml...', encoding='utf-8'))
    template.docker_compose_gen(orderer_num=1, org_num=2, peer_num=2, couchdb_num=0, ca_num=0)
    time.sleep(2)

def generate_material(conn):
    print('generate_material...')
    conn.sendall(bytes('generate crypto_material...', encoding='utf-8'))
    build_network.prepare()
    build_network.crypto_material_gen()
    time.sleep(2)
    conn.sendall(bytes('orderer_genesis_block', encoding='utf-8'))
    build_network.orderer_genesis_block_gen()
    time.sleep(2)
    conn.sendall(bytes('channel_config', encoding='utf-8'))
    build_network.channel_config_trans_gen()
    time.sleep(2)
    conn.sendall(bytes('anchor_peer_config', encoding='utf-8'))
    build_network.anchor_peer_config_gen(org_num=2)
    time.sleep(2)

def yaml_up(conn):
    conn.sendall(bytes('building network...', encoding='utf-8'))
    build_network.yaml_up()
    print('network up, sleep for 20s')
    conn.sendall(bytes('network up, sleep for 20s', encoding='utf-8'))
    time.sleep(20)

def create_channel(conn):
    print('create channel...')
    conn.sendall(bytes('create channel...', encoding='utf-8'))
    exit_code, output = build_network.create_channel(orderer_num=1)
    if exit_code == 0:
        conn.sendall(bytes("create channel success\n\n", encoding='utf-8'))
        conn.sendall(output)
    else:
        conn.sendall(bytes("create channel faild\n\n", encoding='utf-8'))
        conn.sendall(output)
    time.sleep(2)

def join_channel(conn):
    print('join channel...')
    conn.sendall(bytes('join channel...', encoding='utf-8'))
    results = build_network.join_peer(peer_num=2,org_num=2)
    for result in results:
        if result[0] == 0:
            conn.sendall(bytes("join channel success\n\n", encoding='utf-8'))
            conn.sendall(result[1])
        else:
            conn.sendall(bytes("join channel faild\n\n", encoding='utf-8'))
            conn.sendall(result[1])
    time.sleep(2)

def install_chaincode(conn):
    print('install chaincode...')
    conn.sendall(bytes('install chaincode...', encoding='utf-8'))
    results = build_network.install_chaincode(peer_num=2, org_num=2)
    for result in results:
        if result[0] == 0:
            conn.sendall(bytes("install chaincode success\n\n", encoding='utf-8'))
            conn.sendall(result[1])
        else:
            conn.sendall(bytes("install chaincode faild\n\n", encoding='utf-8'))
            conn.sendall(result[1])
    time.sleep(2)

def instantiate_chaincode(conn):
    print('instantiate chaincode...')
    conn.sendall(bytes('instantiate chaincode...', encoding='utf-8'))
    exit_code, output = build_network.instantiate_chaincode(orderer_num=1)
    if exit_code == 0:
        conn.sendall(bytes("instantiate chaincode success\n\n", encoding='utf-8'))
        conn.sendall(output)
    else:
        conn.sendall(bytes("instantiate chaincode faild\n\n"+output, encoding='utf-8'))
        conn.sendall(output)
    time.sleep(2)

def query_chaincode(conn):
    print('query chaincode...')
    conn.sendall(bytes('query chaincode...', encoding='utf-8'))
    exit_code, output = build_network.query_chaincode()
    if exit_code == 0:
        conn.sendall(bytes("query success\n\n", encoding='utf-8'))
        conn.sendall(output)
    else:
        conn.sendall(bytes("query faild\n\n", encoding='utf-8'))
        conn.sendall(output)
    time.sleep(2)

def query_installed_cc(conn):
    print('query installed chaincode...')
    #conn.sendall(bytes('query installed chaincode...', encoding='utf-8'))
    monitor = Monitor()
    output = monitor.query_installed_chaincode()
    conn.sendall(bytes(output, encoding='utf-8'))
    #time.sleep(2)

def query_instantiated_cc(conn):
    print('query instantiated chaincode...')
    #conn.sendall(bytes('query instantiated chaincode...', encoding='utf-8'))
    monitor = Monitor()
    output = monitor.query_instantiated_chaincode()
    conn.sendall(bytes(output, encoding='utf-8'))
    #time.sleep(2)

def query_channel(conn):
    print('query channel...')
    #conn.sendall(bytes('query channel...', encoding='utf-8'))
    monitor = Monitor()
    output = monitor.query_channel()
    conn.sendall(bytes(output, encoding='utf-8'))
    #time.sleep(2)

def get_channel_config(conn):
    print('get channel config...')
    #conn.sendall(bytes('get channel config...', encoding='utf-8'))
    monitor = Monitor()
    output = monitor.get_channel_config()
    conn.sendall(bytes(output, encoding='utf-8'))
    #time.sleep(2)

def query_info(conn):
    print('query info...')
    #conn.sendall(bytes('query info...', encoding='utf-8'))
    monitor = Monitor()
    output = monitor.query_info()
    conn.sendall(bytes(output, encoding='utf-8'))
    #time.sleep(2)

def query_block_by_hash(conn, block_hash):
    print('query block by hash...')
    #conn.sendall(bytes('query block by hash...', encoding='utf-8'))
    monitor = Monitor()
    output = monitor.query_block_by_hash(block_hash)
    conn.sendall(bytes(output, encoding='utf-8'))
    #time.sleep(2)

def query_block_by_txid(conn, tx_id):
    print('query block by txid...')
    #conn.sendall(bytes('query block by transaction id...', encoding='utf-8'))
    monitor = Monitor()
    output = monitor.query_block_by_txid(tx_id)
    conn.sendall(bytes(output, encoding='utf-8'))
    #time.sleep(2)

def query_transaction_by_txid(conn, tx_id):
    print('query transaction by txid...')
    #conn.sendall(bytes('query transaction by tx_id...', encoding='utf-8'))
    monitor = Monitor()
    output = monitor.query_transaction_by_txid(tx_id)
    conn.sendall(bytes(output, encoding='utf-8'))
    #time.sleep(2)

def end_connection(conn):
    print('end')
    conn.sendall(bytes('end', encoding='utf-8'))
    #time.sleep(2)
    conn.close()

def networking():
    sk = socket.socket()
    sk.bind(('', 1347))
    sk.listen(3)
    while True:
        conn, address = sk.accept()
        print(address[0])
        client_data = conn.recv(1024)
        print(client_data)
        client_data = client_data.decode()
        #time.sleep(2)
        print('connected...')
        #conn.sendall(bytes('connected...', encoding='utf-8'))
        #time.sleep(2)

        ## get these data from client...
        orderer_num=1
        org_num=2
        peer_num=2
        couchdb_num=0
        ca_num=0

        if client_data == 'start':
            #install_software(conn)
            #pull_image(conn)
            #download_binary(conn)
            #generate_config(conn)
            #generate_material(conn)
            yaml_up(conn)
            create_channel(conn)
            join_channel(conn)
            install_chaincode(conn)
            instantiate_chaincode(conn)


        if client_data == 'software':
            install_software(conn)


        if client_data == 'image':
            pull_image(conn)


        if client_data == 'binary':
            download_binary(conn)


        if client_data == 'config':
            generate_config(conn)


        if client_data == 'material':
            generate_material(conn)


        if client_data == 'build':
            yaml_up(conn)


        if client_data == 'createChannel':
            create_channel(conn)


        if client_data == 'joinChannel':
            join_channel(conn)


        if client_data == 'installChaincode':
            install_chaincode(conn)


        if client_data == 'instantiateChaincode':
            instantiate_chaincode(conn)


        if client_data == 'queryChaincode':
            query_chaincode(conn)


#        print('invoke chaincode...')
#        conn.sendall(bytes('invoke chaincode...', encoding='utf-8'))
#        time.sleep(2)
#        if client_data == 'end':
#            end_connection(conn)

        if client_data == 'installed':
            query_installed_cc(conn)

        
        if client_data == 'instantiated':
            query_instantiated_cc(conn)

        if client_data == 'queryChannel':
            query_channel(conn)

        if client_data == 'channelConfig':
            get_channel_config(conn)

        if client_data == 'queryInfo':
            query_info(conn)

        if client_data.startswith('blockHash'):
            """\315\364\"==~\230\376\340\355Y\345\334\353\247r\367\237\034!\262\263\266\013\253\302\334,O\243\306#"""
            h = client_data[11:]
            print(h)
            block_hash = "\037\031\031\264rW\307\337\307\330=\331\247\317\242\315D\"\025\367\002T\341\265\3578\025\326\340\037\243\312"
            query_block_by_hash(conn, block_hash)

        if client_data.startswith('blockTxid'):
            print('in transaction')
            tid = client_data[11:]
            print(tid)
            tx_id = "1244b10f878e87a701911c9b6f6e747b6e97833769cb4770dfb544cb9abe348d"
            query_block_by_txid(conn, tx_id)

        if client_data.startswith('transactionId'):
            print('in transaction')
            tid = client_data[13:]
            print(tid)
            tx_id = "1244b10f878e87a701911c9b6f6e747b6e97833769cb4770dfb544cb9abe348d"
            query_transaction_by_txid(conn, tx_id)



        end_connection(conn)

if __name__ == '__main__':
    networking()
    #build_network.install_chaincode(peer_num=2, org_num=2)
    #build_network.instantiate_chaincode(orderer_num=1)
    #build_network.query_chaincode()
