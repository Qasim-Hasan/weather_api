from fastapi import fastapi;

app = Fastapi()

@app.get("/")
def root():
    return {"message":"Hello World"}