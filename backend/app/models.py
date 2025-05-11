from pydantic import BaseModel, IPvAnyAddress
from typing import List, Optional

class IPInput(BaseModel):
    ip_address: IPvAnyAddress
    subnet_mask: Optional[str] = None  # Allow both CIDR and mask

class SubnetSplitInput(BaseModel):
    ip_address: IPvAnyAddress
    subnet_mask: str
    required_subnets: int

class SubnetResult(BaseModel):
    network_id: str
    broadcast_address: str
    first_usable_ip: str
    last_usable_ip: str
    total_usable_hosts: int
    wildcard_mask: str
    ip_class: str
    is_private: bool

class IPInputV6(BaseModel):
    ip_address: IPvAnyAddress
    cidr: int  

class SubnetResultV6(BaseModel):
    ip_address: str
    full_ip_address: str
    total_addresses: str
    network_id: str
    ip_range: str
    first_usable_ip: str
    last_usable_ip: str
    is_private: bool

class IPv6SplitInput(BaseModel):
    ip_address: IPvAnyAddress
    cidr: int
    required_subnets: int

class IPv6SubnetResult(BaseModel):
    network_id: str
    prefix_length: int
    total_addresses: str
    ip_range: str
    first_usable_ip: str
    last_usable_ip: str
    is_private: bool


class MaskSuggestionInput(BaseModel):
    host_count: int

class MaskSuggestionResult(BaseModel):
    suggested_cidr: str
    subnet_mask: str
    usable_hosts: int
    wildcard_mask: str
