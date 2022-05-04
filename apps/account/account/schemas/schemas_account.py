from pydantic import BaseModel


class NewAccountReq(BaseModel):
    passphrase: str


class AccountRes(BaseModel):
    address: str
    key: str
    privateKey: str
    mnemonic: str


class NewAccountRes(AccountRes):
    pass


class GenAccountReq(BaseModel):
    mnemonic: str
    passphrase: str


class GenAccountRes(AccountRes):
    pass
