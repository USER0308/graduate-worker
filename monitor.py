import hfc
from hfc.fabric import Client

class Monitor:

    def query_installed_chaincode(self):
        cli = Client(net_profile='network.json')
        org1_admin = cli.get_user(org_name='org1.example.com', name='Admin')
        channel = cli.new_channel('mychannel')
        installed_chaincode = cli.query_installed_chaincodes(requestor=org1_admin,peer_names=['peer0.org1.example.com'])
        print(installed_chaincode)
        return str(installed_chaincode)

    def query_instantiated_chaincode(self):
        cli = Client(net_profile='network.json')
        org1_admin = cli.get_user(org_name='org1.example.com', name='Admin')
        channel = cli.new_channel('mychannel')
        instantiated_chaincode = cli.query_instantiated_chaincodes(requestor=org1_admin, channel_name='mychannel', peer_names=['peer0.org1.example.com'])
        print(instantiated_chaincode)
        return str(instantiated_chaincode)

    def query_channel(self):
        cli = Client(net_profile='network.json')
        org1_admin = cli.get_user(org_name='org1.example.com', name='Admin')
        channel = cli.new_channel('mychannel')
        channel = cli.query_channels(requestor=org1_admin, peer_names=['peer0.org1.example.com'])
        print(channel)
        return str(channel)

    def get_channel_config(self):
        cli = Client(net_profile='network.json')
        org1_admin = cli.get_user(org_name='org1.example.com', name='Admin')
        channel = cli.new_channel('mychannel')
        config = cli.get_channel_config(requestor=org1_admin, channel_name='mychannel', peer_names=['peer0.org1.example.com'])
        return str(config)

    def query_info(self):
        cli = Client(net_profile='network.json')
        org1_admin = cli.get_user(org_name='org1.example.com', name='Admin')
        channel = cli.new_channel('mychannel')
        info = cli.query_info(requestor=org1_admin, channel_name='mychannel', peer_names=['peer0.org1.example.com'])
        print(info)
        return str(info)

    def query_block_by_hash(self, block_hash):
        cli = Client(net_profile='network.json')
        org1_admin = cli.get_user(org_name='org1.example.com', name='Admin')
        channel = cli.new_channel('mychannel')
        info = cli.query_info(requestor=org1_admin, channel_name='mychannel', peer_names=['peer0.org1.example.com'])
        block_hash = info.currentBlockHash
        block = cli.query_block_by_hash(requestor=org1_admin, channel_name='mychannel', peer_names=['peer0.org1.example.com'], block_hash=block_hash)
        print(block)
        return str(block)

    def query_block_by_txid(self, tx_id):
        cli = Client(net_profile='network.json')
        org1_admin = cli.get_user(org_name='org1.example.com', name='Admin')
        channel = cli.new_channel('mychannel')
        block = cli.query_block_by_txid(requestor=org1_admin, channel_name='mychannel', peer_names=['peer0.org1.example.com'], tx_id=tx_id)
        print(block)
        return str(block)

    def query_transaction_by_txid(self, tx_id):
        cli = Client(net_profile='network.json')
        org1_admin = cli.get_user(org_name='org1.example.com', name='Admin')
        channel = cli.new_channel('mychannel')
        transaction = cli.query_transaction(requestor=org1_admin, channel_name='mychannel', peer_names=['peer0.org1.example.com'], tx_id=tx_id)
        print(transaction)
        return str(transaction)


if __name__ == '__main__':
    query_installed_chaincode()
    query_instantiated_chaincode()
    query_channel()
    get_channel_config()
    query_info()
#    query_block_by_hash(block_hash=)
#    query_block_by_txid(tx_id=)
#    query_transaction_by_txid(tx_id=)
