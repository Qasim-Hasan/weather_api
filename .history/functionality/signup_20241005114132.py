from sqlalchemy.orm import Session
from sqlalchemy import text
from pydantic import BaseModel, EmailStr
from fastapi import HTTPException, status, BackgroundTasks
from passlib.hash import bcrypt  # For password hashing
import smtplib  # For sending email
from email.mime.text import MIMEText  # For creating email messages
from email.mime.multipart import MIMEMultipart  # For multipart emails

# Define Pydantic models
class AdminCreate(BaseModel):
    username: str
    password: str
    email: EmailStr  

def send_email(to_email: str, username: str, password: str):
    # Configure your email details
    from_email = "aervion.careers@gmail.com"
    from_password = "Alhsq1965"  # Use an app password if 2FA is enabled

    # Create the email content
    subject = "Account Created Successfully"
    body = f"""
    Hi {username},

    Your admin account has been created successfully.
    Username: {username}
    Password: {password}  # It is recommended to change this password after the first login.

    Best Regards,
    Your Company
    """

    # Set up the email server
    try:
        # Create a multipart email
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Attach the body to the email
        msg.attach(MIMEText(body, 'plain'))

        # Send the email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Start TLS encryption
            server.login(from_email, from_password)  # Login to your email account
            server.send_message(msg)  # Send the email
        print(f"Email sent to {to_email}")

    except Exception as e:
        print(f"Failed to send email: {str(e)}")

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

    # Send an email to the admin with the account details
    background_tasks.add_task(send_email, admin.email, admin.username, admin.password)

    return {"message": "Admin created successfully"}



