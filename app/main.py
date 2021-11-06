from fastapi import FastAPI
import pika
from fastapi.middleware.cors import CORSMiddleware
import paho.mqtt.client as mqtt

broker_address="40.71.125.21"
app = FastAPI(title="api de botones", description="esta es una api de control", version="1.0.0")

client = mqtt.Client("test")
client.connect(broker_address)

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/fan/{status}")
async def index(status: str):
    client.publish("device1", status)
    return "status => " + status
