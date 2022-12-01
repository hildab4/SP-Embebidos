# subscribe to mqtt topic and save to wav file

import paho.mqtt.client as mqtt
import math

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))


print("Connecting to MQTT broker")

client = mqtt.Client()

client.on_connect = on_connect

client.connect("localhost", 1883, 60)

# Publish sine wave of peak to peak amplitude of 1000, center at 500 and length of 3500 samples
for i in range(0, 3500):
    val = int(500 * math.sin(i * 2 * math.pi / 3500) + 500)
    client.publish(
        "esp32/Mic", val.to_bytes(2, byteorder='little'), qos=0, retain=False)
