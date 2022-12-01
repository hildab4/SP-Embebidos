# subscribe to mqtt topic and save to wav file

import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))


print("Connecting to MQTT broker")

client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

client.publish("esp32/Mic", "Hello")
