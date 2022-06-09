from typing import Dict, Optional

from pydantic import BaseModel


class Tenant(BaseModel):
    tenant: str


class AWS(BaseModel):
    aws_access_key_id: str
    aws_access_secret: str
    aws_region: str
    aws_output: str


class S3(BaseModel):
    bucket: str
    default_object_prefix: str


class Web3Provider(BaseModel):
    provider_uri: str


class TenantConfig(Tenant):
    aws: Optional[AWS]
    s3: Optional[S3]
    web3: Optional[Web3Provider]


class Config(BaseModel):
    SYSTEM: Optional[TenantConfig]
    tenants: Optional[Dict[str, TenantConfig]]
