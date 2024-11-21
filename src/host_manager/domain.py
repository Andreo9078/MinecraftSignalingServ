import uuid
from ipaddress import IPv4Address

from pydantic import BaseModel


class Host(BaseModel):
    user_id: uuid.UUID
    ip: IPv4Address
    port: int
