from sqlalchemy.orm import Session
from sqlalchemy import text
from pydantic import EmailStr
from models import Admin  # Assuming Admin is your SQLAlchemy model
from fastapi import HTTPException, status, BackgroundTasks
from passlib.hash import bcrypt  # For password hashing
from smtplib import SMTP  # For sending email
from schemas import AdminCreate  # Assuming Pydantic models are in schemas.py

def send_email(email: str, username: str, password: str):
    try:
        with SMTP("smtp.example.com", 587) as smtp:
            smtp.starttls()
            smtp.login("your_email@example.com", "your_password")
            
            subject = "Admin Account Created"
            body = f"Hello {username},\n\nYour admin account has been created. Your password is: {password}"
            msg = f"Subject: {subject}\n\n{body}"

            smtp.sendmail("your_email@example.com", email, msg)
    except Exception as e:
        print(f"Failed to send email: {e}")

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

    # Add the email sending task to the background
    background_tasks.add_task(send_email, admin.email, admin.username, admin.password)

    return {"message": "Admin created successfully"}


