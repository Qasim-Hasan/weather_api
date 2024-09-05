from fastapi import FastAPI;

app = Fastapi()

@app.get("/")
def root():
    return {"message":"Hello World"}