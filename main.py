from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models, schemas

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()






#Return all Users | Query Parameters: skip, limit | Default: skip=0, limit=10
@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(models.User).offset(skip).limit(limit).all()   
    response = [user.get_user() for user in users]
    # print(response)
    return response



#Return User based on ID
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user.get_user()







#Create User | Request Body: UserCreate | Response Body: User
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):    

    user_data = user.model_dump(exclude={'interests'})

    
    user_exists = db.query(models.User).filter(models.User.email == user.email).first()
    if user_exists:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_user = models.User(**user_data)
    db_user.set_interests(user.interests)  
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    

    
    return db_user.get_user()







#Update User | Request Body: UserUpdate | Response Body: User
@app.post("/users/{user_id}",response_model=schemas.User)
def update_user(user_id:int,user:schemas.UserUpdate,db:Session=Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id==user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404,detail="User not found")
    
    
    if user.name is not None:
        db_user.name = user.name
    if user.age is not None:
        db_user.age = user.age
    if user.gender is not None:
        db_user.gender = user.gender
    if user.email is not None:
        db_user.email = user.email
    if user.city is not None:
        db_user.city = user.city
    if user.interests is not None:
        db_user.set_interests(user.interests)
        
    db.commit()
    db.refresh(db_user)
    return db_user.get_user()





#Delete User 
@app.delete("/users/{user_id}")
def delete_user(user_id:int,db:Session=Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id==user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404,detail="User not found")
    
    db.delete(db_user)
    db.commit()
    return {"message":"User deleted successfully"}





#Find Matching Users based on Interests |  Query Parameters: user_id, skip, limit | Default: skip=0, limit=10 | Response Body: List of Users
@app.get("/users/{user_id}/matches",response_model=list[schemas.User])
def read_users(user_id:int,skip: int = 0, limit: int = 10,age_diff:int =0, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    client_age = user.age
    user_interests = user.get_interest()
    users = db.query(models.User).filter(models.User.id != user_id).all()
    matching_users = []
    for user in users:
        if len(set(user.get_interest()).intersection(user_interests))!=0 and abs(user.age-client_age)<=age_diff:
            matching_users.append(user.get_user())
    return matching_users



#Ping Server
@app.get("/hello")
def hello():
    return "Hello World"