from fastapi import APIRouter
from fastapi.responses import FileResponse
import os
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/isobar", response_class=FileResponse)


@router.get("/isobar-data")
def get_isobar_data():
     # URL to the PNG image and coordinates
     
    data = {
        "png_url": "http://localhost:8000/assets/kriging_isobars.png",  
        "coordinates": {
            "bounds": [
                [60.87, 23.63],
                [77.05, 37.23]
            ]
        }
    }
    return JSONResponse(content=data)
