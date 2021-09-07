from backend.blockchain.block import Block


class Blockchain:
    """
    Blockchain: a public ledger of transactions.
    Implemented as a list of blocks - data sets of transactions
    """

    def __init__(self):
        self.chain = [Block.genesis()]

    def add_block(self, data):
        self.chain.append(Block.mine_block(self.chain[-1], data))

    def __repr__(self):
        return f'Blockchain: {self.chain}'

    def replace_chain(self, chain):
        """
        Replace the local chain with the incoming one if thw following rules applies:
            - The incoming chain is longer than the local one
            - the chain is formatted properly
        """
        if len(chain) <= len(self.chain):
            raise Exception('Cannot replace. Incoming chain must be longer')

        try:
            Blockchain.is_valid_chain(chain)
        except Exception as e:
            raise Exception(
                f'Cannot replace. The incoming chain is invalid: {e}')

        self.chain = chain

    @staticmethod
    def is_valid_chain(chain):
        """
        Validate the incoming chain.
        Enforce the following rules of the blockchain:
            - the chain must start with the genesis block
            - the blocks must be formatted correctly
        """
        if(chain[0] != Block.genesis()):
            raise Exception('The genesis block must be valid')

        for i in range(1, len(chain)):
            block = chain[i]
            last_block = chain[i-1]
            Block.is_valid_block(last_block, block)

    def to_json(self):
        """
        Serialize the blockchain into a list of blocks.
        """
        return list(map(lambda block: block.to_json(), self.chain))

    @staticmethod
    def from_json(chain_json):
        """
        Deserialize a list of serialized blocks into a Blockchain instance
        The result will contain a chain list of Block instances.
        """
        blockchain = Blockchain()
        blockchain.chain = list(
            map(lambda block_json: Block.from_json(block_json), chain_json)
        )

        return Blockchain
        
def main():
    blockchain = Blockchain()

    blockchain.add_block("one")
    blockchain.add_block("two")
    blockchain.add_block("three")
    blockchain.add_block("four")
    blockchain.add_block("five")
    # blockchain.chain[2].hash = 'gsdgddg'

    for i in range(len(blockchain.chain)):
        print(blockchain.chain[i])
        print('\n')

    Blockchain.is_valid_chain(blockchain.chain)


if __name__ == '__main__':
    main()
