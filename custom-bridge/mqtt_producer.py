import paho.mqtt.client as mqtt
from random import randrange, uniform
import time

mqttBroker = "mqtt.eclipseprojects.io"
client = mqtt.Client("MQTTProducer2")
client.connect(mqttBroker)

while True:
    randNumber = randrange(10)
    client.publish("temperature4", randNumber)
    print("Just published " + str(randNumber) + " to Topic temperature4")
    time.sleep(1)
