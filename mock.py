# subscribe to mqtt topic and save to wav file

import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))


print("Connecting to MQTT broker")

client = mqtt.Client()

client.on_connect = on_connect

client.connect("localhost", 1883, 60)

# Publish sine wave of amplitude 1000 and period 100
for i in range(0, 3500):
    value = int(1000 * math.sin(i * 2 * math.pi / 100))
    client.publish("esp32/Mic", value.to_bytes(2, byteorder='little'))
