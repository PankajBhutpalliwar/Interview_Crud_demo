from sqlalchemy import Column, Integer, String
from db import Base

# model/table
class Place(Base):
    __tablename__ = "address_table1"

    # fields 
    id = Column(Integer,primary_key=True, index=True)
    address = Column(String, index = True)
    latitude = Column(Integer, index=True)
    longitude = Column(Integer, index=True)
