
from fastapi import FastAPI
import model, crud, schemas
from db import engine
from db import SessionLocal
from fastapi import Depends
from sqlalchemy.orm import Session
import logging


# Create and configure logger
logging.basicConfig(filename="data.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
 
# Creating an object
logger = logging.getLogger()
 
# Setting the threshold of logger to Critical
logger.setLevel(logging.CRITICAL)

#create the database tables on app startup or reload
model.Base.metadata.create_all(bind=engine)
logger.info("Database created")

app = FastAPI()
#database connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"Hello": "FastAPI_TEST"}


#define endpoint
@app.post("/create_address", response_model=schemas.Address)
def create_address(data: schemas.AddressCreate, db:Session = Depends(get_db)):
    try:
        address = crud.create_address(db, data)
    except Exception as e:
        logging.critical(e, exc_info=True)
    ##return object created
    return address

#get/retrieve address 
@app.get("/get_address/{id}/") #id is a path parameter
def get_address(id:int, db:Session = Depends(get_db)):
    try:
        address = crud.get_address(db=db, id=id)
    except Exception as e:
        logging.critical(e, exc_info=True)
    return address

@app.post("/retrieve_address")
def retrieve_address(data: schemas.AddressCreate, db:Session = Depends(get_db)):
    try:
        address_list = crud.retrieve_address(db=db,data=data)
    except Exception as e:
        logging.critical(e, exc_info=True)
    return address_list

@app.put("/update_address/{id}/", response_model=schemas.Address) #id is a path parameter
def update(id: int, data: schemas.AddressUpdate, db:Session=Depends(get_db)):
    #get Place object from database
    #check if Place object exists
    try:
        item = crud.update_address(db, id, data)
        if item is None:
            logger.error("address doesnt exist")
            return {"error": f"address with id {id} does not exist"}
    except Exception as e:
        logging.critical(e, exc_info=True)        
    return item
        

@app.delete("/delete_address/{id}/") #id is a path parameter
def delete_address(id:int, db:Session=Depends(get_db)):
    #get Place object from database
    db_address = crud.get_address(db=db, id=id)
    #check if Place object exists
    if db_address is not None:
        crud.delete_addresss(db, id)
        return None
    else:
        logger.error("address doesnt exist")
        return {"error": f"address with id {id} does not exist"}