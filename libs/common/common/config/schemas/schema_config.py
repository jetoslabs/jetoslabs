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


class TenantConfig(Tenant):
    aws: Optional[AWS]
    s3: Optional[S3]


class Config(BaseModel):
    SYSTEM: TenantConfig
    tenants: Dict[str, TenantConfig]
