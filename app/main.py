from fastapi.middleware.cors import CORSMiddleware
import paho.mqtt.client as mqtt
from fastapi import FastAPI
import pika, os

print('BUCKET=> ' + os.environ.get("DOCKER_INFLUXDB_INIT_BUCKET_MOTOBOMBA"))

broker_address="40.71.125.21"
my_bucket = os.environ.get("DOCKER_INFLUXDB_INIT_BUCKET_MOTOBOMBA")
app = FastAPI(title="API del proyecto final", description="API de IOT", version="1.0.0")

client = mqtt.Client("test")
client.loop_start()
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

@app.get("/motobomba/{status}")
async def index(status: str):
    client.publish(my_bucket, status, 2)
    return "STATUS MOTOBOMBA => " + status
