from pydantic import BaseModel

from common.config.schemas.schema_config import Config


class PublicHomeSchema(BaseModel):
    title: str
    desc: str
    config: Config | None
