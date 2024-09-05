from fastapi import APIRouter
from fastapi.responses import FileResponse
import os

router = APIRouter()

@router.get("/isobar", response_class=FileResponse)
def get_geojson():
    # Manually set the absolute file path
    file_path = "../../../assets/isobars.geojson"  # Adjust this path as needed
    
    # Check if the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    return FileResponse(file_path, media_type="application/geo+json", filename="isobars.geojson")
