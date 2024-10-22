from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel

router = APIRouter()

# Global variable to hold the received data type
received_data_type: str = "synop"  # Default data type

# Request model for the data type
class DataTypeRequest(BaseModel):
    datatype: str

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

# Function to retrieve image data based on the current datatype
def get_image_data_for_datatype(datatype: str):
    # Define the bounds (coordinates) common for all images
    coordinates = {
        "bounds": [
            [60.87, 23.63],
            [77.05, 37.23]
        ]
    }

    # Check if the data type is supported
    if datatype not in image_paths:
        return {"error": "Invalid or unsupported data type."}

    # Assuming 'isobar' as default image type for the selected data type
    image_type = "isobar"
    
    if image_type not in image_paths[datatype]:
        return {"error": "Invalid image type for the selected data type."}

    # Get the image URLs for the default image type
    image_data = image_paths[datatype][image_type]

    # Return the image data with the coordinates
    return {
        "layer_image_url": image_data["layer_image_url"],
        "heatmap_image_url": image_data["heatmap_image_url"],
        "coordinates": coordinates
    }

@router.post("/data-type", response_model=dict, status_code=201)
async def receive_data_type(data: DataTypeRequest):
    global received_data_type  # Declare the global variable
    received_data_type = data.datatype.lower()  # Update the data type and convert to lowercase for consistency
    print(f"Received data type: {received_data_type}")

    # Fetch the image data for the updated datatype
    image_data = get_image_data_for_datatype(received_data_type)
    
    # If there's an error in fetching the images, return it
    if "error" in image_data:
        return JSONResponse(content={"message": "Data type received successfully", "datatype": received_data_type, "error": image_data["error"]}, status_code=400)
    
    # Return the confirmation and the image data
    return {
        "message": "Data type received successfully",
        "datatype": received_data_type,
        "image_data": image_data
    }

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
