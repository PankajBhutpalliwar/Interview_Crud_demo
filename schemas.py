from typing import Optional
from model import Place
from pydantic import BaseModel


class AddressBase(BaseModel):
    address : str
    latitude: int
    longitude:int

class AddressCreate(AddressBase):
    pass


class AddressUpdate(AddressBase):
    pass

class Address(AddressBase):
    id:int
    
    class Config:
        orm_mode = True