# subscribe to mqtt topic and save to wav file

import paho.mqtt.client as mqtt

from matplotlib import pyplot as plt
import matplotlib.animation as animation
import time
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

start = time.time()


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("esp32/Mic")


array = []
count = 0


def on_message(client, userdata, msg):
    payload = msg.payload
    count += 1
    if (count > 3000):
        print(time.time()-start)

    """int_val = int.from_bytes(payload, byteorder='little')
    array.append(int_val)
    if len(array) > 3500:
        array.pop(0)
    print(int_val)
    ax.clear()
    ax.plot(array)"""


client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)


client.loop_forever()
