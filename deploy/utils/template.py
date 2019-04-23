#!/usr/bin/python

import os
from deploy.utils.utils import log_debug


def configtx_gen(orderer_num=1,org_num=1,peer_num=1,ca_num=0,couchdb_num=0,cli=1):
    profile = '''Profiles:

    OrdererGenesis:
        Orderer:
            <<: *OrdererDefaults
            Organizations:
                - *OrdererOrg
        Consortiums:
            SampleConsortium:
                Organizations:
                    - *Org1'''
    if org_num != 1:
        for i in range(2, org_num+1):
            profile += ('\n                    - *Org' + str(i))
    #log_debug(profile)

    channel_profile = '''    Channel:
        Consortium: SampleConsortium
        Application:
            <<: *ApplicationDefaults
            Organizations:
                - *Org1'''
    if org_num != 1:
        for i in range(2, org_num+1):
            channel_profile += ('\n                - *Org' + str(i))
    #log_debug(channel_profile)

    organization_profile = '''Organizations:

    - &OrdererOrg
        Name: OrdererOrg

        ID: OrdererMSP

        MSPDir: crypto-config/ordererOrganizations/example.com/msp

    - &Org1
        Name: Org1MSP

        ID: Org1MSP

        MSPDir: crypto-config/peerOrganizations/org1.example.com/msp

        AnchorPeers:
            - Host: peer0.org1.example.com
              Port: 7051

'''
    if org_num != 1:
        for i in range(2, org_num+1):
            template = '''    - &Org1
            Name: Org1MSP

            ID: Org1MSP

            MSPDir: crypto-config/peerOrganizations/org1.example.com/msp

            AnchorPeers:
                - Host: peer0.org1.example.com
                  Port: 7051

'''
            template = template.replace('rg1',('rg'+str(i)))
            organization_profile += template
    #log_debug(organization_profile)

    orderer_profile = '''Orderer: &OrdererDefaults

    OrdererType: solo

    Addresses:
        - orderer.example.com:7050

    BatchTimeout: 2s

    BatchSize:

        MaxMessageCount: 10

        AbsoluteMaxBytes: 99 MB

        PreferredMaxBytes: 512 KB

    Kafka:
        Brokers:
            - 127.0.0.1:9092

    Organizations:

'''
    if orderer_num != 1:
        orderer_profile = orderer_profile.replace('solo', 'kafka')
        address = ''
        for i in range(1, orderer_num+1):
            address += '        - orderer%s.example.com:7050\n' %i
        orderer_profile = orderer_profile.replace('        - orderer.example.com:7050', address)
        broker_profile = '''- k1:9092
            - k3:9092'''
        orderer_profile = orderer_profile.replace('- 127.0.0.1:9092', broker_profile)
    #log_debug(orderer_profile)

    application_profile = '''Application: &ApplicationDefaults

    Organizations:

''' 
    #log_debug(application_profile)

    total_profile = profile + '\n' + channel_profile + '\n' + organization_profile + orderer_profile + application_profile
    #log_debug(total_profile)

    # write to cryptotx.yaml
    f = open('configtx.yaml', 'w')
    f.write(total_profile)
    f.close()

def crypto_config_gen(orderer_num=1,org_num=1,peer_num=1,ca_num=0,couchdb_num=0,cli=1):
    orderer_config = '''OrdererOrgs:
  - Name: Orderer
    Domain: example.com
    Specs:
      - Hostname: orderer'''
    peer_config = '''PeerOrgs:
  - Name: Org1
    Domain: org1.example.com
    Template:
      Count: 1
    Users:
      Count: 1'''

    # if orderer_num != 1,that is orderer type is not solo
    if orderer_num != 1:
        orderer_config = orderer_config + '1'
    for num in range(1, orderer_num):
        addition = '''      - Hostname: orderer''' + str(num+1)
        orderer_config = orderer_config + '\n' + addition

    # add other org info
    for num in range(1,org_num):
        addition = '''  - Name: Org1
    Domain: org1.example.com
    Template:
      Count: 1
    Users:
      Count: 1'''
           # change to OrgN,orgN
        addition = addition.replace('rg1', 'rg'+str(num+1))
        peer_config = peer_config + '\n'+ addition

    # change to peer_num
    if peer_num != 1:
        peer_config = peer_config.replace('''    Template:
      Count: 1''', '''    Template:
      Count: '''+str(peer_num))
    #log_debug(orderer_config+'\n'+peer_config)

    # write to crypto-config.yaml
    f = open('crypto-config.yaml', 'w')
    f.write(orderer_config+'\n'+peer_config)
    f.close()

def docker_compose_gen(orderer_num=1,org_num=1,peer_num=1,ca_num=0,couchdb_num=0,cli_num=1):
    version_config = """version: '2'"""
    #log_debug(version_config)
    network_name_config = """networks:
  fabricnetwork:"""
    #log_debug(network_name_config)
    services_config = """services:"""
    #log_debug(services_config)
    
    #############################################
    #
    #   ca config
    #
    #############################################
    total_ca_config = ''
    if ca_num == 0:  # didn't use ca
        total_ca_config = """"""
    elif ca_num == 1:  # each organization has one ca
        ca_config = """  ca.example.com:
    image: hyperledger/fabric-ca
    environment:
      - FABRIC_CA_HOME=/etc/hyperledger/fabric-ca-server
      - FABRIC_CA_SERVER_CA_NAME=ca.example.com
      - FABRIC_CA_SERVER_TLS_ENABLED=false
      - FABRIC_CA_SERVER_TLS_CERTFILE=/etc/hyperledger/fabric-ca-server-config/ca.orgX.example.com-cert.pem
      - FABRIC_CA_SERVER_TLS_KEYFILE=/etc/hyperledger/fabric-ca-server-config/CA_PRIVATE_KEY
    ports:
      - "PORT:7054"
    command: sh -c 'fabric-ca-server start --ca.certfile /etc/hyperledger/fabric-ca-server-config/orgX.example.com-cert.pem --ca.keyfile /etc/hyperledger/fabric-ca-server-config/CA_PRIVATE_KEY_sk -b admin:adminpw -d'
    volumes:
      - ./crypto-config/peerOrganizations/orgX.example.com/ca/:/etc/hyperledger/fabric-ca-server-config
    container_name: ca.example.com
    networks:
      - fabricnetwork"""
        for i in range(0, org_num):
            ca_config_tmp = ca_config.replace('ca.example.com', ('ca'+str(i+1)+'.example.com'))
            ca_config_tmp = ca_config_tmp.replace('orgX', 'org'+str(i+1))
            ca_config_tmp = ca_config_tmp.replace('PORT', str(7054+i*1000))
            ca_private_key = 'CA_PRIVATE_KEY'
            path = 'crypto-config/peerOrganizations/org'+str(i+1)+'.example.com/ca/'
            paths = os.listdir(path)
            for p in paths:
                if p.endswith('_sk'):
                    ca_private_key = p[:-3]
                    break
            ca_config_tmp = ca_config_tmp.replace('CA_PRIVATE_KEY', ca_private_key)
            total_ca_config += (ca_config_tmp + '\n')
    #log_debug(total_ca_config)

    #############################################
    #
    #   orderer config
    #
    #############################################
    orderer_config = ''
    if orderer_num != 1:
        zookeeper_config = ''
        zookeeper_config_template = """  zNUM:
    image: hyperledger/fabric-zookeeper
    restart: always
    container_name: zNUM
    hostname: zNUM
    environment:
      - ZOO_MY_ID=NUM
      - ZOO_SERVERS=server.1=z1:2888:3888 server.2=z2:2888:3888 server.3=z3:2888:3888
    networks:
      - fabricnetwork
    ports:
      - '2181'
      - '2888'
      - '3888'"""
        for i in range(1,4):  ## zookeeper num is 3
            zookeeper_config += zookeeper_config_template.replace('NUM',str(i))
            zookeeper_config += '\n'
        kafka_config = ''
        kafka_config_template = """  kNUM:
    image: hyperledger/fabric-kafka
    restart: always
    container_name: kNUM
    hostname: kNUM
    environment:
      - KAFKA_MESSAGE_MAX_BYTES=103809024
      - KAFKA_REPLICA_FETCH_MAX_BYTES=103809024
      - KAFKA_UNCLEAN_LEADER_ELECTION_ENABLE=false
      - KAFKA_BROKER_ID=NUM
      - KAFKA_MIN_INSYNC_REPLICAS=2
      - KAFKA_DEFAULT_REPLICATION_FACTOR=3
      - KAFKA_ZOOKEEPER_CONNECT=z1:2181,z2:2181,z3:2181
    depends_on:
      - z1
      - z2
      - z3
    networks:
      - fabricnetwork
    ports:
      - '9092'"""
        for i in range(1,5): ## kafka num is 4
            kafka_config += kafka_config_template.replace('NUM', str(i))
            kafka_config += '\n'

        orderer_config_template = """  ordererNUM.example.com:
    image: hyperledger/fabric-orderer
    restart: always
    container_name: ordererNUM.example.com
    environment:
      - CORE_VM_DOCKER_HOSTCONFIG_NETWORKMODE=graduate_fabricnetwork
      - ORDERER_GENERAL_LOGLEVEL=error
      - ORDERER_GENERAL_LISTENADDRESS=0.0.0.0
      - ORDERER_GENERAL_LISTENPORT=7050
      - ORDERER_GENERAL_GENESISMETHOD=file
      - ORDERER_GENERAL_GENESISFILE=/var/hyperledger/orderer/orderer.genesis.block
      - ORDERER_GENERAL_LOCALMSPID=OrdererMSP
      - ORDERER_GENERAL_LOCALMSPDIR=/var/hyperledger/orderer/msp
# enabled TLS - ORDERER_GENERAL_TLS_ENABLED=false
      - ORDERER_GENERAL_TLS_PRIVATEKEY=/var/hyperledger/orderer/tls/server.key
      - ORDERER_GENERAL_TLS_CERTIFICATE=/var/hyperledger/orderer/tls/server.crt
      - ORDERER_GENERAL_TLS_ROOTCAS=[/var/hyperledger/orderer/tls/ca.crt]
      - ORDERER_KAFKA_RETRY_LONGINTERVAL=10s
      - ORDERER_KAFKA_RETRY_LONGTOTAL=100s
      - ORDERER_KAFKA_RETRY_SHORTINTERVAL=1s
      - ORDERER_KAFKA_RETRY_SHORTTOTAL=30s
      - ORDERER_KAFKA_VERBOSE=true
      - ORDERER_KAFKA_BROKERS=[k1:9092,k2:9092,k3:9092,k4:9092]
    working_dir: /opt/gopath/src/github.com/hyperledger/fabric
    command: orderer
    volumes:
      - ./channel-artifacts/genesis.block:/var/hyperledger/orderer/orderer.genesis.block
      - ./crypto-config/ordererOrganizations/example.com/orderers/ordererNUM.example.com/msp:/var/hyperledger/orderer/msp
      - ./crypto-config/ordererOrganizations/example.com/orderers/ordererNUM.example.com/tls/:/var/hyperledger/orderer/tls
    networks:
      - fabricnetwork
    ports:
      - "7050"
    depends_on:
      - z1
      - z2
      - z3
      - k1
      - k2
      - k3
      - k4"""
        for i in range(1, orderer_num+1):
            orderer_config += orderer_config_template.replace('NUM', str(i))
            orderer_config += '\n'
        orderer_config = zookeeper_config + kafka_config + orderer_config
    else:
        orderer_config = """  orderer.example.com:
    restart: always
    container_name: orderer.example.com
    image: hyperledger/fabric-orderer
    environment:
      - ORDERER_GENERAL_LOGLEVEL=debug
      - ORDERER_GENERAL_LISTENADDRESS=0.0.0.0
      - ORDERER_GENERAL_GENESISMETHOD=file
      - ORDERER_GENERAL_GENESISFILE=/var/hyperledger/orderer/orderer.genesis.block
      - ORDERER_GENERAL_LOCALMSPID=OrdererMSP
      - ORDERER_GENERAL_LOCALMSPDIR=/var/hyperledger/orderer/msp
      # enabled TLS
      - ORDERER_GENERAL_TLS_ENABLED=false
      - ORDERER_GENERAL_TLS_PRIVATEKEY=/var/hyperledger/orderer/tls/server.key
      - ORDERER_GENERAL_TLS_CERTIFICATE=/var/hyperledger/orderer/tls/server.crt
      - ORDERER_GENERAL_TLS_ROOTCAS=[/var/hyperledger/orderer/tls/ca.crt]
    working_dir: /opt/gopath/src/github.com/hyperledger/fabric
    command: orderer
    ports:
      - 7050:7050
    volumes:
        - ./channel-artifacts/genesis.block:/var/hyperledger/orderer/orderer.genesis.block
        - ./crypto-config/ordererOrganizations/example.com/orderers/orderer.example.com/msp:/var/hyperledger/orderer/msp
        - ./crypto-config/ordererOrganizations/example.com/orderers/orderer.example.com/tls/:/var/hyperledger/orderer/tls
    networks:
      - fabricnetwork"""
    #log_debug(orderer_config)

    #############################################
    #
    #   peer config
    #
    #############################################
    peer_config = """  peerX.orgY.example.com:
    container_name: peerX.orgY.example.com
    image: hyperledger/fabric-peer
    environment:
      - CORE_VM_ENDPOINT=unix:///host/var/run/docker.sock
      # the following setting starts chaincode containers on the same
      # bridge network as the peers
      # https://docs.docker.com/compose/networking/
      - CORE_VM_DOCKER_HOSTCONFIG_NETWORKMODE=graduate_fabricnetwork
      #- CORE_LOGGING_LEVEL=ERROR
      - CORE_LOGGING_LEVEL=DEBUG
      - CORE_PEER_TLS_ENABLED=false
      - CORE_PEER_GOSSIP_USELEADERELECTION=true
      - CORE_PEER_GOSSIP_ORGLEADER=false
      - CORE_PEER_PROFILE_ENABLED=true
      - CORE_PEER_TLS_CERT_FILE=/etc/hyperledger/fabric/tls/server.crt
      - CORE_PEER_TLS_KEY_FILE=/etc/hyperledger/fabric/tls/server.key
      - CORE_PEER_TLS_ROOTCERT_FILE=/etc/hyperledger/fabric/tls/ca.crt
      #- CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/orgY.example.com/users/Admin@orgY.example.com/msp

      COUCHDB

      - CORE_PEER_ID=peerX.orgY.example.com
      - CORE_PEER_ADDRESS=peerX.orgY.example.com:7051
      - CORE_PEER_GOSSIP_EXTERNALENDPOINT=peerX.orgY.example.com:7051
      - CORE_PEER_GOSSIP_BOOTSTRAP=peerX.orgY.example.com:7051
      - CORE_PEER_LOCALMSPID=OrgYMSP
    working_dir: /opt/gopath/src/github.com/hyperledger/fabric/peer
    command: peer node start
    volumes:
        - /var/run/:/host/var/run/
        - ./crypto-config/peerOrganizations/orgY.example.com/peers/peerX.orgY.example.com/msp:/etc/hyperledger/fabric/msp
        - ./crypto-config/peerOrganizations/orgY.example.com/peers/peerX.orgY.example.com/tls:/etc/hyperledger/fabric/tls
    DEPANDENCY
    ports:
      - PORT1:7051
      - PORT2:7053
    networks:
      - fabricnetwork"""
    total_peer_config = ''
    if couchdb_num == 0:  # didn't use couchdb
        peer_config = peer_config.replace('COUCHDB', '')
        peer_config = peer_config.replace('DEPANDENCY', '')
    elif couchdb_num == 1:  # each org use one couchdb
        peer_config = peer_config.replace('COUCHDB', """- CORE_LEDGER_STATE_STATEDATABASE=CouchDB
      - CORE_LEDGER_STATE_COUCHDBCONFIG_COUCHDBADDRESS=couchdb:5984""")
        
    for x in range(0,peer_num):  # each org has x peers
        for y in range(1,org_num+1):  # total y orgs
            peer_config_tmp = peer_config.replace('peerX', ('peer'+str(x)))
            peer_config_tmp = peer_config_tmp.replace('rgY', ('rg'+str(y)))
            peer_config_tmp = peer_config_tmp.replace('PORT1', str(7051+((y-1)*peer_num+x)*1000))
            peer_config_tmp = peer_config_tmp.replace('PORT2', str(7053+((y-1)*peer_num+x)*1000))
            peer_config_tmp = peer_config_tmp.replace('couchdb','couchdb'+str(org_num*x+y-1))
            peer_config_tmp = peer_config_tmp.replace('DEPANDENCY', """depends_on:
      - couchdb"""+str(org_num*x+y-1))
            total_peer_config += (peer_config_tmp + '\n')
    #log_debug(total_peer_config)

    #############################################
    #
    #   couchdb config
    #
    #############################################
    total_couchdb_config = ''
    if couchdb_num == 0:  # didn't use couchdb
        total_couchdb_config = """"""
    elif couchdb_num == 1:  # each peer has one couchdb
        couchdb_config = """  couchdbX:
    container_name: couchdbX
    image: hyperledger/fabric-couchdb
    ports:
      - "PORT:5984"
    networks:
      - fabricnetwork"""

        for i in range(0,peer_num*org_num):
            couchdb_config_tmp = couchdb_config.replace('couchdbX', ('couchdb'+str(i)))
            couchdb_config_tmp = couchdb_config_tmp.replace('PORT', str(5984+i*1000))
            total_couchdb_config += (couchdb_config_tmp + '\n')
    #log_debug(total_couchdb_config)

    #############################################
    #
    #   cli config
    #
    #############################################
    cli_config = ''
    if cli_num == 1:
        cli_config = """  cli:
    container_name: cli
    image: hyperledger/fabric-tools
    tty: true
    environment:
      - GOPATH=/opt/gopath
      - CORE_VM_ENDPOINT=unix:///host/var/run/docker.sock
      - CORE_LOGGING_LEVEL=DEBUG
      - CORE_PEER_ID=cli
      - CORE_PEER_ADDRESS=peer0.org1.example.com:7051
      - CORE_PEER_LOCALMSPID=Org1MSP
      - CORE_PEER_TLS_ENABLED=false
      - CORE_PEER_TLS_CERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/server.crt
      - CORE_PEER_TLS_KEY_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/server.key
      - CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt
      - CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp
    working_dir: /opt/gopath/src/github.com/hyperledger/fabric/peer
    #command: /bin/bash -c './scripts/script.sh ${CHANNEL_NAME}; sleep $TIMEOUT'
    volumes:
        - /var/run/:/host/var/run/
        - ./chaincode/:/opt/gopath/src/github.com/hyperledger/fabric/examples/chaincode/go
        - ./crypto-config:/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/
        - ./scripts:/opt/gopath/src/github.com/hyperledger/fabric/peer/scripts/
        - ./channel-artifacts:/opt/gopath/src/github.com/hyperledger/fabric/peer/channel-artifacts
    DEPANDENCY
    networks:
      - fabricnetwork"""
        depandency = 'depends_on:\n'
        if orderer_num == 1:
            de = '      - orderer.example.com'
            depandency += (de+'\n')
        else:
            for i in range(1,orderer_num+1):
                de = '      - orderer' + str(i) +'.example.com'
                depandency += (de+'\n')
        for x in range(0,peer_num):
            for y in range(1,org_num+1):
                de = '      - peer'+str(x)+'.org'+str(y)+'.example.com'
                depandency += (de+'\n')
        cli_config = cli_config.replace('DEPANDENCY', depandency)
    #log_debug(cli_config)

    # write to crypto-config.yaml
    f = open('docker-compose.yaml', 'w')
    f.write(version_config+'\n'+network_name_config+'\n'+services_config+'\n'+total_couchdb_config+total_ca_config+orderer_config+'\n'+total_peer_config+cli_config)
    f.close()


if __name__ == '__main__':
    a = raw_input('crypto-config(1) or configtx(2) or docker-compose(3)? ')
    if a == '1':
        crypto_config_gen(orderer_num=3, org_num=2, peer_num=2, couchdb_num=0, ca_num=0)
    elif a == '2':
        configtx_gen(orderer_num=3, org_num=2, peer_num=2, couchdb_num=0, ca_num=0)
    elif a == '3':
        # one orderer, two Orgs, two peers
        #docker_compose_gen(orderer_num=1, org_num=2, peer_num=2)
        # one orderer, two Orgs, two peers, one cli
        #docker_compose_gen(orderer_num=1, org_num=2, peer_num=2, cli_num=1)
        # one orderer, one Org, one peer, one couchdb
        #docker_compose_gen(orderer_num=1, org_num=1, peer_num=1, couchdb_num=1)
        # one orderer, one Org, one peer, one CA
        #docker_compose_gen(orderer_num=1,org_num=1,peer_num=1, ca_num=1)
        # one orderer, two Orgs, two peers, one couchdb
        #docker_compose_gen(orderer_num=1, org_num=2, peer_num=2, couchdb_num=1)
        # one orderer, two Orgs, two peers, one couchdb, one CA
        docker_compose_gen(orderer_num=3, org_num=2, peer_num=2, couchdb_num=0, ca_num=0)
