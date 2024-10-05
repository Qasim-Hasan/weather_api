import bcrypt
from sqlalchemy.orm import Session
from sqlalchemy import text
from pydantic import BaseModel
from models import Admin  # Assuming Admin is your SQLAlchemy model
from fastapi import FastAPI, HTTPException, Depends,status
import bcrypt
print(bcrypt.__version__)

class AdminResponse(BaseModel):
    success: bool
    message: str
  
class AdminLogin(BaseModel):
    username: str
    password: str
    
class UserResponse(BaseModel):
    id: int
    username: str
    email: str




def get_admin_by_username(db: Session, username: str) -> UserResponse:
    query = text("SELECT id, username, email FROM admins WHERE username = :username")  # Fetch the password
    result = db.execute(query, {"username": username}).fetchone()

    if result is None:
        return None  # Admin not found

    return UserResponse(id=result[0], username=result[1], email=result[2])  # Include password in response


# Function to handle admin login logic
def login_admin(db: Session, admin: AdminLogin) -> AdminResponse:
    
    # Fetch admin details by username
    query = text("SELECT id, username, password FROM admins WHERE username = :username")
    result = db.execute(query, {"username": admin.username}).fetchone()
    
    if result is None:
        print("Admin not found in the database")
        return AdminResponse(success=False, message="Admin not found")

    # Extract the stored password
    stored_password = result[2]  # Assuming password is the third column in the result

    # Verify the provided password with the stored hashed password
    if not bcrypt.checkpw(admin.password.encode('utf-8'), stored_password.encode('utf-8')):
        return AdminResponse(success=False, message="Invalid password")
    
    return AdminResponse(success=True, message="Login successful")
