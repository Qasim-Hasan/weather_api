from fastapi import APIRouter
from fastapi.responses import FileResponse
import os

router = APIRouter()

@router.get("/isobar", response_class=FileResponse)
def get_geojson():
    # Construct the file path using the correct relative path
    file_path = os.path.join(os.getcwd(), "../../../assets/", "isobars.geojson")
    
    # Check if the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    return FileResponse(file_path, media_type="application/geo+json", filename="isobars.geojson")
