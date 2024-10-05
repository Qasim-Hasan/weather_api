from sqlalchemy.orm import Session
from sqlalchemy import text
from pydantic import BaseModel
from models import Admin  # Assuming Admin is your SQLAlchemy model

# Define Pydantic models
class AdminCreate(BaseModel):
    username: str
    password: str

class AdminResponse(BaseModel):
    id: int
    username: str
   

    class Config:
        from_attributes = True  # Enables compatibility with ORM

def create_admin(db: Session, admin: AdminCreate):
    query = text("SELECT * FROM admins WHERE username = :username")
    result = db.execute(query, {"username": admin.username}).fetchone()

    if result:
        return None  # Username already exists

    insert_query = text("INSERT INTO admins (username, password) VALUES (:username, :password)")
    db.execute(insert_query, {"username": admin.username, "password": admin.password})
    db.commit()
    
    return {"message": "Admin created successfully"}

def get_admin_by_username(db: Session, username: str) -> AdminResponse:
    query = text("SELECT id, username, password FROM admins WHERE username = :username")  # Fetch the password
    result = db.execute(query, {"username": username}).fetchone()

    if result is None:
        return None  # Admin not found

    return AdminResponse(id=result[0], username=result[1], password=result[2])  # Include password in response
