from fastapi import FastAPI
from fastapi.responses import FileResponse
import os

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/geojson", response_class=FileResponse)
def get_geojson():
    # Construct the file path to the isobars.geojson file in the assets folder
    file_path = os.path.join(os.getcwd(), "assets", "isobars.geojson")
    return FileResponse(file_path, media_type="application/geo+json", filename="isobars.geojson")
