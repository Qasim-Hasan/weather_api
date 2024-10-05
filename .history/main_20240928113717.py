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
from models import Admin
from sqlalchemy import text
app = FastAPI()
router = APIRouter()
models.Base.metadata.create_all(bind=engine)

# Define the Pydantic model for Admin creation
class AdminCreate(BaseModel):
    username: str
    password: str

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins, change to specific origins for production
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
def root():
    return {"message": "Hello World"}

# Station data is in csv
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
async def create_admin(admin: AdminCreate, db: db_dependency):
    # Check if the admin username already exists using raw SQL
    query = text("SELECT * FROM admins WHERE username = :username")
    result = db.execute(query, {"username": admin.username}).fetchone()

    if result:
        raise HTTPException(status_code=400, detail="Username already registered")

    # Insert the new admin into the database using raw SQL
    insert_query = text(
        "INSERT INTO admins (username, password) VALUES (:username, :password)"
    )
    db.execute(insert_query, {"username": admin.username, "password": admin.password})

    # Commit the transaction
    db.commit()

    return {"message": "Admin created successfully"}