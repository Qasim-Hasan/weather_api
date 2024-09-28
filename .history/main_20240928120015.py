from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Annotated
from pydantic import BaseModel
import models
from database import engine, SessionLocal

app = FastAPI()
router = APIRouter()
models.Base.metadata.create_all(bind=engine)

# Define Pydantic models
class AdminCreate(BaseModel):
    username: str
    password: str

class AdminResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True  # Enables compatibility with ORM

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    query = text("SELECT * FROM admins WHERE username = :username")
    result = db.execute(query, {"username": admin.username}).fetchone()

    if result:
        raise HTTPException(status_code=400, detail="Username already registered")

    insert_query = text("INSERT INTO admins (username, password) VALUES (:username, :password)")
    db.execute(insert_query, {"username": admin.username, "password": admin.password})
    db.commit()

    return {"message": "Admin created successfully"}

@app.get("/admin/{username}", response_model=AdminResponse)
async def get_admin_by_username(username: str, db: db_dependency):
    print(f"Fetching admin with username: {username}")
    
    query = text("SELECT id, username FROM admins WHERE username = :username")
    result = db.execute(query, {"username": username}).fetchone()

    if result is None:
        print("Admin not found in the database")
        raise HTTPException(status_code=404, detail="Admin not found")

    admin = AdminResponse(id=result[0], username=result[1])
    return admin


