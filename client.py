# subscribe to mqtt topic and save to wav file

import paho.mqtt.client as mqtt

import matplotlib.pyplot as plt
# import DataPlot and RealtimePlot from the file plot_data.py
from plot_data import DataPlot, RealtimePlot

start = time.time()
count = 0

fig, axes = plt.subplots()

data = DataPlot()
dataPlotting = RealtimePlot(axes)

count = 0


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
    global count
    count += 1
    data.add(count, int_val)
    dataPlotting.plot(data)
    plt.pause(0.001)


print("Connecting to MQTT broker")

client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

client.loop_forever()
