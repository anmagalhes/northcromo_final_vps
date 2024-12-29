# testetony.py
from fastapi import FastAPI, HTTPException, Depends
from http import HTTPStatus
import uvicorn
from sqlalchemy.orm import Session
from sqlmodel import Session as SQLSession, select, create_engine

# Importing the models and schemas
from app.schemas.tony import UserSchema, UserPublic, UserList
from app.models.aa import UserDB

# Database Setup
DATABASE_URL = "sqlite:///./test.db"  # You can change this to your actual DB URI
engine = create_engine(DATABASE_URL, echo=True)

# Create tables in the database
from sqlmodel import SQLModel
SQLModel.metadata.create_all(engine)

app = FastAPI()

# Dependency to get the database session
def get_db():
    with SQLSession(engine) as session:
        yield session

@app.get("/", status_code=HTTPStatus.OK)
def red_root():
    return {'message': 'teste', 'bata': 'A'}

# Create a user in the database
@app.post("/users/", status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, db: Session = Depends(get_db)):
    # Create a UserDB instance and add to the session
    db_user = UserDB(username=user.username, email=user.email, password=user.password)
    db.add(db_user)
    db.commit()  # Commit to save the user in the database
    db.refresh(db_user)  # Refresh to get the new ID
    return db_user

# Get all users from the database
@app.get("/users/", response_model=UserList)
def read_users(db: Session = Depends(get_db)):
    users = db.exec(select(UserDB)).all()  # Query all users from the database
    return {"users": users}

# Update a user's details
@app.put("/users/{user_id}", response_model=UserPublic)
def update_user(user_id: int, user: UserSchema, db: Session = Depends(get_db)):
    db_user = db.get(UserDB, user_id)  # Find the user by ID
    if not db_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    
    # Update the user's details
    db_user.username = user.username
    db_user.email = user.email
    db_user.password = user.password
    db.commit()  # Commit the changes
    db.refresh(db_user)  # Refresh to get the updated user
    return db_user

# Delete a user from the database
@app.delete("/users/{user_id}", response_model=UserPublic)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.get(UserDB, user_id)  # Find the user by ID
    if not db_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    
    db.delete(db_user)  # Delete the user
    db.commit()  # Commit the changes
    return db_user  # Return the deleted user details

if __name__ == "__main__":
    uvicorn.run("testetony:app", host="0.0.0.0", port=8000, log_level="info", reload=True)
