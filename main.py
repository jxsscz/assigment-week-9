import Adafruit_DHT
import time
import paho.mqtt.client as paho
from paho import mqtt
from time import sleep
 
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4
 
while True:
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        print("Temp={0:0.1f}C Humidity={1:0.1f}%".format(temperature, humidity))
    else:
        print("Sensor failure. Check wiring.");
    time.sleep(3);
    # define static variable
    # broker = "localhost" # for local connection
    # broker = "test.mosquitto.org"  # for online version
    broker = "broker.emqx.io"  # for online version
    port = 1883
    timeout = 60

    username = ''
    password = ''
    topic = "wian/status"
    topicPublish = "wian/greetings"

    def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        client.subscribe(topicPublish,qos=2)
    
    def on_publish(client,userdata,result):
        print("data published \n")

    def on_message(client, userdata, msg):
        print(msg.topicPublish+": "+str(msg.payload.decode('utf-8')))
        


    client1 = paho.Client("device1-wian",userdata=None,protocol=paho.MQTTv5)
    client1.username_pw_set(username=username,password=password)
    client1.on_connect = on_connect
    client1.on_publish = on_publish
    client1.on_message = on_message
    client1.connect(broker,port,timeout)

    count = 0
    while True:
        status = str(input("input? "))
        message = status
        ret = client1.publish(topic,payload=message,qos=1)
        sleep(1)
        count = count + 1