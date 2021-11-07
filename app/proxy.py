import pika, os, csv, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime
import paho.mqtt.client as mqtt

broker_address="40.71.125.21"
my_bucket = os.environ.get("DOCKER_INFLUXDB_INIT_BUCKET")
my_org = os.environ.get("DOCKER_INFLUXDB_INIT_ORG")
my_token  = os.environ.get("DOCKER_INFLUXDB_INIT_ADMIN_TOKEN")
client_influx = InfluxDBClient(url="http://influxdb:8086", token=my_token, org=my_org)

def process_function(mesage):
    print(mesage)      
    write_api = client_influx.write_api(write_options=SYNCHRONOUS)
    query_api = client_influx.query_api()
    point = Point("Medicion").tag("Ubicacion", "Santa Marta").field("temperatura", float(mesage)).time(datetime.utcnow(), WritePrecision.NS)
    write_api.write(my_bucket, my_org, point)    
    return

def on_message(client, userdata, message):
    msg = str(message.payload.decode("utf-8"))
    process_function(msg)

client = mqtt.Client("test")
client.on_message=on_message
client.connect(broker_address)
client.loop_start()
client.subscribe(my_bucket, qos=1)
client.loop_forever()