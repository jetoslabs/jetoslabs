# https://web3py.readthedocs.io/en/stable/web3.eth.account.html

from eth_account import Account
from eth_account.signers.local import LocalAccount

from web3.auto import w3
from eth_account.messages import encode_defunct


async def create_with_mnemonic(passphrase: str = "") -> tuple[LocalAccount, str]:
    """
    Creates new eth Account and mnemonic
    :param passphrase:
    :return: tuple of LocalAccount and mnemonic
    """
    Account.enable_unaudited_hdwallet_features()
    account, mnemonic = Account.create_with_mnemonic(passphrase)
    return account, mnemonic


async def gen_from_mnemonic(mnemonic: str, passphrase: str = "") -> LocalAccount:
    """
    Generate an account from a mnemonic
    :param mnemonic:
    :param passphrase:
    :return: LocalAccount
    """
    Account.enable_unaudited_hdwallet_features()
    account: LocalAccount = Account.from_mnemonic(mnemonic=mnemonic, passphrase=passphrase)
    return account


def sign(msg, private_key):
    message = encode_defunct(text=msg)
    signed_message = w3.eth.account.sign_message(message, private_key=private_key)
    return signed_message


def verify_return_address(msg, signed_message):
    message = encode_defunct(text=msg)
    address = w3.eth.account.recover_message(message, signature=signed_message.signature)
    return address


def verify(msg, signed_message, from_address):
    # message = encode_defunct(text=msg)
    # address = w3.eth.account.recover_message(message, signature=signed_message.signature)
    return from_address == verify_return_address(msg, signed_message)
