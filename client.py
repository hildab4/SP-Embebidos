# subscribe to mqtt topic and save to wav file

import paho.mqtt.client as mqtt

from matplotlib import pyplot as plt
import matplotlib.animation as animation
import time

start = time.time()
count = 0

fig = plt.gcf()
fig.show()
fig.canvas.draw()


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("esp32/Mic")


array = [0]*3500

index = 0


def on_message(client, userdata, msg):
    global index
    payload = msg.payload

    int_val = int.from_bytes(payload, byteorder='little')
    array.append(int_val)
    array[index] = int_val
    index += 1

    if index >= 3500:
        print("Plotting")
        index = 0
        plt.plot(array)
        plt.pause(0.01)
        fig.canvas.draw()


print("Connecting to MQTT broker")

client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

client.loop_forever()
