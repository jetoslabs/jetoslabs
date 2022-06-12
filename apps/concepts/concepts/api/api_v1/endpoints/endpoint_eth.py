import ipfshttpclient
from fastapi import APIRouter, Depends
from fastapi.requests import Request
from web3 import Web3

from common.ipfs_client.ipfs_client import ipfs_cat, ipfs_add_bytes
from common.web3_client import eth_account
from common.web3_client.eth_account import ecrecover_for_hex_message_and_signature, recover, sign_msg, ecrecover_from_locally_signed_message
from common.web3_client.eth_tx import send_eth, tx_sign_and_send
from concepts.abi.abi import STORAGE_ABI
from concepts.api.deps import get_w3_provider, get_ipfs_client

from concepts.schemas.schemas_account import NewAccountReq, NewAccountRes, GenAccountRes, GenAccountReq

router = APIRouter()

"""
Note: Using `Request` in route methods: a. to get logger contextualized by middlewares
"""


@router.post("/new_account", response_model=NewAccountRes)
async def post_new_account(req: Request, req_body: NewAccountReq) -> NewAccountRes:
    logger = req.scope.get("logger")
    logger.debug("/new_account")
    account, mnemonic = await eth_account.create_with_mnemonic(req_body.passphrase)
    res = NewAccountRes(
        address=account.address,
        key=account.key.hex(),
        privateKey=account.privateKey.hex(),
        mnemonic=mnemonic
    )
    return res


@router.post("/gen_account", response_model=GenAccountRes)
async def post_gen_account(req: Request, req_body: GenAccountReq) -> GenAccountRes:
    logger = req.scope.get("logger")
    logger.debug("/gen_account")
    account = await eth_account.gen_from_mnemonic(req_body.mnemonic, req_body.passphrase)
    res = GenAccountRes(
        address=account.address,
        key=account.key.hex(),
        privateKey=account.privateKey.hex(),
        mnemonic=req_body.mnemonic
    )
    return res


@router.post("/ecrecover_from_locally_signed_message")
async def post_ecrecover_from_locally_signed_message(req: Request, msg: str, key: str, address: str, w3_provider: Web3 = Depends(get_w3_provider)):
    logger = req.scope.get("logger")
    logger.debug("/ecrecover_from_locally_signed_message")

    signed_msg = sign_msg(w3_provider, msg, key)
    logger.debug(f"Signed message: {signed_msg}")

    signed_address = recover(w3_provider, msg, signed_msg, address)
    if signed_address == "":
        raise Exception("recovered address should not be empty")
    # print(f"{v}\n")

    return ecrecover_from_locally_signed_message(signed_msg)


@router.post("/ecrecover_for_hex_message_and_signature")
async def post_ecrecover_for_hex_message_and_signature(req: Request, msg: str, key: str, address: str, w3_provider: Web3 = Depends(get_w3_provider)):
    logger = req.scope.get("logger")
    logger.debug("/ecrecover_for_hex_message_and_signature")

    hex_message = Web3.toHex(msg.encode('utf-8'))
    logger.debug(f"hex_message: {hex_message}")

    signed_msg = sign_msg(w3_provider, msg, key)
    logger.debug(f"Signed message: {signed_msg}")

    hex_signature = Web3.toHex(signed_msg.signature)
    logger.debug(f"hex_signature: {hex_signature}")

    return ecrecover_for_hex_message_and_signature(hex_message, hex_signature)


@router.post("/send_eth")
async def post_send_ether(req: Request, from_address:str, from_key: str, to_address: str, ether: float, w3_provider: Web3 = Depends(get_w3_provider)):
    logger = req.scope.get("logger")
    logger.debug("/send_eth")
    return send_eth(w3_provider, from_address, from_key, to_address, ether)


@router.post("/call_storage_contract_store_fn")
async def post_call_storage_contract_store_fn(req: Request, from_address:str, from_key: str, to_address: str, ether: float, contract_address: str, w3_provider: Web3 = Depends(get_w3_provider)):
    logger = req.scope.get("logger")
    logger.debug("/call_contract")

    #TODO: error handling when contract address is nkt right.. etc
    storage_contract = w3_provider.eth.contract(address=contract_address, abi=STORAGE_ABI)

    storage_txn = storage_contract.functions.store(456).buildTransaction({
        # 'chainId': 1,
        'gas': 4000000,
        'gasPrice': w3_provider.toWei('50', 'gwei'),
        # 'maxFeePerGas': w3_provider.toWei('2', 'gwei'),
        # 'maxPriorityFeePerGas': w3_provider.toWei('1', 'gwei'),
        'nonce': w3_provider.eth.getTransactionCount(from_address),
    })

    tx_hash_hex = tx_sign_and_send(w3_provider, from_key, storage_txn)

    return tx_hash_hex


@router.post("/ipfs_add")
async def post_ipfs_add(data: str, ipfs_client=Depends(get_ipfs_client)):
    return ipfs_add_bytes(ipfs_client, data.encode('utf-8'))


@router.post("/ipfs_cat")
async def post_ipfs_cat(content_hash: str, ipfs_client=Depends(get_ipfs_client)):
    return ipfs_cat(ipfs_client, content_hash)

