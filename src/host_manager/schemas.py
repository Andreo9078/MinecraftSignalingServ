from ipaddress import IPv4Address

from pydantic import BaseModel


class CreateHost(BaseModel):
    ip: IPv4Address
    port: int
