from typing import Tuple

import loguru
from aiohttp import ClientResponse
from eth_account import Account
from eth_account.signers.local import LocalAccount

from account.core.server_resources import server_resources
from common.decorators.retry import retry


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


async def ping_google(*, logger: loguru.logger) -> Tuple[ClientResponse, str]:
    @retry(times=3, logger=logger)
    async def ping():
        async with server_resources.http_client.get("https://www.google.com") as resp:
            return resp, await resp.text()
    return await ping()
