from pydantic import BaseModel


class FirewallRule(BaseModel):
    ip_address: str
    mac_address: str
