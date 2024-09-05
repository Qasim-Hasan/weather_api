from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware  # Import CORS middleware
import os

app = FastAPI()

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

@app.get("/geojson", response_class=FileResponse)
def get_geojson():
    # Construct the file path to the isobars.geojson file in the assets folder
    file_path = os.path.join(os.getcwd(), "../assets", "isobars.geojson")
    return FileResponse(file_path, media_type="application/geo+json", filename="isobars.geojson")
