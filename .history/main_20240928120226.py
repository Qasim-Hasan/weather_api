# main.py
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import Annotated
from database import engine, SessionLocal, models
from database import crud  # Import the CRUD operations
from pydantic import BaseModel

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
async def create_admin(admin: crud.AdminCreate, db: db_dependency):
    success = crud.create_admin(db, admin)
    if not success:
        raise HTTPException(status_code=400, detail="Username already registered")

    return {"message": "Admin created successfully"}

@app.get("/admin/{username}", response_model=crud.AdminResponse)
async def get_admin_by_username(username: str, db: db_dependency):
    print(f"Fetching admin with username: {username}")

    result = crud.get_admin_by_username(db, username)
    if result is None:
        print("Admin not found in the database")
        raise HTTPException(status_code=404, detail="Admin not found")

    # Map the result to the AdminResponse model
    admin = crud.AdminResponse(id=result[0], username=result[1])
    return admin
