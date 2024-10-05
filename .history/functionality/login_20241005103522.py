from sqlalchemy.orm import Session
from sqlalchemy import text
from pydantic import BaseModel
from models import Admin  # Assuming Admin is your SQLAlchemy model
from fastapi import FastAPI, HTTPException, Depends,status


# AdminResponse Pydantic model to return success or failure
class AdminResponse(BaseModel):
    success: bool
    message: str
        
        # Pydantic model for admin login
class AdminLogin(BaseModel):
    username: str
    password: str
    
class UserResponse(BaseModel):
    id: int
    username: str
    password: str




def get_admin_by_username(db: Session, username: str) -> UserResponse:
    query = text("SELECT id, username, password FROM admins WHERE username = :username")  # Fetch the password
    result = db.execute(query, {"username": username}).fetchone()

    if result is None:
        return None  # Admin not found

    return UserResponse(id=result[0], username=result[1], password=result[2])  # Include password in response


# Function to handle admin login logic
def login_admin(db: Session, admin: AdminLogin) -> AdminResponse:
    print(f"Login attempt for username: {admin.username}")
    
    # Fetch admin details by username
    query = text("SELECT id, username, password FROM admins WHERE username = :username")
    result = db.execute(query, {"username": admin.username}).fetchone()
    
    if result is None:
        print("Admin not found in the database")
        return AdminResponse(success=False, message="Admin not found")

    # Extract the stored password
    stored_password = result[2]  # Assuming password is the third column in the result
    print(f"Stored password: {stored_password}, Provided password: {admin.password}")

    # Compare the provided password with the stored password
    if stored_password != admin.password:
        print("Invalid password provided")
        return AdminResponse(success=False, message="Invalid password")

    # Return success if the password matches
    print(f"Admin {admin.username} logged in successfully")
    return AdminResponse(success=True, message="Login successful")
