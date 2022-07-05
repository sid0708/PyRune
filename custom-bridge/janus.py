import paho.mqtt.client as mqtt
from pykafka import KafkaClient
import os
import random
from tenacity import wait_exponential, retry, stop_after_attempt

# MQTT
print("The MQTT configs are being set up....")
NODE_IP = os.getenv("NODE_IP", "localhost")
mqttBroker = NODE_IP
mqttPort = 31883
mqtt.Client.connected_flag = False
mqtt.Client.bad_connection_flag = False
unique_client_id = "MQTTBRIDGE" + str(random.randint(0, 10000))
# Kafka


print("The KAFKA configs are being set up....")
kafka_client = KafkaClient(hosts='zkless-kafka-bootstrap:9092')
kafka_topic = kafka_client.topics['topic1']
kafka_producer = kafka_topic.get_sync_producer()


def on_message(client, userdata, message):
    msg_payload = str(message.payload)
    print('Received MQTT message', msg_payload)
    kafka_producer.produce(str(msg_payload).encode('ascii'))
    print('KAFKA: Just published '+ str(msg_payload) + 'to topic topic1 ')

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        mqtt.Client.connected_flag = True # set flag
        print("Connected OK")
        return mqtt.Client.connected_flag
    else:
        print("Bad connection, RC = ", rc)
        mqtt.Client.bad_connection_flag = True

@retry(wait=wait_exponential(multiplier=2, min=2, max=30), stop=stop_after_attempt(5))
def mqtt_run():
    mqtt_client = mqtt.Client(unique_client_id, protocol=mqtt.MQTTv31)
    mqtt_client.connect(host=mqttBroker, port=mqttPort)
    print("Connected to MQTT")
    mqtt_client.on_connect = on_connect
    try:
        mqtt_client.subscribe(topic='topic1',qos=1)
        print("Connected to topic1")
        mqtt_client.on_message = on_message
        mqtt_client.loop_forever()
    except Exception as e:
        mqtt_client.disconnect()
        mqtt_client.loop_stop()

if __name__ == '__main__':
    print("Main execution started.")
    mqtt_run()








