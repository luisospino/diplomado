# example_consumer.py
import pika, os, csv, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime
import paho.mqtt.client as mqtt #import the client1

broker_address="40.71.125.21"

# my_bucket = "device1"
# my_org    = "taller3"
# my_token  = "-77eJIW6Bd3NWSLnHsnsfT5U90P-SKgeYx8R2JI5lxRPHVFKR_O5Wl4kkZ7WpvNGO-OukFqAVWbP7tDW9tMYYg=="

# client = InfluxDBClient(url="http://influxdb:8086", token=my_token, org=my_org)

def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)

client = mqtt.Client("test") #create new instance
client.on_message=on_message
client.connect(broker_address) #connect to broker
client.loop_start()
client.subscribe("device1", qos=1)
client.publish("device1","Yo soy un topico melo")#publish
# time.sleep(10) # wait
client.loop_forever() #stop the loop

print("..s.s")

# def process_function(mesage):
#   mesage = mesage.decode("utf-8")
#   print(mesage)      
#   write_api = client.write_api(write_options=SYNCHRONOUS)
#   query_api = client.query_api()
#   point = Point("Medicion").tag("Ubicacion", "Santa Marta").field("temperatura", float(mesage)).time(datetime.utcnow(), WritePrecision.NS)
#   write_api.write(my_bucket, my_org, point)    
#   return

# while 1:
#   url = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@rabbit:5672/%2f')
#   params = pika.URLParameters(url)
#   connection = pika.BlockingConnection(params)
#   channel = connection.channel() # start a channel
#   channel.queue_declare(queue='mensajes') # Declare a queue
#   # create a function which is called on incoming messages
#   def callback(ch, method, properties, body):
#     process_function(body)

#   # set up subscription on the queue
#   channel.basic_consume('mensajes',
#     callback,
#     auto_ack=True)

#   # start consuming (blocks)
#   channel.start_consuming()
#   connection.close()