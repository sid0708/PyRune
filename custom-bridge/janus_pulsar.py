import paho.mqtt.client as mqtt
import pulsar
import json
import os
import random
import datetime
from tenacity import wait_exponential, retry, stop_after_attempt

# MQTT
print("The MQTT configs are being set up....")
NODE_IP = os.getenv("NODE_IP", "localhost")
mqttBroker = NODE_IP
mqttPort = 31884
mqtt.Client.connected_flag = False
mqtt.Client.bad_connection_flag = False
unique_client_id = "MQTTBRIDGE" + str(random.randint(0, 10000))
# Pulsar configs
client = pulsar.Client('pulsar://pulsar-broker.petuum-system:6650')
producer = client.create_producer('topic1')



def on_message(client, userdata, message):
    msg_payload = str(message.payload)
    new_dict = {}
    print('Received MQTT message', msg_payload)
    # Cast byte string to string
    z = json.loads(msg_payload)
    try:
        if z.get("values")is not None:
            new_dict = [dict([a, str(x)] for a, x in b.items()) for b in z["values"]]
        else:
            print("No Payload")
    except IndexError as e:
        print(f"Exception occured in payload {e}")
    #cast the values to  str
    current_timestamp =curr_timestamp = int(datetime.now().timestamp() * 1000)
    msg_payload = {{"timestamp": current_timestamp, "values": new_dict}}
    producer.send(msg_payload.encode())
    print('Pulsar: Just published '+ str(msg_payload) + 'to topic topic1 ')

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








