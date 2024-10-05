from fastapi import FastAPI, HTTPException, Depends,status
from fastapi.middleware.cors import CORSMiddleware  # Import CORS middleware
from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
from controllers.csv_data.station import router as csv_data
from controllers.image_data.images import router as image_data
from typing import Annotated
import models 
from database import engine,SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel
# Import the Admin model from models.py
from models import Admin  # <-- Import your models here
from sqlalchemy import text
from crud import create_admin, get_admin_by_username, AdminCreate, AdminResponse  # Import CRUD functions and Pydantic models
import bcrypt
app = FastAPI()
router = APIRouter()
models.Base.metadata.create_all(bind=engine)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Hello World"}

# Include other routers
app.include_router(csv_data)
app.include_router(image_data)

# Static files serving
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.post("/admin/", status_code=status.HTTP_201_CREATED)
async def create_admin_route(admin: AdminCreate, db: db_dependency):
    result = create_admin(db, admin)
    if result is None:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    return result

@app.get("/admin/{username}", response_model=AdminResponse)
async def get_admin_by_username_route(username: str, db: db_dependency):
    admin = get_admin_by_username(db, username)
    
    if admin is None:
        raise HTTPException(status_code=404, detail="Admin not found")

    return admin

# Pydantic model for admin login
class AdminLogin(BaseModel):
    username: str
    password: str

@app.post("/admin/login", response_model=AdminResponse)
async def login_admin(admin: AdminLogin, db: Session = Depends(db_dependency)):
    print(f"Login attempt for username: {admin.username}")
    
    # Fetch admin details by username
    query = text("SELECT id, username, password FROM admins WHERE username = :username")
    result = db.execute(query, {"username": admin.username}).fetchone()
    
    if result is None:
        print("Admin not found in the database")
        raise HTTPException(status_code=404, detail="Admin not found")

    # Extract the stored password
    stored_password = result[2]  # Assuming password is the third column in your result
    print(f"Stored password: {stored_password}, Provided password: {admin.password}")

    # Compare the provided password with the stored password
    if stored_password != admin.password:
        print("Invalid password provided")
        raise HTTPException(status_code=403, detail="Invalid password")

    # Return admin details if the password is correct
    admin_response = AdminResponse(id=result[0], username=result[1])
    print(f"Login successful for user: {admin_response.username}")
    
    return admin_response




