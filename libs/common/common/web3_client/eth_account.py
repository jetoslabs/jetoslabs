# https://web3py.readthedocs.io/en/stable/web3.eth.account.html#working-with-local-private-keys
# https://soliditydeveloper.com/ecrecover
# https://soliditydeveloper.com/meta-transactions

from eth_account import Account
from eth_account.signers.local import LocalAccount
from pydantic import BaseModel
from web3 import Web3

from eth_account.messages import encode_defunct, _hash_eip191_message


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


def sign_msg(w3_provider, msg, private_key):
    message = encode_defunct(text=msg)
    signed_message = w3_provider.eth.account.sign_message(message, private_key=private_key)
    return signed_message


def recover(w3_provider, msg, signed_message, signer_address) -> str:
    message = encode_defunct(text=msg)
    address = w3_provider.eth.account.recover_message(message, signature=signed_message.signature)
    if address != signer_address:
        return ""
    return address


#####################
class Ecrecover_Schema(BaseModel):
    msghash: str
    v: int
    r: str
    s: str


# ecrecover in Solidity expects v as a native uint8, but r and s as left-padded bytes32
# Remix / web3.js expect r and s to be encoded to hex
# This convenience method will do the pad & hex for us:
def to_32byte_hex(val):
    return Web3.toHex(Web3.toBytes(val).rjust(32, b'\0'))


def ecrecover_from_locally_signed_message(signed_message) -> Ecrecover_Schema:
    """
    Prepare locally signed_message for Solidity
    :param signed_message:
    :return:
    """
    ec_recover = Ecrecover_Schema(
        msghash=Web3.toHex(signed_message.messageHash),
        v=signed_message.v,
        r=to_32byte_hex(signed_message.r),
        s=to_32byte_hex(signed_message.s)
    )
    return ec_recover


#
# For message and a signature encoded to hex. Then this will prepare ecrecover args for Solidity
def ecrecover_for_hex_message_and_signature(hex_message: str, hex_signature: str):
    # ecrecover in Solidity expects an encoded version of the message

    # - encode the message
    message = encode_defunct(hexstr=hex_message)

    # - hash the message explicitly
    message_hash = _hash_eip191_message(message)

    # Remix / web3.js expect the message hash to be encoded to a hex string
    hex_message_hash = Web3.toHex(message_hash)

    # ecrecover in Solidity expects the signature to be split into v as a uint8, and r, s as a bytes32
    sig = Web3.toBytes(hexstr=hex_signature)
    v, hex_r, hex_s = Web3.toInt(sig[-1]), Web3.toHex(sig[:32]), Web3.toHex(sig[32:64])

    # ecrecover in Solidity takes the arguments in order = (msghash, v, r, s)
    ec_recover_args = (hex_message_hash, v, hex_r, hex_s)
    return ec_recover_args

