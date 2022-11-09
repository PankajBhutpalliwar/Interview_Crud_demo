from sqlalchemy.orm import Session
from model import Place
from schemas import AddressCreate,AddressUpdate
from typing import Union

def create_address(db:Session, data: AddressCreate):
    """
    function to create a address model object
    """
    # create Place instance 
    new_address = Place(**data.dict())
    #place object in the database session
    db.add(new_address)
    #commit your instance to the database
    db.commit()
    #reefresh the attributes of the given instance
    db.refresh(new_address)
    return new_address

def retrieve_address(db:Session, data: AddressCreate):
    """
    get the first record with a given latitude and longitude, if no such record exists, will return null
    """
    new_address = Place(**data.dict())
    lat=new_address.latitude
    long=new_address.longitude
    addrs = new_address.address
    db_address = db.query(Place).filter(Place.latitude==lat,Place.longitude==long, Place.address==addrs).all()
    return db_address


def get_address(db: Session, id: int):
    return db.query(Place).get(id)

def update_address(db:Session,item: Union[int, Place], data: AddressUpdate):
    """
    Update a Place object's attributes
    """
    if isinstance(item, int):
        item = get_address(db, item)
    for key, value in data:
        setattr(item, key, value)
    db.commit()
    #db.refresh(db_address) #refresh the attribute of the given instance
    return item

def delete_addresss(db:Session, id:int):
    """
    Delete a Place object
    """
    db_address = get_address(db=db, id=id)
    db.delete(db_address)
    db.commit() #save changes to db

