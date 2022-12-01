# subscribe to mqtt topic and save to wav file

import paho.mqtt.client as mqtt
import wave


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("esp32/Mic")


payload = []


def on_message(client, userdata, msg):
    payload = msg.payload
    print(payload)


client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

client.loop_forever()
