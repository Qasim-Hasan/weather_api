from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

router = APIRouter()

# Assume received_data_type is defined globally somewhere in your main application.
received_data_type: str = "synop"  # Default data type

@router.get("/image-data")
def get_image_data(
    image_type: str = Query(..., description="Type of image requested (e.g., 'isobar', 'isotherm', 'isoneph')")
):
    # Check if the current data type is 'synop'
    if received_data_type == "synop":
        # Hardcoded URLs for the images
        if image_type == "isobar":
            layer_image_url = "http://localhost:8000/assets/isobars.png"
            heatmap_image_url = "http://localhost:8000/assets/isobars_heatmap.png"
        elif image_type == "isotherm":
            layer_image_url = "http://localhost:8000/assets/isotherms.png"
            heatmap_image_url = "http://localhost:8000/assets/isotherms_heatmap.png"
        elif image_type == "isoneph":
            layer_image_url = "http://localhost:8000/assets/isonephs.png"
            heatmap_image_url = "http://localhost:8000/assets/isonephs_heatmap.png"
        else:
            return JSONResponse(content={"error": "Invalid image type"}, status_code=400)

        # Define coordinates (bounds)
        coordinates = {
            "bounds": [
                [60.87, 23.63],
                [77.05, 37.23]
            ]
        }

        # Construct the response data
        data = {
            "layer_image_url": layer_image_url,
            "heatmap_image_url": heatmap_image_url,
            "coordinates": coordinates
        }

        return JSONResponse(content=data)

    # Handle the cases for 'metar' and 'wis2'
    elif received_data_type in ["metar", "wis2"]:
        return JSONResponse(content={"error": "No image data available for the requested data type."}, status_code=204)

    # If the data type is not recognized
    return JSONResponse(content={"error": "Invalid data type."}, status_code=400)

