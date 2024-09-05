from fastapi import FastAPI
from fastapi.responses import FileResponse
import os

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/geojson", response_class=FileResponse)
def get_geojson():
    file_path = os.path.join(os.getcwd(), "data.geojson")
    return FileResponse(file_path, media_type="application/geo+json", filename="data.geojson")
