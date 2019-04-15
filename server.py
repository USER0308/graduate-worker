# encoding: utf-8
#!/usr/bin/python

import socket
import time
import docker
from deploy.utils import build_network, software_dl, template, utils

def networking():
    sk = socket.socket()
    sk.bind(('', 1347))
    sk.listen(3)
    while True:
        conn, address = sk.accept()
        print address[0]
        client_data = conn.recv(1024)
        print client_data
        time.sleep(2)
        print 'connected...'
        conn.sendall('connected...')
        time.sleep(2)

        ## get these data from client...
        orderer_num=3
        org_num=2
        peer_num=2
        couchdb_num=0
        ca_num=0

#        print 'install software...'
#        conn.sendall('install software...')
#        time.sleep(2)
        # software_dl.install_all()
#        conn.sendall('installing curl...')
#        install_log, error_log = software_dl.install_curl()
#        conn.sendall(install_log)
#        time.sleep(2)
#        conn.sendall('installing pip...')
#        install_log, error_log = software_dl.install_pip()
#        conn.sendall(install_log)
#        time.sleep(2)
#        conn.sendall('install docker by pip...')
#        install_log, error_log = software_dl.install_pydocker()
#        conn.sendall(install_log)
#        time.sleep(2)
#        conn.sendall('installing docker...')
#        install_log, error_log = software_dl.install_docker()
#        conn.sendall(install_log)
#        time.sleep(2)
#        conn.sendall('installing docker-compose...')
#        install_log, error_log = software_dl.install_compose()
#        conn.sendall(install_log)
#        time.sleep(2)

        
#        print 'pull images...'
#        conn.sendall('pull images [peer, orderer, couchdb, ccenv, javaenv, kafka, zookeeper, tools] with tag "x86_64-1.0.0" ...')
#        software_dl.download_img(tag='x86_64-1.0.0')
#        time.sleep(2)
#        conn.sendall('pull images ca with tag "x86_64-1.0.0"... ')
#        software_dl.download_ca(tag='x86_64-1.0.0')
#        time.sleep(2)

#        print 'download binary...'
#        conn.sendall('download binary from https://nexus.hyperledger.org...')
#        install_log, error_log = software_dl.download_binary()
#        conn.sendall(install_log)
#        time.sleep(2)

#        print 'generate config...'
#        conn.sendall('generate crypto-config...')
#        template.crypto_config_gen(orderer_num=3, org_num=2, peer_num=2, couchdb_num=0, ca_num=0)
#        time.sleep(2)
#        conn.sendall('generate configtx...')
#        template.configtx_gen(orderer_num=3, org_num=2, peer_num=2, couchdb_num=0, ca_num=0)
#        time.sleep(2)
#        conn.sendall('generate docker-compose.yaml...')
#        template.docker_compose_gen(orderer_num=3, org_num=2, peer_num=2, couchdb_num=0, ca_num=0)
#        time.sleep(2)

#        print 'building network...'
#        conn.sendall('generate crypto_material...')
#        build_network.prepare()
#        build_network.crypto_material_gen()
#        time.sleep(2)
#        conn.sendall('orderer_genesis_block')
#        build_network.orderer_genesis_block_gen()
#        time.sleep(2)
#        conn.sendall('channel_config')
#        build_network.channel_config_trans_gen()
#        time.sleep(2)
#        conn.sendall('anchor_peer_config')
#        build_network.anchor_peer_config_gen(org_num=org_num)
#        time.sleep(2)

#        conn.sendall('building network...')
#        build_network.yaml_up()
#        print 'network up, sleep for 20s'
#        conn.sendall('network up, sleep for 20s')
#        time.sleep(20)
#        print 'create channel...'
#        conn.sendall('create channel...')
#        exit_code, output = build_network.create_channel(orderer_num=3)
#        if exit_code == 0:
#            conn.sendall("create channel success\n\n"+output)
#        else:
#            conn.sendall("create channel faild\n\n"+output)
#        time.sleep(2)
#        print 'join channel...'
#        conn.sendall('join channel...')
#        results = build_network.join_peer(peer_num=2,org_num=2)
#        for result in results:
#            if result[0] == 0:
#                conn.sendall("join channel success\n\n"+result[1])
#            else:
#                conn.sendall("join channel faild\n\n"+result[1])
#        time.sleep(2)
#        print 'install chaincode...'
#        conn.sendall('install chaincode...')
#        results = build_network.install_chaincode(peer_num=2, org_num=2)
#        for result in results:
#            if result[0] == 0:
#                conn.sendall("install chaincode success\n\n"+result[1])
#            else:
#                conn.sendall("install chaincode faild\n\n"+result[1])
#        time.sleep(2)
#        print 'instantiate chaincode...'
#        conn.sendall('instantiate chaincode...')
#        exit_code, output = build_network.instantiate_chaincode(orderer_num=3)
#        if exit_code == 0:
#            conn.sendall("instantiate chaincode success\n\n"+output)
#        else:
#            conn.sendall("instantiate chaincode faild\n\n"+output)
#        time.sleep(2)
        print 'query chaincode...'
        conn.sendall('query chaincode...')
        exit_code, output = build_network.query_chaincode()
        if exit_code == 0:
            conn.sendall("query success\n\n"+output)
        else:
            conn.sendall("query faild\n\n"+output)
        time.sleep(2)
#        print 'invoke chaincode...'
#        conn.sendall('invoke chaincode...')
#        time.sleep(2)
        print 'end'
        conn.sendall('end')
        time.sleep(2)
        conn.close()

if __name__ == '__main__':
    networking()
    #build_network.install_chaincode(peer_num=2, org_num=2)
    #build_network.instantiate_chaincode(orderer_num=3)
    #build_network.query_chaincode()
