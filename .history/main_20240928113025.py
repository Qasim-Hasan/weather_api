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
app = FastAPI()
router = APIRouter()
models.Base.metadata.create_all(bind=engine)

class AdminBase(BaseModel):
    id: int
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


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()   
        
        
db_dependency = Annotated[Session, Depends(get_db)]        

@app.post("/admin/")
def create_admin(username: str, password: str, db: Session = Depends(get_db)):
    admin = Admin(username=username, password=password)
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return {"message": "Admin created", "admin": admin}