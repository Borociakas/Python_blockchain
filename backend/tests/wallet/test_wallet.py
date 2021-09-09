from backend.config import STARTING_BALANCE

from backend.wallet.wallet import Wallet
from backend.blockchain.blockchain import Blockchain
from backend.wallet.transaction import Transaction

def test_calculate_balance():
    blockchain = Blockchain()
    wallet = Wallet()

    assert Wallet.calculate_balance(blockchain, wallet.address) == STARTING_BALANCE

    amount = 50
    transaction = Transaction(wallet, 'recipient', amount)
    blockchain.add_block([transaction.to_json()])

    assert Wallet.calculate_balance(blockchain, wallet.address) == STARTING_BALANCE - amount

    received_amount_1 = 25
    received_transaction_1 = Transaction(
        Wallet(),
        wallet.address,
        received_amount_1
    )

    received_amount_2 = 55
    received_transaction_2 = Transaction(
        Wallet(),
        wallet.address,
        received_amount_2
    )

    blockchain.add_block(
        [received_transaction_1.to_json(), received_transaction_2.to_json()]
    )

    assert Wallet.calculate_balance(blockchain, wallet.address) == STARTING_BALANCE - amount + received_amount_1 + received_amount_2
