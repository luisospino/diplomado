# example_consumer.py
import pika, os, csv, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime
import paho.mqtt.client as mqtt #import the client1

broker_address="40.71.125.21"

my_bucket = "device1"
my_org    = "taller3"
my_token  = "YJSP3DWMheK7UQcXngRpFAYIqvhLtaVn25BYnursFzix9A3L5V4qNtFDuZXKrk422eBSCQrAnInKDIo78GKRzA=="
client_influx = InfluxDBClient(url="http://influxdb:8086", token=my_token, org=my_org)

def process_function(mesage):
    #mesage = mesage.decode("utf-8")
    print(mesage)      
    write_api = client_influx.write_api(write_options=SYNCHRONOUS)
    query_api = client_influx.query_api()
    point = Point("Medicion").tag("Ubicacion", "Santa Marta").field("temperatura", float(mesage)).time(datetime.utcnow(), WritePrecision.NS)
    write_api.write(my_bucket, my_org, point)    
    return

def on_message(client, userdata, message):
    msg = str(message.payload.decode("utf-8"))
    process_function(msg)
    #enviar la data al influx

client = mqtt.Client("test") #create new instance
client.on_message=on_message
client.connect(broker_address) #connect to broker
client.loop_start()
client.subscribe("device1", qos=1)
# client.publish("device1", 12)#publish
client.loop_forever() #loop forever