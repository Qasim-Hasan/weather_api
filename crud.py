# database/crud.py
from sqlalchemy.orm import Session
from sqlalchemy import text
from models import Admin
from pydantic import BaseModel

class AdminCreate(BaseModel):
    username: str
    password: str

class AdminResponse(BaseModel):
    id: int
    username: str

def create_admin(db: Session, admin: AdminCreate):
    # Check if the admin username already exists using raw SQL
    query = text("SELECT * FROM admins WHERE username = :username")
    result = db.execute(query, {"username": admin.username}).fetchone()

    if result:
        return False  # Indicate that the username already exists

    # Insert the new admin into the database
    insert_query = text("INSERT INTO admins (username, password) VALUES (:username, :password)")
    db.execute(insert_query, {"username": admin.username, "password": admin.password})
    db.commit()
    return True

def get_admin_by_username(db: Session, username: str):
    query = text("SELECT id, username FROM admins WHERE username = :username")
    result = db.execute(query, {"username": username}).fetchone()
    return result  # Returns None if not found
