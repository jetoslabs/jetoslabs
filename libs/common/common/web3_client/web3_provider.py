from fastapi import HTTPException
from starlette import status
from web3 import Web3


def get_w3_provider(uri: str) -> Web3:
    if not uri or len(uri) == 0:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="web3 provider is not available"
        )
    return Web3(Web3.HTTPProvider(uri))
