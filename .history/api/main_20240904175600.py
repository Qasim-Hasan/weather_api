from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # Import CORS middleware
from controllers.geojson_data.isobars import router as isobar_router  
from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
import os

app = FastAPI()
router = APIRouter()

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

# Include the isobar router
app.include_router(isobar_router)

# Static files serving
app.mount("/assets", StaticFiles(directory="../assets"), name="assets")  # Ensure this path is correct

@router.get("/isobar-data")
def get_isobar_data():
    data = {
        "png_url": "http://localhost:8000/assets/kriging_isobars.png",  # Adjust URL if necessary
        "coordinates": {
            "bounds": [
                [23.64, 60.87],
                [37.08, 23.13]
            ]
        }
    }
    return JSONResponse(content=data)