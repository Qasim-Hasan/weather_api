from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel

router = APIRouter()

# Global variable to hold the received data type
received_data_type: str = "synop"  # Default data type

# Request model for the data type
class DataTypeRequest(BaseModel):
    datatype: str

@router.post("/data-type", response_model=dict, status_code=201)
async def receive_data_type(data: DataTypeRequest):
    global received_data_type  # Declare the global variable
    received_data_type = data.datatype.lower()  # Update the data type and convert to lowercase for consistency
    print(f"Received data type: {received_data_type}")
    return {"message": "Data type received successfully", "datatype": received_data_type}

@router.get("/image-data")
def get_image_data(
    image_type: str = Query(..., description="Type of image requested (e.g., 'isobar', 'isotherm', 'isoneph')")
):
    # Define the bounds (coordinates) common for all images
    coordinates = {
        "bounds": [
            [60.87, 23.63],
            [77.05, 37.23]
        ]
    }

    # Dictionary to store image paths based on data type and image type
    image_paths = {
        "synop": {
            "isobar": {
                "layer_image_url": "http://localhost:8000/assets/isobars.png",
                "heatmap_image_url": "http://localhost:8000/assets/isobars_heatmap.png"
            },
            "isotherm": {
                "layer_image_url": "http://localhost:8000/assets/isotherms.png",
                "heatmap_image_url": "http://localhost:8000/assets/isotherms_heatmap.png"
            },
            "isoneph": {
                "layer_image_url": "http://localhost:8000/assets/isonephs.png",
                "heatmap_image_url": "http://localhost:8000/assets/isonephs_heatmap.png"
            }
        },
        "metar": {},  # Add respective images for METAR if necessary
        "wis2": {}    # Add respective images for WIS2 if necessary
    }

    # Check if the data type is supported
    if received_data_type not in image_paths:
        return JSONResponse(content={"error": "Invalid or unsupported data type."}, status_code=400)

    # Check if the image type is valid for the received data type
    if image_type not in image_paths[received_data_type]:
        return JSONResponse(content={"error": "Invalid image type for the selected data type."}, status_code=400)

    # Get the image URLs for the selected image type
    image_data = image_paths[received_data_type][image_type]

    # Return the image data with the coordinates
    data = {
        "layer_image_url": image_data["layer_image_url"],
        "heatmap_image_url": image_data["heatmap_image_url"],
        "coordinates": coordinates
    }

    return JSONResponse(content=data)
