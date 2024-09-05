from fastapi import APIRouter
from fastapi.responses import FileResponse
import os
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/isobar", response_class=FileResponse)

def get_geojson():
    # Construct the file path using the correct relative path
  #  file_path = "C:/Users/Aala computer/Desktop/fyp_api/assets/isobars.geojson"
    # file_path = os.path.join(os.path.dirname(__file__), "../../../assets/isobars.geojson")
    # Define the filename as a variable
    filename = "isobars.geojson"
    
    # Construct the file path using the directory of the current file and the filename
    file_path = os.path.join(os.path.dirname(__file__), "../../../assets", filename)
    
    # Check if the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    return FileResponse(file_path, media_type="application/geo+json", filename="isobars.geojson")


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

@router.get("/isobar-csv", response_class=FileResponse)
def get_isobar_csv():
    # Construct the file path for the CSV file
    filename = "station.csv"  # Replace with your actual CSV filename
    file_path = os.path.join(os.path.dirname(__file__), "../../../assets", filename)

    # Check if the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    return FileResponse(file_path, media_type="text/csv", filename="data.csv")