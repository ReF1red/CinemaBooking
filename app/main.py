from fastapi import FastAPI

app = FastAPI(title="Cinema Booking API")

@app.get("/")
def root():
    return {"message": "Cinema Booking API is running"}