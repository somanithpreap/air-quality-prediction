import pickle
import requests
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

app = FastAPI()

# CORS setup for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

frontend_path = os.path.join(os.path.dirname(__file__), "../frontend")
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")

@app.get("/")
def root():
    return FileResponse(os.path.join(frontend_path, "index.html"))

# Load model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

# Input schema
class LocationInput(BaseModel):
    country: str
    state: str
    city: str

@app.post("/predict")
def predict(location: LocationInput):
    API_KEY = os.getenv("IQAIR_API_KEY")
    url = (
        f"http://api.airvisual.com/v2/city?city={location.city}"
        f"&state={location.state}&country={location.country}&key={API_KEY}"
    )

    resp = requests.get(url)
    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail="Failed to fetch data from IQAir")

    current_data = resp.json().get("data", {}).get("current", {})
    pollution = current_data.get("pollution", {})
    weather = current_data.get("weather", {})

    # Extract features (you can update the list to match your model)
    features = [
        pollution.get("pm2_5", 0),
        pollution.get("pm10", 0),
        pollution.get("o3", 0),
        pollution.get("co", 0),
        pollution.get("no2", 0),
        pollution.get("so2", 0),
        weather.get("tp", 0),
        weather.get("ws", 0),
    ]

    prediction = model.predict([features])[0]
    actual = pollution.get("aqius", None)

    return {
        "predicted_aqi": prediction,
        "actual_aqi": actual,
        "features": {
            "PM2.5": pollution.get("pm2_5", 0),
            "PM10": pollution.get("pm10", 0),
            "O3": pollution.get("o3", 0),
            "CO": pollution.get("co", 0),
            "NO2": pollution.get("no2", 0),
            "SO2": pollution.get("so2", 0),
            "Temperature": weather.get("tp", 0),
            "Wind": weather.get("ws", 0)
        }
    }
