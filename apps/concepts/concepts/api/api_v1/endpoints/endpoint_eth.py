from fastapi import APIRouter
from fastapi.requests import Request

from common.web3 import eth_account
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

