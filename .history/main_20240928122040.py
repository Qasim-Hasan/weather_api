from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter
from fastapi.staticfiles import StaticFiles
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel
from sqlalchemy import text
from crud import create_admin, get_admin_by_username, login_admin, AdminCreate, AdminResponse, AdminLogin  # Import CRUD functions and Pydantic models

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
async def login_admin_route(admin: AdminLogin, db: db_dependency):
    # Fetch admin details by username
    query = text("SELECT id, username, password FROM admins WHERE username = :username")
    result = db.execute(query, {"username": admin.username}).fetchone()
    
    if result is None:
        raise HTTPException(status_code=404, detail="Admin not found")

    # Validate the provided password against the stored password
    stored_password = result[2]  # Assuming password is the third column in your result
    if stored_password != admin.password:
        raise HTTPException(status_code=403, detail="Invalid password")

    # Return admin details if the password is correct
    return AdminResponse(id=result[0], username=result[1], password=stored_password)  # Include password in response
