from fastapi import FastAPI, HTTPException, Depends,status
from fastapi.middleware.cors import CORSMiddleware  # Import CORS middleware
from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
from controllers.csv_data.station import router as csv_data
from controllers.image_data.images import router as image_data
from typing import Annotated
from functionality.login import AdminLogin, AdminResponse, get_admin_by_username, login_admin
from functionality.signup import AdminCreate, create_admin
import models 
from database import engine,SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel
# Import the Admin model from models.py
from models import Admin  # <-- Import your models here
from sqlalchemy import text
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

# sending username and password from frontend and returning login success and message
@app.post("/admin/login", response_model=AdminResponse)
async def login_admin_route(admin: AdminLogin, db: Annotated[Session, Depends(get_db)]):
    return login_admin(db, admin)  # Call the login_admin function from crud.py

