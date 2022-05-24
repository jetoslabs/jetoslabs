from fastapi import APIRouter
from fastapi.requests import Request
from web3 import Web3

from common.web3 import eth_account
from common.web3.eth_account import ecrecover_for_hex_message_and_signature, recover, sign_msg, ecrecover_from_locally_signed_message
from concepts.schemas.schemas_account import NewAccountReq, NewAccountRes, GenAccountRes, GenAccountReq

router = APIRouter()

"""
Note: Using `Request` in route methods: a. to get logger contextualized by middlewares
"""


@router.post("/new_account", response_model=NewAccountRes)
async def new_account(req: Request, req_body: NewAccountReq) -> NewAccountRes:
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
async def gen_account(req: Request, req_body: GenAccountReq) -> GenAccountRes:
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
async def get_ecrecover_from_locally_signed_message(req: Request, msg: str, key: str, address: str):
    logger = req.scope.get("logger")
    logger.debug("/ecrecover_from_locally_signed_message")

    signed_msg = sign_msg(msg, key)
    logger.debug(f"Signed message: {signed_msg}")

    signed_address = recover(msg, signed_msg, address)
    if signed_address == "":
        raise Exception("recovered address should not be empty")
    # print(f"{v}\n")

    return ecrecover_from_locally_signed_message(signed_msg)


@router.post("/ecrecover_for_hex_message_and_signature")
async def get_ecrecover_for_hex_message_and_signature(req: Request, msg: str, key: str, address: str):
    logger = req.scope.get("logger")
    logger.debug("/ecrecover_for_hex_message_and_signature")

    hex_message = Web3.toHex(msg.encode('utf-8'))
    logger.debug(f"hex_message: {hex_message}")

    signed_msg = sign_msg(msg, key)
    logger.debug(f"Signed message: {signed_msg}")

    hex_signature = Web3.toHex(signed_msg.signature)
    logger.debug(f"hex_signature: {hex_signature}")

    return ecrecover_for_hex_message_and_signature(hex_message, hex_signature)
