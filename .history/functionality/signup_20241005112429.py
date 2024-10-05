from sqlalchemy.orm import Session
from sqlalchemy import text
from pydantic import BaseModel, EmailStr
from models import Admin  # Assuming Admin is your SQLAlchemy model
from fastapi import HTTPException, status, BackgroundTasks
from passlib.hash import bcrypt  # For password hashing

# Define Pydantic models
class AdminCreate(BaseModel):
    username: str
    password: str
    email: EmailStr  

def create_admin(db: Session, admin: AdminCreate, background_tasks: BackgroundTasks):
    # Check if the username already exists
    query = text("SELECT * FROM admins WHERE username = :username")
    result = db.execute(query, {"username": admin.username}).fetchone()

    if result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

    # Hash the password before storing it
    hashed_password = bcrypt.hash(admin.password)

    # Insert the new admin into the database
    insert_query = text(""" 
        INSERT INTO admins (username, password, email) 
        VALUES (:username, :password, :email)
    """)
    db.execute(insert_query, {"username": admin.username, "password": hashed_password, "email": admin.email})
    db.commit()

    # For now, we can simply print the email details instead of sending an email
    print(f"Admin account created for {admin.username}. Email would be sent to: {admin.email} with password: {admin.password}")


    return {"message": "Admin created successfully"}




