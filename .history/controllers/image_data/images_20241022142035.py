from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel

router = APIRouter()

# Global variable to hold the received data type
received_data_type: str = "synop"  # Default data type

# Request model for the data type
class DataTypeRequest(BaseModel):
    datatype: str

# Common image paths based on data type and image type
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

# Define the bounds (coordinates) common for all images
coordinates = {
    "bounds": [
        [60.87, 23.63],
        [77.05, 37.23]
    ]
}

@router.post("/data-type", response_model=dict, status_code=201)
async def receive_data_type(data: DataTypeRequest):
    global received_data_type  # Declare the global variable
    received_data_type = data.datatype.lower()  # Update the data type and convert to lowercase for consistency
    print(f"Received data type: {received_data_type}")
    
    # Automatically trigger the image response for the updated data type
    response = get_image_data_automatically(received_data_type)

    if isinstance(response, JSONResponse):
        return response

    return {"message": "Data type received successfully, but no image was returned.", "datatype": received_data_type}


def get_image_data_automatically(data_type: str):
    # Check if the data type is supported
    if data_type not in image_paths:
        return JSONResponse(content={"error": "Invalid or unsupported data type."}, status_code=400)

    # Get the first available image type for the current data type
    # This can be modified to choose a specific image type or allow the client to specify it
    if data_type == "synop":
        image_type = "isobar"  # For example, auto-select "isobar"
        if image_type not in image_paths[data_type]:
            return JSONResponse(content={"error": f"No images available for {data_type} and {image_type}."}, status_code=204)
        
        image_data = image_paths[data_type][image_type]

        data = {
            "layer_image_url": image_data["layer_image_url"],
            "heatmap_image_url": image_data["heatmap_image_url"],
            "coordinates": coordinates
        }

        return JSONResponse(content=data)

    # Handle the cases for 'metar' and 'wis2' where no images are available yet
    elif data_type in ["metar", "wis2"]:
        return JSONResponse(content={"error": "No image data available for the requested data type."}, status_code=204)

    # If the data type is not recognized
    return JSONResponse(content={"error": "Invalid data type."}, status_code=400)


