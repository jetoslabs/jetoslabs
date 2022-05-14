from eth_account import Account
from eth_account.signers.local import LocalAccount


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