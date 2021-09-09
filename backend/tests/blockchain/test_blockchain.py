import pytest

from backend.blockchain.blockchain import Blockchain
from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet
from backend.blockchain.block import GENESIS_DATA

@pytest.fixture
def blockchain_three_blocks():
    blockchain = Blockchain()
    for i in range(3):
        blockchain.add_block([Transaction(Wallet(), 'recipient', i).to_json()])
    return blockchain

# def test_valid_transaction_chain():
#     blockchain = Blockchain()
#     for i in range(3):
#         blockchain.add_block([Transaction(Wallet(), 'recipient', i).to_json()])

#     Blockchain.is_valid_transaction_chain(blockchain.chain)


# def test_is_vallid_transaction_chain_duplicate_transactions(blockchain_three_blocks):
#     transaction = Transaction(Wallet(), 'recipient', 1).to_json()


# def test_is_valid_transaction_chain_bad_historic_balance():
#     blockchain = Blockchain()
#     for i in range(3):
#         blockchain.add_block([Transaction(Wallet(), 'recipient', i).to_json()])

#     wallet = Wallet()
#     bad_transaction = Transaction(wallet, 'recipient', 1)
#     bad_transaction.output[wallet.address] = 9000
#     bad_transaction.input['amount'] = 9001
#     bad_transaction.input['signature'] = wallet.sign(bad_transaction.output)

#     blockchain.add_block([bad_transaction.to_json()])

#     with pytest.raises(Exception, match='has an invalid input amount'):
#         Blockchain.is_valid_transaction_chain(blockchain.chain)