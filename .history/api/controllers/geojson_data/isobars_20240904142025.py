# isobar.py
from fastapi import APIRouter
from fastapi.responses import FileResponse
import os

router = APIRouter()

@router.get("/isobar", response_class=FileResponse)
def get_geojson():
    # Construct the file path to the isobars.geojson file in the assets folder
    file_path = os.path.join(os.getcwd(), "..\..\..\assets", "isobars.geojson")
    return FileResponse(file_path, media_type="application/geo+json", filename="isobars.geojson")
