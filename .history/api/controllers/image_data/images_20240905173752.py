from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/image-data")
def get_image_data():
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
