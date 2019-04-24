import hfc
from hfc.fabric import Client

class Monitor:

    cli = Client(net_profile='network.json')
    org1_admin = cli.get_user(org_name='org1.example.com', name='Admin')
    channel = cli.new_channel('mychannel')

    def query_installed_chaincode(self):
        installed_chaincode = self.cli.query_installed_chaincodes(requestor=self.org1_admin,peer_names=['peer0.org1.example.com'])
        print(installed_chaincode)
        return str(installed_chaincode)

    def query_instantiated_chaincode(self):
        instantiated_chaincode = self.cli.query_instantiated_chaincodes(requestor=self.org1_admin, channel_name='mychannel', peer_names=['peer0.org1.example.com'])
        print(instantiated_chaincode)
        return str(instantiated_chaincode)

    def query_channel(self):
        channel = self.cli.query_channels(requestor=self.org1_admin, peer_names=['peer0.org1.example.com'])
        print(channel)
        return str(channel)

    def get_channel_config(self):
        config = self.cli.get_channel_config(requestor=self.org1_admin, channel_name='mychannel', peer_names=['peer0.org1.example.com'])
        return str(config)

    def query_info(self):
        info = self.cli.query_info(requestor=self.org1_admin, channel_name='mychannel', peer_names=['peer0.org1.example.com'])
        print(info)
        return str(info)

    def query_block_by_hash(self, block_hash):
        block = self.cli.query_block_by_hash(requestor=self.org1_admin, channel_name='mychannel', peer_names=['peer0.org1.example.com'], block_hash=block_hash)
        print(block)
        return str(block)

    def query_block_by_txid(self, tx_id):
        block = self.cli.query_block_by_txid(requestor=self.org1_admin, channel_name='mychannel', peer_names=['peer0.org1.example.com'], tx_id=tx_id)
        print(block)
        return str(block)

    def query_transaction_by_txid(self, tx_id):
        transaction = self.cli.query_transaction(requestor=self.org1_admin, channel_name='mychannel', peer_names=['peer0.org1.example.com'], tx_id=tx_id)
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
