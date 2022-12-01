# subscribe to mqtt topic and save to wav file

import paho.mqtt.client as mqtt

import matplotlib.pyplot as plt
import time
import numpy as np

SAMPLES = 3500

start = time.time()
count = 0

x = np.arange(0, SAMPLES, 1)

y = [0]*SAMPLES

fig = plt.figure()
ax = fig.add_subplot(111)
line1, = ax.plot(x, y, 'b-')

count = 0


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("esp32/Mic")


def on_message(client, userdata, msg):
    payload = msg.payload
    int_val = int.from_bytes(payload, byteorder='little')
    lin1.set_ydata(int_val)
    fig.canvas.draw()
    fig.canvas.flush_events()


print("Connecting to MQTT broker")

client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

client.loop_forever()
