from fastapi import APIRouter
from fastapi.responses import FileResponse
import os
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/isotherm", response_class=FileResponse)

def get_geojson():

    filename = "isotherms.geojson"
    
    # Construct the file path using the directory of the current file and the filename
    file_path = os.path.join(os.path.dirname(__file__), "../../../assets", filename)
    
    # Check if the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    return FileResponse(file_path, media_type="application/geo+json", filename="isobars.geojson")
