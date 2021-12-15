import pika, os, csv, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime
import paho.mqtt.client as mqtt

broker_address="40.71.125.21"
my_bucket_voltaje = os.environ.get("DOCKER_INFLUXDB_INIT_BUCKET")
my_bucket_corriente = os.environ.get("DOCKER_INFLUXDB_INIT_BUCKET_CORRIENTE")
my_bucket_potencia = os.environ.get("DOCKER_INFLUXDB_INIT_BUCKET_POTENCIA")
my_bucket_water = os.environ.get("DOCKER_INFLUXDB_INIT_BUCKET_WATER")
my_bucket_motobomba = os.environ.get("DOCKER_INFLUXDB_INIT_BUCKET_MOTOBOMBA")

buckets = [my_bucket_voltaje, my_bucket_corriente, my_bucket_potencia, my_bucket_water, my_bucket_motobomba]
print("Iniciando...")
print("Buckets ->", buckets, end = "\n\n")

my_org = os.environ.get("DOCKER_INFLUXDB_INIT_ORG")
my_token  = os.environ.get("DOCKER_INFLUXDB_INIT_ADMIN_TOKEN")
client_influx = InfluxDBClient(url="http://influxdb:8086", token=my_token, org=my_org)

def proccess_function(message, bucket):
    print(message)
    
    try:
        message = float(message)
        if(bucket == 'water'):
            message = ((50 - message)/50) * 100
            
        write_api = client_influx.write_api(write_options=SYNCHRONOUS)
        query_api = client_influx.query_api()
        point = Point(bucket+'_target').field(bucket, message).time(datetime.utcnow(), WritePrecision.NS)
        write_api.write(bucket, my_org, point)
        return
    except ValueError:
        return

def on_message(client, userdata, message):
    print("nuevo mensaje ->", message.topic)
    msg = str(message.payload.decode("utf-8"))
    
    if message.topic == 'voltaje':
        proccess_function(msg, my_bucket_voltaje)
        
    if message.topic == 'corriente':
        proccess_function(msg, my_bucket_corriente)
        
    if message.topic == 'potencia':
        proccess_function(msg, my_bucket_potencia)
    
    if message.topic == 'water':
        proccess_function(msg, my_bucket_water)
        
    if message.topic == 'motobomba':
        proccess_function(msg, my_bucket_motobomba)

client = mqtt.Client("broker")
client.on_message=on_message
client.connect(broker_address)
client.loop_start()
client.subscribe(my_bucket_voltaje, qos=1)
client.subscribe(my_bucket_corriente, qos=1)
client.subscribe(my_bucket_potencia, qos=1)
client.subscribe(my_bucket_water, qos=1)
client.subscribe(my_bucket_motobomba, qos=1)
client.loop_forever()